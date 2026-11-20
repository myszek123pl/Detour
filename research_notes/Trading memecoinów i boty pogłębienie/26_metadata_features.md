# Token metadata as success predictors (name/ticker, image, links, description, copycats, impersonation)

Note: research done Nov 2026 with 5 web searches. arxiv.org was NOT reachable for WebFetch (DNS blocked in session), so paper details rest on search-result summaries only; no primary-paper numbers were verified.

## 1. What do studies (CoinCLIP etc.) show about metadata/image/text as predictors?

### Takeaway
CoinCLIP is the main published multimodal study (pump.fun logo + description + comments -> "viable"/not). Reported to beat text-only/image-only baselines, but I could not verify its numbers or what "viable" means. No rigorous public evidence found for name/ticker length effects.

### Cited Findings
- CoinCLIP uses a frozen CLIP (ViT-L/14) plus lightweight adapter modules; image and text fused via Hadamard product; classifies memecoins as viable / not viable — [arXiv 2412.07591](https://arxiv.org/html/2412.07591v2)
- Its CoinVibe dataset has >6,200 memecoins with text descriptions, logo images, community comments (comments carry timestamps/likes), sourced from pump.fun; 80/10/10 split; code and data said to be public on GitHub — [arXiv 2412.07591](https://arxiv.org/html/2412.07591v2) (via search summary)
- A secondary review states CoinCLIP "consistently outperformed baselines" (text-only, image-only, other multimodal); no numbers obtained — [Moonlight review](https://www.themoonlight.io/en/review/coinclip-a-multimodal-framework-for-assessing-viability-in-web3-memecoins)
- Related dataset "Coin-Meme" (arXiv 2412.04913): 3,751 memecoins created Jan-Nov 2024 that migrated to Raydium; multimodal cultural/financial analysis — [arXiv 2412.04913](https://arxiv.org/html/2412.04913v3)
- MemeChain (2026) is a cross-chain dataset including website HTML, logos and linked social accounts, potentially usable for copycat detection — [arXiv 2601.22185](https://arxiv.org/html/2601.22185v1)
- arXiv 2602.14860 does an on-chain analysis of early pump.fun launches to predict graduation; per search summary it focuses on early trading dynamics and participant composition and does not appear to examine naming (I saw only the abstract-level summary) — [arXiv 2602.14860](https://arxiv.org/html/2602.14860v1)
- No study found testing name/ticker length or style. Closest: a Towards Data Science piece hypothesizing readable names matter (no results reported) — [TDS](https://towardsdatascience.com/cognitive-bias-in-cryptocurrency-naming-74c5d6a7990f)

### Inferences
- Visual/text semantics seem to carry some signal in CoinCLIP, but label definition ("viable") and leakage via comments (post-launch) may inflate it; comments are not available at launch, so a sniper bot cannot use that modality at t=0.
- Early trading dynamics (buyers, flow) likely dominate metadata for predicting graduation; metadata is a weak/secondary prior.

### Gaps
- CoinCLIP accuracy/F1 and ablation (image vs text) numbers: unverified (arxiv blocked).
- Name/ticker length/style effect: no source.
- AI-generated vs. human image effect: no source found.
- Description-text features: no source found beyond CoinCLIP's use of text.

## 2. Do website / X / Telegram links predict success?

### Takeaway
No reliable evidence that social links raise graduation odds. A large audit explicitly withdrew its Telegram-effect statistic.

### Cited Findings
- Brave New Coin audit of 832,941 pump.fun launches: author withdrew stats on the apparent effect of advertising a Telegram channel because they inherited limits from the underlying labels — [Brave New Coin](https://bravenewcoin.com/insights/what-auditing-832941-pump-fun-launches-taught-me-about-memecoin-success)
- Practitioner template lists Twitter/Telegram presence as tracked signals, not an empirical result — [skills.sh](https://skills.sh/sanctifiedops/solana-skills/pump-fun-mechanics)
- Base rate context: pump.fun graduation stayed below 1% from Feb 17, 2025 after a 1.67% peak in Nov 2024 — [Cointelegraph](https://cointelegraph.com/news/pump-fun-memecoins-are-dying-at-record-rates-less-than-1-survive); ~0.26% in a 2026 DEXTools report — [DEXTools](https://www.dextools.io/news/pump-fun-graduation-collapse-solana-fees-2026); spike to 6.7% after BOOST (per The Block summary, unverified) — [The Block](https://www.theblock.co/post/409815/robinhood-chain-deposits-climb-even-as-volume-and-daily-users-fade)

### Inferences
- Links are trivially cheap to fake (any URL can be entered), so they are a weak filter; at best a necessary-not-sufficient hygiene check. Verify links are live/age-appropriate rather than just present.

### Gaps
- No controlled graduation/return comparison with vs. without links.
- Whether links were added at creation vs. later: not found.

## 3. Copycat tickers of trending coins and impersonation of famous names

### Takeaway
Copycat/impersonation launches are common and usually harmful for buyers, but I found no quantified study of copycat success rates (CoinCLIP-style copycat analysis was not found). Evidence is anecdotal/news.

### Cited Findings
- Fake Saudi "KSA" memecoin announced from account impersonating the crown prince; contract launched on pump.fun a week before announcement — [Cointelegraph](https://cointelegraph.com/news/saudi-prince-impersonators-launch-fake-saudi-arabia-memecoin)
- Hijacked celebrity accounts used to push tokens: Doja Cat (DOJA) ~$1.6M investor losses — [Cointelegraph](https://cointelegraph.com/news/investors-lose-1-6-million-doja-cat-x-reportedly-hacked); Sydney Sweeney (SWEENEY) — [FXStreet](https://www.fxstreet.com/cryptocurrencies/news/why-investors-need-to-be-careful-about-celebrity-meme-coins-after-sweeney-token-scam-202407312221); Instagram accounts of Adele/Future/Michael Jackson — [Decrypt](https://decrypt.co/336465/adele-future-michael-jackson-instagram-accounts-hijacked-crypto-scam?amp=1)
- Common playbook: take over verified account, post token address/pump.fun link — [Cointelegraph](https://cointelegraph.com/learn/articles/top-memecoin-scams)
- June 2026: Ansem disavowed multiple $ANSEM tokens; with many same-name tokens only the contract address is unforgeable — [DEXTools](https://www.dextools.io/news/ansem-disavows-ansem-memecoins-onchain-data-june-2026)

### Inferences
- Pump-and-dump by fast insiders can still yield short-lived pumps on hijack/impersonation events (one token reported hitting $900K then -98%, unverified), so these can be tradeable only for ultra-fast entries, with very high rug risk. For a bot: treat name-collision with a trending token as a risk flag unless contract matches an officially announced CA.
- Cloned image/ticker detection (CLIP embedding similarity to existing tokens) is technically feasible given CoinCLIP's CLIP backbone, but this is my inference, not a published result.

### Gaps
- No quantitative win-rate/return data on copycat tickers vs. originals.
- No source found on AI-generated image quality effect.
