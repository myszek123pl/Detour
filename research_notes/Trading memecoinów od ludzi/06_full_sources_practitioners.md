# Practitioners' stated rules, read from the original sources (full text) vs. our data

Compiled 2026-11-21. Supersedes the "snippet-only" caveats in notes 01, 02 and 04 for the sources listed as READ below. Public figures' public statements only. Nothing here is investment advice, and nothing here was independently verified by us on-chain.

## 0. Labels used

- CLAIM = the person's own words (podcast, interview, X post). Unaudited. Selective by default (survivorship, self-promotion, platform or token interests).
- 3P-STAT = number published by a third party (analytics vendor, news site). Not audited by us. Vendors have commercial motives.
- EMPIRICAL = analysis of on-chain data in a research paper. Only one such source here.
- SUMMARY = editorial write-up or AI-generated summary of a talk. Quotes may be trimmed or rearranged. Weaker than a transcript.
- VERIFIED-BY-US = we checked it against data. Used only in section 5 for our own results. No practitioner claim below carries this label.

## 1. What was actually read (and what was not)

READ in full (HTML or transcript text):
| Source | Type | Note |
|---|---|---|
| YouTube JbWa-Jss-18, "Cupsey Explains the SECRET to Trading Memecoins..." (channel threadguy2) | Auto-caption transcript, ~10K characters | A clip, roughly 10-12 minutes of speech by length estimate (not a full episode). Auto-captions garble "SOL" as "soul". Real first-person Cupsey. |
| X posts by @Cupseyy, 3 Jul 2024 | Two tweets | Only the two shown on the status page, plus one reply from @orangie. |
| fomo.family, "In the Trenches" Ep. 16 (Satsdats), 17 (notanicecat69 "Wood"), 15 (chang_defi), 18 (Logjam), Coyote AMA | Editorial write-ups with direct quotes | SUMMARY level. Not full transcripts. |
| Wu Blockchain podcast EP-51 (Mr. K, Jackson of 0xScope, defioasis, Maodi) | Full AI-generated transcript | Chinese-language trading community, TRUMP/MELANIA, Jan 2025. Transcript is GPT-generated, may contain errors. |
| Odaily interview with "Da Gen" | Full interview text | Chinese retail trader, debt case. |
| Substack: threadingontheedge (author tag "arndxt"), "The ultimate trenches playbook" (May 2025) | Full text | Anonymous guide, no returns shown. |
| Substack: insightfulinfo, "Stop roundtripping your massive memecoin" (2024) | Full text | Anonymous guide, no returns shown. |
| Substack: davidzmorris, interview with "Mr. Krabs" | Intro only | Paywalled after the first answers. Only background and two answers readable. |
| SozAI transcripts of two YouTube videos ("$300 into $200K in one trade"; "$50 into $500K scalping guide") | Auto transcript + AI summary | Speakers are anonymous YouTubers. Treat as marketing content. |
| KuCoin flash on Cented, memecoin.wiki and uwuu.ai on Cupsey | Third-party articles | 3P-STAT. |
| Ding, Luo, Xu, "Decompose Market Manipulation Strategies: Evidence from On-chain Meme Coin Market" (SBFC 2025, PDF) | Full text | The only EMPIRICAL source. 6,000 pump.fun coins. |
| Mobula "Detecting Snipers & Bundlers", MadeOnSol CTO guide | Vendor docs | Not practitioners. Used only for thresholds. |

