# GMGN.ai deep dive: metrics, data APIs, copy-trade, fees, accuracy, lessons for in-house implementation

Research caveats: only 2 web searches returned results (a third hit a rate limit) and 1 fetch succeeded (GMGN CLI usage doc). datawallet.com and docs.mobula.io were not reachable (not in session's allowed network domains). Items tagged [UNVERIFIED] come from model background knowledge or third-party snippets and were not confirmed against primary sources. No official GMGN definitions page was found.

## 1. How does GMGN define its wallet/token labels (smart money, KOL, sniper, insider, bundler, rat trader, rug ratio)?

### Takeaway
GMGN publishes tags and fields but (as far as found) no formal thresholds. The API exposes labels such as smart_degen, renowned (KOL), rat_trader, bundler, fresh_wallet, transfer_in and a 0-1 rug_ratio; exact algorithms are proprietary and must be reverse-engineered or re-derived.

### Cited Findings
- Tag/field names seen in GMGN CLI/skill docs and mirrors: smart money = `smart_degen` (wallets with proven profitable history, tagged by GMGN's algorithm); KOL = `renowned`; `rat_trader` = insider/sneak-trading volume share; `bundler` = bot-bundled buy wallets; `transfer_in` = wallets with transfer-in record for the token; `fresh_wallet` = new wallets with no prior history. Counts exposed as `smart_degen_count`, `renowned_count`. — [search synthesis of GMGN skills/CLI docs](https://docsearch.algolia.com/mcp/docs/repo/gmgnai/gmgn-skills) and [gmgn-cli README](https://cdn.jsdelivr.net/npm/gmgn-cli@1.5.2/Readme.md)
- `rug_ratio` is described as a 0-1 score of rug-pull likelihood, values >0.3 treated as high risk; a separate "suspected insider hold rate" metric exists. — same search synthesis (secondary; thresholds not confirmed on primary page)
- GMGN's own CLI doc references signal types `SignalTypeSmartDegenBuy`, `SignalTypeKOLBuy` and filters `smart-degen-count`, `renowned-count` but does not define tags or list token-security fields. — [GMGN cli-usage.md](https://raw.githubusercontent.com/GMGNAI/gmgn-skills/HEAD/docs/cli-usage.md)
- Sniper is described by third parties as wallets buying at the exact moment of launch; thresholds (blocks/seconds) not given. — search synthesis; exact GMGN logic unconfirmed.
- Wallet stats: `portfolio profits` returns realized profit, unrealized profit, total profit, total cost, buy/sell counts for selected period and all-time; `portfolio stats` has no documented field list. — [cli-usage.md](https://raw.githubusercontent.com/GMGNAI/gmgn-skills/HEAD/docs/cli-usage.md)
- Dev rug ratio [UNVERIFIED]: on the GMGN UI it is commonly understood as share of a deployer's previous tokens that were rugged/dumped; precise rule not found.
- Winrate / PnL [UNVERIFIED]: UI shows 7d/30d PnL, winrate (share of closed positions profitable), buy-size distribution (e.g. <0.1 SOL, 0.1-1, etc.) and flags to exclude "dust"/airdrop-like tokens; exact definitions not confirmed.

### Inferences
- Labels are probably heuristics on on-chain graph data (same-slot buys, common funding source, token creation links, early-block buys), not ML-verified ground truth.
- "rat trader" = insider cluster volume share, comparable to what other tools call insiders/team-linked wallets.

### Gaps
- No primary-source thresholds for any label; no formal PnL/winrate formula; GMGN docs site not reachable via search.

## 2. What data APIs does GMGN offer and under what access model?

### Takeaway
GMGN now has an official OpenAPI (openapi.gmgn.ai) with API key, private-key signed auth for trade/follow endpoints, tiered rate limits, plus CLI/agent skills. Earlier the data API was private/closed.

### Cited Findings
- CLI command groups: token (info, security, pool, holders, traders); market (kline, trending, trenches, signal, hot-searches); portfolio (holdings, activity, stats, profits, info, token-balance, created-tokens); track (follow-tokens, follow-token-groups, follow-wallet, kol, smartmoney); callout; order (quote, get, strategy create/list/cancel); swap, multi-swap; cooking (token launch). — [cli-usage.md](https://raw.githubusercontent.com/GMGNAI/gmgn-skills/HEAD/docs/cli-usage.md)
- Auth: `GMGN_API_KEY` for all; `GMGN_PRIVATE_KEY` for swap/strategy/cooking; signed auth for follow-wallet; IP whitelist per key (`AUTH_IP_BLOCKED`); timestamp within +/-5 s; replay protection. — same
- Rate limits (leaky bucket rate/capacity): Free 5/5, Plus 20/20, Pro 50/50; per-route weights; 429 includes X-RateLimit-Reset; requests during cooldown extend bans by 5 s up to 5 min; Free plan cannot call swap (403 PLAN_UPGRADE_REQUIRED). — same
- Unofficial Python SDK targets host openapi.gmgn.ai. — [PyPI gmgn-sdk](https://pypi.org/project/gmgn-sdk/) (via search snippet)
- Bitquery characterizes OpenAPI as trading-oriented and tied to account/trading volume (third-party, unverified); Mobula article says earlier GMGN kept its data API closed (may be outdated). — [Bitquery](https://docs.bitquery.io/docs/examples/Solana/solana-gmgn-api), [Mobula](https://docs.mobula.io/guides/gmgn-closed-apis) (snippets only)
- Many Apify scrapers exist for GMGN smart-money, wallet activity, trending (unofficial scraping). — [Apify example](https://apify.com/logiover/gmgn-smart-money-hunter)

### Inferences
- Free tier throughput (5 req/s-ish bucket) is enough for dashboards but not for bulk wallet scoring; in-house indexing is needed for scale.

### Gaps
- Exact endpoint paths/response schemas; whether paid tiers are volume-gated vs subscription; current pricing.

## 3. Copy-trade engine and fee model

### Takeaway
Copy-trade/follow-wallet and strategy orders (limit/TP/SL style) are exposed via account-bound trading wallets; fee details were not verified.

### Cited Findings
- `track follow-wallet` returns trades of wallets the user follows; filters side, amount range, limit 1-100; requires signed auth. The CLI doc lists no dedicated copy-trade command. — [cli-usage.md](https://raw.githubusercontent.com/GMGNAI/gmgn-skills/HEAD/docs/cli-usage.md)
- `order strategy create|list|cancel` and `order quote` exist; `TRADE_WALLET_MISMATCH` shows trading is bound to a GMGN-managed wallet. — same

### Inferences
- Copy-trade engine is likely: monitor followed wallet txs (stream) -> filter (min amount, token age, mcap) -> size (fixed/ratio) -> execute through own router with MEV protection/priority fee -> TP/SL.

### Gaps
- Fee model [UNVERIFIED, background knowledge]: GMGN bot reportedly charges ~1% per swap (lower with referral/reduced for some), plus Solana priority fee/Jito tip; could not confirm for Nov 2026 (search rate-limited, datawallet unreachable).
- Copy-trade latency, slippage handling, and security incidents not verified.

## 4. Accuracy critiques

### Takeaway
No primary critique sources retrieved. Known structural weaknesses (inference, not cited) apply to any such tagging.

### Cited Findings
- Third-party sources explicitly note sniper/bundler/rat-trader descriptions are partly from third-party tools and thresholds may differ from GMGN's internal logic. — search synthesis above.

### Inferences
- Smart-money tags suffer survivorship bias and wash/multi-wallet farming (wallets are cheap to create, PnL can be faked via self-trading or sybil sets); winrate is easily inflated by many tiny wins.
- Insider/bundler detection misses wallets funded via CEX or staggered; false positives hit legitimate same-slot buyers (e.g. via aggregators/Jito bundles).
- Copy-trading tagged wallets suffers latency decay and alpha leakage because tagged wallets are crowded.

### Gaps
- No empirical accuracy study located; recommend own back-test against labeled rugs.

## 5. Lessons for in-house implementation

### Takeaway
Re-derive each label from raw on-chain data with explicit, versioned definitions and back-tested thresholds; use GMGN only as a cross-check.

### Cited Findings
- Inputs GMGN exposes that you must replicate: holders, traders, pool, kline, per-wallet profits (realized/unrealized/cost/buy-sell counts). — [cli-usage.md](https://raw.githubusercontent.com/GMGNAI/gmgn-skills/HEAD/docs/cli-usage.md)

### Inferences (proposed design, not GMGN facts)
- Sniper: buys within first N slots (e.g. <=3-5) of pool creation; Bundler: >=k wallets buying in same slot/Jito bundle or sharing funder; Insider: wallets linked to deployer/funder graph or receiving transfers pre-launch (transfer_in); Rat trader: volume share of insider cluster; Dev rug ratio: rugged/total tokens by deployer plus linked wallets; define "rug" (liquidity pulled, >90% drawdown within X hours with dev sell).
- Wallet PnL: FIFO realized PnL in SOL with unrealized at mark price; exclude dust, airdrops, transfers; winrate on closed positions weighted by size; require min trades, cap per-token contribution, check for sybil/self-trade; measure persistence (out-of-sample 30d).
- Smart money: rank by risk-adjusted out-of-sample PnL and follow-through (price after wallet buy at your achievable latency), not headline PnL.
- Copy engine: gRPC/Yellowstone stream, slot-level dedupe, pre-trade risk gate using the above labels, Jito bundles, per-wallet latency tracking.
- Budget fee model into backtests (platform ~1% [UNVERIFIED] + tip + slippage).

### Gaps
- Thresholds need empirical tuning; no ground-truth rug dataset identified.
