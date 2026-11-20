# On-chain microstructure signals for evaluating memecoins in real time (as of Nov 2026)

> **Research-process caveats (read first):**
> - In this session WebFetch could not resolve arxiv.org, emergentmind.com or docs.mobula.io, which are outside the allowed network domains. As a result, **every finding below comes from search-engine snippets and summaries of the pages, not from reading the full documents.** Numbers taken from papers come from their abstracts and excerpts, so check them against the PDFs before quoting them precisely.
> - The shared web-search budget ran out partway through the research. That left the flow-metric thresholds, wash-trading quantification and Photon filters thinly covered (see the Gaps sections).
> - Several of the "arXiv" papers cited are 2026 single-author preprints with corrigenda and changing titles across versions. None is peer reviewed. They are flagged where relevant.

## 1. Holder metrics: holder growth, top-10/top-20 concentration, fresh-wallet share, sniper share, dev holdings

### Takeaway
Practitioner tools converge on a few concentration gates: top-10 holders below ~30% of supply (excluding the LP/bonding curve), dev holdings below ~5%, and bundler, insider and sniper shares below ~20–30%. GMGN itself documents only the top-10 < 30% rule; the rest are community conventions. Academic work on Pump.fun finds that coordinated early-buyer and sniper wallets are associated with more early flow, but they add little or no predictive power for actual graduation once the bonding-curve state is known.

