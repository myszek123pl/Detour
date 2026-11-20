# KOL (Key Opinion Leader) and Telegram/Discord Call-Channel Influence on Memecoin Price Action

> Research status note (Nov 20, 2026): Full-text fetches were blocked in this session's network sandbox (arxiv.org, link.springer.com, theblock.co, hbswk.hbs.edu and madeonsol.com all failed to resolve). The shared web-search budget then ran out after 12 queries. Every finding below therefore comes from search-result snippets and summaries, not full papers. Numbers should be checked against the primary PDFs before anyone relies on them for trading parameters. Planned searches that never ran: La Morgia et al. pre-announcement insider timing; DL News on the Kolscan acquisition; KOL price-per-post economics; regulatory (SEC/FTC) disclosure cases; the HBS celebrity-token paper. These topics appear under Gaps.

## 1. Empirical evidence on the price impact of KOL tweets and calls (size, duration, decay)

### Takeaway
The best peer-reviewed evidence is Merkley, Pacelli, Piorkowski and Williams (Review of Accounting Studies, 2024): about 36,000 tweets from 180 crypto influencers. It finds small, short-lived positive returns of about +1.8% on day one. These returns start to reverse within about five days and turn negative over months (one report says about −19% at three months). The effect is largest for small caps and for self-described "experts" with large followings. Newer memecoin and Telegram studies find the same shape: a short spike, then a drawdown larger than the gain.

