# What memecoin traders say publicly on X about how they trade (2024 - 2026)

Compiled 2026-11-21. Public posts only. No login bypass, no spoofed sessions, no Nitter. Every quote below was obtained from a public, unauthenticated source (see "Access log"). Claims are the authors' own and are UNVERIFIED unless stated otherwise. Dates are the tweet dates shown by X.

## 0. Access log (what worked, what did not)

| Host / method | Result |
|---|---|
| `publish.twitter.com/oembed?url=<x.com status url>` (use `x.com`, not `twitter.com`, which returns a 301) | Works, returns official tweet text. LIMITATION: long tweets are cut with "..." (only the first ~280 chars of a long post, and no thread continuation). It cannot return replies or the rest of a thread. |
| `x.com/<user>/status/<id>` and `x.com/<user>` via curl | HTTP 200 but only a JS app shell with no content (not scraped, not used). |
| `x.com/i/trending/<id>` (public Grok-written story pages with embedded public posts) | Readable without login. Text is a Grok summary ("Grok can make mistakes") plus 3-6 embedded real posts with handle and date. Summaries are NOT the traders' words; I only quote the embedded posts and re-checked the key ones through oEmbed. |
| `threadreaderapp.com/thread/<id>.html` and `/scrolly/<id>` | Works for some old threads (0x_gremlin, 0xReflection, jacknuked, VoltWeb3). For the 2026 threads I tried (camol 2097069948128645547, pr6spr 2090301751165374543) it returned only a generic 17 KB shell, so full text was NOT obtained. |
| techflowpost.com, medium.com (coinmonks) | HTTP 403 from curl. Only search snippets available. |
| WebSearch with `site:x.com` | Weak. Search engine ignores exact phrases and returns few real status URLs. Most hits are aggregator blogs, vendor guides and Google/Notion docs of unknown authorship (ignored as evidence). |
| Not tried by design | Nitter mirrors, X API, logged-in scraping. |

Coverage gap: Euris, Ansem (own rule list), Cented and Cupsey produced no first-person process thread I could read. Gake and Orange appear only as 2026 opinions on bundling, not as process threads. Orangie/Cupsey/Cented process claims are in earlier notes (01, 02) and are third-party summaries.

## 1. Concrete practitioner claims (attributed)

### 1.1 Entry filters and tooling

- **@0x_gremlin, "How I Made $1M Using Only Photon" (Nov 18, 2024, 15 tweets)** - https://x.com/0x_gremlin/status/1858552433015665140 (full text via https://threadreaderapp.com/thread/1858552433015665140.html)
  - "Degen filters for Memescope: pump progress 15%-25%, holders 15-25, dev holding 0%-5%, snipers 0-2"; quick-buy size 0.1-0.5 SOL.
  - "Pumpfuns are a bloodbath, you'll get rekt most of the time. Increasingly hard to profit on low val coins ... most of my gains have come from higher-cap plays." Entering at $1-5M on a coin that reaches $200M-1B is still "a tremendous win".
  - Distribution check: top 10 holders should not exceed 10-15%; spot-check top 100 for empty wallets; Bubblemaps for clusters; MEV protection on.
  - "Conviction bets": "if you're jeeting after just 2x, 5x, or 10x, ngmi"; admits "I've round-tripped tens of trades worth $200k - $1M". On meta: be early to the whole meta (AI coins, first runners under $5M); "90% of them failed, a few wins compensated".
  - Conflict of interest: ends with a promo of his Telegram group and a "$10 -> $10,000 challenge"; $1M claim is unverified.
- **@jacknuked, 69-tweet Solana guide (Apr 8, 2024)** - https://x.com/jacknuked/status/1777289921885323287 (threadreader copy). "90% [of new deploys] don't even see the light past 10k mc"; split the game into (1) new-pair hunting with safety vetting and (2) narrative/chart plays. Author also warns that his earlier thread's Discord/Telegram links were swapped for wallet-drainer scams. 2024, so pre-dates the 2025-2026 meta; included for the "most deploys die under 10k" figure only.
- **@VoltWeb3, "How to Get Rich in Memecoins (without getting lucky)" (Aug 18, 2025)** - https://threadreaderapp.com/scrolly/1957465848354156583 (tweet id 1957465848354156583 on X).
  - Pick ONE of two strategies: high hit rate (60-70%+ winners, take profit at 2-3x, buy only $300k+ mcap, fewer trades) or low hit rate / high return (limit sells, many small trades, buy under $5M, target 10-50x with ~10% hit rate). "Chasing both is where most lose."
  - Scanner checklist: bundled? held by smart/whale wallets? renamed? DEX paid? "Significantly improved my hit rate (mostly by avoiding scams)." Wallet tracking called "arguably the most important tool".
  - Conflict of interest: sells a Telegram "top wallets list" to the first 100 joiners; hit-rate claims unverified. The advice to follow wallets printing 1000%+ is the copy-trade approach that the Detour logs measured as negative (see section 3).
