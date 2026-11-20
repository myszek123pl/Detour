# X/Twitter data access for a memecoin bot (as of Nov 2026)

Note: research used 5 web searches (budget ~6). Most figures come from vendor marketing or secondary guides; items marked [UNVERIFIED] must be checked on the vendor's live page.

## 1. Cost, latency, reliability, legal risk of each option

### Takeaway
Official X API is pay-per-use at about $0.005 per post read (3M reads/month cap) and is the lowest legal risk but costly for broad scanning. Third-party APIs (twitterapi.io ~$0.15/1k tweets, SocialData ~$0.20/1k) are ~25-35x cheaper per tweet, with vendor-claimed sub-second push monitoring, but are gray-area scrapers with vendor/ToS risk. xAI's x_search tool is for LLM-style search ($5/1k calls, pricing possibly changing), not low-latency streaming.

### Cited Findings
- Official X API: pay-per-usage, no subscription, credits bought up front in Developer Console; most 2026 guides list $0.005 per post read, $0.001 per owned read; 3M post reads/month cap, above that needs Enterprise (unpublished price). Some third-party pages say 2M cap, but X docs say 3M. Post creation prices conflict ($0.01 vs $0.015; URL posts reportedly $0.20). — [X docs pricing](https://docs.x.com/x-api/getting-started/pricing), [opentweet](https://opentweet.io/x-api-pricing), [postproxy](https://www.postproxy.dev/blog/x-api-pricing-2026/), [bundle.social](https://bundle.social/blog/x-api-pricing-2026-costs-limits)
- X replaced its $200 entry-level plan with the pay-per-use model — [Open Terms Archive](https://opentermsarchive.org/en/memos/x-replaces-its-dollar200-entry-level-api-plan-with-a-pay-per-use-model/)
- twitterapi.io: from $0.15 per 1k tweets (15 credits/tweet, 100k credits = $1), no monthly floor, no read cap; claims median response <0.5s, firehose-fed sub-second freshness, WebSocket and webhook support; a third-party review quotes 500-800 ms stream latency. All mostly vendor-sourced, no independent benchmark found. Competitor Sorsa says minimum per-request charge rose 25% in 2025 and ToS fixes no price. — [twitterapi.io](https://twitterapi.io/), [Sorsa comparison](https://api.sorsa.io/compare/twitterapi-io-pricing)
- GetXAPI lists twitterapi.io at ~$0.003/call (~20 tweets/call); its own monitoring plans from $19/month for 6 monitored accounts, no per-request charge on monitor endpoints (competitor claims, [UNVERIFIED]) — [GetXAPI pricing](https://www.getxapi.com/pricing?tab=monitoring)
- SocialData: $0.0002/tweet ($0.20/1k) for timelines, mentions, lookups; no subscription, balance doesn't expire; 120 req/min per key (raise on request). — [SocialData pricing](https://socialdata.tools/pricing.md), [docs](https://socialdata.gitbook.io/docs/pricing)
- SocialData monitoring reported by competitor twitterapi.io as ~$4.49 per user monitor (50 accounts ~ $224.50) [UNVERIFIED, competitor claim]; native webhook delivery not confirmed — [twitterapi.io vs SocialData](https://twitterapi.io/compare/vs-socialdata)
- Apify: kaitoeasyapi "Tweet Scraper" actor advertised at $0.25/1k tweets pay-per-result (actor-run model, batch-oriented, not push) — [Apify actor](https://apify.com/kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest)
- xAI Grok API: x_search tool ("search X posts, user profiles, threads") listed at $5/1k calls plus token costs on official docs. One secondary article (RuntimeWire) claims from Sept 21 (2026) billing switches to $5/1k posts fetched and $10/1k user profiles fetched [UNVERIFIED, single secondary source]. — [xAI pricing](https://docs.x.ai/developers/pricing), [RuntimeWire](https://runtimewire.com/article/xai-is-changing-the-economics-of-x-search-runtimewire-was-built-for-a-narrower-r)
- Legal: In X Corp v. Bright Data (N.D. Cal. 3:23-cv-03698), Judge Alsup dismissed X's claims in May 2024 (contract claim not plausibly alleged for scraping public data; copyright preemption of data-resale claims). Reports say X later partially revived contract claims and then settled; dates unconfirmed. — [CNBC](https://www.cnbc.com/2024/05/10/elon-musks-x-loses-lawsuit-against-bright-data-over-data-scraping.html), [Law360](https://law360.com/amp/articles/2266208), [Bloomberg Law](https://news.bloomberglaw.com/ip-law/musks-x-settles-data-scraping-dispute-against-israeli-data-firm)

### Inferences
- Cost illustration: scanning 1M tweets/month costs ~$5,000 on official API vs ~$150-200 on third-party; the official 3M cap (~$15k) also binds. Official API is only sensible for narrow KOL-timeline polling or if legal cleanliness matters.
- Bright Data outcome suggests scraping public data is lower civil risk for a bot operator than for the vendor, but X's ToS prohibit it and X can ban accounts/ IPs; the real risk is vendor disappearance or breakage (third-party APIs depend on guest tokens/accounts that X periodically blocks), not litigation against end users. Not legal advice.
- Grok x_search is useful for narrative/sentiment summarization of a token, not for sub-second KOL alerts (LLM latency of seconds, per-call cost).
- Recommended stack: third-party push monitor for ~50-200 KOL accounts (primary) + second vendor as failover + optional official API for verification of high-value calls.

### Gaps
- No independent latency benchmark for any vendor; official X filtered-stream availability/pricing under pay-per-use not confirmed in my searches.
- Current Apify and SocialData monitoring prices, and the date/terms of the X v. Bright Data settlement, unverified.
- Whether xAI's Sept 2026 X Search billing change is real.

## 2. Low-latency KOL account monitoring

### Takeaway
Use vendor push monitoring (webhook/WebSocket) on a fixed KOL list rather than polling; vendor-claimed latency is ~0.5-1s, versus polling intervals bounded by rate limits (SocialData 120 req/min/key).

### Cited Findings
- twitterapi.io advertises WebSocket/webhook live data and sub-second latency (vendor claim) — [twitterapi.io](https://twitterapi.io/)
- GetXAPI monitoring plans (6 accounts from $19/mo) and SocialData monitors (~$4.49/monitor, competitor claim) show push monitoring is priced per account, not per tweet — [GetXAPI](https://www.getxapi.com/pricing?tab=monitoring), [twitterapi.io vs SocialData](https://twitterapi.io/compare/vs-socialdata)
- Polling math with SocialData: 120 req/min shared over all endpoints — [SocialData docs](https://socialdata.gitbook.io/docs/pricing)

### Inferences
- Polling 100 KOLs once every 5s needs 1,200 req/min, 10x SocialData's default limit, so push monitoring or a raised limit is needed.
- Measure end-to-end latency yourself (tweet created_at vs receipt timestamp) per vendor before trusting claims.

### Gaps
- No verified data on KOL-tweet delivery latency percentiles (p50/p99) or missed-tweet rates.

## 3. Fields that matter for detecting CA posts and KOL calls

### Takeaway
Source did not document a field standard; the following is analytical guidance. Combine text signals (CA regex) with author-quality and engagement fields. I found no cited source for "smart followers" availability by vendor.

### Cited Findings
- None sourced in this search budget for field-level specifics. Vendors return standard tweet/user objects (follower counts, created_at, etc.) per general API design; not verified per vendor.

### Inferences
- Tweet fields: text (Solana base58 32-44 chars regex; EVM 0x + 40 hex; $TICKER cashtags), entities/urls (pump.fun, dexscreener, birdeye links), created_at (latency/ordering), id, is_reply/is_quote/retweet (a KOL quoting a CA is a call; replies under big accounts are spam), media, lang, view/like/retweet/reply counts early (velocity in first minutes).
- Author fields: followers_count, following ratio, account created_at (new accounts <30 days = shill/bot risk), verified/blue status, statuses_count, profile description/ name changes, and whether author is on your KOL whitelist.
- "Smart followers" (count of followed-by known influential accounts, as on Ethos/ TweetScout/ Kaito-type scores) is a third-party derived metric, not a native X field; compute yourself by intersecting follower lists with a curated KOL set (costly) or use a dedicated analytics API [UNVERIFIED availability].
- Dedupe: same CA from many fresh low-follower accounts within minutes = coordinated shilling; weight by author quality and count of distinct KOLs mentioning the CA.
- Always validate the CA on-chain (token exists, age, liquidity) since fake CAs and lookalike addresses are common.

### Gaps
- No verified per-vendor field lists or smart-follower sources; recommend checking each vendor's response schema.

## 4. Grok/xAI access (summary)

### Takeaway
Grok API gives X search via the x_search tool (priced per call, possibly moving to per-item billing); consumer Grok subscription is not an API for bots.

### Cited Findings
- x_search at $5/1k calls on xAI docs; token costs separate — [xAI pricing](https://docs.x.ai/developers/pricing)
- Possible per-post/profile billing from Sept 21 ($5/1k posts, $10/1k profiles) [UNVERIFIED] — [RuntimeWire](https://runtimewire.com/article/xai-is-changing-the-economics-of-x-search-runtimewire-was-built-for-a-narrower-r)

### Inferences
- Best used as an enrichment step on already-flagged tokens (sentiment, "who is talking about this CA"), not as the detection layer.

### Gaps
- Rate limits, latency, and whether results are complete (vs sampled) not found.
