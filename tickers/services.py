import yfinance as yf

class Finance:
    def __init__(self, symbol):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)

    def get_info(self):
        return self.ticker.info

    def get_history(self, period="1mo"):
        return self.ticker.history(period=period)

    def get_actions(self):
        return self.ticker.actions

    def get_dividends(self):
        return self.ticker.dividends

    def get_splits(self):
        return self.ticker.splits

    def get_capital_gains(self):
        return self.ticker.capital_gains

    def get_shares_full(self, start="2024-02-08", end=None):
        return self.ticker.get_shares_full(start=start, end=end)

    def get_income_stmt(self):
        return self.ticker.income_stmt

    def get_quarterly_income_stmt(self):
        return self.ticker.quarterly_income_stmt

    def get_balance_sheet(self):
        return self.ticker.balance_sheet

    def get_quarterly_balance_sheet(self):
        return self.ticker.quarterly_balance_sheet

    def get_cashflow(self):
        return self.ticker.cashflow

    def get_quarterly_cashflow(self):
        return self.ticker.quarterly_cashflow

    def get_major_holders(self):
        return self.ticker.major_holders

    def get_institutional_holders(self):
        return self.ticker.institutional_holders

    def get_mutualfund_holders(self):
        return self.ticker.mutualfund_holders

    def get_insider_transactions(self):
        return self.ticker.insider_transactions

    def get_insider_purchases(self):
        return self.ticker.insider_purchases

    def get_insider_roster_holders(self):
        return self.ticker.insider_roster_holders

    def get_recommendations(self):
        return self.ticker.recommendations

    def get_recommendations_summary(self):
        return self.ticker.recommendations_summary

    def get_upgrades_downgrades(self):
        return self.ticker.upgrades_downgrades

    def get_earnings_dates(self):
        return self.ticker.earnings_dates

    def get_isin(self):
        return self.ticker.isin

    def get_options(self):
        return self.ticker.options

    def get_news(self):
        return self.ticker.news