- **@0xReflection, "How to turn $100 into $100,000 in 30 days" (Nov 14, 2024, 17 tweets)** - https://x.com/0xReflection/status/1857120472640676050 (threadreader copy).
  - Cites "statistics" that wallets sniping before $3M mcap earn 93.8% of total profit (source not given); advises copying "insider" wallets from Dexscreener top-traders tab (min 50x profit, few txs), auto-copy with max mcap $20M.
  - Exit rules: "2-3x: take back your investment, keep the rest as moonbag; if it keeps rising ride to 25-100x then sell slowly"; "never fall in love with your bags".
  - Conflict of interest: pushes a Telegram trading bot ("no promo" claim contradicted by the bot link and a referral-style Telegram funnel) and a "go private soon" call-group funnel. Title promise ($100 -> $100k) is a lure.
- **@camolNFT (Sep 7, 2026)** - https://x.com/camolNFT/status/2097069948128645547. oEmbed shows only the first lines: "$75 unit size, can double units or blast multiple into a chart. But always $75. Sell 50% immediately after a 2x. Don't be afraid to take a quick loss. Don't ..." (rest truncated, not retrieved). Notable as one of the few 2026 first-person sizing statements: fixed unit size, half off at 2x. Unverified; no PnL attached to the rule in the visible text.
- **@DeFiMinty, "10 tips I wish I knew before trading memecoins" (May 27, 2024)** - https://x.com/DeFiMinty/status/1795197886663123100. Visible text only: "Price action is king ... memecoins are an attention-driven economy, volume and tx count show real attention." Rest not retrieved.

### 1.2 "How I made X" headline claims in 2026 (rules mostly not retrievable)

- **@pr6spr (Ethan Prosper), "How I turned $200 into multi millions trading memecoins in less than two years" (Aug 20, 2026)** - https://x.com/pr6spr/status/2090301751165374543. Only the headline is retrievable via oEmbed; thread content not read. Same account is at the centre of the April 2026 bundling controversy (section 1.4) and published an X article "I Didn't Break the Game - I Played It" (Apr 3, 2026; text not read). Self-reported; conflict of interest: streamer/content income, terminal/referral relationships typical for this category.
- **Trending case "$99 -> $200K on a Solana memecoin via the Fomo app" (Aug 15-16, 2026)** - https://x.com/i/trending/2088746475459125415 ; a Lookonchain post on the same event claims a different wallet turned $120 into $205.8K (822x). Entry at ~$10K mcap, peak above $17M. This is on-chain-verifiable by Lookonchain but is a lottery outlier, i.e. survivorship bias, not a method.

### 1.3 Meta change: holding time and "trenches are dead" (2025 - 2026)

- **Cointelegraph quoting Dune Analytics (Mar 31, 2026):** average Solana memecoin hold time 58 s in 2026, ~100 s in 2025, ~1 day in 2024 - https://x.com/Cointelegraph/status/2039055293842104684. Later posts quote 42 s (camol, Aug 26, 2026, https://x.com/camolNFT/status/2092703310625038651) and 40 s (vibhu, Aug 30, 2026, https://x.com/vibhu/status/2094113917144326576). The figures are different datasets/definitions (a search also returned a 62 s median and 60 s median reading); treat as "tens of seconds", not as a precise number.
- **@frankdegods (Nov 11, 2025):** "people that complain about short hold times remind me of virtue signalers. hold times decreased because of the exponential overproduction of tokens ... it's rotational and PVP but it is opt-in at the end of the day, and most people should not play" - https://x.com/frankdegods/status/1988094609181077615. Note the last clause: a top-profile trader saying most people should not play.
- **@RuneCrypto_ (Apr 1, 2026):** "the trenches are dead maybe dying ... nobody holds anything, nobody believes in anything, even good narratives top at $200K mc" and asks whether anyone is holding one coin with conviction vs "flipping 8-second positions" - https://x.com/RuneCrypto_/status/2039134365968388404 and https://x.com/RuneCrypto_/status/2039133751695827426.
- **@cryptolyxe (Apr 1, 2026):** hold times are bad not because of Pump.fun or terminals but a "mindset shift" from "1 SOL and a dream" - https://x.com/cryptolyxe/status/2039172120849072186 (rest truncated).
- **@StarPlatinum_ (Aug 27-28, 2026)**, via the trending page https://x.com/i/trending/2092803745449136638 (posts https://x.com/StarPlatinum_/status/2092895090049962421 and https://x.com/StarPlatinum_/status/2093265503221420120): says he rotated his largest position from Solana memes to Robinhood-chain tokens because "every token is either being vamped or used by the cabal" (PVP); second post admits a repeated mistake: forcing himself into hot trenches because he is "a victim of hype". Only first lines read; text partially truncated.
- **@vibhu (Aug 30, 2026):** memecoins are "the short form videos of assets" (analogy, not evidence).

