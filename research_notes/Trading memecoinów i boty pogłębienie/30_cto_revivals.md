# Community takeovers (CTOs) and revivals of dead memecoins

Research limits: 3 web searches ran (the third was rate-limited and returned unsourced general knowledge). All WebFetch calls failed (blofin.com, decrypt.co and cointelegraph.com are not in the session's allowed network domains). Everything below comes from search-result summaries, not full pages. Treat it as thin and unverified.

## How do CTOs happen, and what are the pump.fun CTO features?

### Takeaway
On pump.fun a CTO is a platform-approved handover of a coin's creator-fee position and some admin rights, not an automatic crowd action. It usually follows the original dev abandoning the coin. Pump.fun reportedly decides each case at its discretion and has sped up approvals.

### Cited Findings
- Control passes by application and pump.fun decides each one at its sole discretion. The rules sit in pump.fun's Terms of Use (creator fees and cashback coins section). — [BloFin Academy: what is a community takeover](https://blofin.com/academy/education/pumpfun/what-is-a-community-takeover) (via search summary, unverified)
- The new team gets the creator-fee position and some admin rights, and can set fee percentages through pump.fun tools. Holders' tokens do not move. — [BloFin Academy](https://blofin.com/academy/education/pumpfun/pump-fun-cto-coins-risk) (search summary)
- The revamped fee system reportedly lets teams and CTO admins split fees across up to 10 wallets, transfer coin ownership and revoke update authority. A streamlined CTO feature reportedly cut approval times from days to a few hours. — [Cointelegraph](https://cointelegraph.com/news/pumpfun-revamps-creator-fees-fee-sharing-cto-controls) (search summary only; not fetched, exact dates not verified)
- Pump.fun reportedly focused on CTO tokens in Aug 2025, and TROLL was cited as hitting an all-time peak. — [Mitrade](https://www.mitrade.com/au/insights/news/live-news/article-3-1015971-20250806) (headline only)
- Pump.fun enabled creator-fee redirection for abandoned coins. — [Altcoinbuzz](https://www.altcoinbuzz.io/cryptocurrency-news/pumpfun-enables-creator-fee-redirection-for-abandoned-coins/) (headline only)
- A typical trigger is the original creator walking away or selling off. — [crypto.news](https://crypto.news/what-is-a-community-takeover-cto-when-a-memecoins-holders-seize-the-wheel/) (search summary)
- The process is criticised as opaque. In the $PENGUIN case, some alleged the internal CTO ownership handling was discretionary or hijacked. — [OurCryptoTalk](https://ourcryptotalk.com/news/penguin-cto-hijack-allegations-rock-pump-fun) (headline and summary; allegations, not confirmed)
- The Gochu.fun CTO page (199 USDC fee) describes a different platform, so it is not pump.fun's process. — [Gochu docs](https://gochu-fun.gitbook.io/gochufun/additional/community-takeover)

### Inferences
- Because pump.fun gatekeeps CTOs and ties them to fee redirection, a CTO is partly a monetisation mechanism for the new team. That is an incentive to run it, and also a possible conflict of interest.
- A "CTO" label on a screener is not proof of a community. Check that the platform actually approved the fee handover.

### Gaps
- No primary pump.fun source (ToS or docs) was read. Exact criteria, fees, timelines and dates are unverified.
- The $PENGUIN dispute details were not read.

## Notable successes and failures, and outcome data

### Takeaway
Billy is the standard CTO success story and TROLL is cited as a pump.fun CTO peak. No dataset measuring CTO outcomes was found, and commentary suggests most CTOs fizzle.

### Cited Findings
- Billy (Solana) survived its dev abandoning it and is the example usually cited as a CTO that worked. The takeover group is described as up to 100 people with marketing and social roles. — [Decrypt](https://decrypt.co/241846/how-solana-meme-coin-billy-survived-being-abandoned-by-its-dev) (search summary; figures not verified)
- One analysis states most community takeovers do not lead to moonshots or moderate success and trend toward zero. It is commentary, not data. — [Capwolf](https://capwolf.com/communityresolving-conflicting-category-instructions-takeover-cto-when-memecoin-holders-seize-the-wheel/) (search summary)
- The "97% of meme coins fail" figure is widely repeated, but I could not trace its underlying data. — [BeInCrypto](https://beincrypto.com/?p=571208) (unverified)
- Cryptonary claims 37% of Ethereum memecoins fizzle. — [Cryptonary](https://cryptonary.com/research/dont-buy-meme-coins-before-reading-this) (unverified)
- The most rigorous related academic work is an arXiv study of 34,988 tokens on market manipulation in the meme coin ecosystem. It does not focus on CTOs. — [arXiv 2507.01963](https://arxiv.org/abs/2507.01963v2)
- TROLL as a pump.fun CTO coin reaching an all-time peak (Aug 2025). — [Mitrade](https://www.mitrade.com/au/insights/news/live-news/article-3-1015971-20250806) (headline only)

### Inferences
- Survivorship bias is likely: the CTOs that get written up are the winners. The base rate for a CTO coin is probably worse than the examples suggest. This is an inference, not measured.

### Gaps
- No on-chain or peer-reviewed comparison of CTO vs non-CTO tokens. Suggested next step: Dune or Bitquery analysis of pump.fun tokens with fee-admin changes.
- No verified market-cap figures for Billy or TROLL, and no named failures with data.

## Signals distinguishing genuine revivals from setups

### Takeaway
No sourced study exists. The checklist below is general-knowledge guidance from a rate-limited search (no sources), so treat it as unverified heuristics.

### Cited Findings
- None sourced. The following is unsourced general guidance and is unverified:
  - Dev or deployer wallet still holds a large share.
  - Mint or freeze authority not revoked (Solana), or owner privileges active (EVM).
  - LP not burned or locked.
  - Honeypot or sell restrictions (simulate a sell first).
  - Bundled or linked wallets and coordinated early buys.
  - Anonymous "new team" with socials created simultaneously (possibly the old deployer).
  - Insider sells during the hype spike.

### Inferences
- Pump.fun coins have mint authority renounced by design. Check this, as I believe it is so, but it was not verified here. The main setup risks are therefore insider or old-dev holdings, fee-seat capture and coordinated hype, not contract tricks.

### Gaps
- No sourced evidence on revival-vs-setup signals, no rate of CTO rugs, and nothing on bot tooling for detecting CTOs (for example, DexScreener "CTO" tags or fee-claim wallet monitoring). Requires a fresh search with the network allowlist widened.
