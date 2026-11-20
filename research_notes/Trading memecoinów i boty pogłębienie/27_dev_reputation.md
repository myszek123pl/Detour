# Developer/deployer reputation scoring for memecoins (as of Nov 2026)

Note: 5 searches, 2 fetches (both blocked: killy7.substack.com, dextools.io not in allowed network domains). Most figures below come from search-result summaries, not read-through of primary pages. Treat as UNVERIFIED unless stated.

## 1. Serial deployer statistics (counts per deployer, outcomes)

### Takeaway
No primary-source study quantifying serial deployers' outcomes was verified. Available figures are overall rug rates (Solidus) and one secondhand "1 in 3 rugs from deployers with 20+ launches" claim (unverified).

### Cited Findings
- Solidus Labs: 98.6% of Pump.fun tokens launched Jan 2024 to Mar 2025 collapsed into pump-and-dump/rug patterns (all deployers, not serial-specific); Pump.fun disputed it — [Solidus report](https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance); coverage [CoinDesk](https://hotfix.coindesk.com/business/2025/05/07/98-of-tokens-on-pump-fun-have-been-rug-pulls-or-an-act-of-fraud-new-report-says)
- CoinGecko analysis (18.67M tokens): only ~5% of Pump.fun tokens survive past 90 days — [Crypto Briefing](https://cryptobriefing.com/pump-fun-token-survival-rate-study/)
- Graduation rate ~0.7-0.8% of launches in Jul-Aug 2025 (secondhand via search summary; UNVERIFIED) — [Cointelegraph](https://cointelegraph.com/news/how-pump-fun-captured-80-of-solana-memecoins-and-can-it-last)
- Claim: "one in three rug-flagged tokens trace to deployers with 20+ prior launches" attributed to a "DeFade State of Solana Rugs 2026" report, seen only via a guide — [Coinpaprika](https://coinpaprika.com/ko/education/launchpad-red-flags/). UNVERIFIED; primary report not found.
- One trader reportedly created ~17,000 memecoins in 3 months and earned ~$840K (illustrates industrial-scale serial deployment; individual not named here) — [Decrypt](https://decrypt.co/303439/crypto-trader-840k-17000-meme-coins-three-months)
- Substack analysis "Serial Token Deployers on Solana" exists with serial-deployer analysis of Pump.fun — [link](https://killy7.substack.com/p/serial-token-deployers-on-solana); could not fetch, no figures captured.

### Inferences
- Per-deployer base rate is extremely skewed: a small number of wallets produce a large fraction of launches, so "launch count" alone is a weak good/bad signal; outcome-conditioned stats (rug ratio, migration ratio) matter.

### Gaps
- No verified distribution of tokens-per-deployer or % of serial deployers' tokens that migrate/rug. Needs Dune/Flipside query or the Substack/arXiv papers (arXiv 2602.14860 "Predicting the success of new crypto-tokens", 2512.11850 surfaced but unread).

## 2. How tools compute dev reputation (GMGN, RugCheck, Axiom)

### Takeaway
Tools aggregate per-creator history (count of tokens launched, how many rugged/dead, sometimes migrated) plus funding-origin and social-account signals. Exact formulas are not publicly documented in what I found.

### Cited Findings
- GMGN: third-party Apify scraper of GMGN data exposes fields for creator token count and community rug-history fields (rugRatio, holderRuggedNum, holderTokenNum, ruggedTokens), plus dev/creator history items (Twitter rename count, deleted tweets, fund-from origin). Definitions not documented; scraper is third-party — [Apify](https://apify.com/logiover/gmgn-token-rugcheck-analytics)
- GMGN reviewed as offering previous-creator activity and rug warnings — [CryptoPotato](https://cryptopotato.com/gmgn-review/)
- RugCheck: risk report includes a "rugging" check on whether creator previously deployed scam/rugged tokens; API summary score_normalised 0-100, higher = riskier (other tools describe other scales) — [Mirror write-up](https://mirror.xyz/0xF362eaCAf0a28651d6f6218e5fD0Faf360fa779F/yPq27VSoIl4nOBhjXGVt6h8NYw9iXWAOXEp7NBJvSxc); [Solana Tracker docs](https://docs.solanatracker.io/guides/token-safety.md)
- Axiom: screening filters include developer holdings %, sniper %, insider %, top-10 concentration, bundle % across New Pairs / Final Stretch / Migrated tabs — [Solana Compass](https://solanacompass.com/projects/axiom). Per-dev "migrated tokens" stat existence not confirmed from sources found.
- Data-provider APIs for dev history: Mobula token dev-history endpoint — [docs](https://docs.mobula.io/guides/how-to-track-token-dev-history); OKX onchainos token developer info reports rug-pull counts per developer — [OKX docs](https://web3.okx.com/onchainos/dev-docs/market/market-memepump-get-token-developer-info); third-party MCP tool classifies deployers legitimate_builder / suspicious / serial_rugger — [Glama](https://glama.ai/mcp/servers/Marcus-Rug-Intel/rug-munch-intelligence/tools/check_deployer_history)

### Inferences
- A typical computation: enumerate tokens whose creator == wallet, label each "rugged" via heuristics (liquidity/price collapse >X% within N hours, dev sold majority), then ratio. Threshold choices are not published; labels are heuristic and can misclassify normal dumps as rugs.

### Gaps
- Exact GMGN/RugCheck/Axiom definitions of "rug", lookback windows, and weights not found; vendor docs not reachable/located.

## 3. Creator-fee incentives after 2025 pump.fun changes

### Takeaway
Pump.fun moved from no creator payout to creator revenue share (May 2025), tiered dynamic fees (Sep 2025), fee sharing to up to 10 wallets (Jan 2026), and cashback coins (Feb 2026); incentives now reward deployers for volume even without a pump, intensifying launch spam but also making fee-claim behavior a reputation signal.

### Cited Findings
- May 2025: PumpSwap creator revenue sharing (reported 0.05% per trade; coverage said 50% of revenue per token to deployer); critics said it rewards rugs — [The Block](https://www.theblock.co/news/defi/2025-05-13-pumpswap-revenue-tokens-354038)
- Top creator reportedly earned $93,780 in 3 weeks; top 25 >$12,900 each — [Decrypt](https://decrypt.co/323276/top-solana-meme-coin-creator-on-pump-fun-has-earned-93000-in-three-weeks)
- New fee model paid out ~$2M to creators in first 24h (Sep 2025) — [Decrypt](https://decrypt.co/337872/pump-funs-new-fee-model-hands-out-2m-to-creators-in-first-24-hours)
- Dynamic fees tiered by market cap (lower creator fees as cap grows) — [Cointelegraph](https://cointelegraph.com/news/pumpfun-revamps-creator-fees-fee-sharing-cto-controls)
- Jan 2026: fee sharing to up to 10 wallets; CTO controls; Feb 2026 cashback coins (creator chooses at launch, irreversible); one-change cap on redirecting fees — [CoinMarketCap](https://coinmarketcap.com/academy/article/pumpdotfun-redirects-fees-to-traders-with-new-cashback-model); [CMC cap](https://coinmarketcap.com/academy/pt/article/pumpdotfun-caps-creator-fee-changes-to-one-per-token)
- Pump.fun fees $31.8M in Jan 2026, down ~75% from $148M in Jan 2025 (DefiLlama, via search summary) — UNVERIFIED primary.

### Inferences
- Creator-fee wallet / fee-share config is a new on-chain reputation feature (who receives fees, whether locked). Fee income lowers the need to rug, but also raises the payoff of mass-launching and wash volume.

### Gaps
- Changes after ~Mar 2026 not captured; exact current fee percentages not verified.

## 4. Evasion: fresh deployer wallets

### Takeaway
Reputation keyed to wallet address is trivially reset with a new wallet; defenders must cluster by funding source, timing, and behavior.

### Cited Findings
- Serial deployers split SOL into burner wallets (qualitative) — [Notion piece](https://unruly-mandolin-c0f.notion.site/The-Rug-Factory-Next-Door-1e0fb2db7d0c80f29dd4c512f9fae08b)
- Bubblemaps linked 23 wallets to one token's deployer via shared funding from exchanges (Bitget/Binance), similar deposit amounts and identical timing; those wallets bought 40% of supply — [Cointelegraph](https://cointelegraph.com/news/bubblemaps-ava-ai-token-sniping-deployer-wallets-solana)
- Pine Analytics: deployers route SOL through intermediary wallets often 5-7 hops deep, defeating direct-funding detection — [Pine Analytics](https://pineanalytics.substack.com/p/exit-liquidity-machines)
- GMGN-exposed fields include fund-from origin of dev wallet (see section 2).

### Inferences
- Useful features for a bot: dev wallet age, funding-source cluster history (multi-hop), exchange-withdrawal funding (clean-looking), buy-timing correlation of snipers with deployer, shared fee-recipient addresses. "Fresh wallet" is the default for most launches, so absence of history should be neutral-to-negative, not strongly informative.

### Gaps
- No measured % of launches from fresh vs. recycled deployers; DexTools "recycled deployers" tutorial not fetchable.
