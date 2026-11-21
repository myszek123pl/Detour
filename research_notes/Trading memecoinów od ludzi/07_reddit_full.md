# 07 - Reddit: retail memecoin traders, self-reported experience (aggregated)

Date: 2026-11-21. Language: English. Supersedes the "no Reddit access" gap in 03_retail_experiences.md.

## Method and limits (read first)
- reddit.com itself returned 403 "blocked by network security" from this environment (old.reddit.com redirected to login). With explicit approval I used the public Arctic Shift archive instead: `https://arctic-shift.photon-reddit.com/api/posts/search` and `/api/comments/search`.
- Arctic Shift cannot sort by score, only by date. So I fetched posts after 2025-01-01 by keyword and ranked them locally by comment count and score. "Top" below means "most-discussed among keyword matches", not Reddit's all-time top.
- Coverage: about 372 unique posts from r/memecoins, r/SolanaMemeCoins, r/pumpfun and r/solana. Keywords: "lessons learned", "lost everything", "profitable", "journal". r/CryptoCurrency and r/CryptoMoonShots calls all failed, and a few other subreddit/keyword combinations failed (solana "lost everything"/"profitable", SolanaMemeCoins "lost everything", pumpfun "profitable"). "sniper bot results" and "copy trading results" were not run as separate queries (request budget; roughly 57 requests were wasted on a field-name error early on). Copy trading appears only incidentally.
- Comments: read in full for only 2 threads (the "are you profitable" threads, 68 and 55 comments). Other threads: post text only. Top-comment coverage is therefore thin.
- A large share of keyword hits is promotion (token shills such as repeated "RAWW", "$QUANT", "$RCTO" posts, paid tracker/bot tools, "I need $1" begging posts). I excluded these from the findings. Even among genuine-looking posts, the archive holds only people who chose to post: heavy selection toward losers who vent and winners who advertise.
- No usernames, wallet addresses or personal details are recorded. Post links use `https://www.reddit.com/comments/<id>/`. I deliberately do not link the posts that contain expressions of self-harm; they are counted in aggregate only.

## Typical journey (pattern repeated across many first-person posts)
1. Entry via social proof: "random kids doing really well", leaderboards, an ad on pump.fun via X, a friend who "made millions".
2. First deposit lost fast (days, sometimes hours: a $240 start gone in a few hours, a first $1,000 gone in a couple of days).
3. A single big hit creates the belief that it is skill: $3k to $30k in 12 hours; $3k debt to $5k, then $23k, then $38k within weeks. Several people quit job/school to trade full time right after this.
4. Escalation: size up, chase narratives ("next TRUMP"), revenge trading. Typical blow-ups cite the $LIBRA episode (about $30k lost in one position), missed $TRUMP, tariff crash.
5. Round trip: "up over $100,000 and did not take profits" -> "lost everything"; 30k -> 1.4k over a year while "holding the bag".
6. Fallout described repeatedly: debt (one reports $50k+ lost year to date and debt; another $50k in debt overall), relationship breakups, eviction, sleep loss, depression, gambling-addiction self-diagnosis. A noticeable minority of the "lost everything" posts contain suicidal language (3 of roughly 25 first-person loss posts I read).
7. Exit paths: quit, "need a break", or rebuild with rules (see below). Many still say they are "close to being profitable" after months or years.

## Time to profitability claims
- No credible quantified time-to-profit. Self-reports: 18 months of trading before a rules-based approach started working (one post, unverified); 8 months of losing and "50k in debt" (pumpfun); "2 years" of chasing losses; "started 2023, down 50-80k, still here".
- Someone claiming to be profitable "since mid August" (started that month) is the typical shape: a few weeks, no audited record.
- One commenter: profitable overall 5 years if you include launching tokens, "not even close" when only trading in the last 1-3 years.
- Conclusion: claims are rare, short, and unverifiable. Nothing here supports "profit in N months" as a base rate.

## Size of losses (self-reported)
- Small: $240 in hours; $1,000 in days; ~$3,000 "every dollar I had" into one token that went to zero instantly; ~$3,000 of savings.
- Medium: $10k+ (post by a self-described profitable dev/trader, after the first months); $30k on one position; "mid five figures" portfolio down 75%, then fully round-tripped; $30k from a 30k peak to 1.4k.
- Large: $50k+ in a year plus debt; $50k debt; "down 50-80k since 2023".
- Pattern: losses are mostly 100% of the account, not drawdowns. Winners' paper gains are returned at roughly 90-95%.