NOT obtained (so nothing is claimed from them):
- HuggingFace `zirobtc/oracle/FullCryptoGuide.md`: HTTP 401, "Access to model zirobtc/oracle is restricted. You must have access to it and be authenticated". The repo is gated. We did not try to get around it. Everything note 01 and 02 said about "the Cupsey guide" (crime-spotting, 3 SOL at 8K mcap, "Pioneer" group anecdote) therefore remains UNVERIFIED secondhand.
- YouTube UHs0tP2z6Tc (TG Podcast, "Millionaire Crypto Traders Explain BEST Strategies...", 2025) and efq61vbmotM (TG Podcast, Cupsey and Jack Duval): metadata read (titles), but captions blocked (HTTP 429 from YouTube's caption endpoint after the first success; empty caption URLs). No transcript.
- The Memecoin Podcast (Buzzsprout): episode pages exist (S2E8 Guardian1771, S2E5 Shibtoshi) but contain only title and audio player, no transcript or show notes. Nothing to extract. Crash episode (Audible listing) likewise no text.
- In the Trenches (FOMO) audio itself: only the fomo.family write-ups above.
- cryptonews.com "Can traders still win in meme coins in 2026" (JavaScript challenge, empty), cryptobriefing.com (Bubblemaps/Cupsey), theblock.co, benzinga.com, gate.com (Gate Learn "meme whale" article): HTTP 403. Allegations about Cupsey and Murad stay at note-01 level (not re-read).
- reddit.com: 403 for direct requests and WebFetch refused the host. No Reddit material gathered.
- Bloomberg cabal article (paywall), PANews/TechFlow Cupsey analysis (not fetched), Nansen, Kolscan.
- Cupsey's published Axiom scanner filters: searched, no primary source found (only generic third-party guides). Not claimed.

## 2. Practitioner cards

### 2.1 Cupsey (@Cupseyy), Solana pump.fun scalper (CLAIM unless stated)

Primary words:
- X, 3 Jul 2024: "I've made over $1,000,000 on pump.fun alone, 0 insider plays, 0 raydium coins, Just in the trenches 12+ hours a day." Reply tweet: "All I do is trade pump funs for hours daily, 0 insider plays and 0 raydium coins, all verifiable on chain... 6k+ tokens traded in 30d and im top 5 on photon weekly." (481K views.) @orangie replied that he "sits on his PC all day buying the most random shitters".
- threadguy2 clip (date not shown; he refers to "January" and "AI hackathon coins"):
  - Style: "Just throwing into anything with a pulse and just hoping it's something and look at it. See it's nothing. Just cut quick, go next. If it is, then you know you hold and look into it more."
  - Volume and holds: "probably like 300 coins a day. A little bit more." Holds range from about 2 seconds to 30 minutes, an hour, two hours. "I wasn't taking breaks... scanning like 18 hours a day straight."
  - Execution: "no tech. Everything just raw." Says nobody else has ever traded from his wallet, and that people assumed he was a bot.
  - Sniping: for a hyped launch (Twitter monitor posts a contract address, Telegram bot buys), first-block buy needs about 200-250 SOL spend with a minimum-tokens setting of about 10-14% of supply, plus a high bribe. Best snipe: 500 SOL fee and bribe still made "600k" (he forgot the coin; "one of the AI hackathon coins", January). Current state: "It's pretty much gone. Everything migrates instantly."
  - Market state: on a dead launchpad he buys only to "hope for some crime", and "it's just a sad reality like everything's just crime now."
  - Learning curve: he grinded through a very dead market ("September" when one coin bonded every two hours and one coin a day approached 500K). "I fully grinded when it was so dead... you sharpen your blade for when it gets good." He had been scanning pump.fun new pairs on Photon since about "May last year".
  - Motivation and cost: "addicted to the grind", works about 16 hours a day, "my dopamine is fried", needs "like a year with no internet" to recover. A $2,000/day (10 SOL) result is described as "an unreal amount of money" to a normal person.
  - Self-reported lifetime PnL "20-25 million" was a figure thrown by the hosts and not rebutted in the clip. Not a claim he states himself.

3P-STAT about him (not audited):
- uwuu.ai (vendor selling copy-trading): 30 days to 8 Sep 2026, wallet 2fg5Q...x6f: $447,372 realized, 94.25% win rate, 2,346 trades (~78/day), ~$191 per trade. Names Axiom Pro as terminal.
- memecoin.wiki citing Gate Learn: one 3-month window, #1 on OKX wallet leaderboard, ~$5.14M profit, 67.7% win rate, ~95,000 trades (about 1,050/day).
- Internal inconsistency worth keeping: 78 trades/day (uwuu) vs about 300 coins/day (own words) vs about 200 tokens/day (2024 tweet) vs about 1,050 trades/day (Gate). Different windows, wallets and definitions of "trade". The 94% vs 67.7% win rates differ for the same reason. None of these can be reconciled from here.
- Bubblemaps allegation (from note 01, not re-read): ~$1.74M via ~30 linked wallets and callout rewards. Unverified here, and we did not see his response.

Reading: this is a speed/volume style with very short holds and many tokens, and his own account stresses tolerance of manipulated launches ("crime") rather than avoiding them. It is not a rule set a slower trader can apply.

### 2.2 Cented ("7-Second Trader") (3P-STAT only, no first-person material found)

KuCoin flash (data from cielo.finance): >$10M realized over 357 days, 308,666 trades, 62.3% win rate, median hold 7 s, 845 trades/day, about $33/trade, largest single win ~$90K (GORK). Address flagged by some as MEV-bot-like. Author alleges multi-wallet bundling when market caps are in the thousands and exit near $100K or lower. cookin.fun test: copying Cented with a 10 s delay and selling after 10 min returned -21.3%. Cented launched 1,000 coins, 30 graduated. The article is an opinion piece (it calls such traders a "cancer"); the allegations about bundling are the author's, not shown with evidence. Our note: the -21.3% test is a single vendor simulation with a specific delay and exit rule.

### 2.3 Satsdats, Solana trader (SUMMARY of In the Trenches Ep. 16, Head of Product at Bonk Fun, so a platform interest)

- Background: perps trader. "I ran up a few accounts to life-changing money and lost them probably three or four times over." One AXS position, then just over $1M lost within two weeks. Cause he names: obsession with portfolio all-time highs ("I wanted home runs or I wanted nothing").
- Sizing: fixed bankroll in the hot wallet (about 100K now), treated as fully losable, rest in stables. Entries in about 10K clips. No DCA ("on Solana, when you create a DCA order, other traders get notified... frontruns"), no full stack at once.
- Entry zone: avoids sniping sub-100K launches. "I make the most on tokens which are 5 mil to 10 mil market cap already and I'm betting on them going to 60 or 70 mil."
- Exit: 9-length EMA on the 1h chart: "It loses the EMA, you cut." Does not care if price rises after he sells. For higher-cap assets 200 EMA on 4h. Uses deep-liquidity venues (Meteora) to exit large size.
- Conviction filters: novelty, information flow ("strongest thing you have"), launchpad and team, who holds ("right holders, the right calls").
- Risk and psychology: moves profits off-chain into stable vaults "and forgetting it exists"; money starts to feel like "chips"; advice to try spending $10K in real life. Biggest skills for the next bull: "being selective for coins and being quick to cut... quick to cut your losses."
- Network: got into alpha chats through a public tracked wallet; describes Frank DeGods' group of about 70-80 traders as the gold standard (mixed skill levels, psychological safety, chronically online). No direct Frank DeGods statements found.

### 2.4 Wood / notanicecat69 (SUMMARY of In the Trenches Ep. 17)

- Path: low seven figures in the first cycle (DeFi, Avalanche) returned to "30 or 40 grand" because he never sold. Restarted with about $4,000 (1 ETH + 1 asset) when SOL was about $25. GoFX bought at 800K mcap, 20x. WIF bought around 1.5M mcap; WIF "went on to reach a $5 billion market cap" with four separate drawdowns of 70%+; position reached seven figures; sold enough in Feb 2025 to cover "several years of living expenses".
- Sizing: "Every coin that I've done really well on, I put in an amount of money that if it went to zero, I generally didn't care about." Keeps about 2.5% of net worth in the active wallet. Hot wallet funded only with what he can lose; rest on a hardware wallet; leaves the Ledger at home on purpose; stopped using trading terminals (e.g. Bunkbot) "because they made it too easy to overtrade".
- Entry rule: "Don't buy new pairs because new pairs are a game that's rigged against you." Waits at least two days after launch; if the coin is "still alive, still showing strength, and has a visible community after 48 hours", then evaluates. Reason: bundlers/snipers; someone likely owns 20% and will dump.
- Exits: sells in small increments on the way up, keeps a moon bag. "Selling is the right thing 99% of the time." Useless: sold entire position between $25M and $40M mcap (later $400M, but first dropped to $6M).
- No-double-dip rule: re-entry is "the one that you break all the rules on". Example: Penguin entry about $15M, sold around $100M on the way down, re-entered at $80M with a larger size, lost.
- Focus rule: more than 2-3 tickers at once and "I trade poorly". Stops trading (about 5 days, cash to hardware wallet, cut to 2-3 tokens) when he sees "liquidity vamping" (one token's rise dumps the others).
- Learning: borrowed conviction "never works". Echo chambers hurt; build a network with different views. Daily posting plus replies to build contacts.
- Market view at time of interview: "no trade", mostly cash. Date mismatch in the article ("Feb-March 2025" while discussing a 2026 outlook); treat the timing as unclear. Also cites "roughly 12 million failed tokens launched in 2025 vs 3 million" (CoinGecko, as quoted, not checked).

### 2.5 Logjam (SUMMARY of In the Trenches Ep. 18; one famous trade, Penguin)

- Selection: TikTok virality (500K-1M likes across multiple creators), checks Know Your Meme and X; prefers a character; "is it funny? Does it have some sort of shock value?" Avoids tech plays.
- Sizing and exits: 3% of supply at first, trimmed to about 6M tokens, rebought to 2%, held 1.5% on the run. Pre-planned sale of 0.5% of supply at above $10M mcap (about $60K). "Take your initial investment off the table after a 2x." Sold the rest at $50-60M mcap (next morning $170M). Off-ramped 95% of profits. Says he would "never" put more than 75% of his portfolio into one trade (that is a maximum, not a normal size).
- Mistakes: first win (Chill Guy, about $1K to $35K) "was a terrible thing for me honestly", burned half of it in two weeks; hyper-rotation "kills your port balance so quickly".
- Learning curve: started Oct 2024 as a Coinbase buyer; lessons after the euphoric first trades through early 2025.

### 2.6 chang_defi (SUMMARY of Ep. 15) and Coyote (SUMMARY)

- Chang: "90% of the time I'm unprofitable and once or twice or three times a year I just have this windfall." Treats on-chain as "a casino". Exhaustion signal: when a token is the top PnL on FOMO and everyone has its icon, "this thing is gigatop", yet he could not sell his own bag (down 80%, sold the bottom). WORM: put "300k" in at 8-10M mcap, it nuked, ended at zero. Tilt: "look away, go outside". Advice to beginners: get a job first.
- Coyote: lost $250K on the FOMO app "death by a thousand cuts" (re-depositing $30-50K). Causes: ignored red-light markets; thinking in USD instead of SOL size; following too many traders (top-blasted on "19 people you follow bought" alerts); EVM trades where he had no edge (his two biggest losses). Says wallet tracking is overrated: "I don't really track wallets", it shakes him out of good positions and fresh wallets have eliminated most insider signal. Tilt types: notional vs ego. Hard rules: never trade unlocked LP tokens; skip content with a ceiling (offensive/sexual). Green flags: many coins reaching moderate caps, novelty; red flags: large extraction events, weak majors.

### 2.7 Wu Blockchain podcast, Chinese on-chain traders (CLAIM; AI transcript; Jan 2025 TRUMP/MELANIA)

- Mr. K: first buy 2,000 USDT, later added; "sold to get back my principal after it doubled"; sold 10% more at ATH; peak profit "400-500K" on about 30-40K invested. Sources: tools with smart-money tracking, WeChat/Telegram groups; sometimes buys on the coin's name. Moved to AI sector afterwards: "every time a so-called miracle coin appears, the second and third days are usually filled with intense PVP... not a good time to enter".
- Jackson (0xScope): sold 25% at about $20, 50% at about $50, held 25%. Invested $50-70K in total. Strategy: pick high-quality KOLs/addresses, check basics and narrative, buy fast ("there's hardly any data to analyze").
- defioasis: kept a 1,000-1,600 USDT initial position, withdrew principal at 2x; then put a pre-set $200K into MELANIA through Jupiter in 3-4 pieces at about 12.9, set a sell at 15, peak was 14, did not sell, exited at 3-4 (a 5x unrealized gain became about +30%). Built a Twitter-monitor alarm for new contract addresses.
- Maodi: bought a few hundred USD, took principal at 2x, kept selling into strength and ended with 1/32 of the position; a cautionary case of selling a runner too early. Notes TRUMP's contract address was not a pump.fun style address and 80% of supply was locked, which changes the dynamics.

### 2.8 Da Gen (Odaily; CLAIM, Chinese civil servant)

- 2021: 30K RMB into DOGE futures became 2M, liquidated in the May 2021 crash. Early 2024 Solana memes (BONK, WIF, POPCAT), assets "A8" (eight figures in RMB). Bought TRUMP at about $0.7 ($100K) after seeing a large wallet buy, sold gradually near $70.
- Failure: "second dip buying" on GOAT (bought "nearly $900,000", about 1% of supply, after a 90% fall; it fell another 90%), VINE, TST, BROCCOLI (lost over $1M while helping "support the price"). "Small wins, big losses." Cause named: path dependence and a fixation on "A9". Since Aug 2025 bank loans; debt about 1M RMB. His quote: "after TRUMP, most Memes were just one-shot pumps."

### 2.9 Mr. Krabs (David Z. Morris interview; free part only; pseudonymous full-time trader)

- Background: software developer, burned in 2020-2022, on-chain from 2023 (Base, Arbitrum), memecoin trading from Oct-Dec 2023. "Late 2023 to early 2024 was really great... Right now [mid-2025], the game is hyperoptimized."
- Rules readable: skips pre-bonded tokens ("If you have 10,000 coins being created a day, 9,950 don't make it past the curve and 50 do" is his estimate), trades "graduated only, things that have strong overarching trends". "If volume is below market cap... a lot of supply is concentrated, usually." Says follow-the-cult holders "are the suckers" and "the people who are less experienced forget how ephemeral things are". The rest (tools, metrics, manipulation checks) is paywalled. Do not cite beyond this.

### 2.10 Anonymous guides and YouTubers (CLAIM, no track record shown; low weight)

- "arndxt" (threadingontheedge, May 2025): entry at 7-15K mcap for a narrative you believe in, 50K as a psychological level, 200K+ "overhyped zone", target exit 2x/3x, take initials at 2x or 5x, "mental" stop or limit just below support, "40-65% win rate can be extremely profitable if you cut losses quickly and let winners ride". Admits stops "may not always be feasible".
- "Insightful" (2024): 25% sold at 3-4x, then 25% at every further 2-3x, 10-20% moon bag; allocation of 20-25% of a four-figure portfolio per play "to move out of this phase"; after a 2-4x do not re-enter; no shown results.
- "Seda"-type scalping video (SozAI, unverified speaker; sells a course/Discord): pump.fun only, insiders max 20%, bundle check on top-5 holder balances and funding times, "40% dip method" ("after a 40-50% dip people buy it back up another 45%... every time"), sell if price falls below average entry ("be a Jeet"), size caps by bankroll (0.1 SOL port: 0.05 per buy, 1 SOL port: 0.25, 5 SOL port: 1 SOL). Claims "100% of the time". AI summary itself flags this as unsubstantiated.
- "$300 into $200K" speaker (anonymous, SozAI): first month red from copy-trading and rage trading, "zeroed out a couple times", quit his job 2 weeks before the interview; favours holding high-conviction narratives (sold about $124K, still holding about $90K at the time). He credits luck partly.

## 3. EMPIRICAL anchor: Ding, Luo, Xu (SBFC 2025)

6,000 pump.fun coins with account-level on-chain data. Findings relevant to practitioner claims:
- Creators and snipers earn from concealed, low-cost accumulation. Creators make about $104/project on average without front-running bots, +$161 with a "rat" bot; sniper presence cuts creator profit about $54; wash-trading bots add about $432 (used in about 4% of projects) and fabricated activity roughly doubles trader participation without improving trader profit.
- Non-creators lose on average (example quoted: -$6.37 vs -$4.47 per trader depending on manipulation).
- "Winners" (significant positive PnL) are 19.2% creators and 16.0% snipers against 4.4% / 3.3% for normal participants. Winners avoid manipulated, crowded, high-profile coins, choose smaller earlier-stage ones, and initiate most dumps in premature projects.
- Losers react to recent losses and "learning plateaus"; underperformers "keep making the same mistakes" (passive learning does not protect).
- Creators start the sell-off in about half of cases; the party with the larger low-cost inventory dumps first.
This is the closest thing to independent evidence for the claim "early entrants with inventory win, late entrants lose" and for "learning curve is slow for most".

## 4. Consolidated extraction (attributed)

### 4.1 Setups
| Setup | Who (label) | Details |
|---|---|---|
| High-frequency early scalp | Cupsey (CLAIM), Cented (3P-STAT) | Hundreds of tokens/day, holds from seconds to about an hour, cut anything that does not move. Tolerates "crime" launches. |
| Launch snipe on hyped CA | Cupsey (CLAIM) | 200-250 SOL, minimum 10-14% of supply, high bribe; he says this is "pretty much gone". |
| Narrative/viral hold | Logjam, Wood, Satsdats, chang_defi (SUMMARY) | One-sentence thesis, relatable character, first mover, information flow. Few trades, partial profit-taking. |
| Post-traction mid-cap | Satsdats (SUMMARY) | 5-10M mcap, target 60-70M. |
| Wait-48h filter | Wood (SUMMARY) | Skip new pairs for two days, evaluate survivors. |
| Graduated-only | Mr. Krabs (CLAIM) | Ignore pre-bonded tokens. |
| Event/celebrity coin | Wu Blockchain panel (CLAIM) | Speed to the contract address (Twitter monitor), principal out at 2x. Panel itself says repeats are unlikely. |
| Dip buy ("40% method", second dip) | YouTuber (CLAIM), Da Gen (CLAIM, lost) | The only practitioner with a large documented loss using it is Da Gen. |

### 4.2 Entry rules reported
- Satsdats: about $10K clips, no DCA, no full stack.
- Wood: never new pairs, 48-hour wait; one-sentence thesis test.
- Logjam: virality and character check before entry; bought Penguin within 50 minutes of launch and then sat through 5-6 days below 1M mcap.
- Pump.fun scalping video: insiders under 20%, check top-5 holders for equal-sized wallets and same-day funding.
- Vendor thresholds (Mobula, not practitioners): top-10 under 25-30%, dev under 3-5%, no snipers in top 20, snipers over 20% combined is red.
- Arndxt: 7-15K entry; avoid 200K+ without catalyst.

### 4.3 Exit rules reported
- Principal out at 2x: Mr. K, defioasis, Maodi, Logjam, arndxt (2x or 5x).
- Ladders: Jackson 25% at about $20, 50% at about $50 (TRUMP). Insightful 25% at 3-4x then 25% at each further 2-3x, 10-20% moon bag.
- Trailing/technical: Satsdats 9-EMA on 1h; scalper "sell below your average price".
- Discretionary: Wood sells in small increments and never re-enters; Logjam pre-planned 0.5% supply sale then sold the rest on a friend's advice.
- Quick-cut: Cupsey "cut quick, go next"; Satsdats ranks "quick to cut" above selectivity.
- Outcome examples that cut both ways: Maodi sold too early (1/32 left), defioasis held to a round trip (5x to +30%), Logjam sold before a further 3x, Chang sold the bottom.

### 4.4 Sizing and risk rules
- Wood: about 2.5% of net worth in the active wallet; size so total loss is irrelevant; 2-3 tickers max. Hot/cold wallet separation, physical friction.
- Satsdats: bankroll of about 100K treated as lost; profits to stables.
- Logjam: off-ramp 95% of the big win; at most 75% of portfolio per trade (upper bound); about 1.5-3% of supply positions.
- Coyote: size in SOL terms not USD; reduce size (not stop) while tilted; skip unfamiliar chains.
- Wu panel: principal back at 2x; defioasis planned a fixed $200K bucket in advance.
- Anonymous guides: 20-25% per play for 4-figure accounts (arndxt/Insightful), fixed SOL tables by bankroll (scalper video). These are outliers in aggressiveness compared with Wood/Satsdats.
- Nobody here gives a stop-loss that is claimed to work on pump.fun; two sources note stops are infeasible or use "mental" stops.

### 4.5 Routines and tools
- Cupsey: 16-18 hours/day scanning, "no tech", Photon then Axiom Pro, voice calls with other traders (per memecoin.wiki, 3P-STAT), phone trading even in a van.
- Wood: daily posting/replies, diverse network, leaves Ledger at home, takes a 5-day no-trade break.
- Satsdats: tracked public wallet to enter alpha chats; group chats as "information flow".
- Logjam: TikTok, Know Your Meme, X.
- Wu panel: GMGN holder view, 0xScope smart-money tool, Twitter-monitor alarm, Jupiter routing, WeChat/Telegram groups.
- Others: Solscan reading (Coyote, Da Gen), FOMO app leaderboards (Chang, Coyote; both say leaderboards and follower alerts can mislead).

### 4.6 Learning curve and money lost (all CLAIM unless noted)
- Cupsey: scanning daily since about May 2024 plus a "dead market" grind period; says 2024 was easier than now.
- Satsdats: 3-4 account blowups over four to five years; Wood: first cycle round trip of low seven figures; Logjam: first-month euphoria then lost half of the first win in 2 weeks; $300-speaker: red about a month, zeroed twice, quit his job after one big win; Coyote: $250K on one app; Da Gen: from "A9" proximity to about 1M RMB debt in about a year; Chang: "90% of the time I'm unprofitable".
- No source gives a hard "time to consistency". Plateau in learning is supported by the SBFC paper (EMPIRICAL).
- Scale of attention cost: Cupsey describes dopamine damage; Satsdats and Logjam describe "chips" and unrealized-gain stress.

### 4.7 Most repeated mistakes
1. Oversizing, especially after a win (Wood, Satsdats, Logjam, Coyote, Da Gen).
2. Re-entry or averaging down into a fallen coin (Wood double-dip; Da Gen GOAT/BROCCOLI; Chang WORM).
3. No profit-taking, round trips (Wood, Satsdats, defioasis).
4. Hyper-rotation and too many tickers (Logjam, Wood).
5. Copying or following too many wallets and alerts (Coyote, $300-speaker).
6. Trading chains or token types outside edge (Coyote, Logjam).
7. Emotional attachment to a bag or community (Chang, Wood on borrowed conviction).

### 4.8 Conflicts of interest to carry along
Satsdats is Head of Product at Bonk Fun and co-hosts RiskOnPod (as is Wood); Cupsey and Cented earn from terminal rebates and followings (3P allegations); the scalping YouTubers sell courses/Discord; FOMO publishes the podcast that interviews its own app's users; vendors (uwuu, Mobula, MadeOnSol) sell tools. Only Wood and Da Gen give detailed numbers of losses, and Da Gen's is a debt case.

## 5. Comparison with our measurements

Our data (from `reports/Backtest memecoinów podsumowanie.md`): 9,684 pump.fun tokens, June 2026, 15m candles, plus wallet/order-flow and bot-log analyses. All figures below are ours (VERIFIED-BY-US inside that sample); practitioner statements remain CLAIM/SUMMARY.

| Practitioner statement | Our data | Verdict |
|---|---|---|
| Speed is the edge (Cupsey: sub-second to seconds holds, hundreds of tokens/day; Cented 7 s median hold) | Only profitable bot entered in the launch second, about 180 USD, about 6 s hold, 938K USD in 111 days; execution gap ideal -7.2%, bot -26.7%, manual -29.2% per trade | Consistent in kind (profit exists only at extreme speed and volume). Not replicable from a normal setup. Cupsey's "no tech, raw" claim cannot be checked and conflicts with our finding that bots take 53% of profit, but bots net -15%. |
| Copying fast wallets fails (Cented copy -21.3%, Coyote avoids tracking, panel members warn) | Wallet copying -22% to -38% OOS; top-20 Kolscan copy about -23% at 2 s delay | Strong agreement: two independent estimates (cookin.fun -21.3%, ours about -23%) land close. |
| Few people earn most of the profit; "90% of the time unprofitable" (Chang), Chang/Wood/Satsdats long-run blowups | 10.9% of wallets profitable; 1% take 95% of gross profit; one-time buyers -81%; snipers -79% | Agrees. The SBFC paper adds that winners are over-represented by creators/snipers (EMPIRICAL). |
| Do not buy new pairs, wait 48 h (Wood); Satsdats 5-10M mcap; Krabs graduated-only | Our sample is fresh tokens: no entry timing edge, per-trade -17% to -34% unfiltered, 67% peak in the first 15m candle, 86% within 1 h, median 0.65x entry at 24 h; most tokens never graduate | Partially supported: our data say fresh-token entry loses, which is the premise of these rules. But the rules select survivors and our sample cannot test "alive after 48 h" or 5-10M entries (no such cohort). Open test. |
| Buy the dip / second dip ("40% method"; Da Gen's second-dip buying) | Return to entry after a -50% drop only 6.6%; catching drops of more than 50% is an exclusion rule; after a pump candle buying gives median -20% (1 h), -38% (4 h) | Conflicts. The only practitioner with documented numbers (Da Gen: GOAT, about $900K, fell another 90%) lost. The YouTuber's "works every time" is not supported anywhere. |
| Chase narrative/momentum, buy strength on volume (arndxt "follow volume", whale-involvement) | No momentum, reversal after +50%, only a one-candle +17% signal that vanishes with a one-candle delay | Conflicts for chasing; narrative selection by humans is not measured (our features contain no narrative). |
| Take initials at 2x; ladders (25% at 3-4x etc.; Jackson 25% at $20, 50% at $50) | 10,962 exit rule combinations walk-forward: 0 profitable OOS even at zero cost; 473 in-sample (overfit); stops slip (-18% stop filled about -84%) | No edge shown for any ladder. Practitioner ladders are applied to conviction holds in rare winners, not to the median token, so our test says nothing against their usefulness as risk bookkeeping. Their own outcomes (Maodi too early, defioasis round trip) show ladders cut both ways. |
| EMA trailing exit (Satsdats 9-EMA 1h) | Not tested; operates at 1h on tokens with traction; our exits are rule grids on early 15m candles | Gap. Test on survivor cohort. |
| Quick cut / "sell below average" (Cupsey, Satsdats, scalper video) | Stops are unreliable on pump.fun (slippage), so "cut" must be market-sell speed; unfiltered per-trade loss remains | Agrees directionally (do not hold losers) but execution quality dominates. |
| Sizing small, only what you can lose; about 2.5% net worth (Wood); bankroll treated as lost (Satsdats) | Our only directly supported advice: small size vs liquidity, slippage dominates; 10% supply dump = -55% price | Strong agreement. Conflicts with the 20-25% per play advice from anonymous guides. |
| Avoid bundles/snipers/insiders; dev holding check (Wood, scalper video, Mobula thresholds) | Dev >20% supply: 62-69% dumps vs 38% base; flags work as warnings; dev history AUC 0.52; "low bundler" rule was a data bug (-27.5% on reliable features) | Agrees as an exclusion filter, not an entry signal. SBFC supports that insiders extract. |
| Exit liquidity is created by hype and wash activity (Chang exhaustion signal; Cented article) | 14-33% of volume is quick same-wallet buy+sell; 87% of pump-candle sells are earlier buyers; SBFC: wash trading nearly doubles participation without improving profits | Agrees. |
| Re-entry after exit loses (Wood, Insightful) | Not directly tested; our 6.6% return-to-entry statistic is related | Consistent, not tested as a rule. |
| Market-state brake ("liquidity vamping", Wood steps back; Chang waits for energy) | Good days cluster (r about 0.6) but no June day was profitable; regime acts as brake | Consistent with brake use, not a profit source. |
| Learning curve takes a long time; losers do not learn (Satsdats, Wood, Coyote, Da Gen) | Not measurable in our data; SBFC: losers "learn little" | Consistent with SBFC. |
| Graduated tokens only (Krabs); sniping is "gone" because of instant migration (Cupsey) | No clean graduation study; BOOST (Jul 2026) postdates our data | Untested. Cented's own 30 of 1,000 graduating and Krabs' 50 of 10,000 are CLAIM/3P-STAT, same order as our "most never graduate". |

### What changed versus note 04
- 04 compared our data to vendor and anonymous guides. Now first-person practitioners and one empirical paper confirm the main structure of our conclusion: profit sits with extreme-speed operators and insiders, copying fails, and the transferable advice is about sizing and not holding losers.
- New conflict: the practitioners' strongest rules (wait 48 h; 5-10M mcap) point to an area our dataset does not cover. They do not contradict our result; they imply that the fresh-launch cohort is where an outsider loses, which our data supports.
- Dip-buying rules are now contradicted by both our statistic (6.6%) and the only practitioner loss ledger (Da Gen).

## 6. Gaps and what would close them
1. TG Podcast transcripts (UHs0tP2z6Tc, efq61vbmotM) and the full Cupsey interview: need a way around YouTube's caption rate limit (a cookie/PO-token setup that the user provides, or a pre-downloaded .vtt).
2. HF FullCryptoGuide.md: gated repo; needs an account with access.
3. The Memecoin Podcast and In the Trenches audio: no transcripts on the hosting pages found; needs audio transcription or the show's own transcript feed.
4. Test candidates created by practitioners but not in our data: (a) entry at 48 h on tokens still alive; (b) 5-10M mcap entry with 1h 9-EMA exit; (c) graduated-only entries; (d) dev-sold/CTO outcomes. All need a dataset with longer horizons than 15m candles in the first hours.
5. Reconcile Cupsey trade counts (78/day vs 300 coins/day vs 1,050/day) with on-chain data before citing any one number.
6. Reddit and X threads: Reddit blocked, X only status pages.
