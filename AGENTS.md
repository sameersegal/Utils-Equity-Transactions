# Transaction Ledger

You are provided transactions.csv with master ledger data. You need to filter data for income tax calculation for foreign equity. Transaction data needs to be calculated for the Indian Financial Year (1April to 31March) for the years FY18-19, FY19-20, FY20-21 and FY21-22.

For each year, we need to find the transactions that occurred in the time frame. For those stocks we need complete history to be able to calculate the correct cost price. 

Your job is only to compile the raw data and not do any tax calculation.

Create 1 file per FY year. 

Tab 1 - Transactions - Should list only the sell transactions that occurred in the relevant time period
Tab 2+ - <Stock Code> - Should list the complete transaction history, including buy, sell, transfer in and transfer out for the given <stock code>

Note: this data is only for international stocks and not Indian stocks. 

Column names of the transactions.csv:
Platform,Owner,Account ID,Instrument,Symbol,TradeTime,B/S,Amount,Price,Trade Value,Currency,Flag,Cost Basis,SKIPXIRR,Skip,Currency Ratio,Price in INR

Column `TradeTime` has date in format mm/dd/yyyy
Column `B/S` has values Bought, Sold, TransferIn, TransferOut
Column `Currency` has values USD, INR, CAD

