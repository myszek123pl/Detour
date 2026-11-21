# 03 - Retail memecoin traders: self-reported experience (aggregated)

Date: 2026-11-21. Language: English.

## Method and limits (read first)
- WebSearch worked; WebFetch was blocked for reddit.com and failed DNS for zikoko.com, beincrypto.com, crypto.news (outside allowed network). I did not bypass this.
- So everything below comes from SEARCH-RESULT SUMMARIES, not full-page reads. Treat claims as unverified second-hand.
- No Reddit threads (r/solana, r/memecoins, r/CryptoCurrency, r/SolanaMemeCoins) were reachable. No Polish forum/Wykop/Reddit-PL first-person accounts were found; Polish hits were only news/explainers (antyweb.pl, comparic.pl, bitcoinist.com/nowe-solana-meme-coins), which say most people will lose funds.
- GitHub: repo search for "memecoin trading journal lessons learned" returned nothing; code search returned only unrelated files. No usable personal journals found.
- Selection bias: published stories skew to dramatic wins/losses and to self-promotion (paid guides, bot referrals). Silent median loser is under-represented.

## Typical beginner journey (pattern across sources)
1. Entry via hype: social media/Reddit/friends, often buying a famous coin at/near the top (HackerNoon author: first coin Dogecoin bought at the top because Reddit said "moon").
2. Early small win (e.g. $50 -> $200 flip, Zikoko essay) creates overconfidence; then a much larger bet.
3. Escalation: bigger size, new launches, presales, copy-trading, Telegram sniper bots.
4. Big loss: single rug/dump or round-trip of paper gains (Zikoko: ~$5k put in one coin, lost overnight; other reports: $88.9k on WYNN, $210k on a peak buy in 24h, ~$900k of ~$1M spread over 13 memes).
5. Either quit, or rebuild with rules (position sizing, profit-taking). Sources describing "a first year" frame it as learning patience, risk respect, humility.

## Base rates (analyst data, not self-reports)
- BeInCrypto citing Dune: >60% of addresses on Pump.fun incurred substantial losses; another BeInCrypto piece: ~90% of Pump.fun traders lost or made <$100. Figures not independently verified.

## Common mistakes reported
- FOMO buying at highs / after the pump; no stop-loss or risk plan (Mexc/Coinmonks list).
- Oversizing; "all-in" on one coin.
- Not selling: round-tripping huge paper gains back to near zero (Substack "stop roundtripping" example: $9 -> $40,000 -> ~$1,600; FOMO Family profile: ran small account to low seven figures, gave it all back in the cycle, then restarted with $4,000).
- Chasing presales and trending-list tokens (Cointelegraph; Anatoly Yakovenko urged people to stop investing in memecoin presales).
- Drifting from "solid projects" to pure speculation (Coinfomania story).
- Trusting hype figures/KOL claims; promo content passing as experience.

## Scams and security incidents retail fell for
- Rug pull: dev drains liquidity pool; honeypot tokens that cannot be sold (one dev reportedly took ~$1.62M this way; Cointelegraph Sept 2024).
- Fake-volume tokens on trending lists (GMGN) with hidden code letting dev move holders' tokens (researcher Roffett.eth, Cointelegraph).
- Telegram trading-bot compromises: Solareum/BONKbot-linked incident ~ $523k from 300+ wallets (Decrypt/BeInCrypto; BONKbot denied link); Banana Gun ~ $1.9M (The Block, Cyvers estimate); Bloom ~ $953k in 94s (Bitquery); SIGMA bot >$200k single user (private-key leak suspected). Bot-held keys are a custodial-style risk.
- Phishing/drainers: fake verification bots (Inferno Drainer via fake Collab.Land), fake "Jupiter verification" DMs, Telegram group malware; drainer kits sold for ~$300.
- Caveat: several attributions rest on on-chain analysis/community reports.

