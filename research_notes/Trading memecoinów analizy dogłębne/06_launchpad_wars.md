# Solana launchpad wars 2025-2026 (as of Nov 2026)

NOTE ON COVERAGE: Web search was rate-limited (3 of 4 calls returned "too_many_requests"). Verified data below stops at ~Aug 2025. Nothing from late 2025-Nov 2026 was verified. Items from model memory are labelled UNVERIFIED and carry no source.

## Mechanics differences between launchpads

### Takeaway
Launchpads differ mainly in creator incentives (fee share, pre-funding), the AMM that receives graduated tokens, and the quality of deployers. Only Jupiter Studio and Moonshot details were sourced; the rest are unverified.

### Cited Findings
- Jupiter Studio launched July 2025; by 2026 "Jupiter launchpad" means Studio, not the older LFG model — [Backpack Learn](https://learn.backpack.exchange/articles/what-is-jupiter-studio); [Bitget Academy](https://web3.bitget.com/en/academy/what-is-jupiter-studio-the-differentiator-in-solanas-defi-ecosystem); [CryptoSlate](https://cryptoslate.com/launchpads/jupiter-studio-review/)
- Jupiter Studio: creators can launch without pre-funding and reportedly get ~50% of swap fees during bonding and after graduation (single Chinese-language report; UNVERIFIED) — [TechFlow/Odaily](https://techflowpost.com/en-US/article/26793)
- CryptoSlate notes Studio is more open: faster launches but more noise, creator risk and quality variance — [CryptoSlate](https://cryptoslate.com/launchpads/jupiter-studio-review/)
- Jupiter took a majority stake in Moonshot in Jan 2025; Moonshot is a mobile-only app — [The Block](https://www.theblock.co/news/ecosystems/2025-01-25-jupiter-acquires-majority-stake-in-moonshot-announces-jupnet-and-10-million-ai-fund-at-catstanbul-event-337059); [Solana Compass](https://solanacompass.com/projects/moonshot)
- LetsBonk launched April 2025 (Raydium LaunchLab-based) — [The Block](https://theblock.co/post/361189/letsbonk-dethrones-pump-fun-with-higher-daily-memecoin-volume-token-launches); [CoinGecko](https://www.coingecko.com/learn/letsbonk-fun-solana-memecoin-launchpad-guide)
- Pump.fun charges a 1% fee on transactions — [Decrypt](https://decrypt.co/332091/pump-fun-revenue-plummets-meme-coin-traders-tap-launchpads)

### Inferences
- Fee-share-to-creator designs (Studio, and by memory Bags/Believe) attract creator-brand launches, not sniper-friendly fair launches; a bot should expect different holder and insider structure.

### Gaps
- UNVERIFIED (memory only, not researched): Meteora DBC is infrastructure that Believe, Jupiter Studio and others build on; Believe uses a creator/X-post launch flow; Bags ties launches to X/social handles with fee-sharing to creators or named accounts; Heaven is a Solana launchpad/DEX with a curve-to-own-AMM design. Heaven returned zero search results; its details are entirely unconfirmed.
- Per-launchpad graduation thresholds and post-graduation venues (Raydium, PumpSwap, Meteora DAMM) not verified.

## Market share over time

### Takeaway
2025 saw pump.fun lose dominance to LetsBonk in July, then recapture it by August; the sources' numbers conflict because they measure different things. No post-Aug-2025 share data was found.

### Cited Findings
- LetsBonk overtook pump.fun in early July 2025 on daily volume and launches — [The Block](https://theblock.co/post/361189/letsbonk-dethrones-pump-fun-with-higher-daily-memecoin-volume-token-launches)
- Jupiter data: LetsBonk 49.80% vs pump.fun 40.90% of launchpad share on one July day — [CoinMarketCap Academy](https://coinmarketcap.com/academy/article/letsbonk-news-pumpfun-loses-market-dominance-as-letsbonk-captures-meme-coin-traders)
- Pump.fun reported at 19% of launchpad tokens on July 26, down from 88% a month earlier; LetsBonk reached nearly 70% of graduated tokens at peak — [CoinMarketCap](https://coinmarketcap.com/community/post/366173273)
- Aug 11, 2025: pump.fun ~75% share — [The Block](https://www.theblock.co/news/markets/2025-08-11-pump-fun-fends-off-letsbonk-in-battle-for-top-solana-memecoin-launchpad-366395); days later pump.fun reportedly ~90%, LetsBonk ~3% — [CoinMarketCap Academy](https://coinmarketcap.com/academy/article/pumpfun-reclaims-90percent-market-share-in-solana-launchpad-war); [The Block](https://www.theblock.co/post/367266/solana-memecoin-launchpad-war-flips-again-as-pump-takes-top-spot-amid-letsbonk-collapse); [Forklog](https://forklog.com/en/letsbonk-loses-80-of-market-share-in-two-weeks/)
- Pump.fun revenue fell as traders used other launchpads — [Decrypt](https://decrypt.co/332091/pump-fun-revenue-plummets-meme-coin-traders-tap-launchpads)

### Inferences
- Share swings tracked where high-volume deployer bots chose to launch (The Block attributes the August reversal to top deployers, many bots, returning to pump.fun) — so share is incentive-driven and reversible; incentive/fee-rebate programs should be tracked as a leading indicator.
- Sources conflict (75% vs 90%, launches vs graduations vs volume); any bot dashboard must fix one metric definition.

### Gaps
- No verified share data for Sep 2025 - Nov 2026, including Bags, Believe, Heaven, Jupiter Studio, Moonshot, Meteora DBC shares. Check Dune launchpad dashboards directly.

## Graduation rates and trader outcomes per launchpad

### Takeaway
No sourced per-launchpad graduation rate or trader PnL was obtained.

### Cited Findings
- LetsBonk accounted for nearly 70% of graduated tokens at its July 2025 peak while holding about 50% of launches, implying a higher graduation share than launch share (inference from [CoinMarketCap](https://coinmarketcap.com/community/post/366173273) and [CoinMarketCap Academy](https://coinmarketcap.com/academy/article/letsbonk-news-pumpfun-loses-market-dominance-as-letsbonk-captures-meme-coin-traders)).

### Inferences
- High graduation counts on a fast-growing venue may reflect low graduation thresholds, bundled/farmed launches, or incentive-driven activity rather than organic demand; do not treat graduation as a quality signal without checking holder distribution.

### Gaps
- UNVERIFIED memory: pump.fun graduation historically ~1% of launches. No figures for other launchpads. No trader-outcome (win rate, median PnL, rug rate) data found.

## Characteristics a bot should treat differently

### Takeaway
Based on the verified material, key differentiators are creator fee-share, openness/spam level, graduation venue and deployer-bot concentration; treat each launchpad as its own regime with separate parameters.

### Cited Findings
- See mechanics section: Studio's openness raises noise and creator risk — [CryptoSlate](https://cryptoslate.com/launchpads/jupiter-studio-review/); Moonshot is mobile-only — [Solana Compass](https://solanacompass.com/projects/moonshot).

### Inferences
- Per-launchpad filters: separate graduation-probability priors, separate creator-fee/ongoing-sell-pressure assumptions (creator fee share creates incentive to farm volume), separate deployer-reputation lists, and avoid pooling stats across launchpads.
- Share swings mean launchpad-specific models need frequent recalibration.
- Treat market-share headlines skeptically: confirm the metric (launches, graduations, volume).

### Gaps
- All 2026 developments (new launchpads, shutdowns, fee changes, pump.fun competitors) unresearched due to search rate limits; re-run with Dune/DefiLlama/The Block sources.