### 1.4 Bundling, devving and multi-wallet (April 2026 dispute)

- **@OrangeSBS (Orange), Apr 6-7, 2026:** "The only way to survive this market and be profitable is by multi wallet and devving" - https://x.com/OrangeSBS/status/2041151274976993341 ; "Not using these tools (mw, devving) right now is like refusing to use a gun in a war just because people used to fight with swords" - https://x.com/OrangeSBS/status/2041434969537429752. Per Grok summary, a Pump.fun affiliate is quoted (via @wirelyss, https://x.com/wirelyss/status/2041431027495678362) as saying "rape or get raped" - I did not read the underlying video.
- **@Ga__ke (gake), Apr 7, 2026:** no objection to tooling per se, but objects to what it enabled: "a guy holding 20-30% supply of a coin to stream himself doing it and selling it immediately" - https://x.com/Ga__ke/status/2041444188521394380.
- **@rasmr_eth, Apr 3, 2026:** attacks streamers "buying 30% of a coin at 6k market cap ... bundling on 75 wallets" - https://x.com/rasmr_eth/status/2039884440558542931. Same account later admitted (stream clip, Jul 2026, per trending page https://x.com/i/trending/2073418929599582319) to buying the "winner" of his own comparison videos on side wallets before posting - an admitted front-running pattern, reported secondhand by Grok summary.
- **@pr6spr (Prosper), Apr 2-3, 2026:** defends himself ("i trade honestly") and says "We need coins to go to billions so the trenches can start to believe in something again" - https://x.com/pr6spr/status/2039703862496366780 ; the Apr 3 post https://x.com/pr6spr/status/2039937710236844538 is only a link (an X article).
- **@DustNukes (Apr 6, 2026):** accuses another "bundle exposer" account of secretly farming/rugging deploys - https://x.com/DustNukes/status/2041135651735925181. Allegation only.
- Why it matters: the loudest "how I trade" voices in the 2026 trenches describe the edge as controlling supply at launch (bundles, devving, multi-wallet), not chart reading. The counterparty is the follower. Cross-check: Bitquery (search result, not X) reports Pump.fun dev bundles made about $579M vs snipers $31.5M.

### 1.5 Skill vs. mechanics debate (Aug 28, 2026)

- **@gainzy222:** trenching is "hard work", claims 300k+/month possible, "they're online 18 hours, they want it more than you" - https://x.com/gainzy222/status/2093309472676446693 (trending page https://x.com/i/trending/2093405232214716915). Self-promotion context; unverified income.
- **@trading_axe:** "anyone with copytraders can do this ... isn't some insane insight outside of viral runners that are sized into" - https://x.com/trading_axe/status/2093339399765340569. Reply by @straightozero shows the criticized trade bought at 579K mcap ($4,956.71) and sold at 494K ($5,612.82), i.e. profit despite a falling price, taken as evidence of a copy-trading/followers effect - https://x.com/straightozero/status/2093341409252086232.
- **@dollargamma:** "they prey on feeble minded retail and win every time as a collective" (opinion) - https://x.com/dollargamma/status/2093361517857063236.

### 1.6 Copy-trading as a mechanism (Sep 2026)

- **@rasmr_eth (Sep 22, 2026):** "having copytraders is so annoying ... I can't sell because then that's dumping on my followers? this shit is straight up nerfing me" - https://x.com/rasmr_eth/status/2102197868757127631. A KOL admitting that followers copying his entries/exits constrain his own exit; replies (not read in full) accused some influencers of treating followers as exit liquidity.

