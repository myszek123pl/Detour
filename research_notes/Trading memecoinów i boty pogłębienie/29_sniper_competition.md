# Solana launch-sniping competition 2025-2026 (as of Nov 2026)

Note: only 2 of ~6 searches succeeded (third rate-limited, one fetch blocked by network). Figures are from search summaries, not full-page reads; treat as unverified unless stated.

## How common is block-0/early sniping, and how many snipers per launch?

### Takeaway
Same-block sniping on pump.fun is widespread (Pine Analytics: >50% of tokens sniped in creation block, subset of behaviour). I found no reliable per-launch sniper count.

### Cited Findings
- Pine Analytics report: over 50% of tokens were sniped in the creation block; report covers only a subset of same-block behaviour (unverified, via search summary; page not fetched) — [Pine Analytics](https://pineanalytics.substack.com/p/exit-liquidity-machines)
- Same research tracked SOL transfers deployer->sniper; developer-funded sniper manipulation reported at up to 1.75% of launches (different metric from the 50%) — [BeInCrypto](https://beincrypto.com/pump-fun-meme-coin-snipers-systematic-problem)
- Bitquery-based study: first-block outside buying fell 42%->32% as slots shortened, but buying within ~1.3 s stayed ~flat (53% vs 52%); sample ends before final slot-time reduction — [CryptoSlate](https://cryptoslate.com/solana-study-finds-rapid-pump-fun-buying-persisted-as-blocks-sped-up/)

### Inferences
- Speed competition is saturated at the very top of the block; faster slots shift buyers but do not remove them.

### Gaps
- Average number of snipers per launch: not found.
- Date range/sample size of the Pine study not verified.

## Profitability of block-0/early snipers

### Takeaway
Claims exist of high sniper win rates, but unverified and likely concentrated in dev-linked wallets.

### Cited Findings
- A secondary outlet claims 87% sniper profitability and 85% liquidated within 5 minutes for the analysed wallets; could not verify against primary report (UNVERIFIED) — [BeInCrypto](https://beincrypto.com/pump-fun-meme-coin-snipers-systematic-problem)
- Vendor guides say profit is never guaranteed; marketing, not evidence — [QuickNode](https://www.quicknode.com/builders-guide/best/top-8-pump-fun-sniper-bots)

### Inferences
- Reported profits likely reflect insider/dev-funded sniping, which a newcomer cannot replicate; organic sniper profitability is unknown.

### Gaps
- No independent data on net profitability after tips/fees/failed txs for non-insider snipers.

## Anti-sniper mechanisms (pump.fun, dynamic fees, Meteora)

### Takeaway
Meteora has a documented anti-sniper suite; pump.fun changes could not be verified (search failed).

### Cited Findings
- Meteora suite: Dynamic Fees (default on for all DLMM Launch Pools; optional on DAMM v2), Fee Scheduler (DAMM v1/v2, also DBC), Alpha Vault (early access for supporters) — [Meteora docs](https://docs.meteora.ag/meteoras-anti-sniper-suite-a.s.s./meteoras-anti-sniper-suite)
- Fee scheduler decays linearly or exponentially; DAMM v2 frontend default: exponential, 50% at start, decaying per second over 120 min to 0.25% — [Meteora fee scheduler](https://docs.meteora.ag/meteoras-anti-sniper-suite-a.s.s./meteoras-anti-sniper-suite/fee-scheduler)
- Newer Fee Market Cap Scheduler (fee falls as market cap grows) for graduated DAMM v2 pools; mutually exclusive with Fee Time Scheduler and Rate Limiter — [Meteora docs](https://docs.meteora.ag/anti-sniper-suite/fee-market-cap-scheduler/what-is-fee-market-cap-scheduler.md)
- Alpha Vault doc note that DAMM v2 support is "soon" may be outdated.

### Inferences
- A 50% starting fee makes block-0 buying on fee-scheduled Meteora pools uneconomic unless price moves >fee; snipers shift to pump.fun bonding curves with no such fee.

### Gaps
- pump.fun anti-sniper/dynamic-fee/creator-fee changes in 2025-2026: NOT verified (search rate-limited). Training-knowledge only: PumpSwap AMM launched 2025, creator fee sharing added; unconfirmed for 2026.
- Other launchpads (Bonk/LetsBonk, Jupiter Studio, DBC) anti-snipe features not researched.

## Can a newcomer compete?

### Takeaway
Evidence suggests no at block 0 (infrastructure arms race, insider/dev-funded wallets); slower early-but-not-first entries remain open but unquantified.

### Cited Findings
- Buying within ~1.3 s of launch ~52-53% of buyers, so a human/retail-grade bot is competing with many fast actors — [CryptoSlate](https://cryptoslate.com/solana-study-finds-rapid-pump-fun-buying-persisted-as-blocks-sped-up/)
- Vendors position RPC speed as the key tool (marketing) — [QuickNode](https://www.quicknode.com/builders-guide/best/top-8-pump-fun-sniper-bots)

### Inferences
- Newcomer lacks edge in latency (Jito/validator-colocated, private RPC) and in insider info; any edge must come from filtering/selection rather than speed.

### Gaps
- No data on newcomer success rates, costs (tips, RPC) or break-even.
