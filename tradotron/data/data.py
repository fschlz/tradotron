import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class FinanceData():

    name = "FinanceData"
    description = "Class to retrieve financial data with yfinance and do data prep on it"

    def __init__(self, ticker_name, ticker_period, **kwargs):
        logger.debug("initializing FinanceData")

        self._ticker = ticker_name
        self._period = ticker_period

        data = self.fetch_ticker_data(
            ticker=ticker_name, period=ticker_period
        )

        self.data = self.prep_data(data)

    @staticmethod
    def fetch_ticker_data(ticker, period, **kwargs):
        """load data from yahoo finance for given handle and period"""

        logger.debug("fetching data for ticker")

        ticker = yf.Ticker(ticker=ticker)

        data = ticker.history(period=period)

        return data

    @staticmethod
    def prep_data(data) -> pd.DataFrame:

        logger.debug("preparing ticker data")

        # standerdizing column names
        data.reset_index(inplace=True)

        data.columns = data.columns.str.lower()
        data.columns = data.columns.str.replace(" ", "_")

        data.set_index("date", inplace=True)

        # rolling means
        for window in [7, 14, 30, 60, 90, 180, 365]:
            data[f"close_rolling_mean_{window}d"] = data.close.ewm(window).mean()

        return data
