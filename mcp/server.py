"""MCP server exposing swiss-finance-data as tools."""

import sys
import os

# Allow running from the mcp/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp.server.fastmcp import FastMCP
from swiss_finance import SNB, FX, CPI, SMI, Bonds

mcp = FastMCP("swiss-finance-data")

# ---------------------------------------------------------------------------
# SNB — Policy Rate
# ---------------------------------------------------------------------------

@mcp.tool()
def get_policy_rate() -> float:
    """Get the current Swiss National Bank (SNB) policy rate in percent."""
    return SNB.get_policy_rate()


@mcp.tool()
def get_historical_rates(start: str = None, end: str = None) -> str:
    """
    Get historical SNB policy rates as a CSV string.

    Args:
        start: Start date in YYYY-MM format (optional)
        end: End date in YYYY-MM format (optional)
    """
    df = SNB.get_historical_rates(start=start, end=end)
    return df.to_csv()


# ---------------------------------------------------------------------------
# SNB — SARON
# ---------------------------------------------------------------------------

@mcp.tool()
def get_saron() -> float:
    """Get the current SARON monthly average (CHF risk-free rate) in percent."""
    return SNB.get_saron()


@mcp.tool()
def get_saron_daily() -> float:
    """
    Get the latest SARON daily fixing in percent.
    Divide by 100/252 to get the daily risk-free rate for Sharpe ratio calculations.
    """
    return SNB.get_saron_daily()


@mcp.tool()
def get_historical_saron(start: str = None, end: str = None) -> str:
    """
    Get historical SARON monthly averages as a CSV string.

    Args:
        start: Start date in YYYY-MM format (optional)
        end: End date in YYYY-MM format (optional)
    """
    df = SNB.get_historical_saron(start=start, end=end)
    return df.to_csv()


@mcp.tool()
def get_historical_saron_daily(start: str = None, end: str = None) -> str:
    """
    Get historical SARON daily fixings as a CSV string (business days only).

    Args:
        start: Start date in YYYY-MM-DD format (optional)
        end: End date in YYYY-MM-DD format (optional)
    """
    df = SNB.get_historical_saron_daily(start=start, end=end)
    return df.to_csv()


# ---------------------------------------------------------------------------
# FX — CHF Exchange Rates
# ---------------------------------------------------------------------------

@mcp.tool()
def get_fx_rate(currency: str) -> float:
    """
    Get the current CHF exchange rate for a given currency.
    Returns units of foreign currency per 1 CHF.

    Args:
        currency: Currency code — one of EUR, USD, GBP, JPY, CAD, AUD, SEK, NOK, DKK
    """
    return FX.get_rate(currency)


@mcp.tool()
def get_historical_fx_rates(currency: str, start: str = None, end: str = None) -> str:
    """
    Get historical CHF exchange rates as a CSV string (monthly, 1999+).

    Args:
        currency: Currency code — one of EUR, USD, GBP, JPY, CAD, AUD, SEK, NOK, DKK
        start: Start date in YYYY-MM format (optional)
        end: End date in YYYY-MM format (optional)
    """
    df = FX.get_historical_rates(currency, start=start, end=end)
    return df.to_csv()


@mcp.tool()
def list_fx_currencies() -> list[str]:
    """List all supported CHF exchange rate currency codes."""
    return FX.list_currencies()


# ---------------------------------------------------------------------------
# CPI — Swiss Inflation
# ---------------------------------------------------------------------------

@mcp.tool()
def get_cpi() -> float:
    """Get the latest Swiss Consumer Price Index value (base: December 2020 = 100)."""
    return CPI.get_current()


@mcp.tool()
def get_inflation_yoy(start: str = None, end: str = None) -> str:
    """
    Get Swiss year-over-year inflation rate as a CSV string.

    Args:
        start: Start date in YYYY-MM format (optional)
        end: End date in YYYY-MM format (optional)
    """
    df = CPI.get_inflation_yoy(start=start, end=end)
    return df.to_csv()


# ---------------------------------------------------------------------------
# Bonds — Swiss Confederation
# ---------------------------------------------------------------------------

@mcp.tool()
def get_bond_yield(maturity: str = "10y") -> float:
    """
    Get the latest Swiss Confederation bond yield for a given maturity.

    Args:
        maturity: Bond maturity — one of 1y, 2y, 3y, 4y, 5y, 6y, 7y, 8y, 9y, 10y, 15y, 20y, 30y
    """
    return Bonds.get_yield(maturity)


@mcp.tool()
def get_yield_curve() -> str:
    """
    Get the latest Swiss Confederation yield curve (all 13 maturities) as a CSV string.
    Returns one row with columns: 1y, 2y, 3y, 4y, 5y, 6y, 7y, 8y, 9y, 10y, 15y, 20y, 30y.
    """
    df = Bonds.get_yield_curve()
    return df.to_csv()


@mcp.tool()
def get_historical_bond_yields(
    maturity: str = None,
    start: str = None,
    end: str = None,
) -> str:
    """
    Get historical Swiss Confederation bond yields as a CSV string.

    Args:
        maturity: Bond maturity e.g. '10y'. If None, returns all 13 maturities.
        start: Start date in YYYY-MM-DD format (optional)
        end: End date in YYYY-MM-DD format (optional)
    """
    df = Bonds.get_historical_yields(maturity=maturity, start=start, end=end)
    return df.to_csv()


@mcp.tool()
def list_bond_maturities() -> list[str]:
    """List all available Swiss Confederation bond maturities."""
    return Bonds.list_maturities()


# ---------------------------------------------------------------------------
# SMI — Swiss Market Index
# ---------------------------------------------------------------------------

@mcp.tool()
def get_smi_prices() -> str:
    """Get current prices for all 20 SMI constituents as a CSV string."""
    df = SMI.get_prices()
    return df.to_csv()


@mcp.tool()
def get_smi_returns(
    tickers: list[str] = None,
    period: str = "1y",
    start: str = None,
    end: str = None,
) -> str:
    """
    Get daily returns for SMI constituents as a CSV string (values are decimals, e.g. 0.01 = 1%).

    Args:
        tickers: List of ticker symbols e.g. ['NESN.SW', 'ROG.SW']. Default: all 20 SMI stocks.
        period: Period string e.g. '1y', '6mo', '2y'. Ignored if start/end are provided.
        start: Start date in YYYY-MM-DD format (optional)
        end: End date in YYYY-MM-DD format (optional)
    """
    df = SMI.get_returns(tickers=tickers, period=period, start=start, end=end)
    return df.to_csv()


@mcp.tool()
def get_smi_constituents() -> dict:
    """Get all 20 SMI constituents as a {ticker: company_name} dictionary."""
    return SMI.get_constituents()


if __name__ == "__main__":
    mcp.run()
