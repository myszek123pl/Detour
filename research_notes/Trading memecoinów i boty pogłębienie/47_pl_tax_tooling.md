# PL tax bookkeeping for a memecoin bot trader (tooling, NBP valuation, DAC8, bot logs)

Not tax advice. Written 2026-11-20. Web search budget was cut short (search tool rate-limited after 2 of 3 calls in a batch); the DAC8-Poland query returned nothing. Items marked [UNVERIFIED] come from background knowledge, not from fetched sources.

## 1. Which tax software supports Poland / PIT-38, and does it cope with thousands of on-chain swaps?

### Takeaway
Koinly, Divly and CoinTracking are the commonly named options, but I could not verify any vendor's Polish-specific method (NBP rates, treatment of crypto-to-crypto swaps) or its performance at thousands of DEX transactions. Test any tool on a sample before relying on it.

### Cited Findings
- Koinly's Poland guide says it calculates cost basis and proceeds and generates reports for filing; a search summary found no confirmation that Koinly applies NBP rates specifically — [Koinly Poland guide](https://koinly.io/fi/guides/crypto-tax-poland/)
- Freenance describes Koinly as a popular tool with Polish regulation support (commercial, secondary source) — [Freenance guide](https://freenance.io/crypto/crypto-tax-guide-poland/)
- Divly has a Polish-language guide on settling crypto trading in Poland (content not read in detail) — [Divly PL](https://divly.com/pl/przewodniki/jak-rozliczyc-handel-kryptowalutami-w-polsce)
- Poland does not use FIFO; guides describe an aggregate-cost approach (costs deducted in the year, not per-lot matching) — [Dudkowiak](https://www.dudkowiak.com/blog/crypto-tax-in-poland-2025-guide/), [Kraken guide](https://www.kraken.com/learn/poland-crypto-tax-guide)

### Inferences
- Because Polish PIT-38 works on aggregate revenue vs. aggregate costs for the year, a foreign tool's FIFO/lot output is not directly the PIT-38 figure; use it for per-transaction PLN valuation, then total revenue and costs yourself or with an accountant.
- Solana memecoin bot volume (thousands of swaps, many obscure tokens with no price feed) is a known weak spot for all aggregators. Expect missing-price and unmatched-transfer errors [UNVERIFIED, general experience].
- CoinTracking and local tools (names I could not verify in this session): no sourced details.

### Gaps
- No verified feature comparison (pricing tiers by transaction count, PIT-38 export, NBP support, Solana/DEX import quality) for Koinly, CoinTracking, Divly or Polish local tools.
- No source on whether any tool outputs PIT-38/PIT-38 crypto-section figures directly.

## 2. Valuation in PLN (NBP rules) and what is actually taxable

### Takeaway
Foreign-currency amounts are converted at the NBP average rate from the last business day before the date revenue arises or the cost is incurred (art. 11a PIT). A conflict exists on whether crypto-to-crypto swaps are taxable events; the current statute, as I recall, says they are not.

### Cited Findings
- Official e-PIT portal: foreign-currency amounts convert at the NBP average rate from the last business day preceding the day revenue was earned — [podatki.gov.pl](https://www.podatki.gov.pl/en/your-e-pit/pit-38-for-2023)
- Guides state the same for revenue and costs (art. 11a PIT), so a weekend trade uses Friday's rate — [Cryptoticker](https://cryptoticker.io/pl/podatek-od-kryptowalut/), [Freenance](https://freenance.io/kryptowaluty/kryptowaluty-podatek-pit-2026/); Podatnik.info words it more loosely ("day preceding") — [Podatnik.info](https://www.podatnik.info/publikacje/podatek-od-kryptowalut,60264f)
- Flat 19% on PIT-38; filing window 15 Feb - 30 Apr; PIT-38 for 2025 due 30 Apr 2026 — [podatki.gov.pl](https://podatki.gov.pl/pit/rozliczenie-ze-sprzedazy-kryptowalut/), [Bankier](https://www.bankier.pl/wiadomosc/Podatek-od-kryptowalut-w-2025-Oto-co-powinien-wiedziec-inwestor-9048156.html)
- CONFLICT: a search summary of commercial guides (Freenance, Divly, Cryptoticker) says crypto-to-crypto swaps are treated as taxable disposals and converted at NBP D-1; one guide notes there is no settled KAS interpretive line for DeFi — [Freenance DeFi](https://freenance.io/kryptowaluty/defi-yield-farming-podatek-pl-2026-pool-likwidnosci-staking-procent-jak-rozliczyc-pit). Interpretation numbers quoted there (e.g. 0114-KDIP3-1.4011.612.2024) were not verified.

### Inferences
- My recollection [UNVERIFIED]: under art. 17 ust. 1f/1g and art. 30b ust. 1a PIT, exchange of one virtual currency for another is not a taxable disposal; tax arises on exchange to fiat, goods, or services. Under that reading, memecoin -> SOL/USDC swaps create no revenue, and only the cash-out to PLN/fiat counts. This directly contradicts the guides above and must be checked against the statute and the current wording (including any 2025-2026 amendments for crypto-asset/MiCA alignment) with an adviser.
- Under the same recollection, costs (purchase price, fees) are recognised in the year the revenue arises, and an excess of costs may be carried forward rather than offset like normal losses [UNVERIFIED].
- Practically: log every swap with a timestamp and NBP D-1 PLN value of each leg regardless, so either interpretation can be computed.

### Gaps
- Primary-source check of art. 17 ust. 1f, art. 22 ust. 14-16, art. 30b, and recent KIS/NSA rulings on DEX swaps, gas fees, and failed transactions was not done.
- Whether gas/priority fees and Jito tips are deductible costs (and when): no source found.
- NBP rate source for non-PLN crypto-quoted pairs (USDC, SOL): NBP publishes fiat only; crypto must be valued via USD/EUR price then NBP rate. No source found for an accepted price-source method.

## 3. DAC8 reporting from 2026

### Takeaway
DAC8 (Directive (EU) 2023/2226) obliges crypto-asset service providers to report user data from 1 Jan 2026, with first exchanges in 2027 [UNVERIFIED, my knowledge]; I could not confirm Poland's transposition status.

### Cited Findings
- None. The search for Polish DAC8 implementation failed (rate limit).

### Inferences
- A bot trader using self-custody wallets and DEXs is mostly outside provider reporting, but any CEX/fiat on-ramp or off-ramp account will report holdings and transactions to the tax authority, so the cash-out leg will be visible; declared PIT-38 should reconcile with it.
- Tax authorities can request on-chain wallet data directly; wallet addresses used should be consistent in records.

### Gaps
- Polish transposition law, effective date, scope of reported data, and whether DEX front-ends/self-hosted wallets are in scope: unverified. Check Ministry of Finance / Sejm legislative tracker.

## 4. Record-keeping the bot should log

### Takeaway
No official Polish list of required crypto records was found; guides advise keeping proof of purchase price, fees and dates for each transaction. The list below is my practical design, not a legal requirement.

### Cited Findings
- Guides say costs and commissions of purchase count as deductible costs and must be documented; one law firm checklist points to historical NBP table rates from transaction dates — [Dudkowiak](https://www.dudkowiak.com/blog/crypto-tax-in-poland-2025-guide/), [Podatnik.info](https://www.podatnik.info/publikacje/podatek-od-kryptowalut,60264f)

### Inferences
Suggested per-trade log (own design [UNVERIFIED as to legal sufficiency]):
- Tx signature/hash, chain, block time (UTC), wallet address, DEX/program, bot strategy/run ID.
- Token mint/contract, symbol, amounts in and out (raw and decimal), fees: network fee, priority fee/tip, DEX/platform fee, bot-service fee, in native units.
- Price source and USD (or SOL/USDC) price of each leg at execution; NBP table number/date and rate used (D-1), resulting PLN value.
- Failed transactions (fee still paid), rug/zero-value positions, airdrops, transfers between own wallets (flag as non-taxable), funding/withdrawal legs with CEX reference IDs and bank statements.
- Immutable export: append-only daily CSV/Parquet plus monthly backups; keep records at least as long as the limitation period (5 years from end of the year the tax is due) [UNVERIFIED, general Polish rule]; separate non-bot costs (infra, RPC, bot subscriptions) with invoices.

### Gaps
- Whether bot infrastructure costs (servers, RPC, subscriptions) can be costs of the crypto source of income on PIT-38, versus being a business activity (possible PIT-36/PIT-36L and ZUS implications at high frequency): not researched.
