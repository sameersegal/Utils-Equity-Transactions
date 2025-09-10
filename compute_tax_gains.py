import argparse
from pathlib import Path

import pandas as pd


def compute_fifo_gains(history_df, sales_events):
    """Compute FIFO gains for given history and sales events."""
    # Prepare inventory: list of dicts with remaining qty and cost per share
    inventory = []
    results = []

    # Sort history by date
    history_df = history_df.sort_values("TradeTime")

    # Iterate through history rows
    for _, row in history_df.iterrows():
        event = row["B/S"]
        qty = row["Amount"]
        price = row["Price"]
        date = row["TradeTime"]

        # Acquisition events (Buys) add to inventory
        if event == "Bought":
            inventory.append({"qty": qty, "cost": price})
            continue

        # Disposal events (Sales) remove from inventory
        if event == "Sold":
            remaining = qty
            cost_total = 0.0

            # Allocate cost via FIFO
            while remaining and inventory:
                lot = inventory[0]
                use = min(remaining, lot["qty"])
                cost_total += use * lot["cost"]
                lot["qty"] -= use
                remaining -= use
                if lot["qty"] == 0:
                    inventory.pop(0)

            # Record gain only for sales in the target FY
            if (date, qty, price) in sales_events:
                proceeds = qty * price
                gain = proceeds - cost_total
                results.append(
                    {
                        "TradeTime": date,
                        "Symbol": row["Symbol"],
                        "Amount": qty,
                        "Price": price,
                        "Proceeds": proceeds,
                        "Cost": cost_total,
                        "Gain": gain,
                        "Currency": row["Currency"],
                    }
                )
        # Ignore TransferIn and TransferOut events
        # Other events are not processed

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Compute FIFO tax gains from an FY transactions workbook"
    )
    parser.add_argument(
        "--file",
        "-f",
        required=True,
        help="Path to the FY Excel file (e.g., FY21-22.xlsx)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output Excel file (defaults to <input>_gains.xlsx)",
    )
    args = parser.parse_args()

    inp = Path(args.file)
    if not inp.exists():
        raise FileNotFoundError(f"Input file not found: {inp}")
    out = Path(args.output) if args.output else None

    # Read sales sheet
    xls = pd.ExcelFile(inp)
    sales_df = pd.read_excel(xls, "Transactions", parse_dates=["TradeTime"])
    sales_df["TradeTime"] = sales_df["TradeTime"].dt.date

    # Prepare sales events set for matching
    sales_events = set(
        zip(sales_df["TradeTime"], sales_df["Amount"], sales_df["Price"])
    )

    # Compute FIFO gains per symbol and print verification tables
    symbols = sales_df["Symbol"].unique()
    all_results = []
    for symbol in symbols:
        hist_df = pd.read_excel(xls, symbol, parse_dates=["TradeTime"])
        hist_df["TradeTime"] = hist_df["TradeTime"].dt.date
        gains = compute_fifo_gains(hist_df, sales_events)
        if gains:
            sym_df = pd.DataFrame(gains)
            print(f"\n=== {symbol} ===")
            print(sym_df.to_string(index=False))
            all_results.extend(gains)

    # Print summary: total proceeds, cost, and gain per symbol in USD
    if all_results:
        summary = (
            pd.DataFrame(all_results)
            .groupby(["Symbol", "Currency"], as_index=False)[["Proceeds", "Cost", "Gain"]]
            .sum()
        )
        print("\n=== Summary ===")
        print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
