# LLM-based real-time narrative/meta detection pipeline for memecoins (as of Nov 2026)

Research limits: only 1 of ~6 planned web searches returned results (others hit "too_many_requests"); dev.to was unreachable from the sandbox (host not in allowed domains), so cited pages were NOT read in full - only search-result summaries. Most content below is marked UNVERIFIED (training knowledge).

## Embedding and clustering token names/tickers/descriptions and tweets

### Takeaway
Common design: embed name/ticker/description/posts, cluster incrementally, then have an LLM label and score each emerging cluster. No independent benchmarks of real-time performance were found.

### Cited Findings
- A Solana write-up describes an engine combining Twitter, Telegram and on-chain data, feeding the LLM recent trending topics, token metadata and recently pumped similar tokens for narrative scoring — [DEV Community (gerus_team)](https://dev.to/gerus_team/how-we-built-an-ai-powered-trend-detection-engine-for-solana-meme-coins-3n67) (search snippet only, page not fetched)
- A separate Solana narrative detector uses simple keyword/topic sets rather than heavy ML — [DEV Community (theauroraai)](https://dev.to/theauroraai/building-a-real-time-solana-narrative-detector-on-chain-signals-github-trends-and-market-data-49i8) (snippet only)
- A 2025 memecoin paper combines LDA topics of descriptions, logo images, community and financial data — [arXiv 2507.01963](https://arxiv.org/pdf/2507.01963) (snippet only)
- Online K-means on streaming Twitter messages for meme clustering; time-series features suggested as an improvement — [arXiv 1411.0652](https://arxiv.org/pdf/1411.0652)
- A misinformation paper clusters embeddings hierarchically and has Claude summarize clusters from centroid-nearest messages, asking for the underlying narrative rather than surface topic — [arXiv 2608.29681](https://arxiv.org/pdf/2608.29681) (snippet only; ID as returned by search, unverified)

### Inferences
- Practical pipeline: (1) ingest new mints + tweets; (2) normalize (lowercase, strip emoji/symbols, keep ticker and emoji separately); (3) embed with a small embedding model (multilingual, since many memes are non-English/image-based); (4) incremental clustering (nearest-centroid assignment with similarity threshold, periodic HDBSCAN re-cluster); (5) LLM labels clusters only when they cross a size/velocity threshold (keeps LLM calls cheap).
- Image/logo matters for memecoins; a vision-embedding (e.g. CLIP-like) channel is likely needed — UNVERIFIED design suggestion.

### Gaps
- No verified details on embedding model choices, thresholds, or dedup of copycat tokens (copycats are themselves the signal of a narrative).

## Trend/burst detection algorithms

### Takeaway
Run burst detection on per-cluster counts (new tokens, unique authors, mention rate), not raw terms. Algorithms are standard; I found no sourced memecoin-specific tuning.

### Cited Findings
- (None sourced; search for burst detection failed.)

### Inferences (all UNVERIFIED, from training knowledge)
- Kleinberg's 2002 burst automaton (rate-state model) for term/cluster arrival rates.
- Simpler, cheaper alternatives for real time: EWMA/z-score on counts, ratio of short vs long window (e.g. 5 min vs 1 h), CUSUM, Twitter-style "trending" = velocity x unique-author count.
- BERTopic (UMAP+HDBSCAN+c-TF-IDF) has online/topics-over-time modes, but is batch-oriented; for streaming prefer custom nearest-centroid or river/DenStream-type online clustering.
- Guard against bot/shill amplification: weight by unique accounts, account age, and dedupe near-identical text.

### Gaps
- No verified paper/benchmark combining burst detection with embedding clusters for crypto.

## Model choices, costs, latency (small vs large)

### Takeaway
Use a tiered setup: embeddings + rules for 100% of stream, small/cheap LLM for cluster labeling and per-token classification, large model only for periodic narrative summaries. Self-reported end-to-end latency in one product was ~8 s.

### Cited Findings
- Gerus team reports 8.2 s average detection-to-alert latency, 34% signal accuracy (token reached >=2x), ~22% false positives after three weeks live — self-reported, unverified — [DEV Community](https://dev.to/gerus_team/how-we-built-an-ai-powered-trend-detection-engine-for-solana-meme-coins-3n67) (snippet only)

### Inferences
- Pricing (UNVERIFIED, training knowledge; searches for current pricing failed): Claude Haiku 4.5 about $1/M input, $5/M output; Haiku 3.5 $0.80/$4; Haiku 3 $0.25/$1.25. Newer models may have changed this — check the official pricing page.
- Rough cost estimate (my arithmetic): 10k tokens/min of classification input at ~$1/M ≈ $0.6/hour; so LLM cost is minor if you filter first; embeddings are cheaper still. Local small models (e.g. 7-8B open models) are an option for latency/cost, UNVERIFIED.
- Prompt caching and batching reduce cost for repeated system prompts (feature exists per training knowledge; verify).

### Gaps
- No current (Nov 2026) model list, prices or latency measurements verified.

## Existing tools

### Takeaway
A few products/blog projects exist; their quality claims are unverified marketing/self-reports.

### Cited Findings
- "Narrative Engine" Telegram channel advertises contextual relevance, narrative structure, deployability scoring, filtering layers and real-time clustering — [t.me/s/narrativeengine](https://t.me/s/narrativeengine/5) (snippet only)
- The two DEV Community projects above (open-style write-ups).

### Inferences
- General trackers (DexScreener, Birdeye, DEXTools; UNVERIFIED) show trending tokens but not LLM-defined narratives. Other commercial tools (e.g. Kaito-style social analytics) may exist — UNVERIFIED, not searched.

### Gaps
- No systematic survey of tools as of Nov 2026; search failed.

## Evaluation methods

### Takeaway
Evaluate narrative detection as a forecasting problem with time-stamped, point-in-time data; the one live report uses hit-rate of >=2x and false-positive rate.

### Cited Findings
- Gerus team metrics: 34% of signals reached at least 2x, ~22% false positives, 3 weeks live — self-reported — [DEV Community](https://dev.to/gerus_team/how-we-built-an-ai-powered-trend-detection-engine-for-solana-meme-coins-3n67)
- No independent benchmark found; none located for real-time memecoin narrative systems.

### Inferences (UNVERIFIED design suggestions)
- Cluster quality: manual labeling of a sample, purity/NMI vs hand labels, LLM-as-judge with human spot checks.
- Detection quality: lead time of alert vs. peak of cluster volume/market cap; precision/recall against retrospectively labeled metas; compare against baseline (DexScreener trending, keyword counts).
- Trading relevance: forward returns of tokens bought at alert vs control tokens, after fees/slippage; avoid look-ahead and survivorship bias; walk-forward testing; 34% hit rate means little without base rate of 2x for all new tokens.

### Gaps
- Base rates and a standard benchmark dataset not found.
