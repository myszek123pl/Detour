# Legal, regulatory and tax rules: individual in Poland trading memecoins with an automated bot (as of Nov 2026; not legal advice)

## 1. Polish crypto tax (PIT-38, 19%, costs, crypto-to-crypto, losses) and 2025-26 changes (Polish crypto-asset market act, KNF)

### Takeaway
Disposals of virtual currency are taxed at a flat 19% on PIT-38 (filed 15 Feb to 30 Apr of the following year); crypto-to-crypto swaps are widely described as not taxable, with tax triggered on conversion to fiat/payment. Poland still had no national MiCA implementing act as of the latest sources I found (mid/autumn 2026, status unverified), which matters for CASPs, not for a private trader's tax.

### Cited Findings
- Flat 19% rate; PIT-38 filing window 15 Feb to 30 Apr of the year after the tax year — [podatki.gov.pl PIT-38 for 2025](https://www.podatki.gov.pl/twoj-e-pit/en-pit-38-za-2025-rok); [Kraken guide](https://www.kraken.com/learn/poland-crypto-tax-guide)
- Commercial guides agree crypto-to-crypto swaps are not taxed; tax arises on fiat conversion; swap costs treated as non-deductible — [Plisio](https://plisio.net/tax/poland-crypto-tax); [CoinTracking](https://cointracking.freshdesk.com/en/support/solutions/articles/29000050303-crypto-taxes-in-poland-2026-the-complete-guide) (vendor sources, not statute)
- Deductible costs: official 2025 guidance frames them as costs of earning revenue from the paid disposal of virtual currency; Kraken says only purchase and sale-related costs are allowable (mining equipment, electricity excluded); Dudkowiak lists purchase costs and exchange fees — [podatki.gov.pl](https://www.podatki.gov.pl/twoj-e-pit/en-pit-38-za-2025-rok); [Kraken](https://www.kraken.com/learn/poland-crypto-tax-guide); [Dudkowiak](https://www.dudkowiak.com/blog/crypto-tax-in-poland-2025-guide/)
- Losses (official): a 2025 return may include losses from 2020-2024; general PIT rule is carry-forward over the next 5 years, with no more than 50% of the loss deducted in any one year; losses can only be set against the same source — [podatki.gov.pl](https://www.podatki.gov.pl/twoj-e-pit/en-pit-38-za-2025-rok); contradicted by vendor claims of "no time limit" — [Plisio](https://plisio.net/tax/poland-crypto-tax)
- Unsettled carried-forward losses must be indicated by the taxpayer in the return — [podatki.gov.pl](https://www.podatki.gov.pl/en/your-e-pit/pit-38-for-2024)
- Polish MiCA implementing act: President Nawrocki vetoed versions in Dec 2025, Feb 2026 and June 2026; Sejm override failed (third vote 241 for, 198 against, short of 3/5); the EU transition period ended 1 July 2026, with Poland described as the only member state without a domestic implementation; KNF is the intended supervisor — [The Block](https://www.theblock.co/post/381598/poland-becomes-eus-lone-mica-holdout-after-parliament-fails-to-overturn-veto-on-crypto-bill); [Intellinews](https://www.intellinews.com/polish-president-vetoes-crypto-assets-bill-for-third-time-448265/); [Dudkowiak](https://www.dudkowiak.com/blog/the-act-on-the-crypto-assets-market-vetoed-again-will-poland-be-ready-with-casp-licences-before-1-july-2026/)
- A new presidential draft was reportedly submitted to the Sejm on 8 Sept 2026; differences concern KNF account-blocking powers and sanction levels — [Dudkowiak](https://www.dudkowiak.com/the-president-submits-a-new-draft-act-on-the-crypto-assets-market-what-does-it-mean-for-the-industry/)

### Inferences
- For a private trader, the unlicensed-CASP gap mainly affects which venues are usable (Polish exchanges risk losing the legal basis to serve customers), not the PIT-38 mechanics.
- A bot trading memecoins on DEXs is mostly token-for-token (e.g. SOL to memecoin), so taxable events cluster at off-ramps; each cash-out must be tracked with cost basis and fees. The bot's volume does not change the rate, but record-keeping burden is large. Whether swaps through DEXs are treated identically to CEX swaps is not addressed by official sources I found.
- Possibility of the activity being classed as business activity (not capital-gains PIT-38) at high frequency: plausible risk, no source found.

### Gaps
- Current (Nov 2026) status of the Polish act (new draft passed? signed?). Sources conflict/are unclear; check sejm.gov.pl and knf.gov.pl.
- Statute text (PIT Act art. 17(1)(11), 22(14-16), 30b) not fetched; whether crypto costs carry forward indefinitely vs the 5-year/50% rule is contested between vendors and official page.
- Any 2025-26 changes to the 19% rate, DAC8/CARF reporting (DAC8 applies from 1 Jan 2026 per my background knowledge; not verified in this research), Polish exchange-reporting obligations: not searched.
- Treatment of airdrops, rug-pull losses, DeFi/liquidity pools, gas fees: not found.

## 2. MiCA treatment of memecoins; when running a bot for others becomes regulated

### Takeaway
Own-account trading needs no CASP licence; offering a bot/service to others can be a regulated crypto-asset service (likely portfolio management if discretionary, or order execution/reception), and since 1 July 2026 doing this without authorisation breaches MiCA. MiCA does not define "auto/copy trading", so classification is case-by-case.

### Cited Findings
- ESMA: MiCA does not define "auto trading" or "copy trading"; the provider must classify the service, applying MiFID II guidance by analogy only for classification — [ESMA Q&A](https://www.esma.europa.eu/node/217075)
- ESMA has said no CASP licence is needed for proprietary trading on own account (no client relationship) — [Mondaq summary of ESMA Q&A](https://webiis08.mondaq.com/fin-tech/1715298/esma-qa-regarding-mica-and-casp)
- Portfolio management = discretionary management under client mandates, triggered by a portfolio including at least one crypto-asset — [KPMG](https://assets.kpmg.com/content/dam/kpmg/cy/pdf/2025/markets-in-crypto-assets-regulation-mica.pdf)
- Authorisation is service-specific and passportable only for listed services; transitional period closed, services to EU clients after 1 July 2026 without authorisation are a breach — [PwC alert](https://legal.pwc.de/content/services/regcore-client-alert/pwc-legal-client-alert-after-the-micar-cliff-edge-june-2026.pdf); [CSSF](https://cssf.lu/en/crypto-assets-service-providers-casp)
- Capital requirement figures conflict across guides (EUR 125,000 vs EUR 50,000 for portfolio management) — [AMLBot](https://blog.amlbot.com/mica-license-explained-casp-requirements-authorization-process-and-eu-passporting/) vs [KPMG](https://assets.kpmg.com/content/dam/kpmg/cy/pdf/2025/markets-in-crypto-assets-regulation-mica.pdf)

### Inferences
- Selling bot software (SaaS, user keeps keys and runs it) is probably not a CASP service, but a bot you operate with others' funds/keys, or pooled funds, likely is; profit-sharing with friends is the risky edge. Inference only; no source specifically on bots.
- Pooling investor money may additionally trigger other regimes (collective investment/AIFMD, Polish law); not researched.

### Gaps
- No source specifically on memecoin classification under MiCA (not asset-referenced/e-money tokens, so likely "other crypto-assets" under Title II; white-paper duty applies to offerors/admission seekers, not ordinary traders). This is background knowledge, not sourced here.
- Polish-specific treatment of unlicensed activity (penalties) pending the national act.

## 3. MiCA market abuse (manipulation, insider dealing) and pump-and-dump risk

### Takeaway
MiCA Title VI (Art. 86-92) prohibits insider dealing and market manipulation for crypto-assets admitted to trading on a platform (or with admission requested); Art. 91 mirrors MAR Art. 12 with a social-media angle. Joining coordinated pump-and-dumps or running a bot that spoofs/wash-trades carries real legal risk, but memecoins never admitted to a trading platform may fall outside scope, a significant uncertainty.

### Cited Findings
- Art. 91: no person may engage in or attempt market manipulation — [ESMA Interactive Single Rulebook](https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mica/article-91-prohibition-market-manipulation)
- List of manipulative behaviours tracks MAR Art. 12 with a crypto-specific addition for social-media-driven markets; promoting a token and selling without disclosure is given as pump-and-dump example; argued to cover manipulation via DEXs if the asset is in scope — [Mondaq, Fintech Insights 12](https://webiis08.mondaq.com/fintech/1792090/fintech-insights-12-mica-prevention-of-market-abuse)
- Scope limit: market abuse rules exclude assets not admitted to trading platforms or without pending request; pump-and-dump listed among key risks — [Cambridge EJRR](https://www.cambridge.org/core/journals/european-journal-of-risk-regulation/article/cryptoasset-market-abuse-under-eu-mica/FDC11EC096728B9EF1097A5346F0EF27)
- ESMA issued supervisory guidelines for national authorities on preventing/detecting market abuse under MiCA (2025); a compliance table dated 29 Oct 2025 lists authorities' intentions — [ESMA press](https://www.esma.europa.eu/press-news/esma-news/esma-issues-supervisory-guidelines-prevent-market-abuse-under-mica); [compliance table](https://www.esma.europa.eu/sites/default/files/2025-10/ESMA75-113276571-1625_Compliance_table_Guidelines_on_market_abuse_MiCA.pdf)

### Inferences
- Memecoins on Pump.fun-style launchpads are often only on DEXs with no formal "admission"; whether DEX pools count as trading platforms is untested in sources found. Do not treat this as a safe harbour.
- Polish criminal law (fraud, art. 286 KK) and consumer/fraud rules could apply independently; not researched. With Poland lacking an implementing act, KNF enforcement powers for MiCA market abuse are unclear.

### Gaps
- No ESMA/national enforcement action against memecoin pump-and-dumps found. Insider dealing detail (Art. 89) not retrieved. Polish sanctions provisions unknown pending the act.

## 4. US: SEC staff statement on memecoins and pump.fun litigation

### Takeaway
SEC Corp Fin staff (27 Feb 2025) said typical meme coins are not securities, so no registration; but no federal securities-law fraud protection follows and the statement is non-binding. Pump.fun faces a SDNY class action with RICO claims.

### Cited Findings
- Statement dated 27 Feb 2025: most meme coins are not securities, applying Howey; "akin to collectibles"; excludes securities labelled as meme coins to evade registration; participants not protected from deception under federal securities laws — [SEC statement](https://sec.gov/newsroom/speeches-statements/staff-statement-meme-coins); [WilmerHale](https://www.wilmerhale.com/en/sitecore/content/whlaunch/home/research/news-publications/20250313-the-state-of-meme-coin-regulation-sec-staffs-statement-and-other-considerations); [Winston](https://winston.com/en/blogs-and-podcasts/non-fungible-insights-blockchain-decrypted/sec-staff-under-new-administration-issues-statement-declaring-that-meme-coins-are-not-securities)
- Statement is not a rule; Commissioner Crenshaw dissented; CFTC status open (likely commodities) — [Crenshaw response](https://www.sec.gov/newsroom/speeches-statements/crenshaw-response-staff-statement-meme-coins-022725); [Harvard CorpGov](https://corpgov.law.harvard.edu/2025/03/19/implications-of-the-secs-stance-that-meme-coins-are-not-securities/)
- Pump.fun: consolidated SDNY class action (Wolf Popper/Burwick) alleges illegal gambling enterprise, unlicensed money transmission, RICO; Solana Labs/Foundation and executives named in amended complaint — [Decrypt](https://decrypt.co/331528/solana-pump-fun-amended-rico-suit-alleging-meme-coin-gambling); [The Block](https://www.theblock.co/news/regulation/2025-07-23-burwick-law-names-solana-and-jito-executives-in-expanded-rico-case-against-pump-363996)
- Reported ruling (Aug 2026, Judge McMahon): claims against Solana Labs/Foundation and five executives dismissed; RICO counts against Pump.fun/Baton survive (reports differ on scope, possibly limited to two named plaintiffs); court found the tokens at issue not securities on those facts — [Solana Compass](https://solanacompass.com/news/federal-judge-clears-solana-labs-and-foundation-from-burwick-laws-class-action-lawsuit); [OurCryptoTalk](https://ourcryptotalk.com/news/judge-clears-solana-pump-fun-lawsuit-rico-survives)

### Inferences
- Traders are not defendants in the cited cases; main US exposure for a Polish individual is manipulation/fraud (wire fraud, CEA anti-manipulation) if participating in coordinated schemes, and US-person/venue restrictions. Unsourced.

### Gaps
- Exact ruling text and date unverified (secondary crypto-press only); docket reportedly 1:25-cv-00880 SDNY. Other US enforcement (DOJ/CFTC memecoin cases), US tax: not searched.

## 5. AML / sanctions risk of tainted funds

### Takeaway
Poland can freeze accounts/crypto tied to suspected crime; receiving tainted funds (e.g. from rug-pull proceeds or sanctioned addresses) risks account blocking and criminal/AML exposure. Sanctions-specific (OFAC/EU) material was not found.

### Cited Findings
- Polish AML Act: GIIF can request a bank hold for up to 96 hours; prosecutor may extend 6 months plus a further 6; banks can also freeze under Banking Law — [Mondaq/Dudkowiak](https://www.mondaq.com/money-laundering/1386358/blocking-bank-account-in-poland)
- Crypto can be secured/blocked by court or prosecutor decision like bank funds — [Dudkowiak](https://www.dudkowiak.com/?p=7827)
- Reported KNF power to block crypto accounts up to 96 hours on suspected criminal activity (criticised as beyond MiCA) — [BeInCrypto](https://beincrypto.com/?p=480308); [Cryptorank](https://cryptorank.io/news/feed/33cd1-polands-regulator-gets-authority-to-block-crypto-access-ahead-of-mica-bill.htm)

### Inferences
- Memecoin flows (anonymous counterparties, mixers, rug-pull wallets) raise the chance that cash-out to a Polish bank triggers bank AML review; keep source-of-funds documentation and trade logs.

### Gaps
- OFAC/EU sanctions on addresses (e.g. Tornado Cash status), analytics tools, EU AMLR/Travel Rule specifics, strict-liability/knowledge standard for receiving tainted crypto in Polish law (art. 299 KK): not found in searches.
