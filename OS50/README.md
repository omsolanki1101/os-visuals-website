# OS50 — Freqtrade Paper Engine Foundation

**Research build — NO REAL MONEY / NO API KEYS / NOT A PROFITABLE SYSTEM.**

This branch adds a separate, inspectable trading-engine starter for OS50. It **does not** replace the [online OS50 dashboard](https://os50-command.vercel.app), and the dashboard is **not connected** to this container. The dashboard currently runs browser-based paper sessions; this Freqtrade container is an independent, long-running Python worker that must be operated in a suitable computer/server environment.

## Why Freqtrade
- [freqtrade/freqtrade](https://github.com/freqtrade/freqtrade): active open-source crypto bot with dry-run, historical backtesting, strategy comparison and safeguards.
- [Official strategy guide](https://docs.freqtrade.io/en/stable/strategy-customization/)
- [Official backtesting guide](https://docs.freqtrade.io/en/stable/backtesting/)
- Upstream Freqtrade is GPL-3.0. This starter is a separate integration template, not a fork of its core.

## What is implemented
1. A $50 CAD **dry-run only** Kraken spot configuration, one virtual position at a time. Bot is initially **stopped**, exchange API credentials are blank, and HTTP API is disabled.
2. An example trend / momentum / breakout / volatility strategy (not validated or profitable).
3. Pure-Python financial ledger: fees, slippage assumptions, realized profits and losses, virtual transfers of **existing** $1 net profits into five round-robin child divisions. These children **do not independently execute trades**.
4. Automated unit tests for double counting, costs, allocation, loss recovery and spending controls.
5. Golden rules and deployment gates.

## Requirements
- Docker Engine + Docker Compose.
- Internet for Kraken OHLCV data and to pull the Freqtrade image.
- A machine that can actually run containers; the OS50 Vercel site cannot host this continuous worker by itself.
- Check Kraken spot pair and order minimums with the supported exchange before starting. $10 CAD stake may fail exchange limits. A failed minimum is a reason **not to trade**, not a reason to bypass the exchange.

## Safe setup (dry-run only)
```bash
cd OS50
docker compose pull
# Download historical candles, then backtest without risking funds:
docker compose run --rm os50-dryrun download-data --config /freqtrade/user_data/config.json --timeframes 1h --days 365
docker compose run --rm os50-dryrun backtesting --config /freqtrade/user_data/config.json --strategy OS50GuardedStrategy --fee 0.008
# Only after inspecting results: start a dry-run worker (still fake money)
docker compose up
```
Backtesting with 0.008 fee models 0.8% **per executed side** but not every spread/slippage condition. Confirm Freqtrade/CCXT-compatible exchange symbols, limits and strategy behavior. Do not add API credentials or change `dry_run` until independent safety review.

## Accounting tests
```bash
cd OS50
python -m unittest discover -s tests -v
```
Tests only cover the stand-alone accounting ledger, **not** live-market execution, the actual exchange API, or Freqtrade runtime integration.

## Absolutely required before any real-money release
- Many months/market regimes of historical data, untouched out-of-sample testing and 100+ forward dry-run trades with positive net expectancy after costs.
- Slippage, spreads, exchange minimums, rate limits, exchange downtime and order reconciliation.
- Broker keys kept outside source with **no withdrawal permission**, verified kill switch and independent account monitoring.
- A separate risk controller that checks account equity and pre-trade order size **in the actual execution path**. The demo guardians in the website and the reserve ledger do not themselves enforce Freqtrade order placement.
- Money not needed for essential living expenses. No capital guarantee.

No scripts here create deposits or real exchange orders.