# Copy-Trading in Memecoin Markets: Mechanics, Real-World Effectiveness, Alpha Decay and Failure Modes

> Research-process note (for the report writer): in this session WebFetch was blocked by network policy (arxiv.org, gmgn.ai, alchemii.io all failed to resolve), and the shared web-search budget ran out after about 13 queries. Every finding below therefore comes from search-result snippets and search-engine summaries, not from full-page reads. Treat exact numbers as "as reported in snippet" and re-check them against the primary page before quoting them prominently. Most practitioner sources are vendors (GMGN, Trojan, Banana Gun, uwuu.ai, MemeScout) or affiliate blogs, which have a commercial interest in copy-trading. The only academic sources found are two 2026 arXiv papers (one also at ASE '26).

## 1. How copy-trading bots work (trigger detection latency, sizing, exit mirroring)

### Takeaway
All mainstream Solana copy-trade tools (GMGN, Trojan, Axiom, Banana Gun, Insiders Bot, Jupiter) follow the same loop. They watch a target wallet, detect its swap, and fire your own swap with your chosen size, slippage, fees and filters. Exits can be mirrored ("copy sells") or set by your own TP/SL. Execution always comes after the leader's trade. Vendors claim same-block fills, but no independent latency benchmark exists.

### Cited Findings
**Pipeline and architecture**
- An academic study of 586 GitHub bot repositories and 200 on-chain Solana bot addresses (more than 44 million transactions) found 15 bot categories in five domains (e.g., Trading Operations, MEV, On-chain Analytics). Implementations share a "largely shared five-stage operational pipeline". Its validation set includes a copy-trading group, but I could not see copy-trading-specific results. — [Demystifying Solana Bots, arXiv 2607.28424 / ASE '26](https://arxiv.org/abs/2607.28424); [Pith review](https://pith.science/paper/2607.28424)
- A reviewer notes that the bot addresses came largely from a few leaderboard bot services, so the fingerprint clusters may not represent sniping or wash-trading bots. — [Pith review](https://pith.science/paper/2607.28424)

**Trigger detection and latency**
- Trojan's own guide says copy trading is "inherently reactive". Its execution infrastructure "minimizes" latency, but "no system eliminates it entirely". — [Trojan blog: Solana copy trading guide 2026](https://trojan.com/blog/solana-copy-trading-guide-2026)
- One bot's marketing claims "up to 65%" of copy trades land in the same block as the original transaction. A separate hands-on test notes that Trojan publishes no first-block inclusion rate and no independently verified latency benchmark. — [TradersDNA: fastest Solana trading bot 2026 test](https://www.tradersdna.com/the-fastest-solana-trading-bot-in-2026-tested-on-live-launches/) (vendor claims; unverified)
- A hands-on review of eight copy-trading tools rated CopyFomo the weakest. It cited slow confirmations and copy signals that "lagged noticeably" behind the target wallets. — [Medium: Best Memecoin Copy Trading Bots in 2026, 8 tools compared](https://medium.com/@thefarazahmadd/best-memecoin-copy-trading-bots-in-2026-8-tools-compared-7aec2aaf8ae5)
- The cost of latency: HTX says a 40-second delay on a memecoin can mean buying about 60% higher. — [HTX: Can Grok Bot really make money automatically?](https://www.htx.com/news/can-grok-bot-really-make-money-automatically-first-understan-GG3U8Ufz/) (illustrative, not a measured statistic)

**Sizing, slippage and fees (tool settings)**
- GMGN's official tutorial covers these settings:
  - Target wallet: one-tap copy from the Rank/Radar pages fills in the address.
  - Sell settings: auto copy-sell, TP/SL and other exit conditions.
  - Token filter settings.
  - "Platforms & blacklist".
  - Copy-trade notifications. — [GMGN docs: Copy Trade](https://gmgn-app.gitbook.io/gmgn-app-tutorial/tutorial/copy-trade)
- DataWallet's overview of GMGN reports a maximum of 10 active copy tasks, with user-set position size and TP/SL. It cites GMGN documentation warning that priority fees from frequent orders can turn a profitable target into an unprofitable copy. — [DataWallet: GMGN explained](https://www.datawallet.com/crypto/gmgn-explained)
- Trojan settings:
  - Default slippage is 15%. A heavily followed wallet likely needs higher slippage.
  - The copy-trade module has its own slippage setting, separate from the global one.
  - Higher priority fees get faster inclusion but burn SOL.
  - Filters: a market-cap range and "Max Spend Per Buy".
  - Troubleshooting guidance advises against copying snipers. — [Trojan docs: FAQ](https://docs.trojanonsolana.com/overview/trojan-on-solana-faq); [Trojan docs: Copy Trade](https://docs.trojanonsolana.com/telegram-bot-user-guide/copy-trade)
- Third-party Trojan guides suggest a Jito tip of about 0.005–0.01 SOL for normal trades and much more for competitive launches. — [CoinCodeCap: Trojan best settings](https://coincodecap.com/best-settings-for-trojan-bot) (affiliate guide)
- Banana Gun controls, as described by third-party guides:
  - "Buy Fixed" sets a fixed amount per trade, which decouples your size from the leader's.
  - "Spend Limit" caps total spending for the strategy.
  - "Min Market Cap" sets a floor.
  - "Copy Sells" makes you sell when the leader sells; with it off, you hold until you act.
  - Limit orders and a trailing stop-loss can sit on top of a copy trade. — [Indie Hackers: how Banana Gun's copy trade mirrors a wallet without copying its trade size](https://www.indiehackers.com/post/how-banana-guns-copy-trade-mirrors-a-wallet-without-copying-its-trade-size-Muu5oRE9LMd8Uz1DE5zg); [PCTechMag: 7 risks and the Banana Gun settings](https://pctechmag.com/?p=101658); [3zebras: 3 Banana bot copy-trade filters](https://3zebras.com/crypto/ape-smarter-the-3-banana-bot-copy-trade-filters-that-cap-a-bad-wallet/15979/)
- Axiom: wallets are tracked in a "Tracker" tab (wallets and Twitter). The user adds a wallet and a buy amount, and trades are mirrored, with slippage, priority and bribe-fee settings. One author suggests 5–15% slippage. — [MadeOnSol: How to use Axiom](https://madeonsol.com/blog/how-to-use-axiom-solana-trading); [Medium: Axiom trade strategy](https://medium.com/@GEMQUEENx/axiom-trade-strategy-best-settings-filters-and-fees-for-maximum-profits-eab7504cb07d) (third-party; the official docs.axiom.trade could not be read)
- Other tools with documented copy-trade modules: Jupiter, Insiders Bot (edit/pause/remove copy tasks), Archr and RustRocket. — [Jupiter docs: copy trading](https://docs.jup.ag/user-docs/trade/trading-bot/copy-trading); [Insiders Bot: Copytrade settings](https://insidersbot.gitbook.io/insiders.bot/copy-trading/copytrade-settings); [RustRocket copy trader](https://rust-rocket.gitbook.io/rust-rocket/copy-trader/introduction)
- An open-source copy trader on GitHub scores wallets and uses time-decay exits. Another repo contains a `wallet_rotation_manager.py` (function not visible). — [GitHub: Jugooch/Memecoin-Trader](https://github.com/Jugooch/Memecoin-Trader); [GitHub: MO3ARAFA/Meme-coin](https://github.com/MO3ARAFA/Meme-coin)

### Inferences
- A copier always buys after the leader, often blocks or seconds later. In thin pump.fun or bonding-curve pools, the copier's own buy, plus every other copier's buy, pushes the price up. Slippage is therefore built into the structure, not occasional.
- Fixed sizing (as in Banana Gun "Buy Fixed") is now the norm. Proportional sizing to a whale's trade would be dangerous in thin pools. The catch: small fixed sizes make per-trade fees (priority fee, Jito tip, platform fee of about 1% on many bots) a large share of the position. This is GMGN's own warning about fees turning a profitable target into a losing copy.
- "Copy sells" is the key, and fragile, exit mechanism. If the leader exits in pieces, through another wallet, or via a transfer rather than a swap, the copier's exit trigger may never fire.

### Gaps
- No independent measurement of copy-trade latency (ms or slots) for GMGN, Axiom, Trojan or Banana Gun was found. Vendor "same-block" claims are unverified.
- Exact current platform fees on copy trades (e.g., GMGN, Axiom, Trojan, about 0.5–1%) were not confirmed from primary docs in this session.
- The official Axiom docs (docs.axiom.trade) and the full GMGN copy-trade page could not be read.

## 2. Evidence on copy-trader performance vs the copied wallets (slippage, latency, crowding)

### Takeaway
The best evidence available, a 2026 academic preprint, finds that even when smart-money wallets earn positive returns and are identified correctly, a naive copier's returns stay negative after the price impact of buying just after them. The broader base rate is grim: about 80% of wallets trading new pump.fun coins were losing money, and high-frequency bot-like wallets did worst. No source shows copy-trading being reliably profitable.

### Cited Findings
**Academic evidence**
- Luo, Feng, Xu and Liu (UCL et al.), "Resisting Manipulative Bots in Meme Coin Copy Trading" (arXiv 2601.08641, Jan 2026, revised to v3 in Feb 2026), is the main finding:
  - "For statistic-driven models, positive smart-money returns are insufficient to yield positive copier profitability, with copier returns remaining negative despite robust copy trading."
  - The model has copiers buy right after the smart money, which moves the price against them. — [arXiv 2601.08641](https://arxiv.org/abs/2601.08641); [arXiv HTML v2](https://arxiv.org/html/2601.08641v2); [UCL Discovery PDF](https://discovery.ucl.ac.uk/id/eprint/10220650/1/Resisting_Manipulative_Bots_in_Meme_Coin_Copy_Trading__A_Multi_Agent_Approach_with_Chain_of_Thought_Reasoning.pdf)
- The same paper names three reasons copy trading does not guarantee profit:
  - manipulative bots are everywhere;
  - followed wallets' future performance is uncertain;
  - trade execution lags. — [arXiv 2601.08641 v1](https://arxiv.org/html/2601.08641v1)
- Its proposed multi-agent LLM system reports 73% precision at identifying high-quality memecoin projects and 70% at identifying KOL wallets, on a dataset of 1,000 memecoin projects. This is a preprint, the evaluation is the authors' own, and it is not peer-reviewed. — [arXiv 2601.08641](https://arxiv.org/abs/2601.08641); [EmergentMind summary](https://www.emergentmind.com/papers/2601.08641)

**Base rates for memecoin traders**
- In an analysis of 921 new pump.fun coins, only 20.5% of the 11,070 wallets that traded them were in profit after 46 hours. The bot-like group (wallets trading 20+ coins) had the worst median result, −$21.42. — [Alchemii: Is meme coin trading profitable? Real wallet data](https://www.alchemii.io/blog/is-meme-coin-trading-profitable) (vendor blog; methodology not verified)

**Survivorship bias and persistence**
- A Solana analyst calls the big PnL of top wallets "survivorship bias dressed up as alpha". — [Medium (N. Baldwin): Copy trading on Solana, how to find alpha wallets](https://medium.com/@nathan.baldwin_31153/copy-trading-on-solana-how-to-find-alpha-wallets-without-getting-faked-out-by-bots-0bc550f07290)
- A tool review makes the same point: past profitability tells you nothing certain about what a wallet does next. — [Medium: 8 tools compared](https://medium.com/@thefarazahmadd/best-memecoin-copy-trading-bots-in-2026-8-tools-compared-7aec2aaf8ae5)
- Contrary claim: a Medium "encyclopedia" cites an 81.5% out-of-sample win rate for a top-200 wallet group. It shows no methodology, so treat it as low-credibility. — [Medium: The Memecoin Trading Encyclopedia](https://medium.com/@rakesh.therani/the-memecoin-trading-encyclopedia-35-concepts-backed-byproduction-data-6745ab79d1c9)

**Crowding**
- Trojan's FAQ says copying a heavily followed wallet likely needs higher slippage. This is an implicit vendor admission that crowding raises execution costs. — [Trojan docs: FAQ](https://docs.trojanonsolana.com/overview/trojan-on-solana-faq)
- Practitioner warnings: you may end up providing exit liquidity for the wallet you copy. — [HTX](https://www.htx.com/news/can-grok-bot-really-make-money-automatically-first-understan-GG3U8Ufz/); [PCTechMag / Banana Gun](https://pctechmag.com/?p=101658)

**Dune dashboards (pointers, numbers not verified)**
- Public dashboards exist for per-bot volume and users, e.g., TradeWiz; Dune's April 2025 post also points to other bots' dashboards. — [Dune on X](https://x.com/Dune/status/1907059375812067386)
- Trojan has a stats dashboard with a "Degen Leaderboard". — [Medium: Top Solana wallets for copy trading (KOLSCAN, Dune)](https://medium.com/@moiofficial/top-solana-wallets-for-copy-trading-310438afc998)
- "Solana Alpha Wallet Signals For Copy Trading" (@pixelz) is a wallet-PnL dashboard. Copy-bot vendors such as OdinBot and Tachyon use Dune dashboards to find wallets by PnL and ROI. — [OdinBot docs: Dune dashboard](https://docs.odinbot.io/tracking-academy/tools/for-finding-wallets/dune-dashboard); [Tachyon docs: Dune copy wallets guide](https://docs.tachyonlabs.info/copy-bot-guide/dune-copy-wallets-guide)
- None of these dashboards compares copier PnL with leader PnL.

### Inferences
- Alpha decay has two parts:
  1. **Execution decay:** the price gap between the leader's fill and the copier's fill, plus fees. This alone can wipe out a positive edge in thin memecoin pools (the Luo et al. result).
  2. **Signal decay:** wallets chosen for past PnL regress toward the mean because of survivorship and selection bias.
- Crowding makes both worse. Every additional copier on a popular wallet raises the price for the copiers after them, and the leader can sell into that flow.
- Copy-trading is most likely to work where execution decay is small relative to the leader's expected move: higher-liquidity tokens, leaders who hold for hours or days rather than seconds, and wallets that are not publicly famous. That is consistent with the practitioner filters in section 4. This is inferred, not empirically shown, in the sources found.

### Gaps
- No public, systematic study measures copier PnL against leader PnL per trade (realized slippage in bps, crowding vs number of copiers). I found no Dune dashboard that does this.
- No quantified "half-life" of a smart wallet's edge (e.g., how many weeks top-decile wallets stay top-decile) was found from a credible source.
- I could not read the full Luo et al. PDF, so the size of the negative copier returns and the exact copy-delay assumption are unknown.

## 3. Counter-strategies by copied wallets (bait trades, selling into copiers, wallet rotation)

### Takeaway
Exploiting copiers is a well-recognized adversarial game. Insiders and KOLs build public "smart money" track records to attract copiers and then sell into the buying those copiers create. They split positions across wallets to hide their size, use wash trading to fake activity, and coordinate dumps. Vendors and academics both acknowledge this, but no study measures how common it is.

### Cited Findings
**Exploitation by manipulative bots**
- Luo et al. say the copy-trading model exposes an attack surface. Adversaries deploy manipulative bots to "front-run trades, conceal positions, and fabricate sentiment, systematically extracting value from naïve copiers at scale." — [arXiv 2601.08641](https://arxiv.org/abs/2601.08641)
- One concealment method they describe is spreading purchases across multiple controlled wallets to hide true positions. This splits the signal and defeats single-wallet copying. — [arXiv 2601.08641 PDF](https://arxiv.org/pdf/2601.08641)
- The paper calculates a per-trader wash-trading score from matched flips vs net position. A token is flagged when any trader's score exceeds a threshold (c = 50). — [arXiv 2601.08641 v1](https://arxiv.org/html/2601.08641v1)

**Exit-liquidity baiting**
- GMGN's own guide, as reported in search snippets, makes three points:
  - "Exit Liquidity Baiting": because public "smart money" labels are visible to everyone, some insider wallets are built specifically to attract copy traders and dump tokens on them.
  - "Copy-trade farmers" dump into the buying pressure their copiers create.
  - Consistent in-and-out trades within seconds may indicate a bot or bait farmer. — [GMGN blog: How to track and copy Solana smart money (2026)](https://gmgn.ai/blog/how-to-track-copy-solana-smart-money/) (search-snippet content; page not readable here)
- Banana Gun-related guidance warns that target wallets may buy pump-and-dumps or honeypots and use copy traders as exit liquidity. It also says a wallet with a strong record can turn bad, and a TP that never triggers never sells. — [PCTechMag: 7 risks + Banana Gun settings](https://pctechmag.com/?p=101658)

**Bot-dominated leaderboards**
- One post says most top leaderboard wallets are automated sniper scripts, which a human-speed copier cannot replicate. — [Medium (N. Baldwin): How to find alpha wallets and avoid bots](https://medium.com/@nathan.baldwin_31153/copy-trading-on-solana-how-to-find-alpha-wallets-and-avoid-bots-26182d750bb2)
- Trojan advises against copying snipers. — [Trojan docs: Copy Trade](https://docs.trojanonsolana.com/telegram-bot-user-guide/copy-trade)

**KOL coordination and insider behavior**
- A vendor guide (uwuu.ai, which sells an auto-copy product) warns that multiple KOLs sometimes buy the same token together and then dump on followers. — [uwuu.ai: How to copy KOL trades on Solana](https://uwuu.ai/blog/how-to-copy-kol-trades-solana)
- This is relevant to "consensus" signals: multi-wallet confluence can itself be staged.
- ZachXBT exposed 16 influencer X accounts that coordinated pump-and-dumps, leaving followers to absorb the losses (as reported via BeInCrypto in the search summary). — [KOLSCAM blog](https://kolscam.blogspot.com/) (anonymous blog of allegations; the ZachXBT item came from the search summary, and the BeInCrypto URL was not captured)
- Insider front-running around Kolscan itself: when Pump.fun acquired the KOL-tracking tool Kolscan, a cluster of connected wallets made more than $3M by buying the related token before the public announcement. — [DL News](https://www.dlnews.com/articles/defi/memecoin-kols-bag-millions-as-pump-fun-buys-kolscan-tracker/)
- Kolscan streams KOL and top-trader wallets in real time with per-token PnL and a public leaderboard. This makes those wallets the most crowded copy targets. — [SolanaBox: Kolscan](https://solanabox.tools/tools/kolscan); [Meme Insider: Kolscan explained](https://meme-insider.com/en/article/kolscan-solana-meme-token-wallet-tracker/)
- A forum user's advice: "I do not recommend copytrading them [KOLs] but rather tracking them to see what they are aping." — cited via search summary of [Kolscan Review 2026 (uwuu.ai)](https://uwuu.ai/blog/kolscan-review) / [BlackHatWorld thread](https://www.blackhatworld.com/seo/list-of-popular-solana-memecoin-wallets.1682445/) (exact attribution unclear)

### Inferences
- The more visible a wallet is (KOL label, GMGN "smart money" tag, Kolscan leaderboard), the more copier flow it attracts. That turns its own buys into a predictable demand source it can sell into, so the wallet's public PnL and a copier's PnL can diverge sharply.
- Wallet rotation and position splitting work against copiers in two ways:
  - A real edge-holder can move to fresh wallets, leaving copiers on a stale address.
  - An exploiter can farm a fresh address with a good track record, then use it as bait.
- Copiers therefore face both survivorship bias and adversarial selection. Wallets that look most copyable may be disproportionately baits.

### Gaps
- No quantitative estimate was found of how often copied wallets sell into their copiers, or of copier flow per famous wallet.
- No sourced documentation of "wallet rotation" or burner-wallet practices by profitable traders specifically to shake off copiers. It is mentioned only indirectly (multi-wallet concealment in Luo et al.; a `wallet_rotation_manager.py` in a GitHub repo).
- Bait-trade patterns (e.g., a tiny buy to trigger copiers followed by a large sell from a linked wallet) are described qualitatively by vendors. No on-chain case study was found in this session.

## 4. Best practices: basket diversification, filters, consensus signals, exit rules

### Takeaway
Practitioner consensus has six parts:
1. Vet wallets for genuine, repeatable, human-speed edge: many distinct tokens, profit not driven by one trade, plausible (not 90%+) win rates, and multi-hour holds rather than seconds.
2. Avoid snipers, KOLs and famous leaderboard wallets as copy targets.
3. Use fixed small sizes with spend caps.
4. Apply token filters such as a min market cap or liquidity, a market-cap range, and mint/freeze-authority and holder-concentration checks.
5. Use your own TP/SL or trailing stops rather than relying only on copy-sells.
6. Treat multi-wallet consensus as a signal to investigate, not to auto-buy, because coordinated KOL buys can be staged.

### Cited Findings
**Wallet vetting**
- Vet the target wallet before setting up any copy trade. Check how many different tokens it bought last week and whether its profit depends on a single trade. — [PCTechMag / Banana Gun guidance](https://pctechmag.com/?p=101658)
- Filter for wallets with at least 30 unique-token trades. Check mint/freeze authority and holder concentration on tokens. — [Medium (N. Baldwin)](https://medium.com/@nathan.baldwin_31153/copy-trading-on-solana-how-to-find-alpha-wallets-and-avoid-bots-26182d750bb2)
- Win-rate thresholds differ between sources:
  - One guide suggests only wallets with a 60%+ win rate over 100+ trades that hold positions for hours or days. — [search summary of Solana copy-trading guides; see GMGN blog](https://gmgn.ai/blog/how-to-track-copy-solana-smart-money/)
  - Another practitioner says real alpha wallets in memecoins land in a 20–60% win-rate range and treats win rates above 80% as a warning sign of cherry-picking or bots. — [Medium (N. Baldwin)](https://medium.com/@nathan.baldwin_31153/copy-trading-on-solana-how-to-find-alpha-wallets-without-getting-faked-out-by-bots-0bc550f07290)
  - Neither threshold is empirically validated.
- Filter out bot-like wallets, e.g., buy delays under 3 seconds after launch, or in-and-out trades within seconds. — [Medium (N. Baldwin)](https://medium.com/@nathan.baldwin_31153/copy-trading-on-solana-how-to-find-alpha-wallets-and-avoid-bots-26182d750bb2); [GMGN blog](https://gmgn.ai/blog/how-to-track-copy-solana-smart-money/)
- Do not copy snipers. — [Trojan docs: Copy Trade](https://docs.trojanonsolana.com/telegram-bot-user-guide/copy-trade)
- Track KOLs for ideas rather than copy them automatically. — [Kolscan review / forum advice](https://uwuu.ai/blog/kolscan-review)

**Token filters and sizing in tools**
- GMGN: token filter settings and a platform blacklist. — [GMGN docs: Copy Trade](https://gmgn-app.gitbook.io/gmgn-app-tutorial/tutorial/copy-trade)
- Trojan: market-cap range and Max Spend Per Buy. — [Trojan docs](https://docs.trojanonsolana.com/telegram-bot-user-guide/copy-trade)
- Banana Gun: Min Market Cap, Buy Fixed and Spend Limit. — [3zebras: 3 Banana bot copy-trade filters](https://3zebras.com/crypto/ape-smarter-the-3-banana-bot-copy-trade-filters-that-cap-a-bad-wallet/15979/); [Indie Hackers](https://www.indiehackers.com/post/how-banana-guns-copy-trade-mirrors-a-wallet-without-copying-its-trade-size-Muu5oRE9LMd8Uz1DE5zg)
- Fees: priority fees on frequent small orders can turn a profitable target unprofitable. Size positions so fixed per-trade costs stay a small fraction. — [DataWallet citing GMGN docs](https://www.datawallet.com/crypto/gmgn-explained)

**Exit rules**
- Copy Sells mirrors the leader's exit. Without it, you hold until you act. Limit orders and trailing stop-loss can be layered on top. — [Indie Hackers / Banana Gun](https://www.indiehackers.com/post/how-banana-guns-copy-trade-mirrors-a-wallet-without-copying-its-trade-size-Muu5oRE9LMd8Uz1DE5zg); [PCTechMag](https://pctechmag.com/?p=101658)
- A TP that never triggers never sells, so you need a stop or time-based exit as well. — [PCTechMag](https://pctechmag.com/?p=101658)
- GMGN sell settings: auto copy-sell plus TP/SL. — [GMGN docs](https://gmgn-app.gitbook.io/gmgn-app-tutorial/tutorial/copy-trade)
- Time-decay exits are used in an open-source copy bot. — [GitHub: Jugooch/Memecoin-Trader](https://github.com/Jugooch/Memecoin-Trader)

**Manipulation screening**
- Academic approach: screen tokens for wash trading (per-trader wash score above threshold c = 50) and screen KOL wallets with a multi-agent LLM. The reported precision is 70–73%, which still means about 30% false positives among selected projects and wallets. — [arXiv 2601.08641](https://arxiv.org/abs/2601.08641)

**Consensus signals**
- Coordinated KOL co-buying followed by dumping is a known pattern, so confluence among public KOL wallets is not a clean signal. — [uwuu.ai](https://uwuu.ai/blog/how-to-copy-kol-trades-solana)

### Inferences
**Basket diversification**
- Copying 5–10 vetted wallets with small fixed sizes and per-wallet spend caps (GMGN allows 10 active tasks) limits the damage from any single wallet turning into bait or regressing.
- Caps per token also matter, because several leaders often buy the same token at once.

**Consensus logic**
- Requiring 2–3 independent, unrelated, non-KOL smart wallets to buy within a time window plausibly cuts false signals.
- Wallets must be checked for linkage (common funding source, timing clusters). Linked wallets are one actor, and coordinated KOL buys are a known bait.
- No source quantified the lift from consensus signals.

**Where copy-trading most plausibly works**
- Leaders with longer holding periods (hours to days).
- Tokens past the bonding-curve or snipe phase with real liquidity (minimum liquidity / market-cap floor).
- Lesser-known wallets that aren't crowded.
- Copy-trading as a discovery and alert tool combined with your own entry and exit rules, rather than blind mirroring.

**Where it most plausibly fails**
- Copying snipers, KOLs or famous leaderboard wallets.
- Micro-cap bonding-curve tokens.
- Tiny positions where fees dominate.
- Relying only on copy-sells for exits.

### Gaps
- No empirical study was found that measures the benefit of multi-wallet consensus, basket size or specific liquidity/market-cap filters on copier PnL. All the recommendations above are practitioner heuristics.
- Specific minimum-liquidity numbers (e.g., "≥$X liquidity") from primary tool docs were not retrieved. Recommendations varied across affiliate blogs and were not verified.
- Searches for consensus/cluster-buy signals and for fee/MEV losses on copy trades could not run because the search budget ran out. A follow-up could target practitioner threads (X, Reddit r/solana / r/memecoins) and Dune queries comparing copier and leader fills.
