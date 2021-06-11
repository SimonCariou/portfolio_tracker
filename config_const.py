#TO BE MODIFIED (will not work as is)

#Number of coins/tokens hodled:
ASSETS = {"XX": 9999,
          "YY": 9999,
          "ZZ": 9999}

#Example:
# ASSETS = {"BTC": 2,
#           "ETH": 3,
#           "BNB": 4}


FIAT_LIST = ['USD', 'EUR']
DEFAULT_FIAT = 'USD'

#URLS where the price of the ASSETS keys are obtained:
URLS = {"XX": "https://coinmarketcap.com/currencies/xx",
        "YY": "https://coinmarketcap.com/en/currencies/yy",
        "ZZ": "https://coinmarketcap.com/en/currencies/zz/"}

# Example
# URLS = {"BTC": "https://coinmarketcap.com/en/currencies/bitcoin/",
#         "ETH": "https://coinmarketcap.com/en/currencies/ethereum",
#         "BNB": "https://coinmarketcap.com/en/currencies/binance-coin/"}

INITIAL_INVESTMENT_EUR = 2000

#In france 30%  on plus value is taxed:
TAX_PERCENTAGE = 0.3