## Mistakes named most often (by frequency in the reads)
1. Not taking profit / round-tripping. Single most common (30k->1.4k; 100k->0; "sold at 2x-3x-never, got rugged after"; the reverse also appears: selling the one runner too early and tilting).
2. Oversizing / all-in after a win (half or all of the portfolio into one hyped token).
3. FOMO and chasing narrative launches; revenge trading after a loss; sizing up to match richer peers.
4. Holding losers on hope ("it has to pump eventually", waiting for an airdrop).
5. Trading while working/exhausted; emotional trades; sleep deprivation ("the biggest theft in meme coins is your time").
6. Trusting "safe-looking" tokens: top-10 holders at 9%, passed security checks, then -90% in one refresh; fake "Robinhood-sponsored" coin; fake token mimicking a legit staked-SOL token.
7. Paying for KOL/"educator" content, Discord software and groups; learning the edge was selling to students.
8. Not telling family, isolating.

## Scams and traps seen
- Instant rugs on tokens that look clean (small top-10, no obvious bundlers).
- Fake/lookalike tokens airdropped to wallets (fake staked-SOL token drained a user who interacted with it; most-upvoted genuine thread in r/solana in this set, score 54): https://www.reddit.com/comments/1m2v88p/
- Paid "Discord software", signal groups, KOL callouts (concerns that leaderboard wallets are coordinated or were picked after one lucky runner): https://www.reddit.com/comments/1x9vglp/ , https://www.reddit.com/comments/1xfwzp6/
- Begging/"fund my challenge" posts and token shills in the sub (spam is ~a third of keyword hits).
- Self-reported rug-pulling as a profitable business: "doubled my income" with ~24 SOL in two weeks (unverifiable, probably bait): https://www.reddit.com/comments/1nm16lm/ ; "how do devs launching hundreds of coins make money" https://www.reddit.com/comments/1w1af2n/ ; commenters repeatedly say the only reliable earners are devs/launchers and insiders.

## Rules that the (few) self-described profitable people credit
Compiled from the rules-based post https://www.reddit.com/comments/1q7rqms/ (score 27, 33 comments) and commenters in https://www.reddit.com/comments/1wvpkr6/ :
- Position sizing: max 2-3% of portfolio per memecoin; "only an amount you can lose".
- Pre-set exits and automation: auto-sell 50% at 3x, 30% at 6x, leave 20% as a free runner; set targets before entry.
- Treat as gambling/lottery: "ape into ~10 tickets, 7-8 rug, 2-3 moon; profit only if you sell the winners".
- Skip research theater; only check not-a-honeypot, exit liquidity, and volume.
- Avoid new pairs and copy trading (one commenter); watch buy/sell flow and net flow over ~5-minute windows; follow the narrative of the week.
- Asymmetric payoffs: "if you secure at least $3 profit on wins, you need only a 50% win rate to break even".
- Entry discipline: avoiding dumb entries mattered more than finding runners; limit orders instead of chasing candles.
- Test with small money or paper first.
- Keep a record: one commenter notes that most "I'm up" claims ignore fees and forgotten rugs; the few really green people they know have strict sizing and exit rules.

