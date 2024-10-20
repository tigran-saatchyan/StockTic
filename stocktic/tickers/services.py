import logging

import yfinance as yf

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Finance:
    def __init__(self, symbol):
        """Initializes the Finance class with a ticker symbol.

        Args:
            symbol (str): The ticker symbol of the company.
        """
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)

    def get_info(self):
        """Fetches the basic information of the company.

        Returns:
            dict: A dictionary containing the company's information.
        """
        try:
            return self.ticker.info
        except Exception as e:
            logger.error(f"Error fetching info for {self.symbol}: {e}")
            return None

    def get_history(self, period="1mo", interval="1d"):
        """Fetches the historical market data for the specified period.

        Args:
            period (str): The period for which to fetch the data
            (e.g., "1mo", "1y").
            interval (str): The interval for the data
            (e.g., "1d", "1wk").
        Returns:
            pandas.DataFrame: A DataFrame containing the historical
            market data.
        """
        try:
            return self.ticker.history(
                period=period,
                interval=interval,
                start=None,
                end=None,
                prepost=False,
                actions=True,
                auto_adjust=True,
                back_adjust=False,
                repair=False,
                keepna=False,
                proxy=None,
                rounding=False,
                timeout=10,
                raise_errors=False,
            )
        except Exception as e:
            logger.error(f"Error fetching history for {self.symbol}: {e}")
            return None

    def get_history_metadata(self):
        """Fetches the metadata of the historical market data.

        Returns:
            dict: A dictionary containing the metadata of the historical data.
        """
        try:
            self.get_history()
            return self.ticker.history_metadata
        except Exception as e:
            logger.error(f"Error fetching history metadata for {self.symbol}: {e}")
            return None

    def get_actions(self):
        """Fetches the actions (dividends, splits, capital gains)
        of the company.

        Returns:
            pandas.DataFrame: A DataFrame containing the actions data.
        """
        try:
            return self.ticker.actions
        except Exception as e:
            logger.error(f"Error fetching actions for {self.symbol}: {e}")
            return None

    def get_dividends(self):
        """Fetches the dividends of the company.

        Returns:
            pandas.Series: A Series containing the dividends data.
        """
        try:
            return self.ticker.dividends
        except Exception as e:
            logger.error(f"Error fetching dividends for {self.symbol}: {e}")
            return None

    def get_splits(self):
        """Fetches the stock splits of the company.

        Returns:
            pandas.Series: A Series containing the stock splits data.
        """
        try:
            return self.ticker.splits
        except Exception as e:
            logger.error(f"Error fetching splits for {self.symbol}: {e}")
            return None

    def get_capital_gains(self):
        """Fetches the capital gains of the company (only for mutual
        funds & ETFs).

        Returns:
            pandas.Series: A Series containing the capital gains data.
        """
        try:
            return self.ticker.capital_gains
        except Exception as e:
            logger.error(f"Error fetching capital gains for {self.symbol}: {e}")
            return None

    def get_shares_full(self, start="2024-02-08", end=None):
        """Fetches the full share count data for the specified period.

        Args:
            start (str): The start date for fetching the share data.
            end (str, optional): The end date for fetching the share
            data. Defaults to None.

        Returns:
            pandas.DataFrame: A DataFrame containing the share
            count data.
        """
        try:
            return self.ticker.get_shares_full(start=start, end=end)
        except Exception as e:
            logger.error(f"Error fetching shares full for {self.symbol}: {e}")
            return None

    def get_income_stmt(self):
        """Fetches the annual income statement of the company.

        Returns:
            pandas.DataFrame: A DataFrame containing the annual income
            statement data.
        """
        try:
            return self.ticker.income_stmt
        except Exception as e:
            logger.error(f"Error fetching income statement for {self.symbol}: {e}")
            return None

    def get_quarterly_income_stmt(self):
        """Fetches the quarterly income statement of the company.

        Returns:
            pandas.DataFrame: A DataFrame containing the quarterly
            income statement data.
        """
        try:
            return self.ticker.quarterly_income_stmt
        except Exception as e:
            logger.error(
                f"Error fetching quarterly income statement for {self.symbol}: {e}"
            )
            return None

    def get_balance_sheet(self):
        """Fetches the annual balance sheet of the company.

        Returns:
            pandas.DataFrame: A DataFrame containing the annual balance
            sheet data.
        """
        try:
            return self.ticker.balance_sheet
        except Exception as e:
            logger.error(f"Error fetching balance sheet for {self.symbol}: {e}")
            return None

    def get_quarterly_balance_sheet(self):
        """Fetches the quarterly balance sheet of the company.

        Returns:
            pandas.DataFrame: A DataFrame containing the quarterly
            balance sheet data.
        """
        try:
            return self.ticker.quarterly_balance_sheet
        except Exception as e:
            logger.error(
                f"Error fetching quarterly balance sheet for {self.symbol}: {e}"
            )
            return None

    def get_cashflow(self):
        """Fetches the annual cash flow statement of the company.

        Returns:
            pandas.DataFrame: A DataFrame containing the annual cash
            flow data.
        """
        try:
            return self.ticker.cashflow
        except Exception as e:
            logger.error(f"Error fetching cashflow for {self.symbol}: {e}")
            return None

    def get_quarterly_cashflow(self):
        """Fetches the quarterly cash flow statement of the company.

        Returns:
            pandas.DataFrame: A DataFrame containing the quarterly
            cash flow data.
        """
        try:
            return self.ticker.quarterly_cashflow
        except Exception as e:
            logger.error(f"Error fetching quarterly cashflow for {self.symbol}: {e}")
            return None

    def get_major_holders(self):
        """Fetches the major holders of the company's stock.

        Returns:
            pandas.DataFrame: A DataFrame containing the major
            holders data.
        """
        try:
            return self.ticker.major_holders
        except Exception as e:
            logger.error(f"Error fetching major holders for {self.symbol}: {e}")
            return None

    def get_institutional_holders(self):
        """Fetches the institutional holders of the company's stock.

        Returns:
            pandas.DataFrame: A DataFrame containing the institutional
            holders data.
        """
        try:
            return self.ticker.institutional_holders
        except Exception as e:
            logger.error(f"Error fetching institutional holders for {self.symbol}: {e}")
            return None

    def get_mutualfund_holders(self):
        """Fetches the mutual fund holders of the company's stock.

        Returns:
            pandas.DataFrame: A DataFrame containing the mutual fund
            holders data.
        """
        try:
            return self.ticker.mutualfund_holders
        except Exception as e:
            logger.error(f"Error fetching mutual fund holders for {self.symbol}: {e}")
            return None

    def get_insider_transactions(self):
        """Fetches the insider transactions of the company's stock.

        Returns:
            pandas.DataFrame: A DataFrame containing the insider
            transactions data.
        """
        try:
            return self.ticker.insider_transactions
        except Exception as e:
            logger.error(f"Error fetching insider transactions for {self.symbol}: {e}")
            return None

    def get_insider_purchases(self):
        """Fetches the insider purchases of the company's stock.

        Returns:
            pandas.DataFrame: A DataFrame containing the insider
            purchases data.
        """
        try:
            return self.ticker.insider_purchases
        except Exception as e:
            logger.error(f"Error fetching insider purchases for {self.symbol}: {e}")
            return None

    def get_insider_roster_holders(self):
        """Fetches the insider roster holders of the company's stock.

        Returns:
            pandas.DataFrame: A DataFrame containing the insider roster
            holders data.
        """
        try:
            return self.ticker.insider_roster_holders
        except Exception as e:
            logger.error(
                f"Error fetching insider roster holders for {self.symbol}: {e}"
            )
            return None

    def get_recommendations(self):
        """Fetches the analyst recommendations for the company's stock.

        Returns:
            pandas.DataFrame: A DataFrame containing the analyst
            recommendations.
        """
        try:
            return self.ticker.recommendations
        except Exception as e:
            logger.error(f"Error fetching recommendations for {self.symbol}: {e}")
            return None

    def get_recommendations_summary(self):
        """Fetches the summary of analyst recommendations for the
        company's stock.

        Returns:
            pandas.DataFrame: A DataFrame containing the
            recommendations summary.
        """
        try:
            return self.ticker.recommendations_summary
        except Exception as e:
            logger.error(
                f"Error fetching recommendations summary for {self.symbol}: {e}"
            )
            return None

    def get_upgrades_downgrades(self):
        """Fetches the stock upgrades and downgrades for the company.

        Returns:
            pandas.DataFrame: A DataFrame containing the upgrades and
            downgrades.
        """
        try:
            return self.ticker.upgrades_downgrades
        except Exception as e:
            logger.error(f"Error fetching upgrades/downgrades for {self.symbol}: {e}")
            return None

    def get_earnings_dates(self):
        """Fetches the future and historic earnings dates for the company.

        Returns:
            pandas.DataFrame: A DataFrame containing the earnings dates.
        """
        try:
            return self.ticker.earnings_dates
        except Exception as e:
            logger.error(f"Error fetching earnings dates for {self.symbol}: {e}")
            return None

    def get_isin(self):
        """Fetches the International Securities Identification Number
        (ISIN) for the company.

        Returns:
            str: The ISIN code.
        """
        try:
            return self.ticker.isin
        except Exception as e:
            logger.error(f"Error fetching ISIN for {self.symbol}: {e}")
            return None

    def get_options(self):
        """Fetches the options expiration dates for the company's stock.

        Returns:
            list: A list of options expiration dates.
        """
        try:
            return self.ticker.options
        except Exception as e:
            logger.error(f"Error fetching options for {self.symbol}: {e}")
            return None

    def get_option_chain(self, expiration_date):
        """Fetches the option chain for the specified expiration date.

        Args:
            expiration_date (str): The expiration date for the options.

        Returns:
            yfinance.option.Opt: An object containing the option chain data.
        """
        try:
            return self.ticker.option_chain(expiration_date)
        except Exception as e:
            logger.error(f"Error fetching option chain for {self.symbol}: {e}")
            return None

    def get_news(self):
        """Fetches the latest news for the company.

        Returns:
            list: A list of dictionaries containing the news data.
        """
        try:
            return self.ticker.news
        except Exception as e:
            logger.error(f"Error fetching news for {self.symbol}: {e}")
            return None

    def get_sustainability(self):
        """Fetches the sustainability data for the company.

        Returns:
            pandas.DataFrame: A DataFrame containing the sustainability data.
        """
        try:
            return self.ticker.sustainability
        except Exception as e:
            logger.error(f"Error fetching sustainability for {self.symbol}: {e}")
            return None

    def get_latest_price(self):
        """Fetches the latest price of the company's stock.

        Returns:
            float: The latest stock price.
        """
        try:
            return self.ticker.history(period="1d")["Close"].iloc[-1]
        except Exception as e:
            logger.error(f"Error fetching latest price for {self.symbol}: {e}")
            return None

    # Additional methods for analysis and aggregation
    def get_pe_ratio(self):
        """Fetches the Price-to-Earnings (P/E) ratio of the company.

        Returns:
            float: The P/E ratio.
        """
        info = self.get_info()
        return info.get("forwardPE") or info.get("trailingPE")

    def get_eps(self):
        """Fetches the Earnings Per Share (EPS) of the company.

        Returns:
            float: The EPS.
        """
        info = self.get_info()
        return info.get("trailingEps")

    def get_dividend_yield(self):
        """Fetches the dividend yield of the company.

        Returns:
            float: The dividend yield.
        """
        info = self.get_info()
        return info.get("dividendYield")

    def get_market_cap(self):
        """Fetches the market capitalization of the company.

        Returns:
            float: The market capitalization.
        """
        info = self.get_info()
        return info.get("marketCap")

    def get_beta(self):
        """Fetches the beta of the company.

        Returns:
            float: The beta.
        """
        info = self.get_info()
        return info.get("beta")
