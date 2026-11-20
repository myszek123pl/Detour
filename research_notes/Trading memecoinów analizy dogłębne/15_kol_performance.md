# Measured performance of publicly tracked KOL wallets (Kolscan, GMGN, Cielo), 2025-2026

Note on method: 6 web searches; WebFetch failed (madeonsol.com and dlnews.com not in the session's allowed network domains), so everything below comes from search-result summaries, not full pages. Figures are marked [UNVERIFIED] where I could not open the primary source. No Kolscan/GMGN/Cielo-specific win-rate dataset from an independent party was found.

## 1. What are the measured win rates and PnL distribution of tracked KOL wallets?

### Takeaway
The only aggregate figures found come from a commercial tracker (MadeOnSol): average 30-day win rate about 42% across 457 scored KOL wallets, with about a quarter above 50%. No independent study of Kolscan/GMGN/Cielo leaderboards was found, and leaderboards show survivors only.

### Cited Findings
- MadeOnSol's June 2026 analysis of 457 scored Solana KOL wallets: average 30-day win rate about 42%, roughly a quarter above 50%; it concludes blindly copying a random KOL is negative expected value. [UNVERIFIED, vendor figure, page not opened] — [MadeOnSol](https://madeonsol.com/blog/what-is-a-kol-in-crypto)
- MadeOnSol August 2026 report: 1.13M trades across 533 wallets; median market cap at a KOL's first buy $4,654 (vendor figure, snippet only). [UNVERIFIED] — [MadeOnSol report](https://madeonsol.com/blog/solana-kol-trading-report-august-2026)
- Vendor guides argue win rate alone misleads; profit factor is preferred (e.g. 50% win rate with 3.0 profit factor beats 80% with 0.9). [UNVERIFIED, vendor opinion] — [MadeOnSol](https://madeonsol.com/blog/how-to-evaluate-solana-signal-callers-win-rate-roi)
- Solana Tracker publishes a KOL leaderboard API ranking named wallets by period PnL (documentation only, no aggregate stats extracted) — [Solana Tracker docs](https://docs.solanatracker.io/guides/pnl-v2/leaderboards)
- Kolscan is a leaderboard of top memecoin traders/KOLs with real-time trades and token PnL — [The Block](https://www.theblock.co/post/362119/pump-fun-makes-first-acquisition-purchases-solana-based-copy-trading-wallet-tracker-kolscan)

### Inferences
- A 42% average win rate is consistent with memecoin trading where a few large winners carry PnL; the PnL distribution is likely heavily skewed (inference, no cited distribution data).
- MadeOnSol sells KOL-tracking products, so its pessimistic framing is not obviously self-serving but its sampling is unverified.

### Gaps
- No Kolscan, GMGN or Cielo published aggregate win rate or PnL percentile data found.
- No data on survivorship bias, sample windows, or wallet-attribution accuracy (KOLs use side wallets, see Q3).

## 2. How do followers perform after KOL buys?

### Takeaway
No study directly measures follower returns. Indirect evidence: Bitquery found only ~26% of large Pump.fun wallet gains were replicable by a copier, and an ACM Web Conference 2026 paper frames copy trading as exit liquidity for early buyers.

### Cited Findings
- Bitquery: 3,170 wallet-token positions with gains of at least $100k (Oct 2025 to Aug 2026), $752.5M sampled gains; only ~26% passed its trading checks, largely because tokens were moved between wallets leaving no visible buy to copy. Bitquery did not measure actual copy-trader performance. — [CryptoSlate](https://cryptoslate.com/pump-funs-biggest-winners-may-be-impossible-to-copy-as-752-million-study-exposes-hidden-trading-gap/); [KuCoin summary (headline "74% cannot be replicated")](https://www.kucoin.com/news/flash/bitquery-study-reveals-74-of-pump-fun-gains-cannot-be-replicated-by-copy-traders)
- ACM Web Conference 2026 paper (arXiv 2601.08641) describes copy trading as common in meme coin markets and says some KOLs on tracking platforms may buy early, induce copiers to inflate the price, then exit — a conceptual framing plus a multi-agent LLM defence proposal, not a measurement of follower losses. — [arXiv](https://arxiv.org/html/2601.08641)
- MadeOnSol claims the second KOL followed the first within 9 seconds in its data, and followers' entry is usually well above the KOL's price. [UNVERIFIED vendor claim] — [MadeOnSol report](https://madeonsol.com/blog/solana-kol-trading-report-august-2026)

### Inferences
- Latency plus thin early liquidity means retail followers likely enter at materially worse prices than the KOL; magnitude unmeasured.

### Gaps
- No independent measurement of follower PnL, slippage or post-call price path found. Bitquery's full report not opened.

## 3. Front-running evidence

### Takeaway
Evidence is case-by-case on-chain forensics (mainly Bubblemaps), not aggregate rates. Allegations, not adjudicated, and not tied to the Kolscan leaderboard itself.

### Cited Findings
- Bubblemaps, Oct 15 2026: KOL Anglio allegedly used five linked wallets for front-running and high-price dumping, ~$130k cumulative cash-out. — [Rootdata/Bubblemaps summary](https://www.rootdata.com/news/817111)
- Bubblemaps, Nov 5 2026: four KOLs examined; 0xEthan allegedly often sells ~3 minutes after a call with public and hidden wallets buying simultaneously, ~$125k related profit; Solstice-promoted coins showed dozens of new wallets buying simultaneously. — [TechFlow](https://techflowpost.com/en-US/article/34592)
- Bubblemaps, Nov 10 2026: KOL Cupsey allegedly traded 27,000+ tokens via 30 associated wallets since May 7, ~$1.74M profit. — [Rootdata](https://www.rootdata.com/news/822794)
- Separate leaked-DM claims that KOLs took payment to shill (snippet truncated, not a Bubblemaps finding). [UNVERIFIED] — [AiCoin/Foresight](https://www.aicoin.com/en/news-flash/3170579)
- Bubblemaps' own blog says many KOLs do want followers to do well — [Bubblemaps blog](https://blog.bubblemaps.io/no-shame-shillers-mesmerizing-bundles-recent-events.md)

### Inferences
- Because KOLs allegedly use undisclosed side wallets, leaderboard PnL on public wallets may both understate KOL profits and fail to show what followers can replicate.

### Gaps
- No rate of front-running across tracked KOLs; KOL responses not checked; alleged amounts are Bubblemaps' estimates.

## 4. Effect of Pump.fun's Kolscan acquisition

### Takeaway
Announced July 2025 (days before the PUMP ICO of July 12), Pump.fun's first acquisition, price undisclosed; Kolscan tools became free and folded into social trading. Traders who bought the Kolscan token just before the announcement made over $3M. Post-deal effects on KOL behaviour or leaderboard integrity were not found.

### Cited Findings
- Pump.fun's first acquisition, undisclosed price; Kolscan analytics to be integrated into social trading features; Kolscan features made free. — [The Block](https://www.theblock.co/post/362119/pump-fun-makes-first-acquisition-purchases-solana-based-copy-trading-wallet-tracker-kolscan); [Blockworks](https://blockworks.co/news/pump-fun-kolscan)
- DL News: traders who bought the Kolscan-linked token just before the deal was public made over $3M (mid-2025 article; I could not open it to check details). — [DL News](https://www.dlnews.com/articles/defi/memecoin-kols-bag-millions-as-pump-fun-buys-kolscan-tracker/)
- Framed as gamifying trading ahead of the ICO — [crypto.news](https://crypto.news/pump-fun-acquires-solana-wallet-tracker-kolscan-to-gamify-trading-ahead-of-ico/)

### Inferences
- Ownership by a launchpad creates a conflict of interest (leaderboards drive volume on Pump.fun); this is inference, no source documents misuse.

### Gaps
- No measured change in KOL win rates, trade volume or copy-trading behaviour after the acquisition; no GMGN or Cielo data found. Which KOLs bought the token is not confirmed in my sources.
