# Storage sizing for Solana memecoin bot. ALL inputs are ASSUMPTIONS (labelled).
scen = {  # trades/day (swap events on DEXs)
 "A_watchlist (bot-tracked tokens only)": 2_000_000,
 "B_memecoin_all (pump.fun+PumpSwap+Raydium+Meteora memes)": 30_000_000,
 "C_full_firehose (all Solana DEX swaps)": 80_000_000,
}
# raw bytes/row (uncompressed logical) and ClickHouse compressed bytes/row (assumed ratio)
trade_raw = 8+8+64+32+32+32+32+8+8+8+8+8+4+2+8  # ts,slot,sig,pool,mint,wallet,...
print("trade raw bytes/row ~", trade_raw)
ch_ratio = {"conservative(4x)":4,"typical(8x)":8,"optimistic(12x)":12}
ts_ratio = {"timescale_compressed(6x)":6,"timescale_uncompressed_pg(1x, +idx 1.6x)":1/1.6}
print()
for n,t in scen.items():
    raw = t*trade_raw/1e9
    print(f"{n}: {t/86400:.0f} avg trades/s, peak(x10) {t/86400*10:.0f}/s, raw {raw:.1f} GB/day")
    for k,r in ch_ratio.items():
        print(f"   CH {k}: {raw/r:.2f} GB/day -> {raw/r*30:.1f} GB/mo, {raw/r*365/1000:.2f} TB/yr")
    pg = raw*1.6  # heap+indexes+tuple overhead ~ (24B header) assumption
    print(f"   Plain PG/Timescale uncompressed (idx+hdr x1.6 assumed): {pg:.1f} GB/day -> {pg*30/1000:.2f} TB/mo")
    print(f"   Timescale compressed (6x of raw): {raw/6:.2f} GB/day")
print()
# other tables, per day
other = {
 "pool_snapshots/OHLCV 1s on watchlist 2000 tokens active 6h": 2000*6*3600*56/1e9/8, # 1s bars, 56B, ~1/8 sparse
 "ohlcv_1m all active tokens 20k*1440 *64B": 20000*1440*64/1e9,
 "new_tokens 40k/day *400B": 40000*400/1e9,
 "wallet_funding_edges 300k/day *150B": 300000*150/1e9,
 "features (1s, 500 tokens, 60 feats f32 = 260B)": 500*86400*260/1e9,
 "features (1s, 500 tok) compressed 5x": 500*86400*260/1e9/5,
 "orders 5k/day *300B": 5000*300/1e9,
 "fills 4k/day *250B": 4000*250/1e9,
 "pnl_ledger/tax_log 4k/day*300B": 4000*300/1e9,
 "raw gRPC firehose archive (zstd Parquet of tx logs) scen B ~600B/tx raw, 6x": 30e6*600/1e9/6,
}
for k,v in other.items(): print(f"{k}: {v:.3f} GB/day")
print()
# Cost: block storage $0.08-0.10/GB-mo (assumed gp3 ~0.08), S3 $0.023
for n,t in scen.items():
    raw=t*trade_raw/1e9; ch=raw/8
    yr=ch*365
    print(f"{n}: 1yr CH@8x = {yr:.0f} GB -> EBS ${yr*0.08:.0f}/mo, S3 ${yr*0.023:.0f}/mo; PG uncompressed 1yr {raw*1.6*365/1000:.1f} TB -> ${raw*1.6*365*0.08:.0f}/mo")
# Redis hot set: 500 tokens * (60 features*8B + 2KB state) + 20 wallets/token ...
hot = 500*(60*8+2048) + 50_000*512
print("Redis hot set bytes ~", hot/1e6, "MB")
# Ingest: rows/s to CH with 1s async-insert batches
for n,t in scen.items(): print(n, "peak rows/s (10x avg, assumed burst):", int(t/86400*10), "| 1 insert/s of", int(t/86400*10), "rows")
