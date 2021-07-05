import requests
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter
from datetime import datetime

# local imports
# import config_const as config
import config
import db_connector


class PortfolioCalculator():
    def __init__(self):
        self.c = CurrencyConverter()

    def get_prices(self, list_assets):
        # init the dictionary that will be returned containing the market prices for each assets (BTC, ETH etc.)
        prices = dict()

        # Creating a dictionary with the assets and the URL where we will get the market prices on for each asset
        # only needed in get_prices so initializing it here
        dict_urls = config.URLS

        # Scraping the webpage corresponding to the asset url
        for asset, url in dict_urls.items():
            req = requests.get(dict_urls[asset])
            scraped_page = BeautifulSoup(req.text, "lxml")
            price_tags = scraped_page.find_all(
                'div', class_='priceValue___11gHJ')
            # prices[asset] = float(price_tags[0].text.split()[1].replace(",","")) #in case there are more than one, pick the first one
            prices[asset] = float(price_tags[0].text.split("$")[
                                  1].replace(",", ""))

        return prices  # dictionnary containg key: asset & value: current value of the asset in $

    def set_up_portfolio_value(self, dict_market_price):
        # formatting into a dict.
        dict_crypto_owned = config.ASSETS

        # calculate the USD value of the portfolio by summing th entire portfolio dictionary.
        return {asset: dict_market_price[asset]*dict_crypto_owned[asset] for asset, val in dict_crypto_owned.items()}

    def calculate_global_portfolio_value(self, dict_portfolio):
        return sum(dict_portfolio[k] for k in dict_portfolio)

    def convert(self, _amount, _from, _to):
        return self.c.convert(_amount, _from, _to)

    def calculate_plus_value_after_taxes(self, total_portfolio_value_raw):
        return (total_portfolio_value_raw - config.INITIAL_INVESTMENT_EUR) * (1 - config.TAX_PERCENTAGE)

    def percent_repartition_portfolio(self, dict):
        total_portfolio_value = sum(dict.values())
        return {asset: round_value(value/total_portfolio_value) for asset, value in dict.items()}


def round_value(number):
    return round(number, 2)


def print_dict(dict):
    for outer_key, outer_value in dict.items():
        print(f"{outer_key}: {outer_value}\n")


if __name__ == "__main__":
    calculator = PortfolioCalculator()
    mongodb = db_connector.DatabaseConnector()
    assets = config.ASSETS

    # Scrape webpages to get current market prices
    prices = calculator.get_prices(assets)
    db = mongodb.get_db()
    client = mongodb.get_client()

    # collection
    db_ticker = db.db_ticker

    portfolio_value = calculator.set_up_portfolio_value(prices)

    # TOTAL portfolio value by multiplying the amount of symbol owned by the market price
    total_portfolio_usd = calculator.calculate_global_portfolio_value(
        portfolio_value)
    total_portfolio_eur = calculator.convert(
        total_portfolio_usd, config.DEFAULT_FIAT, 'EUR')
    percent_change_portfolio_global = total_portfolio_eur / \
        config.INITIAL_INVESTMENT_EUR - 1
    plus_value_after_taxes = calculator.calculate_plus_value_after_taxes(
        total_portfolio_eur)
    total_portfolio_after_taxes = config.INITIAL_INVESTMENT_EUR + plus_value_after_taxes
    percent_change_portfolio_after_taxes = total_portfolio_after_taxes / \
        config.INITIAL_INVESTMENT_EUR - 1

    output = {"timestamp": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
              "assets": {asset: round_value(calculator.convert(value, config.DEFAULT_FIAT, "EUR")) for asset, value in portfolio_value.items()},
              "total": {
                  "total_raw": round_value(total_portfolio_eur),
                  "total_after_taxes": round_value(total_portfolio_after_taxes)},
              "capital_gain": {
                  "capital_gain_raw": round_value(total_portfolio_eur - config.INITIAL_INVESTMENT_EUR),
                  "capital_gain_after_taxes": round_value(plus_value_after_taxes)},
              "percent_change": {
                  "percent_change_raw": round_value(percent_change_portfolio_global*100),
                  "percent_change_after_taxes": round_value(percent_change_portfolio_after_taxes*100)
              },
              }

    # update the db
    db_ticker.insert_one(output)
    client.close()

    print("Portfolio value per coin:")
    for key, value in portfolio_value.items():
        print(f"* {key}:")
        # print(f"\t- {value:.2f}$")
        print(f"\t- {calculator.convert(value, config.DEFAULT_FIAT, 'EUR'):.2f}€")

    print("\n")
    print(f"Total portfolio value ({percent_change_portfolio_global:+.2%})")
    # print(f"* {total_portfolio_usd:.2f}$")
    print(f"* {total_portfolio_eur:.2f}€")
    print("\n")

    print("Plus value:")
    print(f"* Raw: {total_portfolio_eur - config.INITIAL_INVESTMENT_EUR:.2f}€")
    print(f"* After taxes: {plus_value_after_taxes:.2f}€")

    print("\n")
    print(
        f"Total portfolio after taxes ({percent_change_portfolio_after_taxes:+.2%})")

    print(f"* {total_portfolio_after_taxes:.2f}€")
    print(
        f"% repartition portfolio: {calculator.percent_repartition_portfolio(portfolio_value)}")
