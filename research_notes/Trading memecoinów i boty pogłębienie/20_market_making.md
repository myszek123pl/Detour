# Memecoin market making: legitimate business vs wash trading (as of Nov 2026)

Method note: 6 searches used (2 hit rate limits, 1 of those retried). Items marked [UNVERIFIED] come from background knowledge, not a source retrieved in this research.

## How do MM firms/bots provide liquidity on DEXs, and what are the inventory risk and fee income?

### Takeaway
On AMM DEXs, "market making" is mostly concentrated LP provision, which academic work finds frequently loses to impermanent loss/LVR (adverse selection). No retrieved study covers memecoin or long-tail pools specifically, so profitability there is an open inference.

### Cited Findings
- Uniswap v3 pools with TVL >$10m (non-stablecoin): about $199.3m fees vs about $260.1m impermanent loss; about 49.5% of LPs had negative returns versus holding. Covers large pools only. — [Loesch et al., Impermanent Loss in Uniswap v3](https://arxiv.org/pdf/2111.09192)
- LVR (loss-versus-rebalancing) measures LP loss against a hedged rebalancing portfolio and captures adverse selection from arbitrageurs; it is hard for most investors to apply. — [Automated Market Makers: Toward More Profitable LP Strategies](https://arxiv.org/pdf/2501.07828)
- 2024 study measures arbitrage losses and LP profitability across a wider set of Uniswap v3 pools using LVR. — [Measuring Arbitrage Losses and Profitability of AMM Liquidity](https://arxiv.org/pdf/2404.05803)
- High LP returns come only with high risk (Heimbach et al.). — [Risks and Returns of Uniswap V3 LPs](https://arxiv.org/pdf/2205.08904)
- A 2023 blog argues LVR can identify positive-EV pools (opinion, not peer-reviewed). — [teletype.in/@jj221](https://teletype.in/@jj221/OrFRYQdnos7)

### Inferences
- Memecoin pools have extreme volatility, one-directional drift and rug/sniper flow, so LP inventory risk is likely worse than in the studied large pools; fees may be high but are unproven to compensate. Not tested by any source found.
- Professional MMs largely quote on CEXs/own books and hedge; passive DEX LP is the weaker business model. [UNVERIFIED general knowledge]

### Gaps
- No data on memecoin LP/MM P&L, fee tiers, or bot profitability (Solana/pump.fun, Raydium, Uniswap v4). A small-bot profitability verdict cannot be sourced; the evidence only suggests it is a hard, adversarial game (adverse selection, MEV, gas/priority fees, no edge vs. professionals).

## What do MM contracts look like (token loans + options, retainers)?

### Takeaway
Two common models: retainer (fixed fee, possibly plus loaned inventory) and token loan + call option, where the MM borrows project tokens with a strike-price option; the latter is criticized for conflicts of interest and opacity.

### Cited Findings
- Loan + call option: project lends tokens; at maturity (typically ~1 year) MM returns the tokens or a fixed USD amount; the call option lets the MM buy at a pre-agreed price below market if price rises, which critics say incentivizes selling into the market. KPIs often missing or vague. — [Cointelegraph](https://cointelegraph.com/magazine/market-maker-deals-quietly-killing-crypto-projects)
- Retainer: fixed monthly fee (maybe setup fee), MM may still receive a token/stablecoin loan for capital returned at contract end. — [Cointelegraph](https://cointelegraph.com/magazine/market-maker-deals-quietly-killing-crypto-projects)
- Vendor comparison lists Wintermute as loan+option/retainer with 12-24 month terms (weak source: vendor page). — [Spark](https://www.spark.money/tools/crypto-market-maker-comparison)
- Related reporting on token-loan transparency scrutiny. — [Crypto Briefing](https://cryptobriefing.com/market-maker-token-loans-transparency-scrutiny/)

### Inferences
- Legitimate deals should specify spread/depth KPIs, loan return terms, and no-dump clauses; absence of these, or "volume" KPIs, is the red flag, since volume targets incentivize wash trading (see Gotbit).

### Gaps
- No primary contract or exact option strikes/fee levels found.

## Where is the legal line (DOJ cases, MiCA)?

### Takeaway
Market making that quotes real two-sided liquidity is lawful; creating artificial volume via self-trades for paying clients is prosecuted as fraud/manipulation. MiCA Title VI imports MAR-style prohibitions, with wash trading explicitly in scope, and no safe harbour for MMs was found.

### Cited Findings
- Gotbit founder Aleksei Andriunin sentenced 13 Jun 2025 (D. Mass.) to 8 months prison + 1 yr supervised release for conspiracy to commit wire fraud and market manipulation; Gotbit got 5 years probation, forfeited about $23m, and must stop operating. Pleaded guilty in March; prosecutors reportedly sought 15 months; attorney described it as time served. Clients included memecoins Robo Inu and Saitama; conduct 2018-2024. — [DOJ USAO-MA](https://www.justice.gov/usao-ma/pr/cryptocurrency-financial-services-firm-gotbit-and-founder-sentenced-market-manipulation); [The Block](https://www.theblock.co/news/regulation/2025-06-13-gotbit-founder-aleksei-andriunin-sentenced-to-8-months-following-wash-trading-scheme-358107)
- Operation Token Mirrors: 15 people and 3 firms charged; FBI created its own token; Gotbit was the third MM convicted after MyTrade founder (Oct 2024) and CLS Global (Apr 2025). — [CryptoSlate](https://cryptoslate.com/crypto-market-maker-gotbit-and-founder-sentenced-for-fraud-manipulation/)
- MiCA Title VI (Arts 86-92) is modelled on MAR, covers crypto-assets admitted to trading or with pending admission, and reaches conduct on or off trading platforms; draft ESMA material maps wash trading and layering/spoofing to Art. 91(2) (consultation-stage mapping). — [Cambridge EJRR](https://www.cambridge.org/core/journals/european-journal-of-risk-regulation/article/cryptoasset-market-abuse-under-eu-mica/FDC11EC096728B9EF1097A5346F0EF27); [Forvis Mazars](https://www.forvismazars.com/lu/en/insights/newsletters/governance-risk-and-internal-control-insights/navigating-the-future-of-crypto-assets/7-market-abuse-involving-crypto-assets)
- ESMA published guidelines on supervisory practices to prevent and detect market abuse under MiCA (July 2025). — [ESMA](https://www.esma.europa.eu/sites/default/files/2025-07/ESMA75-453128700-1039_Guidelines_on_supervisory_practices_to_prevent_and_detect_market_abuse__MiCA_.pdf)
- Cambridge paper warns MAR-style rules may chill legitimate behaviour (buy-backs, stabilisation) — same Cambridge link above.

### Inferences
- Core test appears to be intent and purpose: trading with oneself/affiliates to fake activity, versus genuine risk-taking quotes. Paid-for "volume" with no real counterparty is the pattern prosecuted.
- A solo bot trading its own wallets to inflate volume for a memecoin would fit the wash-trading pattern regardless of token size; MiCA applies mainly to EU-admitted assets, and most memecoins are not MiCA-admitted [UNVERIFIED], but US wire-fraud/CEA theories are tech-neutral.

### Gaps
- Exact text of MiCA Art. 91 and any MM safe harbour not retrieved; SEC/CFTC memecoin positions (e.g., SEC staff statement on memecoins 2025) and 2026 enforcement developments not searched; first search attempt on DOJ details failed.

## Can a small bot profitably market-make memecoins?

### Takeaway
No source directly answers; evidence on LP profitability is negative-to-mixed even for big pools, so a small bot faces adverse selection and rug risk with unproven edge.

### Cited Findings
- See LP profitability findings above (about half of v3 LPs lost to IL; fees vs IL near break-even in aggregate) — [arXiv 2111.09192](https://arxiv.org/pdf/2111.09192)

### Inferences
- Plausible viable niches: very tight-range LP in high-volume pairs with rapid rebalancing, or spread capture on CEX listings; but returns likely thin after priority fees/MEV and token-risk. Treat as untested hypothesis.
- Being paid as an MM by a token team (loan/option) is not accessible to a small operator and carries the legal exposure above.

### Gaps
- No empirical memecoin MM/LP bot results; no data on Solana-specific (Meteora DLMM, Orca) LP profitability.
