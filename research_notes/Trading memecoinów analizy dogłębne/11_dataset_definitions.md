# Memecoin fraud/failure datasets: definitions, headline numbers, usable bot base rates

Method note: 8 web searches + 1 failed fetch (arxiv.org not resolvable from the session; all arXiv facts come from search-result abstracts/snippets, NOT full papers). Items marked [UNVERIFIED] were not confirmed against a primary source. Figures in snippets that I could not source to a URL were excluded.

## 1. How do definitions drive the headline numbers (Solidus, CoinGecko, Chainalysis)?

### Takeaway
Each headline number answers a different question on a different denominator: Solidus = share of ALL launched tokens with any "manipulation-like" pattern (~98-99%); CoinGecko = tokens that traded then stopped (a mortality count, not fraud); Chainalysis = share of new tokens with classic rug-pull behaviour (3.59%, a strict behavioural test). Same universe, a ~30x spread, purely from definition and denominator.

### Cited Findings
- Solidus Labs "2025 Rug Pull Report": ~98.6-98.7% of Pump.fun tokens (created Jan 2024-Mar 2025) and 93% of Raydium liquidity pools showed pump-and-dump / rug-pull characteristics; >7M tokens, only ~97,000 (<1.4%) ever sustained >=$1,000 liquidity; 388,000 Raydium pools examined, soft-rug median ~$2,832, max $1.9M — [Solidus report](https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance); coverage: [BeInCrypto](https://beincrypto.com/pump-fun-tokens-scams-solidus-labs-report/), [CoinDesk](https://hotfix.coindesk.com/business/2025/05/07/98-of-tokens-on-pump-fun-have-been-rug-pulls-or-an-act-of-fraud-new-report-says). Note 98.6 vs 98.7 appears across outlets.
- Pump.fun publicly disputed the Solidus finding (CoinDesk follow-up); content of rebuttal not retrieved — [CoinDesk](https://hotfix.coindesk.com/business/2025/05/07/98-of-tokens-on-pump-fun-have-been-rug-pulls-or-an-act-of-fraud-new-report-says).
- Solidus "<1.4% kept >=$1k liquidity" is a survival/liquidity metric that sits inside the same report as the "98.6% fraud" figure — i.e. the fraud label is essentially "everything that is not a sustained market" (my reading; the exact classifier was not retrieved) — [Solidus](https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance).
- CoinGecko: "dead/failed" = token once actively traded on GeckoTerminal that stopped trading; ~11.6M failed in 2025 = 86.3% of all closures 2021-2025; Q4 2025 alone 7.7M (34.9%). Counts only tokens with >=1 trade, and for pump.fun only graduated tokens (per one summary, so true failure may be higher/lower depending on coverage) — [CoinGecko research](https://www.coingecko.com/research/publications/how-many-cryptocurrencies-failed), [Cointelegraph](https://cointelegraph.com/news/crypto-project-failures-record-2025-memecoin-turbulence), [KuCoin summary](https://www.kucoin.com/news/flash/11-6m-crypto-projects-fail-in-2025-meme-coins-hit-hardest?lang=en_US). Secondary outlets give conflicting totals (13.4M of 25.2M; ~20.2M launched; "13M dead" in CryptoSlate) — [CryptoSlate](https://cryptoslate.com/why-a-record-13m-crypto-projects-are-now-dead-as-bitcoin-critics-still-claim-anyone-can-launch-a-token/). Discrepancy unexplained.
- Chainalysis 2025 Crypto Crime Report (covering 2024): 3.59% of newly minted tokens showed classic rug-pull behaviour; $2.57B of illicit trading volume artificially generated via wash trading — as reported by secondary coverage [Cointelegraph magazine](https://cointelegraph.com/magazine/crypto-crime-2024-2025-chainalysis); I did not see the primary PDF text. Figure covers all chains/new tokens in 2024, not Pump.fun only, and pre-dates the peak launchpad era.

### Inferences
- Solidus (98.6%) vs Chainalysis (3.59%) is not a contradiction: broad "pattern consistent with P&D/rug" on a launchpad population vs. narrow "classic rug pull" on all tokens. Do not average or cite them as competing estimates of one quantity.
- CoinGecko's number is a death count; "dead" != "fraud". Mortality of micro-cap tokens is expected even with zero malicious intent. It is useful as a survival base rate only after fixing the denominator (GeckoTerminal-traded tokens).
- The 98.6% figure is likely driven mostly by the near-universal zero-liquidity/immediate-abandonment of Pump.fun launches, which is a low-quality-token fact rather than a measure of intentional theft. [Inference; classifier not verified.]

### Gaps
- Solidus's exact classification rules/thresholds and Pump.fun's rebuttal text were not retrieved.
- Chainalysis primary text not read; its precise rug-pull rule (liquidity-removal %, time window) unknown.
- CoinGecko's primary page was not fetched; coverage of pump.fun (graduated-only) rests on a secondary summary.

## 2. Insider / sniper / bot studies (Pine Analytics, Bitquery)

### Takeaway
Pine measures coordination (deployer-funded snipers, ~1.75% of issuance); Bitquery's recent study measures wallet-gain replicability (74%), not insider share of tokens. Both are narrower, more operational definitions than Solidus and are closer to bot-relevant quantities, but they are on different units (tokens vs. dollars of gains).

### Cited Findings
- Pine Analytics "Exit Liquidity Machines": deployers fund sniper wallets that buy in the launch block; >15,000 token launches affected, 4,600+ sniper wallets, 10,400+ deployers (~1.75% of issuance per one summary); funded snipers' net profit >15,000 SOL; funding routed through 5-7 wallet layers; >50% of tokens sniped in creation block, but most of that judged likely "spray and pray" bots rather than insiders — [Pine Substack](https://pineanalytics.substack.com/p/exit-liquidity-machines), [BeInCrypto](https://beincrypto.com/pump-fun-meme-coin-snipers-systematic-problem). The 1.75% and 50% numbers come from secondary summaries and use different definitions (funded-insider vs any block-0 buyer); a source flagged inconsistency between summaries.
- Bitquery: 3,170 wallet-token positions with >=$100k gains (Oct 2025-Aug 2026 per summary): 51% of gains from wallets selling transferred tokens, 13% from potentially coordinated patterns, ~10% unclassified -> ~74% not replicable by copy traders; only $193.9M of $752.5M analysed from buy-then-sell — [KuCoin summary](https://www.kucoin.com/news/flash/bitquery-study-reveals-74-of-pump-fun-gains-cannot-be-replicated-by-copy-traders), [Cointribune](https://www.cointribune.com/en/pump-fun-why-displayed-gains-can-mislead-copy-traders/). Secondary-only; date range looks odd vs today's date so treat as [UNVERIFIED].
- Bitquery: 79% of Pump.fun tokens traded only on launch day — [crypto.news](https://crypto.news/pump-fun-memecoin-trader-fatigue-token-survival/) (secondary, definition of "traded" not checked).
- Graduation: 269 tokens graduated in one day, >1% of that day's creations, highest since summer 2025; some still heavily sniped/insider-controlled — [Cryptopolitan](https://www.cryptopolitan.com/pump-fun-token-graduations-six-month-high/).
- DEXTools sample (June 2026): bots hit ~1 in 4 new Pump.fun tokens at launch, almost none graduate; small sample, vendor source — [DEXTools](https://www.dextools.io/news/pumpfun-new-token-bot-activity-data-june-2026).

### Inferences
- The "bot hit 1 in 4" / "sniped >50%" / "1.75% insider-funded" trio shows how the label (any block-0 buyer vs funded-by-deployer) moves the number 30x again.
- Bitquery's 74% is about profit-attribution of top winners (survivorship-selected sample, >=$100k), so it is not a token-level insider rate.

### Gaps
- Pine report date and primary figure tables not fetched; Bitquery primary study not found (only secondary news).

## 3. arXiv datasets (MemeTrans, MemeChain, Meme Coin Factories, Midsummer Meme's Dream)

### Takeaway
Academic datasets use stricter, documented labels but have narrow samples (migrated-only, short windows). Midsummer (82.8% of high-return tokens manipulated) is conditioned on winners; MemeTrans conditions on tokens that migrated. Neither gives an unconditional launch-level rate.

### Cited Findings
- MemeTrans (arXiv 2602.13480, Feb 2026, Hu/Tekin/Xu/Liu): 41,470 Pump.fun tokens that migrated to Raydium, 218.5M transactions, 122 pre-migration risk features; task = high-risk launch detection; models cut financial loss by 56.1%; single launchpad, four-month window; code at github.com/git-disl/MemeTrans — [arXiv abs](https://arxiv.org/abs/2602.13480), [HTML](https://arxiv.org/html/2602.13480). Exact "high-risk" label definition and class share NOT retrieved (fetch failed).
- Midsummer Meme's Dream (arXiv 2507.01963; Mongardini & Mei; USENIX Security '26): 34,988 coins on Ethereum, BSC, Solana, Base over 3 months; 707 high-return (>100%) tokens, 82.8% (v2; v1 said 82.6%) show artificial growth; wash trading, liquidity-pool-based price inflation (LPI), P&D, rug pulls; >17,000 victim addresses, >$9.3M realized losses — [arXiv](https://arxiv.org/abs/2507.01963v2), [USENIX](https://www.usenix.org/conference/usenixsecurity26/presentation/mongardini).
- MemeChain (arXiv 2601.22185): multimodal cross-chain dataset joining on-chain data with website HTML, logos, social accounts, aimed at forensics/risk analysis — [arXiv HTML](https://arxiv.org/html/2601.22185v1). Label rates not retrieved.
- "Meme Coin Factories": I could not find a paper by this title; closest = serial-deployer analysis on Substack (non-peer-reviewed) and arXiv 2512.11850 "The Memecoin Phenomenon" — [Substack](https://killy7.substack.com/p/serial-token-deployers-on-solana), [arXiv](https://arxiv.org/abs/2512.11850v1). Title unverified; treat as [UNVERIFIED].
- Other candidates surfaced: arXiv 2602.14860 "Predicting the success of new crypto-tokens" (bonding-curve/Pump.fun case study) — [arXiv](https://arxiv.org/html/2602.14860v1); a "Catching the Rug" Solana fraud-ML paper listed with id 2608.20271 [UNVERIFIED: id looks implausible, not opened] — [link](https://arxiv.org/pdf/2608.20271).

### Inferences
- Selection effect: Midsummer's 82.8% is P(manipulated | high return), which is exactly the population a momentum/copy bot targets, so it is relevant but not a base rate over all launches. Because it conditions on return, bot strategies that select winners ex post inherit the contamination.
- MemeTrans migrated-only sample excludes the ~98% that never graduate; its risk rates apply to "post-graduation candidates", the realistic universe for a bot entering after migration.

### Gaps
- arxiv.org unreachable via fetch: label definitions, class balances, thresholds for MemeTrans/MemeChain not verified. Recommend re-fetch once domain allowed.

## 4. Which numbers are safe as bot base rates?

### Takeaway
Use survival/liquidity and funded-insider measures, with the denominator stated; do not use "98.6% fraud" as a probability of loss per trade.

### Cited Findings (candidate base rates and their safety)
- Safer (operational, definition clear): <1.4% of >7M Pump.fun tokens sustained >=$1k liquidity ([Solidus](https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance)); ~1% daily graduation rate, peaks ~1% ([Cryptopolitan](https://www.cryptopolitan.com/pump-fun-token-graduations-six-month-high/)); 79% trade only on launch day ([crypto.news](https://crypto.news/pump-fun-memecoin-trader-fatigue-token-survival/), secondary).
- Moderate: Chainalysis 3.59% classic rug rate (2024, all chains) — strict but dated and secondary-sourced.
- Moderate/context-bound: Pine funded-sniper ~1.75% of issuance; Midsummer 82.8% manipulation among >100% winners.
- Unsafe as a bot base rate: Solidus 98.6%/93% (broad "characteristics" label, unknown thresholds, disputed by Pump.fun); CoinGecko 11.6M "dead" (mortality, not fraud, shifting denominator); Bitquery 74% (gain attribution among top winners); DEXTools 1-in-4 (small vendor sample).

### Inferences
- Recommended practice: define the bot's entry universe (e.g., post-migration, liquidity >= X), take rates from datasets whose sample matches it (MemeTrans-like) and re-estimate empirically from own logs; treat all vendor figures as priors only.
- Any figure should be reported with (label, denominator, period, chain/launchpad) as a four-tuple to avoid mixing.

### Gaps
- No source found that reports a rug/loss rate conditional on post-graduation entry with liquidity filter; MemeTrans likely contains it (not retrieved).
- Pump.fun's rebuttal, Solidus classifier, and Chainalysis primary rule remain unchecked.