### 1.7 Leads that did not resolve (do not cite as findings)

- Ansem (@blknoiz06) recommended "spyzer's memecoin trading guide, over 100 pages" (Jun 30, 2026) - https://x.com/blknoiz06/status/2071973553168118172. The guide's content was not retrieved.
- Cupsey's "over $1,000,000 on pump.fun alone, 0 insider plays, 0 raydium coins, just in the trenches 12+ hours a day" (Jul 3, 2024) - https://x.com/Cupseyy/status/1808348461739241721. Confirmed verbatim through oEmbed. Contains no entry/exit/sizing rule; it is a recruitment post. Allegations about him are listed in note 01.
- Frank (@frankdegods, Dec 25, 2024): "Trading memecoins on Solana is the most fun method to make money known to mankind and it's REALLY not close" - https://x.com/frankdegods/status/1872059985964007560. Sentiment, no rule.
- Solsniper "paper trading" posts (Feb 2025) are product marketing for a paper-trade mode: https://x.com/solsniperxyz/status/1894447429141004617.

## 2. Practitioner rules extracted (de-duplicated)

| # | Rule | Who says it | Quality of support |
|---|---|---|---|
| R1 | Avoid bundled tokens, high sniper share, high dev holding; top 10 under 10-15% | gremlin (dev 0-5%, snipers 0-2, top10 <=10-15%), Volt (bundled/whale checks) | Only anecdote (author says it "improved hit rate"). No numbers on hit rate. |
| R2 | Take initial back at 2-3x ("moonbag") / sell 50% at 2x | Reflection, camol (Sep 2026) | Anecdote. |
| R3 | Fixed small unit size, quick loss cutting | camol ($75 unit, 2026), gremlin (0.1-0.5 SOL quick buys) | Anecdote. |
| R4 | Choose either high hit rate with early profit and bigger mcap (>$300k), or low hit rate/small tickets under $5M | Volt | Opinion; no data. |
| R5 | Wallet tracking / copying "smart money" is the main edge | Volt, Reflection, gremlin | Each sells a Telegram/bot funnel for this. |
| R6 | Be early to the meta, hold conviction through 2-10x | gremlin | Self-admitted round-trips of $200k-1M. Survivorship. |
| R7 | The real 2026 edge is supply control (bundle/multi-wallet/devving) | Orange (Apr 2026), implicitly Prosper, rasmr | Admission of tactics that are accused of harming holders. |
| R8 | Most deploys die fast: "90% don't pass 10k mc"; "most people should not play" | jacknuked (2024), Frank (Nov 2025) | Directionally consistent with data. |
| R9 | Rotate venue when Solana is PVP/vamped | StarPlatinum_ (Aug 2026) | Single trader's opinion. |
| R10 | Paper-trade first | Solsniper | Vendor marketing. |

## 3. Comparison with our measured findings (`reports/Backtest memecoinów podsumowanie.md`)