### Cited Findings
- **"Crypto-influencers"** by Kenneth Merkley, Joseph Pacelli, Mark Piorkowski and Brian Williams. *Review of Accounting Studies*, vol. 29(3), pp. 2254–2297, September 2024 — [IDEAS/RePEc](https://ideas.repec.org/a/spr/reaccs/v29y2024i3d10.1007_s11142-024-09838-4.html); [Springer](https://link.springer.com/article/10.1007/s11142-024-09837-5)
  - Sample: about 36,000 tweets by 180 prominent crypto influencers, covering more than 1,600 crypto assets over the two years to December 2022 — [Kelley School blog](https://blog.kelley.iu.edu/?p=4898); [Futurity](https://www.futurity.org/crypto-influencer-advice-investment-3260122)
  - Mean 1-day return after influencer tweets: **+1.83%**. Mean 2-day return: **+1.57%**, already lower than the 1-day figure. Returns "begin to decline substantially as early as five days after the tweets." One write-up reports an average loss of **about 19% after three months** — numbers relayed by the [Kelley blog](https://blog.kelley.iu.edu/?p=4898), [ProMarket](https://www.promarket.org/2023/04/17/crypto-influencers-give-poor-investment-advice-and-the-sec-is-taking-notice/) and [DL News](https://dlnews.com/articles/defi/crypto-influencers-deliver-only-brief-gains-for-investors/). I could not confirm which outlet gives the −19% figure, or whether it appears in the final published version.
  - Effects are strongest for influencers who call themselves crypto experts, for smaller-cap assets, and for self-described experts with many followers. Longer-horizon returns are more negative for self-described experts, and more negative still for experts with larger followings — [Kelley blog](https://blog.kelley.iu.edu/?p=4898); [ProMarket](https://promarket.org/?p=36952)
  - Fewer than 15% of tweets were negative. Most expressed excitement and urged followers to buy, and the return pattern is stronger for positive-sentiment tweets and buy recommendations — [Kelley blog](https://blog.kelley.iu.edu/?p=4898)
  - The authors describe the pattern as "consistent with pump and dump schemes," or at least as showing that the advice has little long-term investment value. They say it is not a "smoking gun" — [ProMarket](https://www.promarket.org/2023/04/17/crypto-influencers-give-poor-investment-advice-and-the-sec-is-taking-notice/); [Oxford Business Law Blog](https://blogs.law.ox.ac.uk/oblb/blog-post/2023/11/crypto-influencers-give-poor-investment-advice-and-sec-taking-notice)
- Alan Jagolinzer's published discussion (RAST 2024) says the evidence is "consistent with but is not necessarily conclusive regarding influencers being incentivized by pump-and-dump schemes." He also notes that investors may recognize influencer conflicts, which would dampen price impact — [Cambridge repository](https://www.repository.cam.ac.uk/items/4b60be25-ae70-49ca-809d-6d8cbb27d10b); [SUFE academic newsletter](https://academicnewsletter.sufe.edu.cn/info/413908)
- Separate HBS research on celebrity crypto promoters (headline: "when celebrity crypto influencers rake in cash, investors lose big"). Coverage notes that celebrities may receive low-cost or free token allocations, which they can sell once the price starts rising — [HBS Working Knowledge](https://hbswk.hbs.edu/item/when-celebrity-crypto-influencers-rake-in-cash-investors-lose-big). The page itself could not be fetched, so I have no quantitative results from it.
- Twitter amplification of pump-and-dumps: a 2023 arXiv event study finds that Twitter promotion draws attention to targeted coins, with "notable effects on abnormal returns before the event" — [arXiv 2306.02148](https://arxiv.org/pdf/2306.02148v1)
- Telegram-driven activity, "Don't You Know, Pump it Up!" (arXiv 2609.01176, Sept 2026): pump-and-dump events show a **mean peak gain of about 10%** and a **mean maximum drawdown of about −14.8%**. Buyers at the peak lost money. The paper treats public Telegram channels as traces of promotional shilling, not proof of private coordination — [arXiv 2609.01176](https://arxiv.org/html/2609.01176v1)
- Memecoin base rates that shape any post-call decay. More than 73% of Pump.fun memecoins fell below 40% of their migration (graduation) price within the study window — [MemeTrans, arXiv 2602.13480](https://arxiv.org/html/2602.13480v1). Pump.fun accounted for up to 71.1% of Solana token mints in Q4 2024 — [arXiv 2512.11850](https://arxiv.org/abs/2512.11850)

### Inferences
- For liquid, larger-cap tokens, an average KOL call is worth low single-digit percent over hours to a day. Most of the value accrues in the first 24h, and the effect reverses within about a week. For micro-cap memecoins, the same mechanism scales up: the coefficient is largest for small caps. Peaks can be tens to hundreds of percent, but the round trip is faster and deeper.
- The +1.83% (1-day) versus +1.57% (2-day) pattern means even a 2-day hold gives back part of the gain. A bot that trades the signal needs to enter within minutes and exit within hours. It should not "follow the call" as an investment.
- The "expert with a large following" result points to a scoring feature. Large-audience self-proclaimed experts produce the biggest short-term pop and the worst long-term returns. That makes them the best source of a short-window momentum signal and the worst choice for holding.

### Gaps
- No study found gives a minute-level decay curve (for example, half-life in minutes) for memecoin KOL calls on Solana. The 2018–2022 tweet study uses daily returns, which is too coarse for pump.fun-era memecoins.
- I could not verify the exact −19%/3-month figure in the final RAST version, or whether the reported 1-day and 2-day means are raw or abnormal returns.
- No quantitative results were obtained from the HBS celebrity-token paper.

## 2. KOL front-running, paid-promotion economics and disclosure

### Takeaway
Public on-chain investigations, mainly by ZachXBT, document large-scale undisclosed paid promotion. A September 2025 dataset covered 160–200+ influencers, and fewer than five labelled paid posts as ads. The investigations also show wallet-level patterns consistent with buy-before-call / sell-into-followers. Much of this evidence is allegation relayed by crypto media, not adjudicated fact. Academic work is consistent with pump-and-dump incentives but has not proven them.

### Cited Findings
- **ZachXBT's paid-promotion spreadsheet, Sept 2025.** It covered 200-plus influencers, with price lists, wallet addresses and on-chain payment records. Fewer than five labelled their paid posts as ads. Outlets give different counts: The Block's headline says "over 100," other reports say "over 160." Some coverage frames the issue as non-disclosure rather than fraud — [The Block](https://www.theblock.co/post/368956); [99Bitcoins](https://99bitcoins.com/news/altcoins/night-of-terror-for-paid-crypto-influencers-zachxbt-spotlights-the-dirtiest-players-in-crypto-twitter/); [EtherWorld](https://etherworld.co/zachxbt-slams-crypto-kols-over-paid-shilling/)
- Coverage of the same investigation reports two things. First, one wallet may be linked to several KOL accounts and collect promotion fees two or more times for the same project. Second, in one case a KOL's wallet showed profitable trades "precisely around the time of promotion." This comes from secondary Chinese-language crypto media and is an allegation — [Odaily](https://www.odaily.news/en/post/5206059); [TechFlow](https://www.techflowpost.com/en-US/article/27945)
- **One operator, 16 accounts:** ZachXBT reported that one person controlled 16 blue-check X accounts used to shill memecoins. This means a "consensus" of several KOLs calling the same coin can be manufactured — [BeInCrypto](https://beincrypto.com/zachxbt-exposes-16-x-meme-coin-accounts)
- **Ansem, Oct 2024:** ZachXBT accused Zion "Ansem" Thomas of promoting "hundreds" of low-market-cap Solana memecoins that behaved like pump-and-dumps. Thomas disputed the accusation — [The Defiant](https://thedefiant.io/news/hacks/zachxbt-accuses-influencer-ansem-promoting-solana-memecoin-pump-dumps-ac9dfb13); [CoinMarketCap Academy](https://coinmarketcap.com/academy/article/crypto-influencer-ansem-accused-of-promoting-memecoin-pump-and-dumps-by-zachxbt); [Cointelegraph](https://cointelegraph.com/news/zachxbt-slams-crypto-influencer-over-memecoin-promotions)
- **Soulja Boy, Dec 2025:** ZachXBT warned about a new memecoin linked to the rapper. He had earlier tied the rapper to 73 crypto and 16 NFT projects flagged as scams — [Cryptonews AU](https://cryptonews.com.au/news/zachxbt-raises-red-flags-over-new-soulja-boy-promoted-memecoin-132181/)
- **Celebrity and KOL compensation:** besides cash fees, promoters can receive low-cost or free token allocations and sell them once the price rises — [HBS Working Knowledge](https://hbswk.hbs.edu/item/when-celebrity-crypto-influencers-rake-in-cash-investors-lose-big)
- **Kolscan insider episode:** Pump.fun acquired the Kolscan KOL-tracker in mid-2025 (Bitget dates it to July 10, 2025). DL News reported that top traders who bought the Kolscan-themed token just before the deal became public made over $3M in profit — [DL News](https://www.dlnews.com/articles/defi/memecoin-kols-bag-millions-as-pump-fun-buys-kolscan-tracker/); [Bitget DApp Store](https://web3.bitget.com/dapp/kolscan-29881)
- **The SEC is paying attention to influencer conflicts.** Academic commentary links the RAST findings to regulatory interest — [Oxford Business Law Blog](https://blogs.law.ox.ac.uk/oblb/blog-post/2023/11/crypto-influencers-give-poor-investment-advice-and-sec-taking-notice); [ProMarket](https://www.promarket.org/2023/04/17/crypto-influencers-give-poor-investment-advice-and-the-sec-is-taking-notice/)

### Inferences
- The typical extraction sequence has five steps. (1) The project or agency pays a KOL in SOL/USDC or token allocation. (2) The KOL, or wallets linked to them, buy before the post. (3) The KOL posts, often in coordination with other paid or sock-puppet accounts. (4) Followers and copy-trade bots buy. (5) The KOL sells into that demand within minutes to hours. In this sequence, followers are exit liquidity by design.
- Because payment is usually undisclosed, it cannot be detected from the post alone. A bot has to infer it on-chain: transfers from the deployer or team wallets to the KOL's known wallets, KOL buys in the minutes before the post timestamp, and several KOLs posting within a tight time window.
- The "16 accounts, one operator" case and the "one wallet, many KOL accounts" case both suggest that cross-KOL confirmation, often treated as a stronger signal, may be manufactured. Clustering KOL wallets by funding source should come before counting independent calls.

### Gaps
- No systematic dataset of KOL price-per-post for memecoins (USD per tweet or Telegram post by follower tier) was retrieved. The ZachXBT spreadsheet has prices, but I could not access the figures.
- No quantified, population-level measure of front-running was found, such as the share of KOL calls where the KOL wallet bought before the post, or the median time from post to sell.
- No search could be done on specific enforcement actions (SEC/FTC/UK FCA finfluencer cases, EU MiCA marketing rules).

## 3. Public KOL wallet trackers (Kolscan, GMGN KOL lists and others) and how they perform

### Takeaway
Trackers such as Kolscan (owned by Pump.fun since mid-2025), Solana Tracker's KOL leaderboard and MadeOnSol's roster of more than 1,000 wallets make KOL trades visible in real time. Vendor data shows that most tracked KOL wallets are not profitable traders. In June 2026, the average 30-day win rate was 42%, and only about 1 in 4 active KOL wallets won more than 50% of trades. A "KOL" label measures fame, not skill.

### Cited Findings
- **Kolscan:** a Solana wallet tracker that monitors top memecoin traders and KOLs, with real-time trades, PnL and leaderboards. Acquired by Pump.fun around July 10, 2025 — [Kalkine Media](https://kalkinemedia.com/education/guides/kolscan-how-solanas-smart-money-gets-ranked); [Bitget](https://web3.bitget.com/dapp/kolscan-29881); [DL News](https://www.dlnews.com/articles/defi/memecoin-kols-bag-millions-as-pump-fun-buys-kolscan-tracker/)
- **Solana Tracker:** its KOL leaderboard covers tracked wallets with a public identity (name, Twitter handle, avatar) and compares realized and unrealized PnL, ROI, trade count and recency. Its separate top-trader board is not limited to KOLs and is capped at the top 500,000 wallets per period. It offers an API endpoint for KOL leaderboards by period — [Solana Tracker docs: leaderboards](https://docs.solanatracker.io/guides/pnl-v2/leaderboards); [KOL tracking guide](https://docs.solanatracker.io/guides/kol-tracking); [Get KOL leaderboard API](https://docs.solanatracker.io/data-api/pnl-v2/leaderboard/get-kol-leaderboard)
- **MadeOnSol** (vendor, self-reported data):
  - It tracks 1,000+ Solana KOL wallets with PnL leaderboards, median hold time and "early-entry percentile" — [MadeOnSol KOL tracker](https://madeonsol.com/kol-tracker)
  - It defines a KOL as any publicly identified wallet, "regardless of recent performance" — [MadeOnSol methodology](https://madeonsol.com/blog/solana-kol-tracking-methodology-1069-wallets)
  - **June 2026:** of 1,071 tracked KOL wallets, 474 traded in the prior 30 days. Only **118 (about 1 in 4)** had a win rate above 50%. Across 457 scored wallets, the **average 30-day win rate was 42%**, and "the median KOL loses more trades than they win" — [MadeOnSol, "Do KOL calls actually make money?"](https://madeonsol.com/blog/what-is-a-kol-in-crypto)
  - The same post describes a "buy-post-dump" pattern, visible as a short hold time paired with a tweet timestamp — [MadeOnSol](https://madeonsol.com/blog/what-is-a-kol-in-crypto)
  - A 2026 methodology post reports 1.5M SOL of volume from 485 wallets — [MadeOnSol](https://madeonsol.com/blog/solana-kol-tracking-methodology-1069-wallets). A March 2026 report covered 237,380 on-chain trades across 332 wallets — [MadeOnSol](https://madeonsol.com/blog/what-is-a-kol-in-crypto)
  - **August 2026:** 1.13M trades across 533 wallets. 533 of the 1,142 wallets on the roster traded during Aug 1–28, 2026. Buy and sell volume were roughly balanced, with net flow of −6,542 SOL — [MadeOnSol Aug 2026 report](https://madeonsol.com/blog/solana-kol-trading-report-august-2026)
- Vendors also publish copy-trade "top KOL wallet" lists, for example "Top 10 KOL Wallets to Copy Trade on Solana (April 2026)" — [MadeOnSol](https://madeonsol.com/blog/top-solana-kol-wallets-to-copy-trade). These are marketing content, not audited performance.

### Inferences
- KOL wallets on trackers have two very different uses. For copy-trading they are mostly poor: the median win rate is below 50%, followers enter after the KOL with worse fills, and KOLs know they are being watched. As a flow and timing signal they are useful: when a KOL wallet buys, a post and a follower inflow often follow, and when it sells, the top is often in.
- Public tracking creates a reflexive game. Once a wallet is labelled on Kolscan or GMGN, copy-bots front-run it. KOLs can respond by buying through fresh, unlabelled wallets, by "bait buying" from the labelled wallet to attract copiers and then selling from another wallet, or by selling into copy-bot demand. Labelled-wallet signals therefore decay as they become popular.
- A tracker's leaderboard PnL may include profits that come directly from followers. A high-ranking KOL may be skilled at extracting from their audience, not at picking tokens, and copying that wallet makes the copier part of the extraction.

### Gaps
- **GMGN KOL lists:** no source on GMGN's KOL labelling method or on the observed performance of GMGN-labelled KOL wallets was retrieved before the search budget ran out.
- No independent (non-vendor) audit of Kolscan leaderboard performance or copy-trading outcomes was found.
- No data was found on post-to-sell latency, the share of KOL buys preceding a post, or copy-trader slippage. The MadeOnSol "buy-post-dump" claim is qualitative in the retrieved text.

## 4. Telegram call channels and pump groups: how they work and what happens to followers

### Takeaway
Organized Telegram/Discord pump groups are well studied. Groups advertise very large targets (an average of 212% in one sample of 500 schemes), but realized median returns are small (4.1% in a 952-scheme study). Recent Telegram data shows a mean peak gain of about 10% against a mean maximum drawdown of about −14.8% for peak buyers. Organizers and insiders profit at the expense of late followers. Today's memecoin "call channels" follow the same structure and are dominated by the pump.fun launch environment, where most tokens collapse.

### Cited Findings
- **The Block, about 500 pump-and-dump schemes on 230+ tokens:** in the 229 cases where groups stated a target, the **average advertised target return was 212%**. This is a stated target, not a realized outcome — [The Block](https://www.theblock.co/post/2209/researchers-study-over-500-cryptocurrency-pump-and-dump-schemes)
- **Hamrick et al., SSRN, 952 schemes:** **median return of 4.1%**. Returns for "transparent" pumps did not fall over time, while returns for "obscured" pump organizers fell significantly — [UCL Discovery (SSRN 3303365)](https://discovery.ucl.ac.uk/10133232/1/SSRN-id3303365%20%281%29.pdf)
- **Xu & Livshits, "The Anatomy of a Cryptocurrency Pump-and-Dump Scheme"** (USENIX Security 2019): 412 pump-and-dumps organized in Telegram channels, June 17, 2018 to February 26, 2019. The reported "return as high as 80% within three weeks" — [arXiv 1811.10109](https://arxiv.org/pdf/1811.10109v1); [arXiv Vanity](https://www.arxiv-vanity.com/papers/1811.10109/). Caution: the snippet is ambiguous about whether this 80% is the pumps' own return or the return of the authors' prediction-based trading strategy over three weeks. Check the paper before citing it as the pumps' return.
- **"The Doge of Wall Street" (La Morgia et al.)** analyses and detects pump-and-dumps organized on Telegram/Discord — [arXiv 2105.00733](https://arxiv.org/html/2105.00733v2). Its specific findings, such as pre-announcement insider timing, were not retrieved.
- Other pump-and-dump literature: [arXiv 1902.03110](https://arxiv.org/pdf/1902.03110.pdf); [HKBU working paper](https://econ.ntu.edu.tw/wp-content/uploads/2023/12/HKBU_1091015.pdf)
- **PumpSense (arXiv, May 2026):** a dataset of 283,017 Telegram messages from 39 groups, including 2,246 labelled pump-start announcements with target coin and exchange. It is a detection paper, not a returns paper — [arXiv 2605.09431](https://arxiv.org/html/2605.09431)
- **Telegram-driven activity (arXiv 2609.01176):** mean peak gain about +10%, mean maximum drawdown about −14.8% for participants who bought at the peak. Public channels act as promotional shilling — [arXiv 2609.01176](https://arxiv.org/html/2609.01176v1)
- **Memecoin-era manipulation:**
  - "A Midsummer Meme's Dream" (arXiv 2507.01963) studied 34,988 tokens on Ethereum, BSC, Solana and Base. The later version identifies 91 pump-and-dump operations, 54 of them on Solana, and quantifies victim losses. Solana tokens showed a smaller median price decline than other chains — [arXiv 2507.01963v2](https://arxiv.org/html/2507.01963v2)
  - "Meme Coin Factories" (arXiv 2609.10246) covers all 15.2M pump.fun coins and finds that strategic manipulation tactics raise prices and extract value. It cites literature linking Telegram/Discord groups to coin prices but excludes private Telegram channels from its case study — [arXiv 2609.10246](https://arxiv.org/html/2609.10246v1)
  - Pump.fun accounted for up to 71.1% of Solana mints and 40–67.4% of DEX transactions in Q4 2024 — [arXiv 2512.11850](https://arxiv.org/abs/2512.11850)
  - More than 73% of Pump.fun memecoins fell below 40% of migration price — [arXiv 2602.13480](https://arxiv.org/html/2602.13480v1)

### Inferences
- **How call channels work.** This is a synthesis of the pump-group literature applied to memecoin call channels; the general pattern is established, but the memecoin-specific steps are inference.
  - **Tiering:** VIP or paid tiers get the call first, then the public channel, then cross-posts to X. Each tier is exit liquidity for the tier above.
  - **Pre-positioning:** the organizer, dev or KOL wallets accumulate before the announcement.
  - **Announcement:** a coin name or contract address, timed to the second.
  - **Dump:** the price spikes within seconds to minutes and the organizers sell into the peak.
  - **Repeat:** cross-promotion and paid "callers" are recycled.
- **Outcomes for followers.** Realized medians are small or negative after costs, and peak buyers lose (−14.8% mean max drawdown versus a +10% mean peak). In memecoins, the >73% graduation-collapse base rate and the sub-50% KOL win rates imply that the average follower loses money, especially after priority fees, slippage and sniper competition.
- **Decay over time.** The transparent-versus-obscured result (Hamrick) suggests that as groups hide their targets, returns fall, likely because insiders capture more of the move.

### Gaps
- No quantified study of pump.fun-era Solana "call channels" was found, for example one measuring follower PnL by entry delay after a Telegram call. This is the most relevant missing piece for a Solana bot.
- La Morgia et al.'s pre-announcement insider timing results and their real-time detection accuracy were not retrieved.
- No Dune dashboard tracking KOL or call-channel outcomes was located; searches did not reach that stage.

---

## Implications for a memecoin bot

These are inferences drawn from the findings above; this subsection adds no new sourced claims.

**Using KOL and call signals (offence):**
1. Treat a KOL or call-channel post as a short-lived momentum or flow signal, not an investment thesis. The documented decay is about 1 day for liquid tokens (Merkley et al.) and minutes to hours for memecoins. A 2-day hold already underperforms a 1-day hold.
2. Speed is the whole edge. Monitor KOL wallets on-chain, through Kolscan, Solana Tracker or MadeOnSol APIs, rather than waiting for the tweet. A KOL buy often comes before the post.
3. Weight signals by audience size and "expert" self-branding for short-term pop (the RAST result), and discount them for hold duration.
4. Use hard exits: time-stop plus trailing stop. Exit immediately when the calling KOL's wallet sells.
5. Before trusting several KOLs calling the same coin as confirmation, deduplicate them by funding cluster. One operator can run 16+ accounts.

**Defending against KOL and call-channel extraction:**
1. Flag a token as high risk when: known KOL wallets bought in the N minutes before the post; deployer or team wallets funded KOL wallets; several KOL posts arrived within a tight window; or top-holder concentration rose just before the call.
2. Do not enter after the first price spike following a call. The peak-buyer drawdown (about −14.8% in the Telegram data) is the typical outcome.
3. Assume that labelled KOL wallets on public trackers are watched and may bait copy-bots. Prefer unlabelled "smart money" found through your own PnL screening, and re-score every rolling 30 days. Only about 25% of KOL wallets beat a 50% win rate.
4. Size positions assuming most called memecoins round-trip, given the >73% post-graduation collapse base rate.
