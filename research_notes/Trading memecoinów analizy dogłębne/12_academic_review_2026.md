# Academic review 2025-2026: memecoins and pump.fun (arXiv/SSRN)

Access note: arxiv.org, www.arxiv.org, export.arxiv.org, alphaxiv and api.semanticscholar.org all failed DNS resolution in this session (outside the allowed network domains). Only WebSearch snippets were available (9 searches, a couple rate-limited). Every figure below comes from search-result summaries, not from reading the papers. Figures not confirmed against a paper's own text are marked [UNVERIFIED]. Methods, limitations and bot implications that the snippets did not state are labelled as inference or gap, not as findings.

## 2602.14860: Predicting the success of new crypto-tokens, the Pump.fun case (graduation prediction)

### Takeaway
Marino, Naviglio, Tarantelli and Lillo (q-fin.ST, 16 Feb 2026) model the probability that a pump.fun token graduates from its bonding curve, using the evolving state of the curve. Graduation is the base-rate bottleneck: roughly 0.6% of tokens graduate [UNVERIFIED, secondary source]. The paper's predictors, model type and accuracy were not retrievable.

### Cited Findings
- Authors, title and date; graduation is treated as the measure of token "success". The paper builds models estimating graduation probability from the evolving state of the bonding curve — [arXiv abs](https://arxiv.org/abs/2602.14860) (via search snippet)
- Dataset reported by a news site: 655,770 tokens created in September 2025, of which 4,338 (0.63%) graduated. The reported dataset size and rate were not checked against the paper — [Diario Bitcoin](https://www.diariobitcoin.com/memecoins/estudio-revela-que-senales-anticipan-el-exito-de-los-tokens-lanzados-en-pump-fun/) [UNVERIFIED]
- The study is an on-chain analysis of early-stage launches that asks which early trading signals predict graduation — [arXiv HTML v1](https://arxiv.org/html/2602.14860v1) (snippet)

### Inferences
- With a base rate near 0.6%, a classifier needs very high precision at a low alert rate to be useful. Report precision/recall at fixed thresholds rather than AUC.
- Because the paper conditions on curve state, a bot can re-score at several checkpoints (for example, % of curve filled and the first N trades) rather than predict only at launch.
- Graduation is not profit. Buying a token before it graduates is not the same as exiting profitably after graduation. Any model should be backtested on PnL after fees, slippage and tips, not on graduation hit rate.

### Gaps
- Feature list, model (likely gradient boosting or logistic, but not confirmed), AUC/precision numbers, train/test split and limitations: not retrievable (arxiv blocked).

## 2512.11850: The Memecoin Phenomenon, an in-depth study of Solana's blockchain trends

### Takeaway
Davide Mancino (cs.CY, Dec 2025, v3 on 18 Dec 2025) gives a descriptive on-chain picture of Solana in Q4 2024: pump.fun dominates minting and fewer than 2% of tokens reach major DEXs.

### Cited Findings
- Pump.fun accounted for up to 71.1% of tokens minted on Solana, and an estimated 40-67.4% of DEX transactions — [arXiv abs v3](https://arxiv.org/abs/2512.11850v3) (via search summary)
- Fewer than 2% of tokens successfully transitioned to major decentralized exchanges. The author interprets this as a highly speculative market — [arXiv abs v2](https://arxiv.org/abs/2512.11850v2) (via search summary)
- Data window is Q4 2024 on-chain data — [arXiv HTML v2](https://arxiv.org/html/2512.11850v2) (via search summary)

### Inferences
- The "<2% reach a major DEX" figure is for Q4 2024. The Sept 2025 graduation rate (about 0.6%) is lower, which suggests a declining or shifting base rate. The two figures use different definitions of "success", so they are not directly comparable.
- Descriptive study: useful for priors on token counts and platform share, not for edge.

### Gaps
- Methods, data source, per-metric breakdowns and stated limitations were not retrievable.

## 2507.01963: A Midsummer Meme's Dream, market manipulations in the meme coin ecosystem

### Takeaway
Mongardini and Mei (USENIX Security 2026) find that most high-return memecoins show signs of manipulation, so many apparent winners are engineered and end in exit scams.

### Cited Findings
- Dataset: 34,988 meme coins across Ethereum, BNB Smart Chain, Solana and Base, released publicly — [USENIX Security 26 page](https://www.usenix.org/conference/usenixsecurity26/presentation/mongardini) (via search summary)
- 707 tokens had >100% returns in a three-month study window. 82.8% of them show artificial growth in v2 (v1: 82.6%; USENIX listing: 82.89%), through recurrent wash trading and liquidity-pool-based price inflation — [arXiv v2](https://arxiv.org/abs/2507.01963v2); version discrepancy noted in the search summary
- 62.9% of high-return tokens used artificial growth to facilitate exit scams, rising to 86.67% among delisted ones — [arXiv HTML v2](https://arxiv.org/html/2507.01963v2) (via search summary) [UNVERIFIED]

### Inferences
- Volume, holder count and a rising chart are contaminated signals. A bot should filter for wash-trading patterns (repeated same-wallet round trips, funding-linked buyers) and LP-manipulation before treating momentum as organic.
- Most of the sample is outside pump.fun (four chains), so rates may not transfer to Solana bonding-curve launches.

### Gaps
- Detection method details (heuristics vs. classifier), false-positive rate and limitations: not retrieved.

## 2601.08641: Resisting Manipulative Bots in Memecoin Copy Trading (multi-agent LLM, chain-of-thought)

### Takeaway
Luo, Feng, Xu and Liu (submitted 13 Jan 2026; v2 and v3 exist) argue that copy trading is not reliably profitable because of manipulative bots, uncertain wallet persistence and execution lag, and propose a three-agent LLM system.

### Cited Findings
- Three specialised agents (coin evaluation, wallet selection, timing assessment), each using few-shot chain-of-thought prompting — [arXiv abs](https://arxiv.org/abs/2601.08641v3) (via search summary)
- On a dataset of 1,000 meme coin projects, the system reportedly beats traditional ML models and single LLMs, with 73% precision for identifying high-quality projects and 70% for key opinion leader (KOL) wallets — [arXiv HTML](https://arxiv.org/html/2601.08641) (abstract-level only) [UNVERIFIED against full text]
- The paper notes Solana's ~400 ms block times and the absence of a public mempool — [arXiv HTML](https://arxiv.org/html/2601.08641) (via search summary)

### Inferences
- Copy-trade latency (about 400 ms blocks plus detection delay) means you buy after the leader. The paper's framing suggests following wallets should be filtered for manipulation and persistence, not just past PnL.
- Precision is reported as precision only; recall, realised PnL and out-of-time performance were not seen. LLM-call latency and cost are an obvious bot constraint (inference).

### Gaps
- Labelling definition of "high quality", train/test split, PnL results, and limitations: not retrieved.

## 2608.20271 (Catching the Rug) and 2611.11436

### Takeaway
Neither ID could be verified. Searches for "arxiv 2608.20271 Catching the Rug" and "arxiv 2611.11436 memecoin" returned no matching paper. These IDs may be mistyped or not indexed. No content is reported for them.

### Cited Findings
- Search for 2608.20271 returned only unrelated August 2026 papers (for example 2608.12652, 2608.25553) — [search result](https://huggingface.co/papers/2608.12652) (unrelated)
- Search for 2611.11436 returned no hit; nearest results were 2512.00377 and the papers above — [arXiv 2512.00377](https://arxiv.org/abs/2512.00377v1)

### Inferences
- Treat both as unconfirmed until the IDs are checked. Rug-detection literature that was found is covered in the sections on 2507.01963 and the Kamat papers below.

### Gaps
- Title, authors, method and numbers for both IDs: not found.

## Other relevant papers surfaced by the searches

### Takeaway
Three extra items bear directly on a bot: fragility of attention-driven tokens, survival modelling of launches, and label-quality problems for graduation models.

### Cited Findings
- "Measuring Memecoin Fragility" (arXiv 2512.00377) introduces a Sentiment Amplification Score for attention-driven shocks. It finds politically themed tokens (TRUMP, MELANIA, LIBRA) concentrate the highest risks, while ETH and SOL are resilient — [arXiv](https://arxiv.org/abs/2512.00377v1) (via search summary)
- Arati Uday Kamat has a survival analysis of 832,941 token launches [UNVERIFIED, title and ID not captured] — [IDEAS](https://ideas.repec.org/p/arx/papers/2607.02823.html) (listing surfaced; the link to the 832,941 figure is from a search summary and was not confirmed)
- A later paper, "Auditing Collector-Generated Graduation Labels on Pump.fun: Measurement Error and Temporal Non-Generalization", suggests graduation labels from data collectors contain measurement error and that models do not generalise across time — [arXiv 2607.02823](https://arxiv.org/abs/2607.02823) (title only; attribution and findings not verified)
- Platform changes shift base rates: a July 2026 report says graduation rate jumped after "BOOST" changed launch incentives; durability unclear — [The Block](https://theblock.co/news/defi/2026-07-29-pump-fun-token-graduation-rate-jumps-boost-changes-launch-incentives-409815) (headline only)

### Inferences
- Any graduation or rug model trained on 2024-2025 data likely suffers regime drift. Re-fit on a rolling window and monitor the base rate, since the platform's incentives change.
- Check labels yourself (on-chain migration events) rather than trusting scraped datasets.

### Gaps
- Full details of these papers were not read. No SSRN papers were reached.

## Cross-paper practical implications for a bot (inference, not findings)
- Base rate is tiny (about 0.6% graduation, <2% reach major DEXs in other data), so selectivity matters more than model accuracy.
- Most high returns in the broader memecoin set are manipulated (about 83% in Mongardini and Mei); filter wash trading and LP inflation, and expect exit scams.
- Copy trading suffers latency and bot-contamination; wallet selection should test persistence and manipulation.
- Data and labels drift over time; validate out of time.
