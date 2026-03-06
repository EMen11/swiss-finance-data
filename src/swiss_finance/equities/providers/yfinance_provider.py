"""yfinance provider for Swiss equities."""
import pandas as pd
import yfinance as yf
from ...core.base import BaseFetcher
from ...core.exceptions import FetchError, DataValidationError


SMI_CONSTITUENTS = {
    "NESN.SW": "Nestle",
    "ROG.SW": "Roche",
    "NOVN.SW": "Novartis",
    "UBSG.SW": "UBS Group",
    "ZURN.SW": "Zurich Insurance",
    "ABBN.SW": "ABB",
    "SREN.SW": "Swiss Re",
    "GIVN.SW": "Givaudan",
    "LONN.SW": "Lonza",
    "SIKA.SW": "Sika",
    "GEBN.SW": "Geberit",
    "SLHN.SW": "Swiss Life",
    "SCMN.SW": "Swisscom",
    "HOLN.SW": "Holcim",
    "PGHN.SW": "Partners Group",
    "CFR.SW": "Richemont",
    "ALC.SW": "Alcon",
    "SDZ.SW": "Sandoz",
    "STMN.SW": "Straumann",
    "VACN.SW": "VAT Group",
}


class YFinanceProvider(BaseFetcher):
    """Fetches Swiss equity data via yfinance."""

    def fetch(self) -> dict:
        pass

    def validate(self, data) -> bool:
        return data is not None and not data.empty

    def get_constituents(self) -> dict:
        """Return SMI constituents as {ticker: name} dict."""
        return SMI_CONSTITUENTS.copy()

    def get_current_prices(self) -> pd.DataFrame:
        """Get current prices for all SMI constituents."""
        rows = []
        for ticker, name in SMI_CONSTITUENTS.items():
            try:
                hist = yf.Ticker(ticker).history(period="5d")
                if not hist.empty:
                    price = round(float(hist["Close"].iloc[-1]), 2)
                    rows.append({"ticker": ticker, "name": name, "price": price})
            except Exception:
                continue

        if not rows:
            raise FetchError("Failed to fetch any SMI price data")

        df = pd.DataFrame(rows).set_index("ticker")
        return df

    def get_historical_prices(
        self,
        tickers=None,
        period="1y",
        start_date=None,
        end_date=None
    ) -> pd.DataFrame:
        """Get historical closing prices for SMI constituents."""
        if tickers is None:
            tickers = list(SMI_CONSTITUENTS.keys())

        invalid = [t for t in tickers if t not in SMI_CONSTITUENTS]
        if invalid:
            raise ValueError(f"Unknown tickers: {invalid}. Use SMI.get_constituents() to list valid tickers.")

        if start_date and end_date:
            data = yf.download(tickers, start=start_date, end=end_date, progress=False)
        else:
            data = yf.download(tickers, period=period, progress=False)

        if data.empty:
            raise FetchError("No price data returned from yfinance")

        if isinstance(data.columns, pd.MultiIndex):
            closes = data["Close"]
        else:
            closes = data[["Close"]].rename(columns={"Close": tickers[0]})

        closes = closes.dropna(how="all")

        if closes.empty:
            raise DataValidationError("No valid price data after cleaning")

        return closes
