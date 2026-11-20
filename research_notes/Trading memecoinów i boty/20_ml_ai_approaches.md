# ML and AI approaches to memecoin prediction and trading

> **Method note (read first):** These notes come from web-search result snippets only. Full-text fetching failed: arxiv.org, ideas.repec.org, emergentmind.com, themoonlight.io, traderank.ai, yellow.com and bravenewcoin.com do not resolve in this session's network. The shared web-search budget also ran out partway through. Numbers below are as quoted in search snippets or secondary summaries. Read the primary PDFs before any figure goes into a final report as definitive. Several arXiv IDs carry 2026 dates (26xx.xxxxx); they are recent preprints and not peer-reviewed.

## 1. Academic and practitioner ML studies: memecoin success, rug pulls and pump-and-dumps

### Takeaway
Most published ML work on memecoins is defensive. It classifies rug pulls, pump-and-dumps or "viability" early. It does not produce a profitable trading signal. Gradient boosting (XGBoost/LightGBM) on very early on-chain trading features is the recurring strong baseline. Transformers help mainly on text, such as Telegram pump announcements. I found no published GNN benchmark for pump.fun success prediction. Every paper that tests it reports a distribution shift between venues and periods.

### Cited Findings
**Rug-pull and fraud prediction**
- "Catching the Rug: Early Prediction of Fraudulent Memecoins on Solana via Machine Learning" (Jianghai Li et al., arXiv:2608.20271, 2026):
  - Dataset: about 6.4 million Solana tokens over about 7 months.
  - Finding: classic ML, especially XGBoost, is "robust" at flagging likely rug pulls using only the first 5 minutes of trading data, with no code-level features.
  - The authors say most of these memecoins show rug-pull characteristics within one hour of launch.
  - Generalization between Pump.fun and Raydium "reveals a significant distribution shift that challenges naive data fusion approaches."
  - I did not obtain the exact F1/AUC.
  - Sources: [arXiv HTML](https://arxiv.org/html/2608.20271v1); [arXiv PDF](https://arxiv.org/pdf/2608.20271); [ResearchGate](https://www.researchgate.net/publication/413051617_Catching_the_Rug_Early_Prediction_of_Fraudulent_Memecoins_on_Solana_via_Machine_Learning); [takara.ai summary](https://tldr.takara.ai/p/2608.20271); [st-hakky summary](https://book.st-hakky.com/en/news/ml-predicts-solana-memecoin-rug-pulls)
- A separate tool, SolRugDetector (arXiv:2603.24625), reports F1 = 0.96 for Solana rug-pull detection. Do not attribute this figure to "Catching the Rug." — [arXiv 2603.24625](https://arxiv.org/abs/2603.24625)
- Solidus Labs published a "2025 Rug Pull Report" on rug pulls and pump-and-dumps on Solana. This is industry context, not an ML benchmark; I did not read its contents. — [Solidus Labs](https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance)
- MemeChain (arXiv:2601.22185) is a multimodal, cross-chain dataset for meme-coin forensics and risk analysis. — [arXiv 2601.22185](https://arxiv.org/pdf/2601.22185)

**Success, viability and graduation prediction**
- Marino, Naviglio, Tarantelli and Lillo, "Predicting the success of new crypto-tokens: the Pump.fun case" (arXiv:2602.14860, Feb 2026):
  - Defines success as **graduation** from the bonding curve to the on-chain market.
  - Builds a *conditional probability* prediction model from SOL locked in bonding curves, token launch structure and user behavioural features.
  - Chose Pump.fun because its uniform contract avoids honeypots and other DEX quirks that would contaminate labels.
  - I did not obtain its accuracy figures.
  - Sources: [arXiv abs](https://arxiv.org/abs/2602.14860); [arXiv HTML](https://arxiv.org/html/2602.14860v1); [DiarioBitcoin coverage](https://www.diariobitcoin.com/memecoins/estudio-revela-que-senales-anticipan-el-exito-de-los-tokens-lanzados-en-pump-fun/)
- CoinCLIP (arXiv:2412.07591) is a multimodal (image + text, CLIP-style) framework that scores memecoin "viability" from Pump.fun metadata. In its dataset, 44.27% of tokens are labelled "Viable." That share is far above real-world graduation base rates, so the label is not "graduated" or "profitable." — [arXiv 2412.07591](https://arxiv.org/pdf/2412.07591)
- "Bridging Culture and Finance" (arXiv:2412.04913) is a multimodal text + image analysis of Pump.fun memecoins. — [arXiv 2412.04913](https://arxiv.org/pdf/2412.04913)
- "The Memecoin Phenomenon: An In-Depth Study of Solana's Blockchain Trends" (arXiv:2512.11850). — [arXiv 2512.11850](https://arxiv.org/pdf/2512.11850)
- Base rates that any classifier must beat:
  - About 1.41% of Pump.fun tokens reached Raydium, per Dune data. — [BTC-Echo](https://www.btc-echo.de/schlagzeilen/solana-memecoins-nur-141-prozent-aller-token-sind-erfolgreich-189405/)
  - Nearly 69% of tokens launched on Pump.fun since Jan 2024 stopped trading on their first day, per CoinGecko. — [Cointelegraph](https://cointelegraph.com/news/memecoins-pump-fun-99-percent-fail-launch)
  - About 1–3% of tokens graduate, per a practitioner site. — [MadeOnSol](https://madeonsol.com/learn/graduated-pump-fun)
  - Fewer than 100 Pump.fun tokens were above $1M market cap at one point in 2024. — [Decrypt](https://decrypt.co/249107/fewer-than-100-pump-fun-tokens-above-1m-market-cap-amid-meme-coin-lull?amp=1)
- A Solana hackathon track, "Predict Pump.Fun Token Graduation," used graduation as a public ML prediction task. — [Solana Skill Sprint (Notion)](https://solanaskillsprint.notion.site/Predict-Pump-Fun-Token-Graduation-1c59ca5fcbe7803dbda1cc6cc4991761)

**Wallet graphs, coordination and data-quality audits**
- Kamat (arXiv:2607.02795, July 2026) studies coordinated sniper groups on pump.fun:
  - Reports 1,012 persistent wallet rings.
  - Argues that naive causal inference about first-hour buyer flow has limits.
  - A companion paper (arXiv:2607.02823) audits the **graduation labels produced by data collectors**. That directly affects any supervised model trained on them.
  - Sources: [arXiv 2607.02795](https://arxiv.org/abs/2607.02795); [IDEAS 2607.02823](https://ideas.repec.org/p/arx/papers/2607.02823.html)
- "Do Two On-Chain Observation Pipelines See the Same Tokens? Cross-Pipeline Coverage on the Solana pump.fun Launchpad" (arXiv:2609.18975). Its title implies that different ingestion pipelines capture different token sets, which is a dataset-construction risk. — [arXiv 2609.18975](https://arxiv.org/pdf/2609.18975)
- Szwajcok et al., "Meme coin factories: Uncovering large-scale manipulations on pump.fun" is cited in arXiv:2609.10246. I saw only the title. — [arXiv 2611.11436 reference list via search](https://arxiv.org/pdf/2611.11436)
- No published GNN benchmark for pump.fun graduation or memecoin success turned up. The closest work is the wallet-ring and sniper-cohort graph analysis above. — [arXiv 2607.02795](https://arxiv.org/abs/2607.02795)

**Pump-and-dump detection: classic crypto, mostly CEX-listed coins**
- La Morgia et al., "The Doge of Wall Street" (ACM TOIT 2023, arXiv:2105.00733):
  - Data: more than 1,000 confirmed pump-and-dump events from 20 Telegram groups.
  - Result: a market-data model detects a pump within 25 seconds of its start, with **94.5% F1**.
  - Sources: [arXiv 2105.00733](https://arxiv.org/html/2105.00733v2)
- PumpSense (KAUST, arXiv:2605.09431, May 2026):
  - Dataset: over 280,000 Telegram posts from 39 pump-organizing groups, with 2,246 labelled pump announcements.
  - Best detection F1: **0.83 for a BGE-M3 transformer**, against **0.79 for LightGBM**.
  - Latency is reported inconsistently between the abstract and a third-party review, so it is unverified.
  - Sources: [arXiv 2605.09431](https://arxiv.org/abs/2605.09431); [HTML](https://arxiv.org/html/2605.09431)
- Bolz et al. (University of Zurich, arXiv:2412.18848) use NLP/LLMs to classify Telegram messages. They cover 2,079 past pump events and detect new ones in real time. I did not obtain accuracy figures. — [arXiv 2412.18848](https://arxiv.org/html/2412.18848v2)

**Strategy backtests**
- arXiv:2611.11436, "Retrospective Analysis of Team-Following Trading Profitability," tests copying creators or teams who repeatedly launch and pump tokens. It warns that such backtests can rely on information not available in real time, so apparent profits may be illusory. — [arXiv 2611.11436](https://arxiv.org/pdf/2611.11436)

### Inferences
- The F1 scores of roughly 0.8–0.95 in these papers are not comparable. They measure different tasks:
  - detecting that a pump has started;
  - classifying a Telegram message;
  - classifying a token as a future rug.
- None of these is the same as an *exploitable* trading edge after fees, slippage, MEV/sniper competition and latency.
- Rug detection at about 5 minutes is plausibly easy because the base rate of "bad" tokens is extremely high, often above 90%. High accuracy can come largely from class imbalance. Precision and recall on the rare "good" class, and calibration, are the metrics that matter for a trader.
- The repeated distribution shifts (Pump.fun vs Raydium; label audits; pipeline coverage differences) strongly suggest that models trained on one launchpad or period decay quickly.

### Gaps
- Exact precision/recall/AUC for "Catching the Rug" and Marino et al. could not be read, because arxiv.org was unreachable.
- I found no peer-reviewed study showing out-of-sample *profitable* memecoin selection with an ML model, net of costs.
- I found no LSTM-specific memecoin benchmarks in the searches. LSTM work exists mostly for BTC/ETH price forecasting and was not verified here.

## 2. LLM-based trading agents: ai16z/ElizaOS, Virtuals, aixbt, Alpha Arena

### Takeaway
Documented, verifiable P&L for "AI agent" funds (ai16z, Virtuals agents) is essentially absent. The agents' *tokens* rose and then collapsed 80–99%. The best controlled evidence is Nof1's Alpha Arena, which is short, small-sample and run on Hyperliquid perps rather than memecoins:
- Season 1 (Oct–Nov 2025): 2 of 6 LLMs made money and 4 lost heavily.
- Season 1.5 (US-stock perps, ended Dec 3 2025): won by a then-anonymous model, later revealed as Grok 4.20, at +12.11%.

### Cited Findings
**Alpha Arena (Nof1)**
- Season 1 ran Oct 18 to Nov 3, 2025, with six LLMs given $10,000 each in real money on Hyperliquid.
  - Qwen 3 Max won with $12,231 (**+22.31%**). DeepSeek V3.1 was second at **+4.89%**. The other four lost money.
  - Loss figures differ across aggregators. One gives a range of −42% to −59%; another gives Claude −30.8% and GPT-5 −62.7%. Treat them as unsettled.
  - Sources: [Moby](https://moby.win/learn/alpha-arena/); [Keel](https://usekeel.io/agent/ai-trading-arena); [Yellow](https://yellow.com/learn/ai-models-real-money-trading-test)
- Season 1.5 used US stock perpetuals and eight models, including Kimi and a "mystery model," across four competitions with different rules. The mystery model, later revealed as Grok 4.20, won with **+12.11%** aggregate across the four. — [OneDayAdvisor review](https://www.onedayadvisor.com/2025/12/nof1ai-alpha-arena-review-season-15.html); [Traderank](https://www.traderank.ai/alpha-arena-leaderboard)
- Nof1 lessons as reported:
  - Models over-traded, and fees erased small gains.
  - Models were highly sensitive to small prompt changes.
  - Nof1 itself says one run should not name a permanent best model.
  - Sources: [Buildix blog](https://www.buildix.trade/blog/nof1-alpha-arena-lessons-ai-trading-byok-strategy-advisor-2026); [BigGo Finance](https://finance.biggo.com/news/5BSX_Z0BaoGGrU-ID27J)
- One aggregator said that as of August 2026 no Season 2 roster or results had been posted. I could not verify the status as of November 2026 because the search budget was exhausted. — [Traderank alternatives](https://www.traderank.ai/blog/alpha-arena-alternatives-2026)

**ai16z / ElizaOS**
- ai16z is a Solana DAO whose flagship agent is a persona named after Marc Andreessen. It runs on the ElizaOS framework and was "trained on his public writings."
- Sources indicate humans still influenced buy/sell decisions, and community votes govern proposals.
- The project rebranded to ElizaOS in early 2025 after brand concerns from Andreessen Horowitz.
- Sources: [Cointelegraph](https://cointelegraph.com/news/elizaos-rebrand-ai16z-token-drop); [Bybit Learn](https://www.bybit.com/en/learn/ai/what-is-ai16z-crypto); [ElizaOS FAQ](https://elizaos.github.io/eliza/docs/faq)
- I found no independent audit or published P&L for the agent's trading. Market-cap spikes such as "$80M in a day" after a Marc Andreessen tweet reflect token speculation, not trading skill. — [Alea Research](https://alearesearch.substack.com/p/ai16z-autonomous-investment-dao-what)

**Virtuals agents**
- Virtuals' daily revenue fell from about $1.02M in early January 2025 to about $34,792 by late February 2025. VIRTUAL was 88.8% below its $5.07 all-time high. — [Decrypt](https://decrypt.co/309495/virtuals-protocol-revenue-crashes-ai-agent-demand-sinks)
- Weekly AI-agent token volume fell from about $2.5B in December 2024 to $54M in early March 2025, per Flipside. Daily Virtuals agent launches dropped from up to 1,300 in November 2024 to fewer than 100 in all of February 2025. — [Cointelegraph](https://cointelegraph.com/news/ai-agents-virtual-revenue-plunge-token-price-decline); [The Defiant](https://thedefiant.io/virtuals-protocol-revenue-craters-by-95)
- One report says Virtuals revenue was down to about $500/day by April 2026. This is unverified, and the date needs checking. — [CoinGlass](https://www.coinglass.com/news/442676)
- An on-chain whale exited AI-agent tokens at losses of about 91–99%. — [Invezz](https://invezz.com/news/2025/02/12/virtual-price-falls-as-whale-dumps-tokens-at-4-4m-loss)
- A blog post describes a 2026 "agent winter," with agent tokens crashing while production adoption grew. — [BlockEden](https://blockeden.xyz/blog/2026/03/27/agent-winter-paradox-ai-token-crash-production-adoption-soars/)

**aixbt (an Virtuals-ecosystem "alpha caller" agent)**
- Pix On Chain analysis, as reported by Crypto Briefing:
  - 183 of 210 mentioned tokens were "profitable" (83%).
  - Buy-and-hold every call returned about **+4.57%**. Selling at peaks returned **+54.71%**, which is look-ahead and not achievable.
  - Data sources were not specified.
  - Source: [Crypto Briefing](https://cryptobriefing.com/ai-crypto-predictions-impressive-gains)
- BeInCrypto Korea, using Sentient Market data, counted 416 promoted tokens with a **48% win rate** and a 19% average return. — [BeInCrypto KR](https://kr.beincrypto.com/ai-agent-aixbt-crypto-shilling-performance/)
- Researcher Shlok Khemani noted that aixbt mentions cause real price surges, especially for AI tokens under $100M market cap. That is reflexive price impact, not forecasting skill. — [TechFlow](https://www.techflowpost.com/en-US/article/22952); [ChainCatcher](https://chaincatcher.com/en/article/2162356)

### Inferences
- The "AI agent" memecoin wave of 2024–25 was mostly about *tokenized personas and launchpads*, not verified trading performance. The best-documented money flows are token price collapses.
- Alpha Arena shows how dispersed LLM trading results are over a ~2-week window. With n=6 models and one run each, the outcome is consistent with noise plus differences in risk-taking and leverage, rather than proven skill.
- Any "agent call" performance claim that uses peak-exit returns should be discounted. Influential agents can also create self-fulfilling pumps, which inflates measured hit rates.

### Gaps
- I could not find any audited P&L for the ai16z/ElizaOS fund or for Virtuals agents' own wallets.
- I could not confirm whether Alpha Arena Season 2 or later seasons ran in 2026, or their results.
- Other public LLM hedge-fund experiments (for example, open-source "AI hedge fund" GitHub repos) were not researched before the search budget ran out.

## 3. Feature engineering, labeling, overfitting and non-stationarity

### Takeaway
The working features are early-life on-chain microstructure:
- capital in the bonding curve;
- buyer counts and concentration;
- creator and sniper behaviour;
- launch structure;
- the first-minutes trade flow.

Image/text metadata adds modest signal. Labels such as "graduation," "viability" and "rug" are fragile and depend on the pipeline. Distribution shift across launchpads and time is the dominant failure mode.

### Cited Findings
- Marino et al. use SOL locked in the bonding curve, token launch structure and user behavioural features. — [arXiv 2602.14860](https://arxiv.org/abs/2602.14860)
- "Catching the Rug" uses only first-5-minute trading data, with no contract-code features. It finds a significant Pump.fun ↔ Raydium distribution shift. — [arXiv 2608.20271](https://arxiv.org/html/2608.20271v1)
- Sniper and wallet-ring features: 1,012 persistent coordinated wallet rings were found. The author warns that naive causal reading of first-hour buyer flow has limits. — [arXiv 2607.02795](https://arxiv.org/abs/2607.02795)
- Label audits: graduation labels from data collectors were audited in arXiv:2607.02823. Cross-pipeline coverage differences on pump.fun were studied in arXiv:2609.18975. — [IDEAS 2607.02823](https://ideas.repec.org/p/arx/papers/2607.02823.html); [arXiv 2609.18975](https://arxiv.org/pdf/2609.18975)
- Multimodal features: CoinCLIP and "Bridging Culture and Finance" use token image + name/description embeddings. — [arXiv 2412.07591](https://arxiv.org/pdf/2412.07591); [arXiv 2412.04913](https://arxiv.org/pdf/2412.04913)
- Look-ahead bias in strategy backtests is explicitly flagged in team-following research. — [arXiv 2611.11436](https://arxiv.org/pdf/2611.11436)
- Practitioner write-ups on early graduation signals are not peer-reviewed:
  - "first 3 minutes graduation math" — [MadeOnSol](https://madeonsol.com/blog/pump-fun-first-3-minutes-graduation-math)
  - an audit of 832,941 pump.fun launches — [BraveNewCoin](https://bravenewcoin.com/insights/what-auditing-832941-pump-fun-launches-taught-me-about-memecoin-success); not readable in this session
  - a developer's account of building a Solana memecoin intelligence system — [DEV Community](https://dev.to/techkene/what-i-learned-from-building-a-solana-memecoin-intelligence-system-3829)

### Inferences
- Labeling choices define the problem. Each of these yields a different model with a different economic meaning:
  - "graduated" (bonding-curve completion);
  - "viable" (CoinCLIP-style, 44% positive);
  - "reached $X market cap";
  - "N× from entry price at time t."

  Only the last kind maps directly to a trading decision, and it must be computed from a realistic entry price after sniper/MEV fills.
- Survivorship and coverage bias are likely when datasets come from indexers that miss tokens (per arXiv 2609.18975). Leakage is likely when features use data after the decision timestamp.
- Non-stationarity is structural. Launchpad mechanics, fees, the dominant launchpads and sniper tooling change every few months. Walk-forward or time-split validation is mandatory; random K-fold will overstate performance.
- Adversarial adaptation: once a rug/graduation signal is public, coordinated wallet rings can game it, for example by faking organic buyer distribution.

### Gaps
- I did not find quantitative feature-importance tables (for example, SHAP rankings) from the papers, because full texts were inaccessible.
- No source quantified how fast model performance decays over time on memecoin data.

## 4. LLMs for real-time narrative and sentiment classification

### Takeaway
LLMs and transformers are useful for *classifying* crypto text: detecting pump announcements, extracting targets and scoring sentiment, including emojis. Evidence that LLM sentiment produces profitable memecoin trades is thin and largely limited to BTC/ETH backtests.

### Cited Findings
- PumpSense: a BGE-M3 transformer reached F1 0.83 at detecting Telegram pump announcements, beating LightGBM at 0.79. It also performs target-coin extraction. — [arXiv 2605.09431](https://arxiv.org/abs/2605.09431)
- Bolz et al. use LLM/NLP classification of Telegram messages for real-time pump detection (2,079 historical events). — [arXiv 2412.18848](https://arxiv.org/html/2412.18848v2)
- Zuo, Chen and Härdle use GPT-4 and fine-tuned BERT to score **emoji** sentiment in crypto tweets. Emoji sentiment had more predictive power than FinBERT text sentiment for BTC and the VCRIX index, and helped strategies avoid major downturns. — [arXiv 2402.10481](https://arxiv.org/pdf/2402.10481)
- arXiv:2502.14897 adds market context via prompt tuning to fine-tuned CryptoBERT/FinBERT on Bitcoin tweets. It aggregates daily predictions into trading signals and outperforms traditional sentiment + price fusion models in a 3-year backtest covering bull, bear and neutral regimes. — [arXiv 2502.14897](https://pdf.arxiv.org/pdf/2502.14897)
- arXiv:2311.14759 studies BTC/ETH with news, Twitter and Reddit. It finds pre-trained Twitter-RoBERTa and BART-MNLI effective for capturing sentiment, and fine-tuned LLMs give "substantial forecasting improvements." — [arXiv 2311.14759](https://arxiv.org/html/2311.14759v1)
- Roumeliotis et al. (Big Data and Cognitive Computing, June 2024) compare fine-tuned GPT-4, BERT and FinBERT for crypto *news* sentiment classification. — [MDPI](https://mdpi.com/2504-2289/8/6/63)
- Memecoin multimodal "culture" analysis with text + image models on Pump.fun tokens. — [arXiv 2412.04913](https://arxiv.org/pdf/2412.04913)

### Inferences
- For memecoins, the practical LLM uses are:
  - fast triage of new tokens' names, images and tickers into narrative clusters (AI, politics, animal, celebrity);
  - spam and scam detection;
  - monitoring Telegram/X for coordinated calls.

  In these uses latency and cost matter more than marginal accuracy. PumpSense suggests a compact embedding model can beat gradient boosting on text at moderate latency.
- Sentiment edges reported on BTC are unlikely to transfer directly. Memecoin social signal is dominated by paid shills, bots and coordinated groups, and the evidence that coordinated rings exist supports this concern ([arXiv 2607.02795](https://arxiv.org/abs/2607.02795)). Sentiment is likely more useful as a *risk filter* than as an alpha source.
- Reflexivity: LLM agents that post calls (aixbt) move the prices they predict. That contaminates any sentiment → return dataset that includes their posts.

### Gaps
- I found no rigorous study of LLM narrative classification feeding a live *memecoin* trading strategy with net-of-cost results.
- I have no data on LLM inference latency or cost versus the speed of pump.fun price discovery, which happens in seconds to minutes.
