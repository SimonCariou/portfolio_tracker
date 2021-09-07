from flask import Flask, jsonify, request
from bson import ObjectId
from pymongo.errors import BulkWriteError, DuplicateKeyError
from datetime import datetime

from utils import PortfolioCalculator
from utils import round_value
import config
import db_connector

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'ticker_db'
app.config['MONGO_URI'] = 'mongodb://mongo:27017/ticker_db'
app.config['JSON_SORT_KEYS'] = False

assets = config.ASSETS

calculator = PortfolioCalculator()
mongodb = db_connector.DatabaseConnector()

# DB
db = mongodb.get_db()

# collection
db_ticker = db.db_ticker

client = mongodb.get_client()


@app.route('/prices', methods=['GET'])
def log_prices():
    prices = calculator.get_prices(assets)
    portfolio_value = calculator.set_up_portfolio_value(prices)

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

    return jsonify({'result': output})


# # update the db
# db_ticker.insert_one(output)
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
