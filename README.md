# Foreign Equity Transactions Processing

This repository processes raw foreign equity transaction data to prepare worksheets for income tax review for Indian financial years (FY18-19 through FY21-22).

## Overview

The `generate_fy_transactions.py` script reads the master ledger in `transactions.csv`, filters transactions for each Indian financial year (April 1 – March 31), and generates one Excel workbook per financial year. Each workbook includes:

- A **Transactions** sheet listing all `Sold` transactions in the period.
- Separate sheets for each stock symbol sold that year containing the complete transaction history (Bought, Sold, TransferIn, TransferOut).

> **Note:** Only international (non-INR) stock transactions are included.

## Input

- `transactions.csv`: Master ledger of all transactions. Columns:

  | Column Name    | Description                                                |
  | -------------- | ---------------------------------------------------------- |
  | Platform       | Trading platform                                           |
  | Owner          | Account owner                                              |
  | Account ID     | Broker account identifier                                  |
  | Instrument     | Security identifier                                        |
  | Symbol         | Stock ticker symbol                                        |
  | TradeTime      | Trade date (`MM/DD/YYYY`)                                  |
  | B/S            | Transaction type (Bought, Sold, TransferIn, TransferOut)    |
  | Amount         | Number of shares                                           |
  | Price          | Price per share in transaction currency                    |
  | Trade Value    | Total value in transaction currency                        |
  | Currency       | Currency code (`USD`, `INR`, `CAD`)                        |

## Setup

This project uses the `uv` package manager to install and manage dependencies.

```bash
uv sync
```

## Usage

Run the script using `uv` (with optional filters):

```bash
uv run python generate_fy_transactions.py [--owner OWNER ...] [--fy {FY18-19,FY19-20,FY20-21,FY21-22}]
```

## Generated Files

Running the script will produce four files:

- `FY18-19.xlsx`
- `FY19-20.xlsx`
- `FY20-21.xlsx`
- `FY21-22.xlsx`

## Output

Each `FY*.xlsx` file contains:

- **Transactions**: Sheet with all `Sold` transactions in that financial year.
- **<Symbol>**: One sheet per stock symbol sold that year with the full transaction history.

## Notes

- Only transactions with `Currency != INR` are processed.
- Review the script header in `generate_fy_transactions.py` for additional context.
