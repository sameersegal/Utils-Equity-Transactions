# Foreign Equity Transactions Processing

This repository processes raw foreign equity transaction data to prepare worksheets for income tax review for Indian financial years (FY18-19 through FY21-22).

## Overview

The `create_xlsx.py` script reads the master ledger in `transactions.csv`, filters transactions for each Indian financial year (April 1 – March 31), and generates one Excel workbook per financial year. Each workbook includes:

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
  | Flag           | Custom flag (if any)                                       |
  | Cost Basis     | Cost basis per share                                       |
  | SKIPXIRR       | Internal flag                                              |
  | Skip           | Internal flag                                              |
  | Currency Ratio | Exchange rate to INR                                       |
  | Price in INR   | Price per share converted to INR                           |

## Setup

This project uses the `uv` package manager to install and manage dependencies.

```bash
uv sync
```

## Usage

Run the script using `uv`:

```bash
uv run python create_xlsx.py
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
- Review the script header in `create_xlsx.py` for additional context.
