#!/usr/bin/env python3
"""
Compile raw foreign equity transactions per Indian financial year for tax data.

For financial years FY18-19 through FY21-22, reads 'transactions.csv' and outputs
a single Excel workbook ('foreign_equity_fy.xlsx') with one sheet per FY. Each sheet
contains the complete transaction history (buys, sells, transfers) for all symbols
sold during that financial year (currency != INR).
"""
import datetime
import sys
import re
import pandas as pd

# Define financial years
FY_DEFS = [((2018, 4, 1), (2019, 3, 31), 'FY18-19'),
           ((2019, 4, 1), (2020, 3, 31), 'FY19-20'),
           ((2020, 4, 1), (2021, 3, 31), 'FY20-21'),
           ((2021, 4, 1), (2022, 3, 31), 'FY21-22')]
           
FY_DEFS = [((2017, 4, 1), (2018, 3, 31), 'FY17-18')]
FY_DEFS = [((2024, 4, 1), (2025, 3, 31), 'FY24-25')]


def sanitize_sheet_name(name):
    # Excel sheet names max 31 chars and cannot contain : \/?*[]
    sheet = re.sub(r'[:\\/?*\[\]]', '_', name)
    return sheet[:31]

def main():
    # Read transactions
    df = pd.read_csv('transactions.csv', parse_dates=['TradeTime'], dayfirst=False)
    # Parse dates and drop invalid
    df['TradeTime'] = pd.to_datetime(df['TradeTime'], format='%m/%d/%Y', errors='coerce')
    df = df[df['TradeTime'].notna()]
    # Only foreign currencies (exclude INR)
    df_foreign = df[df['Currency'].str.upper() != 'INR'].copy()
    # Normalize B/S text
    df_foreign.loc[:, 'B/S'] = df_foreign['B/S'].str.strip()

    # Determine Excel writer engine (require openpyxl or xlsxwriter)
    engine = None
    for eng in ('openpyxl', 'xlsxwriter'):
        try:
            __import__(eng)
            engine = eng
            break
        except ImportError:
            continue
    if engine is None:
        print('Error: no Excel writer engine (openpyxl or xlsxwriter) found. Please install one.', file=sys.stderr)
        sys.exit(1)

    # For each FY, create one Excel workbook with multiple tabs
    for start_def, end_def, fy_label in FY_DEFS:
        start_dt = datetime.date(*start_def)
        end_dt = datetime.date(*end_def)
        # Filter FY transactions and sells
        mask_fy = (df_foreign['TradeTime'].dt.date >= start_dt) & \
                  (df_foreign['TradeTime'].dt.date <= end_dt)
        df_fy = df_foreign.loc[mask_fy]
        df_sells = df_fy[df_fy['B/S'] == 'Sold']
        # Identify symbols sold this FY
        symbols = sorted(df_sells['Symbol'].dropna().unique())
        # Prepare output file
        out_file = f"{fy_label}.xlsx"
        with pd.ExcelWriter(out_file, engine=engine) as writer:
            # Tab 1: all sell transactions in FY
            df_sells.to_excel(writer, sheet_name='Transactions', index=False)
            # Further tabs: full history per symbol
            for sym in symbols:
                df_hist = df_foreign[df_foreign['Symbol'] == sym].copy()
                if df_hist.empty:
                    continue
                df_hist.sort_values(['TradeTime'], inplace=True)
                sheet = sanitize_sheet_name(sym)
                df_hist.to_excel(writer, sheet_name=sheet, index=False)
        print(f"Wrote {out_file}: Transactions tab + {len(symbols)} symbol tabs.")

if __name__ == '__main__':
    main()