## Quantitative self-reports (all unverified)
| Claim | Source | Notes |
|---|---|---|
| 20 positions in 2 months: 15 rugged/died, 5 hit targets, "up 140% overall" | https://www.reddit.com/comments/1q7rqms/ | Win rate 25%. Also "lost money on ~90% of trades" over 18 months before the rules. |
| November: 11 positions, 8 failed (-$1,800), 3 hit 4x/7x/5x (+$5,300), net +$3,500 | same | Win rate 27%; ~2.9x win/loss dollar ratio. One month only. |
| "In 95% of trades I entered I was set up to lose"; -$50k YTD after being +$100k | https://www.reddit.com/comments/1mvhmpj/ | Score 22. Gambling-addiction warning. |
| 30k peak -> 1.4k, ~95% round trip | https://www.reddit.com/comments/1ozq0fu/ | |
| $3k debt -> $38k -> -$30k (one position) -> $8k -> $1.5k by revenge trading | https://www.reddit.com/comments/1iv05oo/ | |
| 100+ KOL wallets tracked 30 days; "grinder" profile = 60%+ win rate; "scalper" 45-60%; red flag below 35% win rate | https://www.reddit.com/comments/1tpu2tc/ | Promotional post for a free wallet-screening site; treat with caution. |
| Paper AI desk: 158 trades, 74 wins (47%), 84 losses, +$2,922 on $10k | https://www.reddit.com/comments/1xd4akp/ | Self-run paper trading attached to a token launch; promotional. |
| Poll-style threads ("are you profitable?"): replies skew to "down", "started with 1k now zero", "lost $3k", "down 50-80k"; a few "profitable since August" | https://www.reddit.com/comments/1wvpkr6/ , https://www.reddit.com/comments/1wycr98/ , https://www.reddit.com/comments/1lu9ikk/ | No numbers worth aggregating. |

No post in the set shows an audited multi-hundred-trade PnL. The best "win rate" evidence is 25-27% hit rate with ~3-7x winners, and it is a single account.

## Consensus vs contrarian views
Consensus (appears in most threads):
- Most memecoin traders lose; "nobody posts the sideways trades".
- Position size and automated profit-taking decide survival; most people fail at selling.
- Don't rely on KOL calls/groups; many are paid or insider-fed.

Contrarian / split:
- "Research is cope" (1q7rqms) vs "due diligence makes trenching easier" and "only buy what you understand narrative-wise" (replies in 1wvpkr6).
- Copy trading: a poster promotes wallet screening and leaderboards; commenters say "never copy trade", worry the copied wallet dumps before you; others rely on leaderboards. No results shown either way.
- "Consistent profit means rug-pulling, insider or lucky" (top reply in 1wycr98) vs "streamers have no red days, so it is possible" (reply to it).
- "DCA into one conviction coin" (several replies, often shilling a specific token) vs active trading.
- Scale of the problem: one view blames pump.fun's launch volume and fee model for "permanent bear market" (https://www.reddit.com/comments/1sfmuzx/).
- A recurring "earn as a dev/launcher instead of as a trader" narrative.

## Comparison with our measured findings
Source files: reports/Backtest memecoinów podsumowanie.md (backtest) and research_notes/Trading memecoinów od ludzi/03_retail_experiences.md.

Agreement:
1. Most traders lose: Reddit posts mirror our 10.9% of wallets in profit and the 03 note's BeInCrypto/Dune ">60% substantial losses" figure. Reddit also confirms single-wallet outcomes of "all or nothing".
2. Concentration of profit: the posts about "devs/launchers and insiders actually earn" and "only a few wallets make 10k a day" fit our finding that 1% of wallets take 95% of gross profit and bots take 53% of profit yet net -15%.
3. Do not chase pumps / avoid entries after a big candle: Reddit rules ("never buy a vertical candle", "avoid new pairs", "be careful after a big candle") match our result that buying after a pump candle gives a median -20% after 1h and -38% after 4h, and that momentum reverses after +50%.
4. Exits are the heart of the problem: Reddit's top lesson is "didn't sell". Our measurements say 67% of tokens peak in the first 15m candle and median value after 24h is 0.65x; return to entry after -50% occurs only 6.6%. So "take profit early, don't hold losers" is data-consistent; the no-exits-profitable result (0 of 10,962 rules profitable out of sample) says no exit rule rescues an unfiltered entry.
5. Sizing relative to liquidity and execution cost: Reddit mentions slippage, failed transactions, honeypots and unsellable positions; we measure execution gap -7.2% ideal vs -26.7% bot vs -29.2% manual, mainly slippage.
6. Copy trading skepticism: Reddit comments ("never copy trade", "dump before I get in") match our -22% to -38% OOS for wallet copying and about -23% for a Kolscan top-20 copy at 2s delay.
7. Dev/insider flags: Reddit rug-vs-clean confusion matches our finding that flags (dev >20% supply) work as exclusion filters, while "clean" holder maps do not guarantee safety (top-10 holders 9% yet -90% instantly; we found dev history gives no prediction, AUC 0.52).