### Cited Findings
**Tool thresholds (practitioner)**
- GMGN's official "New Pair" documentation: the top-10 check returns "Yes" (relatively safe) when the ten largest holders together own **less than 30%** of total supply. — [GMGN docs: New Pair](https://docs.gmgn.ai/index/new-pair)
- A third-party GMGN filter guide says GMGN documents the filter fields but publishes **no recommended values**. Common community cutoffs: top-10 ~30% (strict 25%, loose 40%), with bundlers and snipers each under ~20–30%. — [gmgnaiapp.com: Best GMGN Filters (2026)](https://gmgnaiapp.com/guides/gmgn-filters/)
- An Apify "GMGN rug-check" scraper preset uses **bundler share < 20%** and **insider share < 20%** as safety filters for new Solana tokens. — [Apify: Find Safer Solana Tokens with GMGN Rug-Check Filters](https://apify.com/muhammetakkurtt/gmgn-trending-scraper/examples/scrape-new-solana-tokens)
- An open-source GMGN-based momentum screener rejects tokens with **bundled supply > 25%**, **insider-held supply > 20%**, **snipers > 40%**, or **bundlers + insiders + dev combined > 40%**. — [GitHub: Jbusiness0810/gmgn_tool](https://github.com/Jbusiness0810/gmgn_tool)
- GMGN's official agent "skills" repo exposes market and holder fields that screeners consume programmatically. — [GitHub: GMGNAI/gmgn-skills, gmgn-market SKILL.md](https://github.com/GMGNAI/gmgn-skills/blob/main/skills/gmgn-market/SKILL.md)
- Axiom "Pulse" offers roughly 14–15 filters (sources disagree on the count): token age, top-10 concentration, dev holdings, sniper activity, insider wallets, bundle detection, liquidity, market cap, volume and transaction counts. — [DEV Community: Axiom Pro Trade Pulse](https://dev.to/crypto_blog/axiom-pro-trade-pulse-a-pro-dashboard-for-real-time-alpha-from-pumpfun-and-beyond-31mj); [Boxmining: Memecoin Trading Guide on Axiom](https://www.boxmining.com/axiom-memecoin-trading-guide)
- Community Axiom setups: a "degen" preset with **dev holding < 5%** and **snipers < 10%**; "top holders ideally under 30% combined"; "be cautious if the dev holds 35–50%+"; Reddit presets with **Snipers max 3** (count, not %) and **Top-10 holders 15%** (optional). — [Medium @GEMQUEENx: Axiom Trade Strategy](https://medium.com/@GEMQUEENx/axiom-trade-strategy-best-settings-filters-and-fees-for-maximum-profits-eab7504cb07d); [r/SolanaMemeCoins Axiom Pro guide (mirror)](https://reddit.birdcat.cafe/r/SolanaMemeCoins/comments/1k3h2u2/axiom_pro_trading_guide_newest_memecoin_trading)
- Mobula's data-API guide to detecting snipers and bundlers uses **Dev < 5% (or locked/burned)** and **Top-10 < 30% excluding liquidity pools** as benchmarks. — [Mobula docs: Detecting snipers & bundlers](https://docs.mobula.io/almanac/detecting-snipers-bundlers) (search snippet only; page not fetchable)

**Dev/creator history as a holder-side signal**
- ScorpLabs (vendor's own pipeline): across **693,331** pump.fun launches, **1.71%** graduated. Restricting to tokens whose **dev had a prior graduation and stayed quiet for ≥7 days** lifted the rate to **12.01% (95% CI 10.0–14.4%)**. The vendor admits that its own real-capital probe **lost money on execution** despite the signal. — [ScorpLabs: Pump.fun graduation rate 1.7% and a 12% signal](https://trader.scorplabs.online/blog/pump-fun-graduation-rate-dev-signal-12-percent)

**Snipers, coordinated wallets and early-buyer groups (academic preprints)**
- Kamat (arXiv 2607.02795): from **1,578,333** buyer observations on **166,098** pump.fun launches over 13.4 days (June 2026), the paper identifies **1,012 persistent wallet cohorts** (2–12 wallets each, 2,965 addresses). The contamination-adjusted propensity-matched estimate of the first-30-minute buyer-count lift is **+16.1%**. A placebo of activity-matched groups produced a median of **+189.6%**, so the author treats it as a bias diagnostic. Graduation outcomes for cohort-touched mints (5,419) were too thin for a Cox-PH estimate. — [arXiv 2607.02795](https://arxiv.org/abs/2607.02795); dataset: [Zenodo RED-COHORT-2026-v1](https://zenodo.org/records/20978742)
- A ResearchGate version of the same paper is retitled around "the limits of naive causal inference". It reports a **+132.3%** real-cohort lift and attributes it to **selection**: cohorts (and placebos) cluster in launches that already attract buyers. **The two versions conflict; the coordination effect is contested.** — [ResearchGate version](https://www.researchgate.net/publication/408521585_Coordinated_Sniper_Cohorts_on_Pumpfun_Detection_of_1012_Persistent_Wallet_Rings_and_the_Limits_of_Naive_Causal_Inference_for_First-Hour_Buyer_Flow)
- Gafarov (arXiv 2610.39458): ~200,000 pump.fun launches, ~15.9M curve trades and 51M SOL transfers over 88.3 hours. A multi-channel discovery procedure (co-buying, shared funding, joint signing, transfers, consolidation) found **23,710 wallet groups**. Pools of tens to 100+ "fast wallets" are associated with a **2–4× higher chance of reaching 20 SOL** in the curve, a smaller excess at 60 SOL, and **no excess for graduation**. Hold-out precision of the team-identification rules is ~50–75%. Many of the signals appear **only after the curve already holds 20 SOL** and **add no information beyond early curve state**. The teams rarely create the tokens they buy. — [arXiv 2610.39458](https://arxiv.org/abs/2610.39458)
- A companion preprint on serial rug-pull-like exits reports that **the number of early buyers has practically no effect** in its model, and suggests early buyers may be team wallets that would trade anyway. — [arXiv 2610.41597](https://arxiv.org/html/2610.41597)
- Bitquery investigation headline: "Pump.fun Devs' Bundles Made $579M+, Snipers Just $31.5M". This suggests creator bundling, not third-party sniping, captures most extractive profit. Only the headline was available. — [Bitquery: pump.fun snipers vs bundles](https://bitquery.io/investigations/pump-fun-snipers-bundles)

### Inferences
- Holder-concentration filters are best treated as **rug and dump-risk exclusion gates**, not as predictors of upside. No source found shows that passing top-10 < 30% raises graduation or return probability by a measured amount.
- Academic evidence suggests early-buyer counts and sniper or cohort presence are largely **endogenous to already-hot launches** (selection). A real-time model should condition on curve state (SOL in the curve) before crediting holder or buyer features.
- The strongest single holder-side signal with a reported effect size is **dev wallet history** (prior graduation plus a dormancy period). It comes from one vendor and has no replication.
- Thresholds differ in what they measure (percentage of supply vs count of snipers; LP included vs excluded), so they are not directly comparable across tools.

### Gaps
- **Holder-count growth rate thresholds** (e.g., holders per minute) and **top-20 concentration** cutoffs: no sourced practitioner values found.
- **Fresh-wallet share** (wallets with no prior history funded just before buying): no sourced threshold or effect size found. GMGN and Axiom expose related "insider" and "fresh" tags, but I could not confirm their exact definitions (searches ran out).
- Exact GMGN definitions of "insider", "sniper" (e.g., first N blocks/slots) and "bundler", and Axiom's official definitions: not confirmed from primary docs. One guide claims Axiom flags a bundle when **≥4 transactions occur in the same block** ([Boxmining](https://www.boxmining.com/axiom-memecoin-trading-guide)); unverified against official docs.

## 2. Flow metrics: buy/sell ratio, unique buyers per minute, volume/liquidity, volume/market cap, trade-size distribution, bonding-curve velocity

### Takeaway
The best-supported flow predictor is **bonding-curve state and progress**: graduation probability rises sharply with SOL locked in the curve. Practitioner ML write-ups find **average swap size / capital efficiency** more predictive than whale or buy-count features. Hard numeric thresholds for buy/sell ratio, unique buyers per minute, volume/liquidity or volume/market cap were **not found in reliable sources**.

### Cited Findings
- Marino, Naviglio, Tarantelli & Lillo (arXiv 2602.14860, Feb 2026) model graduation probability as a function of **SOL currently locked in the bonding curve (vSol)** plus structural and behavioural variables of the launch. Graduation probability **rises sharply with vSol**. Adding the explanatory variables **significantly improves predictive power** and sheds light on speculative and manipulative dynamics in early trading. — [arXiv 2602.14860](https://arxiv.org/abs/2602.14860); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6543715)
- A Medium practitioner study (random forest on extremely imbalanced pump.fun data, features from the **first ~40 seconds**) ranks **capital_efficiency** and **avg_swap_size** (total volume / swap count) as the top features. Buy/sell ratio, volume statistics (e.g., volume_std), token age and total fees rank lower, and **whale-based features rank lowest**. The author notes that early high-volume buyers are often MEV snipers who dump later. The reported base rate is ~2.7% (2.84% in one cohort). Unvetted single blog. — [Medium @alleg88: Predicting Pump.fun Token Graduation With Random Forest](https://medium.com/@alleg88/predicting-pump-fun-token-graduation-with-random-forest-on-extremely-imbalanced-data-9ef8da928390)
- A GitHub capstone (QM640) predicts graduation from **first-30-minute on-chain microstructure features** with XGBoost. It is precision-first on a **1.82% base rate**, and the median token has **~26 trades in its first 30 minutes**. Precision figures were not visible in snippets. — [GitHub: tomdelcarlo-lgtm/pumpfun-graduation-prediction](https://github.com/tomdelcarlo-lgtm/pumpfun-graduation-prediction/tree/main)
- A LightGBM "pumpfun-sniper-model" on Hugging Face reports a validation **AUC of 0.9934** but itself flags a **~900× graduation-rate drift** and platform regime breaks, so the score may not hold out of sample. — [Hugging Face: ProjectSpaice/pumpfun-sniper-model](https://huggingface.co/ProjectSpaice/pumpfun-sniper-model)
- Bitquery (11.5M Solana tokens, 1 Nov 2025 – 7 Oct 2026; Pump.fun = 78%): **half of pump.fun launches had their last trade within ~3 minutes**; **79% had no trades after launch day**; ~1 in 58 reached a full trading pool; 1.5% had any trade in week 5 and 0.2% had 10+ trades. **43% of graduated coins** still traded in week 5, vs **1%** of non-graduated ones. — [Bitquery: Solana launchpad year](https://bitquery.io/investigations/solana-launchpad-year)
- Gafarov: fast-wallet team signals mostly appear after the curve holds 20 SOL and add nothing beyond early curve state. Curve-progress milestones used in the paper: **20 SOL, 60 SOL, graduation**. — [arXiv 2610.39458](https://arxiv.org/abs/2610.39458)
- Axiom Pulse exposes liquidity, market cap, volume and transaction-count filters, but the guides found give no consensus numeric values for them. — [DEV Community: Axiom Pulse](https://dev.to/crypto_blog/axiom-pro-trade-pulse-a-pro-dashboard-for-real-time-alpha-from-pumpfun-and-beyond-31mj)

**Base rates (needed to interpret any flow signal)**
- Published pump.fun graduation rates span **0.198% to 5%** depending on sample, window and date. — [Coinpaprika: What does token graduation mean](https://coinpaprika.com/education/token-graduation-mean-numbers/)
- 1.71% across 693,331 launches (ScorpLabs). — [ScorpLabs](https://trader.scorplabs.online/blog/pump-fun-graduation-rate-dev-signal-12-percent)
- 0.84% (April 2026 data). — [pumpfundata.com](https://pumpfundata.com/blog/pumpfun-graduation-rate-analysis)
- The daily graduation rate hit **6.7%** (≈8× June's average) in late July 2026, after pump.fun's **BOOST** began using post-migration buys and burns to incentivise launches. This is a regime shift, not a stable base rate. — [The Block, 2026-07-29](https://www.theblock.co/news/defi/2026-07-29-pump-fun-token-graduation-rate-jumps-boost-changes-launch-incentives-409815)
- The 0.198% pooled figure from arXiv 2607.02823 was later described by its authors as a lower bound from a fast-regime window, and partly withdrawn via corrigenda. — [arXiv 2607.02823v3](https://arxiv.org/html/2607.02823v3)

### Inferences
- In real time, **curve progress (SOL in curve, and its rate of change)** is the backbone feature, and other flow features should be read *conditional* on it. This is consistent with both Marino et al. and Gafarov.
- Larger average trade size and capital per swap probably proxy for "real" demand vs dust and bot trades. This is consistent with question 3, but rests on a single unvetted study.
- Because most tokens die within minutes, any flow signal measured over 30 minutes is partly a survival filter. Models report high AUCs largely by separating dead from alive tokens, which does not equal tradable edge (cf. ScorpLabs' execution losses).
- Regime breaks (BOOST, Mayhem mode, fee changes) shift base rates by multiples. Thresholds and backtests need to be re-fitted per regime.

### Gaps
- **Buy/sell ratio, unique buyers per minute, volume/liquidity and volume/market-cap thresholds:** no reliable sourced numeric cutoffs found before the search budget ran out. These are common in Telegram and X folklore, but I could not cite them.
- **Bonding-curve velocity** (e.g., time from 0 to X% progress) cutoffs used by Photon, Axiom or GMGN "almost bonded" filters: not found.
- **Photon filter presets:** no sources retrieved.
- **Dune dashboards** with these metrics: none surfaced in searches.

## 3. Signs of artificial activity (volume bots, micro-buys, wash trading, bundles)

### Takeaway
Fraud and manipulation are the base case on pump.fun: Solidus Labs flagged 98.6% of tokens as rug or pump-and-dump. Academic preprints find **bot-like transactions associate with lower graduation probability** at intermediate and late curve stages, and creator **bundles** extract far more value than third-party snipers. Direct quantification of volume-bot and micro-buy share was **not found**.

### Cited Findings
- Solidus Labs (May 2025 report): **98.6%** of >7M pump.fun tokens launched Jan 2024 – Mar 2025 were rug pulls or pump-and-dumps. Only ~**97,000** kept ≥$1,000 liquidity. Of ~388,000 Raydium pools, **~93%** showed "soft rug" traits (slow liquidity withdrawal to avoid detection). Pump.fun disputed the report. — [Solidus Labs report](https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance); [CoinDesk coverage](https://www.coindesk.com/business/2025/05/07/98-of-tokens-on-pump-fun-have-been-rug-pulls-or-an-act-of-fraud-new-report-says)
- Marino et al.: transactions classified as **bot-like** show a **lower probability of graduation beyond intermediate vSol** levels. — [arXiv 2602.14860](https://arxiv.org/pdf/2602.14860)
- Bitquery headline: devs' **bundles made $579M+** vs snipers **$31.5M**. — [Bitquery](https://bitquery.io/investigations/pump-fun-snipers-bundles)
- Gafarov: coordinated "fast-wallet teams" are detectable through shared funding, joint signing, co-buying, transfers and consolidation. They almost never create the tokens they buy. The largest team's cash-out destinations are team-specific, consistent with creator-address obfuscation and coordinated selling. — [arXiv 2610.39458](https://arxiv.org/html/2610.39458)
- Kamat identified 1,012 persistent wallet rings (2–12 wallets) recurring across launches. Recurring co-buying of the same tokens by the same wallet set is a usable fingerprint. — [arXiv 2607.02795](https://arxiv.org/abs/2607.02795)
- Axiom bundle detection reportedly flags coordinated groups of **≥4 transactions in the same block**. — [Boxmining](https://www.boxmining.com/axiom-memecoin-trading-guide) (unverified against official docs)
- A practitioner ML study notes that early high-volume buyers are often **MEV snipers who dump later**, which is why whale features predicted poorly. — [Medium @alleg88](https://medium.com/@alleg88/predicting-pump-fun-token-graduation-with-random-forest-on-extremely-imbalanced-data-9ef8da928390)

### Inferences
- Practical artificial-activity fingerprints, from the sources above:
  - Same-block or same-slot multi-wallet buys (bundles).
  - Wallets sharing a funding source or signer.
  - Recurring wallet sets across many launches.
  - Low average swap size with a high swap count (micro-buy and volume-bot pattern; the inverse of the "capital efficiency" signal).
  - Consolidation transfers to common destinations after selling.
- The micro-buy fingerprint is inferred from the avg_swap_size finding and is not directly measured in a source.
- "Volume" on screeners should be discounted where unique-wallet counts are low relative to trade count. I found no source quantifying the discount.

### Gaps
- **Share of pump.fun / PumpSwap volume generated by volume bots or wash trading:** no reliable quantitative source retrieved. Solidus' wash-trading methodology was not confirmed in snippets.
- **Micro-buy detection thresholds** (e.g., buys under X SOL repeated at fixed intervals): not found.
- GMGN's and Axiom's exact algorithms for "bundler", "insider" and "sniper" tags: not confirmed from primary docs.

## 4. Quantitative studies and practitioner backtests on which features predict outcomes; tool thresholds

### Takeaway
Across 2026 studies, the consistent findings are:
- Graduation is rare (~1–2% long-run; regime-dependent spikes to ~6.7%).
- Curve state, social-channel presence and dev history carry signal.
- Sniper and early-buyer counts carry little incremental signal.
- In-sample models **do not generalise across time windows**.

The tool thresholds (GMGN, Axiom, Mobula) are exclusion heuristics without published backtests.

### Cited Findings
- **Marino et al. (arXiv 2602.14860):** graduation probability conditioned on vSol plus behavioural and structural variables improves prediction; bot-like trading lowers graduation odds. — [arXiv](https://arxiv.org/abs/2602.14860)
- **arXiv 2607.02823** ("Pump.fun Graduation Regime Windows: Survival Analysis of 832,941 Token Launches and the Social-Presence Effect", corrected v2/v3): launches advertising **all three social channels** graduate at much higher rates than those with none, and **Telegram presence** is especially predictive. (The Telegram claim comes via a secondary summary; specific rate ratios were not retrieved.) The pooled 0.198% rate is a lower bound from a fast-regime window. — [arXiv 2607.02823v3](https://arxiv.org/html/2607.02823v3); [deeppaper summary](https://arxiv.deeppaper.ai/papers/2607.02823v1)
- **Same arXiv ID, an audit-framed version** ("Auditing Collector-Generated Graduation Labels on Pump.fun: Measurement Error and Temporal Non-Generalization"): **in-sample discrimination does not extend across a two-week temporal boundary**. — [arXiv 2607.02823 PDF](https://arxiv.org/pdf/2607.02823)
- **Gafarov (arXiv 2610.39458):** fast-wallet groups give 2–4× odds of reaching 20 SOL, but **zero excess for graduation** and no information beyond early curve state. — [arXiv](https://arxiv.org/abs/2610.39458)
- **arXiv 2610.41597:** number of early buyers has practically no effect. — [arXiv](https://arxiv.org/html/2610.41597)
- **Kamat (arXiv 2607.02795):** coordination lift in early buyer flow is +16.1%, but heavily confounded by selection (placebo +189.6%). — [arXiv](https://arxiv.org/abs/2607.02795)
- **ScorpLabs vendor backtest:** dev with a prior graduation and ≥7-day dormancy → 12.01% graduation vs 1.71% base (~7× lift), but the live real-capital probe lost money on execution. — [ScorpLabs](https://trader.scorplabs.online/blog/pump-fun-graduation-rate-dev-signal-12-percent)
- **Random forest blog:** avg_swap_size and capital_efficiency are top features; whale features are lowest. — [Medium](https://medium.com/@alleg88/predicting-pump-fun-token-graduation-with-random-forest-on-extremely-imbalanced-data-9ef8da928390)
- **LightGBM (HF):** AUC 0.9934 with a self-reported ~900× base-rate drift caveat. — [Hugging Face](https://huggingface.co/ProjectSpaice/pumpfun-sniper-model)
- **Bitquery survival:** graduation is the strongest survival separator (43% vs 1% still trading at week 5). — [Bitquery](https://bitquery.io/investigations/solana-launchpad-year)
- **Tool thresholds summary:**
  - GMGN top-10 < 30% (official).
  - Community thresholds: bundlers and insiders < 20%, snipers < 20–40%, bundlers + insiders + dev < 40%, dev < 5%, top-10 15–30%, snipers max 3 (Axiom preset).
  - Sources: [GMGN docs](https://docs.gmgn.ai/index/new-pair); [gmgnaiapp guide](https://gmgnaiapp.com/guides/gmgn-filters/); [GitHub gmgn_tool](https://github.com/Jbusiness0810/gmgn_tool); [Apify](https://apify.com/muhammetakkurtt/gmgn-trending-scraper/examples/scrape-new-solana-tokens); [Medium @GEMQUEENx](https://medium.com/@GEMQUEENx/axiom-trade-strategy-best-settings-filters-and-fees-for-maximum-profits-eab7504cb07d)

### Inferences
- A defensible real-time feature hierarchy suggested by the evidence:
  1. Bonding-curve SOL and its velocity.
  2. Dev wallet history (prior graduations, dormancy, funding source).
  3. Social-channel presence (especially Telegram).
  4. Trade-quality features (avg swap size, capital per swap).
  5. Concentration and bundle exclusion gates (top-10, dev %, bundler/insider %).
  6. Only last, sniper or early-buyer counts.
- **Predicting graduation is not the same as profitable trading.** The vendor that found a ~7× lift lost money live, and models degrade across 2-week windows and platform regime changes (BOOST, Mayhem mode). Any bot built on these features needs rolling re-training and slippage-aware backtests.
- Much of the 2026 academic literature consists of single-author arXiv preprints with corrigenda and version changes. Treat effect sizes as provisional.

### Gaps
- **Photon filter thresholds** and any **official Axiom documentation** of filter definitions: not retrieved.
- **Published, out-of-sample, PnL-based backtests** of GMGN- or Axiom-style filter sets: none found.
- **Dune dashboards** tracking holder, flow or bot metrics: none surfaced.
- **Full feature lists and coefficients** of Marino et al. and of the 2607.02823 survival model: not available, because arxiv.org could not be fetched in this session.
- **EVM-side launchpads** (Four.meme on BNB, Base launchpads) and their equivalent metrics: not covered.
