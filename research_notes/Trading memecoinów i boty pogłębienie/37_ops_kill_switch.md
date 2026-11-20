# Operations for automated trading bots: observability, kill switches, incidents, paper mode, deployment, recovery

NOTE ON SOURCING: 4 web searches were run; 2 returned "too_many_requests" (Knight Capital, crypto runaway incidents) and returned only model memory, no URLs. Items marked [UNVERIFIED] come from memory/general knowledge, not a citable source. Primary sources to fetch next: SEC Release 34-70694 (Knight, Oct 2013), Freqtrade docs (telegram-usage, configuration).

## Kill switches and circuit breakers

### Takeaway
Consensus pattern: layered controls (pre-trade checks, per-position stops, daily-loss / drawdown breakers, and an independent kill switch that assumes strategy logic has failed), with state persisted and human-only reset for the serious ones. Specific thresholds in sources are examples, not standards.

### Cited Findings
- Layered design: pre-trade order checks up to portfolio-level drawdown breakers, plus an independent kill switch assuming trading logic already failed — [NexusFi automated risk controls](https://nexusfi.com/a/automation/automated-risk-controls) (via search summary; page not fetched)
- One open-source config defaults: 10% max drawdown from peak equity, 3% max daily loss; tiered example warn 5%, critical 8%, trip breaker+kill switch at 10% — [alpha-oracle risk management](https://ben-ripley.github.io/alpha-oracle/developer-guide/modules/risk-management.html) (example values from a hobby project, not a standard)
- Reset behavior: most breakers auto-reset when conditions normalize; reconciliation breaker and dead-man switch need human action; kill-switch state should be stored persistently with a cooldown (example: 60 min) and restored on restart before trading resumes — [alpha-oracle docs](https://ben-ripley.github.io/alpha-oracle/user-guide/concepts/risk-management.html) and [skillsmp hyperliquid kill switch skill](https://skillsmp.com/skills/enuno-hyperliquid-trading-firm-multiclaw-metaclaw-skills-risk-drawdown-kill-switch-trigger-skill-md)
- Manual kill switch should cancel open orders and halt all trading; breaker must trip before a rule/limit breach rather than after — [MQL5 prop-firm kill-switch](https://www.mql5.com/en/blogs/post/767321)
- For first week live, use a much lower drawdown limit to catch sizing bugs (not market moves); a developer's claimed 80% loss reduction from a live breaker is anecdotal — [DEV: circuit breaker for AI trading bot](https://dev.to/qcautomation/how-i-added-a-circuit-breaker-to-my-ai-trading-bot-and-why-every-algo-needs-one-4p95)
- When multiple controls trigger, most severe state wins — alpha-oracle docs above

### Inferences
- For a memecoin bot: add controls specific to the domain [inference]: max loss per token, max concurrent positions, max SOL/ETH per trade, wallet balance floor (hot wallet holds only limited funds), consecutive-failure/slippage breaker, and RPC/price-feed staleness halt.
- Kill switch should be a separate process/command path (e.g. Telegram /halt plus a file/flag checked by the main loop) so it works when strategy code hangs.

### Gaps
- No authoritative (regulatory/industry) standard for crypto-bot thresholds found; sources are blogs/hobby repos.

## Incident examples (Knight Capital, crypto runaway)

### Takeaway
Knight Capital is the canonical deployment-failure case; no verified crypto-bot runaway case was retrieved (search failed).

### Cited Findings
- [UNVERIFIED, memory] Knight Capital, 1 Aug 2012: a deployment left old test code ("Power Peg") active on one of eight servers (new code not deployed to it; a reused flag re-activated the old routine), sending a flood of unintended orders; ~US$440-460M loss in ~45 minutes; SEC settled Oct 2013 with a US$12M penalty under the Market Access Rule (the ~$460M is the loss, not the penalty). Fetch SEC order to confirm.
- Lessons commonly drawn [UNVERIFIED]: manual, non-automated deployment to multiple servers; dead code left in production; no kill switch; alerts (automated emails) existed but were ignored/not actionable; no pre-trade position/order-rate limits.

### Inferences
- Map to a small bot: automate deploys identically, remove dead code, don't reuse config flags, enforce order-rate and notional limits independent of strategy, and make alerts actionable and paged.

### Gaps
- No verified crypto-bot runaway-loss incidents (e.g. specific exchange-bot bugs, sandwiched/MEV losses, key leaks) retrieved; search rate-limited. Needs a follow-up search.

## Monitoring, alerting via Telegram, paper mode (Freqtrade as reference)

### Takeaway
Freqtrade is a good reference implementation: per-event Telegram notification verbosity, a /forceexit command, and a dry-run mode.

### Cited Findings
- Telegram notification settings per event type with values like on/off/silent; example config enables emergency_exit and force_exit notifications — [Freqtrade telegram-usage (codeclimate mirror)](https://codeclimate.com/github/freqtrade/freqtrade/docs/telegram-usage.md/source)
- `/forceexit all` (alias `/fx`) exits all open trades ignoring minimum_roi — same source
- `emergency_exit` order type (default market) is used when creating exchange stop-loss orders fails; separate from user-triggered force_exit — [Freqtrade configuration (mirror)](https://codeclimate.com/github/freqtrade/freqtrade/docs/configuration.md/source)
- Dry-run: trades simulated, uses exchange default (lowest-tier) fee in calculations — Freqtrade docs/mirror above

### Inferences
- Alert design [inference/general practice]: tiers (INFO trades, WARN degraded feed/failed tx, CRITICAL breaker/kill/balance mismatch), heartbeat message every N minutes with dead-man alert on absence (external watchdog, since a crashed bot cannot report its own death), rate-limit/dedupe alerts, bot-token and chat-ID allowlist so only owner can send commands.
- Metrics worth tracking [general practice, UNVERIFIED as a source]: PnL, open exposure, wallet balance, tx success/fail rate, slippage vs expected, latency to RPC, data staleness, order rate. Prometheus+Grafana or simple structured JSON logs.
- Paper/shadow: run live signals with simulated fills first; note paper fills overstate quality for memecoins (no slippage/liquidity, MEV, failed tx) so a tiny-size live phase is a necessary third stage.

### Gaps
- Not confirmed whether Freqtrade labels emergency/force-exit messages differently in dry-run. Not researched in depth: Prometheus/Grafana setups, log schemas, shadow-mode comparison methodology.

## Deployment practices and state recovery

### Takeaway
Little sourced material retrieved; recommendations below are general engineering practice.

### Cited Findings
- Restore kill-switch/breaker state from persistent storage on restart before trading resumes — [skillsmp skill (above)](https://skillsmp.com/skills/enuno-hyperliquid-trading-firm-multiclaw-metaclaw-skills-risk-drawdown-kill-switch-trigger-skill-md)
- Reconciliation breaker needing human reset (state vs. exchange mismatch) — [alpha-oracle docs](https://ben-ripley.github.io/alpha-oracle/user-guide/concepts/risk-management.html)

### Inferences
- Recovery [general practice]: treat on-chain/exchange as source of truth; on startup reconcile balances, open positions, and pending txs against chain; persist intent before sending (write-ahead / idempotency keys, client order IDs) to avoid duplicate buys after crash; start in "halted/observe" mode until reconciliation passes; supervisor (systemd/Docker restart policy) with crash-loop backoff and alert.
- Deployment [general practice, Knight lesson]: one identical artifact (container image) deployed via script, canary with tiny size/paper mode first, version/config hash logged and shown in the startup Telegram message, quick rollback, deploy while flat (no open positions) or with positions snapshot.

### Gaps
- No sourced guidance on crash recovery for DEX/Solana bots (pending tx handling, blockhash expiry) retrieved; needs follow-up.
