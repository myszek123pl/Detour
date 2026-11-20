# Failure post-mortems: memecoin bots, AI agents, copy-trading, blown-up traders (as of Nov 2026)

Method note: 6 web searches only (search-result summaries, no full-page fetches). Everything below is from search snippets/summaries; figures are secondary-reported unless stated. No Reddit/X thread was directly read. Aggregate/public cases only.

## 1. What do aggregate data say about how many memecoin traders/bots lose, and what is the evidence quality?

### Takeaway
Most on-chain dashboards show a majority of Pump.fun wallets are net losers (roughly 50-60%+ by realized P&L; ~96% if "made under $500" is counted as non-winners), with a tiny winner tail. Metrics are realized-only, per-wallet, and media-relayed Dune dashboards, so they are indicative, not rigorous. A DIY sniper retrospective showed negative EV.

### Cited Findings
- Several Pump.fun wallet analyses find most traders lose money; one viral Dune dashboard (~1.4M wallets) reported 49-50.6% of wallets lost money in "March 2026" and most of the rest made under $500; adding those gives ~96% non-winners (date and figures from search summary, unverified against primary dashboard) — [crypto.news](https://crypto.news/pump-fun-data-shows-49-of-march-traders-in-the-red-as-platform-locks-fees/)
- BeInCrypto: over 60% of Pump.fun addresses lost money over a six-month window — [BeInCrypto](https://beincrypto.com/pump-fun-meme-coins-trader-losses/)
- Decrypt: only ~0.4% of Pump.fun wallets had profited more than $10,000 (another outlet writes 0.04%/"99.6%" — figures conflict by outlet; treat as order-of-magnitude "tiny") — [Decrypt](https://decrypt.co/300403/pump-fun-traders-millionaires)
- Conflicting data point: BeInCrypto reported >73% of traders profitable in one month (April), highest since 2024 — shows regime/period dependence; methodology unchecked — [BeInCrypto](https://beincrypto.com/pump-fun-traders-profit-comeback-meme-coin-season/)
- CoinGecko research noted realized-P&L-only studies understate losses (unsold underwater bags not counted) — [CoinGecko](https://www.coingecko.com/research/publications/pump-fun-traders-are-making-a-comeback)
- Bitquery-linked study headline: ~74% of Pump.fun gains cannot be replicated by copy traders — [KuCoin flash](https://www.kucoin.com/news/flash/bitquery-study-reveals-74-of-pump-fun-gains-cannot-be-replicated-by-copy-traders) (headline only; method not read)
- Developer retrospective: Claude-assisted Solana sniper of graduated pump.fun tokens reported ~6.5% win rate, avg -0.03%/trade, concluded negative EV (single anecdote) — [DEV Community](https://dev.to/kuba_brzezinski_2d3356a2b/i-built-a-solana-memecoin-trading-bot-with-claude-ai-heres-what-actually-happened-5dl6)
- Another dev post-mortem: ML bot lost money; ML was least important part, strategy/execution mattered more — [DEV Community](https://dev.to/tildalice/my-ml-crypto-trading-bot-lost-money-2-hard-lessons-5e6a)
- SBFC 2025 paper (~6,000 meme coins): sniper/"rat" activity mechanically lifts peak returns under bonding-curve design and attracts traders (late buyers see a flattering picture) — [SBFC2025 paper](https://sbfc.sydney.edu.au/2025/papers/SBFC2025_4G3_P154.pdf)

### Inferences
- Base rate for any new memecoin bot/strategy should be negative EV until proven out-of-sample net of fees, slippage and tips.
- Survivorship bias is heavy: public stories (Decrypt $200K loss then $1.3M gain) are luck-dominated outliers.

### Gaps
- No primary Dune query/dashboard read; no data on bot-specific (vs. human) P&L; no independent multi-user sniper-bot loss study found.

## 2. Execution failures: latency, MEV/sandwiching, fees, copy-trading

### Takeaway
Copy-traders and slow bots systematically get worse fills than the leader; sandwiching and tip/priority-fee wars consume edge. Quantified claims are mostly vendor/blog estimates.

### Cited Findings
- Copiers enter late and are visible to sandwich bots, while leader may use Jito bundles/priority fees — [DEV Community copy-trading guide](https://dev.to/tatelyman/copy-trading-on-solana-how-it-works-and-what-to-watch-out-for-b03)
- Claimed sandwich cost 2-5% of trade on volatile launches (Base guide); ~$50-100 on a $1,000 buy at 10% slippage (Solana piece) — non-measured estimates — [DexTools](https://www.dextools.io/news/mev-2026-avoid-memecoin-sniping)
- A dev lost 12 ETH in a month attributing it to public mempool and loose slippage (generic DEX, not memecoin-specific) — [DEV Community](https://dev.to/apollo_ag/why-most-crypto-bots-get-sandwiched-and-how-to-prevent-it-4c8m)
- Someone paid a ~$200K Solana priority fee with a bad outcome (fee-war risk; details from headline only) — [Decrypt](https://decrypt.co/300084?amp=1)
- Academic: "Resisting Manipulative Bots in Memecoin Copy Trading" (ACM Web Conf 2026) frames copy trading as target of manipulative bots; proposes multi-agent CoT approach; results not read — [arXiv 2601.08641](https://arxiv.org/abs/2601.08641v3)
- Sniper traps: fake contract tweet cost another sniper $75,000 (single anecdote); devs design honeypot-like traps to turn snipers into exit liquidity — [Mitch the Lawyer, Substack](https://mitchthelawyer.substack.com/p/the-predatory-dynamics-of-memecoin-sniping) (URL as returned: https://mitchthelawyer.substack.com/p/the-predatory-dynamics-of-memecoin)

### Inferences
- Latency edge is an arms race (bundles, private routing); retail copy bots are structurally last in the queue. Fees+tips+slippage must be in any backtest.
- Anti-MEV routing claims (Axiom, Nova) are vendor marketing; unverified.

### Gaps
- No measured copier-vs-leader slippage dataset; no independent audit of MEV-protection claims.

## 3. Rugs, insiders and rigged launches (LIBRA etc.)

### Takeaway
Retail and bots lose to insiders who snipe/own supply; LIBRA is the best-documented case.

### Cited Findings
- Nansen (via press): 86% of LIBRA traders realized losses >$1K; ~$251M retail losses vs ~$180M insider/bot profits (secondary reports; original Nansen report not found) — [BeInCrypto](https://beincrypto.com/libra-investors-losses-nansen/)
- Hayden Davis admitted the team sniped LIBRA at launch (said to deter others) and called insider trading widespread; he denies a rug pull — [The Block](https://www.theblock.co/post/341251/libra-memecoin-facilitator-hayden-davis-admits-team-sniped-token-at-launch)
- Bubblemaps: cluster removed ~$87M USDC/SOL from LIBRA liquidity in about an hour; linked wallets sniped via CCTP-funded wallets — [Bubblemaps](https://blog.bubblemaps.io/the-libra-playbook-how-one-cluster-drained-87-million-in-a-single-hour/)
- Bubblemaps alleged 14 wallets tied to Davis made ~$12M sniping YZY (attribution, not proof of insider knowledge) — [The Block](https://www.theblock.co/news/ecosystems/2025-08-25-libra-token-facilitator-earns-12-million-sniping-kanye-west-memecoin-bubblemaps-368164)
- Related: [Blockworks](https://blockworks.co/news/libra-memecoin-sausage-gross)

### Inferences
- Celebrity/political-endorsed launches with concentrated supply are the highest rug-risk category; bundle/cluster detection must be a hard filter.

### Gaps
- Chainalysis analysis not found; $107M vs $87M vs $180M figures differ across outlets; no court findings.

## 4. Key/credential theft and AI-agent failures

### Takeaway
Custody and operational-security failures (bot-platform exploits, dashboard access, account takeovers) have caused larger and more certain losses than strategy errors for AI agents.

### Cited Findings
- Banana Gun (Sept 2024): wallets drained; early estimates ~36 victims/563 ETH (~$1.4M), team later said 11 users, ~$3M, refunded from treasury; cause attributed to a flaw in Telegram message oracle; Maestro/Unibot reportedly also affected earlier (no detailed reports) — [The Block](https://www.theblock.co/news/ecosystems/2024-09-25-banana-gun-exploit-refund-318074); [Cointelegraph](https://cointelegraph.com/news/telegram-bot-banana-gun-users-drained-500-ether); [Forklog](https://forklog.com/en/banana-gun-developers-reveal-details-of-telegram-bot-breach/)
- aixbt (Mar 2025): ~55.5 ETH (~$100K) taken after unauthorized dashboard access queued malicious replies; developers disputed it was the AI being "tricked" — [The Block](https://www.theblock.co/post/346911/ai-crypto-bot-aixbt-lost-eth-hack-unauthorized-dashboard-access); [Cointelegraph](https://cointelegraph.com/news/hacker-breaches-ai-crypto-bot-aixbt-steals-55-eth)
- Truth Terminal founder's X account hacked (Oct 2024) to shill scam memecoin; attackers reportedly cleared >$600K — [Cointelegraph](https://cointelegraph.com/news/truth-terminal-founder-x-account-hacked-promotes-scam-memecoin)
- AI agent token market cap fell from ~$17B (Jan 2025) to <$5B per CoinGecko (via Decrypt) — [Decrypt](https://decrypt.co/310510?amp=1)
- Freysa: challenge game where agent was tricked into releasing funds (only passing mention in results; unverified details).

### Inferences
- Agent attack surface = admin dashboards, social inputs (prompt injection), hot-wallet key custody. Least privilege, spend caps, and human-approval above thresholds are the lessons.
- Third-party Telegram/custodial bots add counterparty risk even if your strategy is fine.

### Gaps
- No post-mortem of an autonomous AI *trading* agent losing via bad decisions found in this pass; no individual blow-up threads (Reddit/X) read directly.

## 5. Synthesis: recurring failure modes and lessons (for report writer)

### Takeaway
Failure modes cluster in: negative-EV base rate, execution costs (latency/MEV/fees/tips), adversarial launches (rugs/insider snipes/traps), custody/opsec, and regime dependence.

### Cited Findings (mapping to sources above)
- Overfitting/ML hype: ML was least important part of failed bot ([DEV](https://dev.to/tildalice/my-ml-crypto-trading-bot-lost-money-2-hard-lessons-5e6a)); test with paper trades before real money ([DEV](https://dev.to/kuba_brzezinski_2d3356a2b/i-built-a-solana-memecoin-trading-bot-with-claude-ai-heres-what-actually-happened-5dl6)).
- Regime change: profitable-share swings from ~49% losing to >73% profitable across months ([crypto.news](https://crypto.news/pump-fun-data-shows-49-of-march-traders-in-the-red-as-platform-locks-fees/); [BeInCrypto](https://beincrypto.com/pump-fun-traders-profit-comeback-meme-coin-season/)); AI-agent token cap -70% ([Decrypt](https://decrypt.co/310510?amp=1)).

### Inferences (concrete lessons)
- Net-of-cost, out-of-sample, regime-split backtests; assume copiers fill worse than the leader.
- Hard filters for bundled/clustered supply and insider snipes; treat fake-announcement/contract-tweet triggers as traps.
- Segregated hot wallet with small balance, private RPC/bundle submission, tight slippage, kill-switch/daily loss cap.
- Avoid third-party custodial bots for size; audit agent permissions; no unreviewed dashboard access.
- Expect outcome distribution dominated by luck; ignore survivor stories.

### Gaps
- Fees/tip share of losses not quantified; key-theft via malicious bot repos/npm not covered; copy-trading fund (vs. wallet) collapses not found.