| Our measurement | What X traders say | Verdict |
|---|---|---|
| Without a filter every exit strategy loses 17-34% per trade; no measured edge for an outsider | Nobody publishes a verified edge. Frank: "most people should not play". gremlin: "you'll get rekt most of the time". | Consistent. The posts claiming profits show screenshots/claims without costs. |
| Exclusion filters (low liquidity, seller dominance, falling knives) are the only thing that works; dev >20% supply -> 62-69% dumps vs 38% base | gremlin: dev 0-5%, snipers 0-2, top 10 <=10-15%; Volt: avoid bundled/whale-held | Direction agrees with our dev-holding finding. Their exact thresholds were not tested by us. NOTE: our own "few bundlers/insiders + liquidity" rule turned out to be a data artifact (frozen mcap) - their "good-looking filter -> better hit rate" claim is the same kind of claim that did not survive our test. |
| Exit rules: 10,962 combos, 0 profitable out-of-sample even at zero cost | "Sell 50% at 2x", "initial back at 2-3x + moonbag", "limit sells for 10-50x" | Not supported. These are risk-management heuristics, not shown to create positive expectancy. Could be tested as one more rule family, but our walk-forward search already covered similar partial-exit structures. |
| Lifecycle: 67% of tokens peak in the first 15m candle; median 24h price 0.65x of entry; recovery after -50% only 6.6% | jacknuked: "90% don't pass 10k"; Volt/gremlin: early entries, hold through 2-10x | Their "hold for conviction" advice conflicts with our median outcome; "take profit early" is closer to it. |
| Pumps: buying after a pump candle -> median -20% after 1h, -38% after 4h; 87% of pump-sells are by earlier buyers | Reflection/Volt: follow top-wallet buys; gremlin: Trending section "unusual volume" | Conflict. Trending/"volume" screening buys what has already pumped. |
| Wallet copying: -22% to -38% out-of-sample; top-20 Kolscan copy about -23% at 2 s delay | Volt/Reflection/gremlin recommend wallet tracking and copy bots as the main edge; Rasmr (Sep 2026) says copiers constrain his own exits | Direct conflict. The tracked-wallet edge exists for the wallet owner at his own latency, not for the follower; trader's own words confirm followers are a liquidity source. Cented's reported -21.3% copy result (note 01) fits. |
| 10.9% of wallets profitable; 1% take 95% of gross profit; bots 53% of profits but net -15%; snipers -79% | Gainzy: "300k+/month if you want it"; Axius/Axe debate: copytrader/PVP effects | Consistent with extreme concentration; the claimed incomes are from the 1% tail. |
| Execution: ideal -7.2%, bot -26.7%, manual -29.2%; slippage is the biggest cost; stops on pump.fun jump (stop -18% filled at -84%) | Reflection: "never use regular DEXs, speed is the difference"; gremlin: MEV protection, auto speed | Consistent that speed/execution matters; none quantify it. Stop-gap risk is rarely discussed in posts. |
| Only profitable bot: ~$938k in 111 days, entry in the same second as token start, ~6 s hold | Hold-time data: 58 s (2026) falling to 42 s; "8-second positions" (Rune) | Consistent. The profitable behavior reported is ultra-short, infrastructure-dependent. Cented's profile (notes 01) matches. |
| pump.fun is a negative-sum game | Orange: "multi wallet and devving ... the only way to survive"; gake: tooling "perpetuated" harmful behavior; rasmr: streamers "ruined on-chain" | Consistent: insiders describe the winners as extractors from other participants, not predictors. |
| Timing (hour/day/age) gives no edge | No X trader argued for time-of-day rules in what I read | No contradiction, no support. |
| Starts/calls: model hits double from 26% to 45%, but a 20% entry delay turns calls into a loss (-9%) | Prosper/"followers" thread: KOL exits are constrained by copiers | Same mechanism: whoever is first wins, followers lose. |

Net result: the self-described practitioner rules (small fixed units, partial profit at 2x, avoid dev/bundle/sniper-heavy tokens, avoid chasing) are risk-hygiene and agree with our exclusion-only conclusion. The advertised "edges" (copy smart wallets, chase trending volume, hold conviction through noise) are the ones our data contradicts.

## 4. Conflicts of interest and credibility flags (summary)

- Telegram/bot funnels: Volt, Reflection, gremlin all end with a group, bot or wallet-list sale. Selling the "list of top wallets" is monetization of follower flow into those wallets.
- Content/streaming income: Prosper, rasmr, Orangie, gainzy - income depends on audience, platform deals or referral fees; a Pump.fun affiliate relationship is alleged for the "rape or get raped" clip (secondhand).
- Survivorship: the $99 -> $200K Fomo case, the $1,491 -> $1.2M "MEME" trending case and similar posts are lottery-tail outcomes.
- Grok-written trending summaries are machine summaries; I treated them as pointers to real posts and re-fetched key posts with oEmbed.
- Dune hold-time statistics differ by dataset and are quoted through news posts, not a primary dashboard.
- Allegations (Dust vs. himothy, Bubblemaps vs. Cupsey, Sahil/Ansem) are allegations; no adjudication.
- None of the tweet-level numbers above include costs, slippage or taxes; no author published a full trade log.

## 5. Open items

- Retrieve full text of camol 2097069948128645547, Prosper 2090301751165374543, Minty 1795197886663123100 and Prosper's Apr 3 article (needs a host that returns thread text; threadreader returned a shell, oEmbed truncates).
- Try other public archives that are not Nitter (e.g. Wayback copies of x.com threads) if allowed.
- Possible test for the next backtest round: gremlin's Memescope filter (pump progress 15-25%, holders 15-25, dev 0-5%, snipers 0-2) as an exclusion-style filter on our 9,684-token set, evaluated with the walk-forward harness, with the caveat of frozen-mcap data artifacts found earlier.