## What reportedly worked for the few who became profitable
- Strict position sizing; small stakes relative to net worth (FOMO Family profile centers on sizing).
- Predefined, automated partial profit-taking (e.g. sell initial stake at 2x-3x, keep a "runner" bag; "banked money stays banked") - AirdropAlert, DEXTools, TechFlow; Benzinga relays Ansem-style advice of preset take-profit levels.
- Written rules instead of discretion; avoiding giving back paper gains.
- Contract/permission checks before buying (mint authority, liquidity lock/owner permissions; TradingView guide).
- Treating memecoins as gambling, not a strategy (crypto.news framing that losses can be educational).
- Caution: "bot-assisted consistent gains" Medium post (hodlhero201) is promotional with unverifiable results; trader-claim pieces (Benzinga "$5K -> $200K twice") promote the author's own guide. No source shows a repeatable edge for retail.

## Time to profitability
- No reliable data. Anecdotes: gave back a whole cycle then rebuilt from $4k (FOMO Family); "first year" lessons pieces. Treat as unknown; likely years or never for most, given base rates above.

## Rules retail adopts after losses (aggregate)
1. Risk only an amount you can lose entirely; cap per-trade size.
2. Take partial profits on predefined levels; withdraw to stablecoins/bank.
3. Never buy a vertical candle/FOMO; skip presales and unsolicited DMs.
4. Verify token permissions, liquidity, holder concentration; assume honeypot until tested with a tiny buy/sell.
5. Use a burner hot wallet; avoid keeping large balances in Telegram bots; never sign unknown transactions.
6. Keep a trade journal; stop after drawdown limit.

## Sources (via search summaries)
- https://hackernoon.com/the-biggest-mistakes-i-made-in-my-first-year-of-trading-and-how-you-can-avoid-them
- https://www.zikoko.com/money/i-put-5k-on-a-meme-coin-and-lost-it-all-overnight/
- https://beincrypto.com/pump-fun-trading-data-majority-lose-money/
- https://beincrypto.com/pump-fun-meme-coins-trader-losses/
- https://benzinga.com/markets/cryptocurrency/25/03/44260478/i-lost-everything-trader-turns-0-into-5-million-loses-it-all-with-meme-coins-that-were-supposed-to-become-the-next-dogecoin-shiba-inu
- https://benzinga.com/z/37184038
- https://benzinga.com/z/38707677
- https://coinfomania.com/from-solid-projects-to-empty-pockets-a-traders-hard-lesson-on-chasing-memes-in-crypto-and-how-he-went-from-steady-to-speculation/
- https://crypto.news/why-losing-money-on-memecoins-might-be-the-best-thing-that-ever-happened-to-you/
- https://fomo.family/blog/learn/notanicecat69-memecoin-trading-strategy
- https://insightfulinfo.substack.com/p/stop-roundtripping-your-massive-memecoin
- https://www.dextools.io/tutorials/memecoin-trading-strategy-take-profits
- https://airdropalert.com/blogs/take-profit-strategy-meme-coins/
- https://medium.com/@hodlhero201/from-rugged-bags-to-consistent-gains-how-sniper-bots-changed-my-meme-coin-season-ad254fc5bb23
- https://cointelegraph.com/news/scammers-memecoin-trending-researcher
- https://cointelegraph.com/magazine/5-risks-apeing-new-solana-memecoins/
- https://decrypt.co/224127/solana-wallet-drained-523k-bonkbot-denies-link
- https://www.theblock.co/post/317282/banana-gun-telegram-bot
- https://cointelegraph.com/news/bloom-bot-hackers-953k-faster-popcorn
- https://antyweb.pl/nadchodzi-era-memecoinow-na-solanie
- https://cryptoslate.com/solana-co-founder-tells-community-to-stop-investing-in-memecoin-pre-sales/

## Follow-ups if network is widened
Allow reddit.com, zikoko.com, beincrypto.com, crypto.news, wykop.pl to read primary threads; then re-verify stats and collect direct r/solana / r/SolanaMemeCoins quotes.
