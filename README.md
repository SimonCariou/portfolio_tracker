# Portfolio Tracker
In the crypto asset ecosystem, many exchanges allow to buy and hold tokens/coins and it's easy to lose track of the actual gains/losses of the global portfolio.
This script is intended to keep track of exactly that plus value by scraping coinmarketcap.com for current asset prices, multiplyin git by the number of tokens/coins owned and calculating a couple of data (percentage change, gains/losses, amount owned after tax etc.).

The results are then stored in a mongodb running locally with a db called ```ticker_db``` and a collection named ```db_ticker```.

The following document represents the data stored (numbers are in €):

```
{
    "timestamp": "2021-06-10 11:26:49",
    "assets": {
        "BTC": 1000,
        "ETH": 1000,
        "BNB": 1000
    },
    "total": {
        "total_raw": 20000,
        "total_after_taxes": 14000
    },
    "capital_gain": {
        "capital_gain_raw": -216.43,
        "capital_gain_after_taxes": -151.5
    },
    "percent_change": {
        "percent_change_raw": -1.72,
        "percent_change_after_taxes": -1.21
    }
}
```
