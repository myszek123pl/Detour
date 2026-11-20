# Memecoin trader outcomes: PnL distribution and value capture (as of Nov 2026)

Method note: 6 web searches run; all WebFetch attempts failed (hosts blocked: coingecko, arxiv, decrypt). All findings below come from search-result summaries, i.e. secondary reports, not verified against original Dune dashboards or papers.

## Share of pump.fun / Solana memecoin wallets profitable at thresholds; loss distribution

### Takeaway
Early-2025 Dune data (Adam Tehc): only ~0.4% of ~13.55M pump.fun wallets realized >$10k, and ~293 realized >$1M. Monthly profitable-wallet share in 2024-2026 usually sits below ~50%, with a low of 30.1% in June 2025. Figures vary widely by window and method (realized vs unrealized, bot filtering). No source found for a clean >$1k or >$100k threshold.

### Cited Findings
- Early 2025 (Jan 2025 coverage): ~0.4% of wallets (about 55,296 of 13.55M) realized >$10,000 profit; 293 wallets realized >$1M — [Decrypt](https://decrypt.co/300403/pump-fun-traders-millionaires), [Cointelegraph](https://cointelegraph.com/news/pump-fun-crypto-traders-majority-do-not-realize-profits-dune-data), [Mitrade](https://www.mitrade.com/insights/news/live-news/article-3-565219-20250111). (Headline variants "0.4%" vs "0.04%" appear in titles; 0.4% matches 55k/13.55M.)
- Critique: pump.fun's Alon said the data undercounts winners (post-Raydium-graduation buys not counted; unrealized gains excluded); many top wallets may be bots/AI agents — [Decrypt](https://decrypt.co/300403/pump-fun-traders-millionaires), [Cointelegraph](https://cointelegraph.com/news/pump-fun-crypto-traders-majority-do-not-realize-profits-dune-data).
- CoinGecko report (Dune data, Apr 2024-Apr 2026): share of profitable wallets rarely above 50%, low of 30.1% in June 2025; a summary cites 70.0% (March 2026) and 73.3% (April 2026) profitable, but the search summary flagged internal inconsistency — [CoinGecko](https://www.coingecko.com/research/publications/pump-fun-traders-are-making-a-comeback), [Crowdfund Insider, May 2026](https://www.crowdfundinsider.com/2026/05/277755-solana-based-meme-coins-trading-platform-pump-fun-makes-recovery-research/). Conflicts with the 50.6%-lost figure below for March 2026.
- March 2026 Dune snapshot: 50.6% of pump.fun traders lost money; ~96% lost or earned <$500 in one tracked period — [Our Crypto Talk](https://ourcryptotalk.com/news/pump-fun-96-percent-traders-losing-money) (via search summary, not verified).
- Solidus Labs: 98.6% of pump.fun tokens (Jan 2024-Mar 2025) became pump-and-dump/worthless; single-vendor classification — [Solidus](https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance).

### Inferences
- Realized-profit tails are extremely thin (<0.5% above $10k, ~0.002% above $1M), and win-rate swings with market phase (30% to ~50%+).
- The 2026 "70% profitable" figure conflicts with 50.6% lost; likely a definitional difference (monthly vs period, bot inclusion). Report-writer should present as range, not point.

### Gaps
- No found figures for >$1k or >$100k thresholds, or a loss-size distribution (median loss, share losing >$1k). Original Dune dashboards not accessed.

## Value capture: pump.fun revenue, bot fees, MEV, insiders vs retail

### Takeaway
Platform and bots collect fees regardless of trader outcome: pump.fun roughly $664M in 2025 and ~$1B+ cumulative; Solana trading bots >$1B lifetime fees; MEV extraction smaller in dollars but concentrated. Insider/sniper rings extract from retail on a minority of launches.

### Cited Findings
- Pump.fun Q1 2026 revenue $124.7M (+17% QoQ), ~36% of Solana app revenue ($342.2M) per Messari — [KuCoin News](https://www.kucoin.com/news/flash/pump-fun-generates-124-7m-in-q1-2026-accounts-for-36-of-solana-app-revenue), [Cointelegraph](https://cointelegraph.com/news/pumpfun-over-third-solana-q1-revenue-memecoin-slowdown?rand=6792).
- Pump.fun earned ~$664M in 2025 (per Blockonomi, as of March 2026) — [Blockonomi](https://blockonomi.com/pump-fun-pump-achieves-1-billion-revenue-milestone-plans-multi-chain-rollout/); cumulative ~$1.08B since early 2024 — [KuCoin](https://www.kucoin.com/news/flash/pump-fun-becomes-first-solana-platform-to-reach-10-billion-in-cumulative-revenue) (URL slug says "10 billion" but summary says $1.08B; verify). Solana app revenue $2.4B in 2025, pump.fun leading — [KuCoin](https://www.kucoin.com/news/flash/pump-fun-leads-as-solana-app-revenue-hits-2-4b-in-2025). A Blockworks piece gave >$834M total with ~$492M annualized run rate, undated — [Blockworks](https://www.blockworks.co/news/pumpdotfun-fee-model).
- Trading bots: lifetime fees ~$1.44B on Solana (2025 post): Photon $421.6M, Axiom $209.3M, BullX $200.6M, Trojan $194.8M, BonkBot $110.7M — [CoinStats citing X post](https://coinstats.app/news/3ada6876cada02f6d450dd38495251c4af63de14d5d17fc15b802cd2c8418e08_4-On-Solana-trading-bots-have-raked-in-144B-in-lifetime-fees-so-far--Photon-4216M-293--Axiom-2093M--BullX-2006M--Trojan-1948M--BonkBot-1107M--and-more-This-fee-growth-is-fueling-Solanas-onchain-economy-like-never-before-pictwittercomIMDtE3TX3J). Fee rates: Trojan 0.9% base (~0.72% effective after cashback), BonkBot 1% — [MadeOnSol](https://madeonsol.com/blog/bonkbot-vs-trojan). Summary says the 144B in the slug is likely $1.44B (unclear).
- MEV: academic paper (IMC 2026) found 521,903 sandwich attacks costing users >$7.7M over ~4 months of early 2025; nearly half of sandwiches from a single bot program (Jito analysis via Helius); Helius reports 3.75M SOL Jito tips in a year — [IMC26 paper](https://cnitarot.github.io/papers/imc26_solana.pdf), [Helius](https://helius.dev/blog/solana-mev-report). Memecoin traders are especially exposed due to high slippage settings (Helius).
- Insiders: Pine Analytics found up to 1.75% of pump.fun launches manipulated by dev-funded sniper wallets; most sniping likely automated — [Pine Analytics](https://pineanalytics.substack.com/p/exit-liquidity-machines), [BeInCrypto](https://beincrypto.com/pump-fun-meme-coin-snipers-systematic-problem). arXiv July 2026 "Coordinated Sniper Cohorts on Pump.fun" reports 1,012 persistent wallet rings (abstract only seen via search; unread) — [arXiv](https://arxiv.org/abs/2607.02795).

### Inferences
- Platform + bot fees (~>$2B combined) exceed measurable sandwich MEV (~$7.7M/4 months) by orders of magnitude; fees are the dominant value-capture channel from retail.

### Gaps
- No total-extraction estimate for insiders vs retail in dollars; no bot-fee total for 2026 (DefiLlama 30-day volumes were low, e.g. Trojan ~$96M, Photon ~$17.6M, BonkBot ~$11.7M, date unclear, suggests sharp decline). Paper figures cover only 4 months.

## Bot vs human performance; bot share of volume

### Takeaway
No reliable source found quantifying bot share of Solana memecoin volume or bot-vs-human PnL. Indirect evidence: bots occupy ~1 in 4 pump.fun tokens at launch (almost none graduate); most sniping is automated.

### Cited Findings
- DEXTools June 2026 sample: bots hold 1 of 4 pump.fun new tokens at launch; almost none graduate — [DEXTools](https://www.dextools.io/news/pumpfun-new-token-bot-activity-data-june-2026-es).
- Pine Analytics: most sniping likely automated; sniper wallets sell quickly — [Pine Analytics](https://pineanalytics.substack.com/p/exit-liquidity-machines).
- Many of the top-profit wallets in Dune data may be bots/AI agents — [Decrypt](https://decrypt.co/300403/pump-fun-traders-millionaires).

### Inferences
- Top-end profit (>$1M wallets) is probably dominated by automated/insider wallets, so "retail profitability" is likely lower than headline wallet stats suggest.

### Gaps
- Share of volume from bots; bot vs human win rates; whether Telegram bot users (Trojan/BonkBot) do better. Searches did not surface them.

## TRUMP coin holder losses and similar aggregate studies

### Takeaway
Multiple analytics firms found large retail losses and tightly concentrated gains: ~813k wallets lost ~$2B (Feb 2025, NYT/Chainalysis); 764k lost vs 58 wallets netting >$10M each (May 2025); Nansen later put ~1M buyers at $3.81B combined loss (date unverified).

### Cited Findings
- Jan 2025: Chainalysis: >77% of TRUMP-holding wallets had losses or earned <$100 as of Jan 21; half of TRUMP/MELANIA holders had never bought a Solana altcoin — [The Block](https://www.theblock.co/news/business/2025-01-23-trump-melania-memecoin-holders-336584).
- Feb 2025: >813,000 wallets lost ~$2B (paper + realized), Trump family ~$100M fees; NYT said true losses likely higher as CEX data excluded — [Fortune](https://fortune.com/crypto/2025/02/11/trump-memecoin-traders-2-billion-dollar-loss-family-100-million-fees/), [AMBCrypto](https://ambcrypto.com/trump-coin-catastrophe-810000-investors-lost-over-2-billion-claims-nyt-report/).
- May 2025: 764,000 of ~2M wallets lost money; 58 wallets made >$10M each (~$1.1B total) — [NBC News/CNBC](https://www.nbcnews.com/tech/crypto/58-crypto-wallets-made-millions-trumps-meme-coin-764000-lost-money-dat-rcna205237); IBTimes: 31 early traders netted ~£540M, >800K lost ~£1.61B — [IBTimes](https://www.ibtimes.co.uk/over-800k-investors-lose-over-161b-trump-meme-coin-as-31-early-traders-netted-540m-1730890).
- Nansen: ~1M buyers at $3.81B combined losses, date not shown in the source (unverified) — referenced in [BeInCrypto](https://beincrypto.com/trump-meme-coin-cycle-retail-losses/).

### Inferences
- Pattern is consistent across studies: ~1/3 or more of wallets lose, tiny early cohort captures >$1B, and issuer fees are another large transfer.

### Gaps
- No post-mid-2025 refresh found (current 2026 TRUMP holder-loss tally); Nansen figure needs date check.
