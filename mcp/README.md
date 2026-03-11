# swiss-finance-data MCP Server

MCP server that exposes the [swiss-finance-data](https://github.com/EMen11/swiss-finance-data) package as tools for Claude Code, Cursor, and any MCP-compatible client.

## Available tools

| Tool | Description |
|------|-------------|
| `get_policy_rate` | Current SNB policy rate |
| `get_historical_rates` | Historical SNB policy rates (CSV) |
| `get_saron` | Current SARON monthly average |
| `get_saron_daily` | Latest SARON daily fixing |
| `get_historical_saron` | Historical SARON monthly (CSV) |
| `get_historical_saron_daily` | Historical SARON daily (CSV) |
| `get_fx_rate` | Current CHF exchange rate |
| `get_historical_fx_rates` | Historical CHF FX rates (CSV) |
| `list_fx_currencies` | Supported currency codes |
| `get_cpi` | Latest Swiss CPI index value |
| `get_inflation_yoy` | Swiss YoY inflation series (CSV) |
| `get_bond_yield` | Latest Confederation bond yield |
| `get_yield_curve` | Full yield curve — all 13 maturities (CSV) |
| `get_historical_bond_yields` | Historical bond yields (CSV) |
| `list_bond_maturities` | Available maturities |
| `get_smi_prices` | Current SMI constituent prices (CSV) |
| `get_smi_returns` | Daily SMI returns (CSV) |
| `get_smi_constituents` | SMI tickers and company names |

---

## Installation

### 1. Install dependencies

```bash
pip install mcp swiss-finance-data
```

Or from the repo root (installs the local package):

```bash
pip install mcp
pip install -e ..
```

---

### 2. Claude Code

Add the server to your Claude Code MCP configuration.

**Option A — project-level** (`.claude/mcp.json` in your project):

```json
{
  "mcpServers": {
    "swiss-finance": {
      "command": "python",
      "args": ["/absolute/path/to/swiss-finance-data/mcp/server.py"]
    }
  }
}
```

**Option B — global** (`~/.claude/mcp.json`):

```json
{
  "mcpServers": {
    "swiss-finance": {
      "command": "python",
      "args": ["/absolute/path/to/swiss-finance-data/mcp/server.py"]
    }
  }
}
```

Then restart Claude Code. You can verify the server is loaded with:

```
/mcp
```

---

### 3. Cursor

Open **Cursor Settings → MCP → Add new MCP server** and fill in:

- **Name:** `swiss-finance`
- **Type:** `command`
- **Command:** `python /absolute/path/to/swiss-finance-data/mcp/server.py`

Or edit `~/.cursor/mcp.json` directly:

```json
{
  "mcpServers": {
    "swiss-finance": {
      "command": "python",
      "args": ["/absolute/path/to/swiss-finance-data/mcp/server.py"]
    }
  }
}
```

Restart Cursor after saving.

---

## Usage examples

Once connected, you can ask Claude or Cursor Agent directly:

```
What is the current SNB policy rate?
→ calls get_policy_rate()

Show me the Swiss yield curve.
→ calls get_yield_curve()

What is the EUR/CHF rate?
→ calls get_fx_rate("EUR")

Give me the latest Swiss inflation figure.
→ calls get_inflation_yoy()

Show me the daily returns for Nestlé and Roche over the last 6 months.
→ calls get_smi_returns(tickers=["NESN.SW", "ROG.SW"], period="6mo")
```

---

## Running manually

```bash
cd mcp/
python server.py
```

The server uses stdio transport (default for MCP). No port is opened.