Tension / where Reddit differs:
1. The best Reddit "rules" claim a profit (+140%, +$3,500 in a month) with a 25-27% hit rate and 3-7x winners and 2-3% sizing. Our data says expected value per trade is -17 to -34% before filter and 0 of 10,962 exit rules profitable out of sample, even at zero costs. That claim is a single, unaudited, short window; with 11-20 trades the CI is wide enough to include any sign. It also depends on sell targets of 3-7x being reachable, whereas our cycle data says median 24h value is 0.65x. Treat as a survivor sample, not contradictory evidence.
2. Reddit's "automate partial sells 50%/30%/20%" is not testable in our results as stated, but our exits grid (which includes staged exits) found no out-of-sample winner.
3. Our fast bot with a 938k USD profit holds about 6 seconds and enters the same second as launch. No Reddit poster reports anything like that; the popular narrative is manual "trenching" with 5-minute flow and narratives, which our flow analysis does not support (signal vanishes with 1-candle delay).
4. Time horizon: Reddit says "years, or never" to profitability and often "I'm close". Our data gives no evidence that skill accumulation exists for outsiders; there is no measured edge to learn.
5. "Insider/dev earns" in Reddit comments: we cannot verify launching economics from our trading-side data; mechanics note (pump.fun is a negative-sum game: -fees -SOL trapped) says launchers collect fees while traders as a group lose.

Where Reddit adds what our data lacks:
- Behavioural layer: round-tripping, size-up after wins, revenge trading, sleep deprivation, gambling-addiction language, and breakups/debt. Consider adding a "behavioural risk" rules section: pre-committed size cap, auto-sells, cooling-off after a drawdown.
- Safety: lookalike tokens, "instant rug despite clean checks", paid-group scams. Fits our exclusion-filter-only approach; add a scam taxonomy to the filter spec.
- Spam share: about a third of keyword hits are promotion, so any sentiment scrape of these subreddits needs spam filtering.

## What this means for our research (short)
- Reddit supports the backtest conclusion (no measured outsider edge; only exclusions and risk control). It does not provide a verifiable positive-edge counterexample.
- Use the Reddit rules (2-3% sizing, pre-set exits, hard loss limits, paper mode first) only as survivable-loss rules, not as profit hypotheses.
- Gaps to close if budget allows: r/CryptoCurrency and r/CryptoMoonShots; dedicated "sniper bot results" and "copy trading results" queries; top comments for the 10 most-discussed threads; a second pass on r/solana "profitable"/"lost everything".

## Threads read (links)
- Are you profitable? https://www.reddit.com/comments/1wvpkr6/ (comments read)
- Most traders losing: https://www.reddit.com/comments/1wycr98/ (comments read)
- Rules that worked / gambling framing: https://www.reddit.com/comments/1q7rqms/
- Warning, gambling addiction, $50k lost: https://www.reddit.com/comments/1mvhmpj/
- Cash-out lesson, 30k to 1.4k: https://www.reddit.com/comments/1ozq0fu/
- Boom and bust, $LIBRA loss: https://www.reddit.com/comments/1iv05oo/
- Lost savings, revenge trading, student, $TRUMP missed: https://www.reddit.com/comments/1l79ntp/
- Lost $3k into fake-sponsored token: https://www.reddit.com/comments/1wfw1mz/
- "Done with memecoins, all rugpulls": https://www.reddit.com/comments/1ik7a5l/
- "Is trading memecoins luck?": https://www.reddit.com/comments/1t5j6hi/
- Copy trading discussion: https://www.reddit.com/comments/1xfwzp6/
- KOL wallets screening (promotional): https://www.reddit.com/comments/1tpu2tc/
- Pump.fun callouts and leaderboard trust: https://www.reddit.com/comments/1x9vglp/
- Pump.fun as ecosystem problem: https://www.reddit.com/comments/1sfmuzx/
- Dev economics question: https://www.reddit.com/comments/1w1af2n/
- Fake lookalike token: https://www.reddit.com/comments/1m2v88p/
- Long post "went too deep into PumpFun" (lost 10k+, then claims success as a dev; unverifiable): https://www.reddit.com/comments/1w7bv68/
