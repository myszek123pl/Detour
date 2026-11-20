# Binance Alpha and Binance Wallet: criteria, points/airdrops, post-listing price behavior, memes, insider cases, bot profitability

Research status (2026-11-20): only 2 of ~8 searches returned results (1 listing/points, 1 price studies); the 3rd was rate-limited and all WebFetch calls failed (binance.com, itiger.com, wublock.substack.com not resolvable from this session). Everything below rests on search-result summaries, not on full-page reads. Treat all figures as UNVERIFIED until checked at the primary source.

## 1. Listing criteria for Binance Alpha

### Takeaway
Binance describes Alpha as a pre-listing selection pool for early-stage Web3 projects; the only criteria I could source are generic (user adoption, industry relevance, business-model applicability). No hard numeric thresholds (liquidity, mcap, holders) were found.

### Cited Findings
- Binance's official notice describes Alpha as a "pre-listing token selection pool" for discovering promising early-stage Web3 projects — [Binance notice](https://www.binance.com/en/support/announcement/d378c2176ac841bb8eae68f63d4c4845) (seen only via search summary; page not fetched)
- A Binance Square post lists user adoption and industry relevance/business-model applicability among evaluation criteria; the post is older and covers the wider listing framework — [Binance Square](https://www.binance.com/square/post/23419426215482) (search summary only)

### Inferences
- Alpha is a low-bar, high-throughput funnel (many listings per week per CMC Academy's recurring "Alpha News" series), so a listing is a weak quality signal compared with spot.

### Gaps
- No numeric criteria (min liquidity, holder count, audit, chain support) found. No data on BSC vs Solana meme share, or specific meme tokens listed (BSC/Solana) — not retrieved.

## 2. Alpha Points and airdrops

### Takeaway
Airdrops are per-project, gated by an Alpha Points threshold (typically ~230-240 in 2026 examples), claimed first-come-first-served, and claiming costs points; eligibility is snapshot-based.

### Cited Findings
- Moonbirds (BIRB) listed on Alpha 28 Jan 2026 with a 230-point claim threshold — [OneKey](https://onekey.so/blog/ecosystem/binacne-alpha-will-list-moonbirds-birb-on-jan-28-at-1900-with-a-230-alpha-points-airdrop-threshold-20260128163715)
- DGrid AI (DGAI): 240-point threshold; first-come-first-served claim of 44 tokens (URL date string suggests Sept 2026, unverified) — [OneKey](https://onekey.so/blog/ecosystem/binance-alpha-lists-dgrid-ai-dgai-airdrop-claim-threshold-set-at-240-points-20260916180445/)
- Another 240-point airdrop (Feb 2026) — [OneKey](https://onekey.so/blog/ecosystem/binance-alphas-new-airdrop-goes-live-soon-240-alpha-points-required-20260206161507); Fabric Protocol (ROBO) Alpha listing 27 Feb with points-based claim — [OneKey](https://onekey.so/blog/ecosystem/binance-alpha-to-list-fabric-protocol-robo-on-feb-27-eligible-users-can-claim-an-airdrop-with-alpha-points-20260226113850)
- Each claim reportedly consumes 15 points; eligibility based on points at start of the event period; participation optional — per Binance FAQ as summarized in search result ([Binance FAQ](https://www.binance.com/sl/support/faq/detail/12e7f2e555704f9c8e852d1c1afb032a)). 24-hour confirmation window claim is from the same summary, unverified.
- Overviews: [CMC Academy guide 2026](https://coinmarketcap.com/academy/article/ultimate-guide-to-binance-alpha-projects-2026), [CMC Alpha News](https://coinmarketcap.com/academy/article/binance-alpha-news-new-listings-drive-activity-as-airdrop-competition-heats-up) (not read in full)

### Inferences
- Threshold escalation (earlier-era lower thresholds, ~230-240 now) implies points are obtained by trading volume on Alpha, so airdrops are partly a volume-farming incentive (mechanics of point earning not verified here).

### Gaps
- How points are earned (volume formula, holding bonus, decay), airdrop USD value per claim, and the Binance Wallet side (Booster/TGE campaigns) not retrieved.

## 3. Measured price behavior: Alpha vs spot/futures listing

### Takeaway
Averages are outlier-driven; medians are modest. Alpha listing shows a short-term bump weaker than spot; spot/futures listing effect on an already-traded token is small/negative.

### Cited Findings
- IOSG-attributed study (post-Feb 2025 window, 14-day peak FDV vs listing FDV): Alpha mean surge 220%, median 19.7%; Launchpad mean ~75%, median 11.5%; Spot mean 15%, median 0.9%; futures weaker because added long after initial listing — [Tiger/IOSG summary](https://www.itiger.com/news/2542690443) (search summary only; methodology unseen)
- Odaily analysis of 38 tokens over six rounds: clear but significantly weaker short-term listing effect than main-platform listings; long-term gains stronger than short-term spikes — via search summary (source: [ChainCatcher](https://www.chaincatcher.com/en/article/2159172) likely; not confirmed)
- PANews/WuBlockchain study of May launches: average change -5.04%, worst -75% — [WuBlock](https://wublock.substack.com/p/binance-alpha-research-how-do-projects)
- Early sankin_eth sample of 29 tokens: 17 up, 12 down; BeInCrypto headline "over 40% drop after announcement" — [BeInCrypto](https://beincrypto.com/tokens-on-binance-alpha-list-drop)
- Conflict: Odaily (long-term stronger) vs WuBlock (average negative); differing windows/samples explain it, not reconciled.

### Inferences
- Peak-based metrics (max within 14 days) overstate achievable returns; a bot cannot sell at the peak. Realized entry-at-announcement returns likely lower than reported peaks.

### Gaps
- No independent 2026 dataset; no separate memecoin subset; no Alpha-then-futures-listing path data (e.g., time-to-futures, post-futures returns).

## 4. BSC and Solana memes listed on Alpha
### Takeaway
Not researched successfully.
### Cited Findings
- CMC Academy runs frequent Alpha news posts citing extreme single-token moves (e.g., "DOYR 5,891% surge", "4,865% gains") — [CMC](https://coinmarketcap.com/academy/article/binance-alpha-news-doyrs-5891percent-surge-defies-market-wide-fear), [CMC](https://coinmarketcap.com/academy/article/binance-alpha-news-4865percent-gains-drop-but-access-gets-pricier); headline figures only, token types and timeframe unverified.
### Inferences
- Fat right tail exists (consistent with mean >> median above) but survivorship in headlines.
### Gaps
- No named BSC/Solana meme list, liquidity, or outcomes.

## 5. Insider / front-running cases
### Takeaway
No sourced cases found (search rate-limited). Cannot assert any specific case.
### Cited Findings
- None.
### Inferences
- Structural risk is plausible (announcement timing known to Binance staff, public on-chain pre-listing accumulation), but this is hypothesis only.
### Gaps
- Specific wallet cases, Binance enforcement statements, on-chain studies: re-search needed (e.g., "Binance Alpha insider wallet Bubblemaps/Lookonchain", "Binance employee front-running Alpha").

## 6. Can a bot trade Alpha announcements profitably?
### Takeaway
Evidence is indirect: mean returns are skewed by outliers, medians ~20% peak (not realizable), and one study flags "professional studios" squeezing ordinary users. Net profitability for a latency-bound bot is unproven by any source found.
### Cited Findings
- WuBlock study title asks whether professional studios squeeze ordinary users (content unread) — [WuBlock](https://wublock.substack.com/p/binance-alpha-research-how-do-projects)
- Tiger/IOSG: peak-FDV median 19.7% within 14 days for Alpha — [Tiger](https://www.itiger.com/news/2542690443)
### Inferences
- With median peak ~20% and negative averages in some samples, after fees/slippage/Alpha's thin liquidity, edge likely requires sub-second execution before announcement-driven spike and strict exits; the fat tail suggests a many-small-losses/few-big-wins profile. Unverified; needs backtest on announcement timestamps.
### Gaps
- No announcement-to-price latency data, slippage, or bot backtests found.
