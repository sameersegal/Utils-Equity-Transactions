import pandas as pd
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Generate FY Excel sheets for foreign equity transactions"
    )
    parser.add_argument(
        "--owner",
        nargs="+",
        help="List of Owner values to include (e.g., --owner DC AC)",
    )
    parser.add_argument(
        "--fy",
        choices=["FY18-19", "FY19-20", "FY20-21", "FY21-22"],
        help="Financial year to process",
    )
    args = parser.parse_args()

    # Read transaction data
    df = pd.read_csv("transactions.csv", parse_dates=[
                     "TradeTime"], dayfirst=False)
    # Drop INR transactions
    df = df[df["Currency"] != "INR"].copy()
    # Filter by owner if requested
    if args.owner:
        df = df[df["Owner"].isin(args.owner)]

    # Ensure TradeTime is datetime
    if df["TradeTime"].dtype == object:
        df["TradeTime"] = pd.to_datetime(df["TradeTime"], format="%m/%d/%Y")

    # Columns to include in output
    cols = [
        "Platform",
        "Owner",
        "Account ID",
        "Instrument",
        "Symbol",
        "TradeTime",
        "B/S",
        "Amount",
        "Price",
        "Trade Value",
        "Currency",
    ]

    # Define financial year periods (start inclusive, end inclusive)
    financial_years = [
        ("FY18-19", "2018-04-01", "2019-03-31"),
        ("FY19-20", "2019-04-01", "2020-03-31"),
        ("FY20-21", "2020-04-01", "2021-03-31"),
        ("FY21-22", "2021-04-01", "2022-03-31"),
        ("FY22-23", "2022-04-01", "2023-03-31"),
        ("FY23-24", "2023-04-01", "2024-03-31"),
        ("FY24-25", "2024-04-01", "2025-03-31"),
        ("FY25-26", "2025-04-01", "2026-03-31"),
    ]
    # Filter financial years if requested
    if args.fy:
        financial_years = [fy for fy in financial_years if fy[0] == args.fy]

    for fy_label, start_str, end_str in financial_years:
        start = pd.to_datetime(start_str)
        end = pd.to_datetime(end_str)

        # Sell transactions within the financial year
        sells = df[
            (df["B/S"] == "Sold") & (df["TradeTime"]
                                     >= start) & (df["TradeTime"] <= end)
        ]

        # Collect symbols for these sell transactions
        symbols = sells["Symbol"].unique()

        # Write to an Excel file with separate sheets
        output_file = f"{fy_label}.xlsx"
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            # Tab 1: sell transactions in period
            sells.to_excel(
                writer, sheet_name="Transactions", index=False, columns=cols
            )

            # Additional tabs: full history per symbol
            for symbol in symbols:
                history = df[df["Symbol"] == symbol]
                history.to_excel(
                    writer, sheet_name=str(symbol), index=False, columns=cols
                )


if __name__ == "__main__":
    main()
