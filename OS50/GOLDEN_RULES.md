# OS50 Golden Rules and Five Guardians

**Scope:** all rules apply to real-money deployment planning; this starter runs dry-run only.

## Five child groups
1. **Trend:** multiple-timeframe directional confirmation and false-trend rejection.
2. **Momentum:** normalized RSI/momentum, no buying exhaustion.
3. **Breakout:** prior-candle resistance and volume verification; no future leakage.
4. **Volatility:** ATR-adjusted positions, spreads, market gaps, and exposure checks.
5. **Risk:** drawdown, equity reconciliation, daily loss lock, venue connectivity.

These are analytical *divisions*, not five independently funded accounts. A child is born only when a complete $1 of **realized net** profit remains unreserved after recovering prior losses. Birth **transfers** a dollar from cash to reserve and does not increase equity.

## Financial rules
- Never use rent, groceries, or emergency cash for trading.
- No leverage, loans, futures, martingale, averaged-down rescue trades or withdrawal-capable keys.
- No mandatory per-hour profit quota. Flat/no trade is a valid decision.
- Use fees, spreads, and adverse fills realistically; apply minimum order/precision constraints.
- On stale data, missing candles, time desync or API errors, **block orders**.
- Record every fill, entry cost, exit fee, slippage, realized and unrealized P&L.
- One capital ledger is the authoritative truth; child sub-ledgers never double-count cash.
- Stop after configured daily/session loss and drawdown limits. Stop-loss orders have gap/slippage risk.
- Treat historical backtests and fast simulations as *research*, not as proof of expected performance.
- Validate strategy out of sample and walk forward through different volatility regimes; test 100+ forward paper trades.
- Update models only from authorized public or licensed market feeds. Don't scrape protected sites, bypass rate limits, or embed API keys in browsers/repos.
- Never activate real execution unless independent security, finance, and runtime controls pass their release review.

## Integration gap
The Freqtrade strategy example scores signals, while the stand-alone PaperLedger records model trades. **They are not yet wired together.** The stoploss in Freqtrade is an order-management feature, not a zero-loss guarantee. No real account or backend bot is connected to the OS50 Vercel site.
