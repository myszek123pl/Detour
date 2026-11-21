"""Audit the frozen RED-PUMP v1.6 deposit, without executing its code or pickle.

python audit_counts.py --archive RED-PUMP-2026-v1_v1.6_reproducibility.zip --output audit.json
Requires numpy and pyarrow. These are label/coverage counts, NOT platform success rates.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

PREFIX = "RED-PUMP-2026-v1_v1.6/"
EXPECTED_MD5 = "c9c056392d91646bc6af8e2a2794d2eb"
LABELS = {"GRADUATED": 1, "TIMEOUT": 2}


def digest(stream, algo="sha256"):
    h = hashlib.new(algo)
    while chunk := stream.read(8 * 1024 * 1024):
        h.update(chunk)
    return h.hexdigest()


def utc(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).isoformat()


def auc(y, p):
    """Mann-Whitney AUROC, averaging exact ties; no sklearn needed."""
    order = np.argsort(p, kind="stable")
    scores, ys = p[order], y[order]
    starts = np.r_[0, np.flatnonzero(scores[1:] != scores[:-1]) + 1]
    ends = np.r_[starts[1:], len(scores)]
    positives = np.add.reduceat(ys, starts)
    average_rank = (starts + 1 + ends) / 2
    npos = float(y.sum())
    nneg = len(y) - npos
    if not npos or not nneg:
        return None
    return float((np.dot(positives, average_rank) - npos * (npos + 1) / 2) / (npos * nneg))


def read_table(z, rel, columns):
    return pq.read_table(pa.BufferReader(z.read(PREFIX + rel)), columns=columns).to_pandas()


def audit(archive):
    with archive.open("rb") as f:
        md5 = digest(f, "md5")
    if md5 != EXPECTED_MD5:
        raise ValueError(f"Unexpected deposit MD5: {md5}; expected {EXPECTED_MD5}")
    result = {
        "source": "https://zenodo.org/records/23018519",
        "version": "v1.6",
        "interpretation": "collector-generated terminal labels; neither platform graduation nor survival probabilities",
        "archive": {"bytes": archive.stat().st_size, "md5": md5},
    }
    with ZipFile(archive) as z:
        checks = []
        for line in z.read(PREFIX + "SHA256SUMS").decode().splitlines():
            expected, rel = line.split(maxsplit=1)
            rel = rel.strip().lstrip("*")
            with z.open(PREFIX + rel) as f:
                actual = digest(f)
            if actual != expected:
                raise ValueError(f"SHA256 mismatch: {rel}")
            checks.append(rel)
        result["internal_sha256"] = {"verified_files": len(checks), "failures": 0}
        print("Archive and internal SHA256 verified", flush=True)

        launch_mints = set()
        launch_keys = set()
        nlaunch = 0
        first = float("inf")
        last = float("-inf")
        launch_days = Counter()
        with gzip.open(z.open(PREFIX + "04_frozen_inputs/red_pump_2026_v1_launches.jsonl.gz"), "rt", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                nlaunch += 1
                launch_keys.update(row)
                launch_mints.add(row["mint"])
                t = row["t"]
                first, last = min(first, t), max(last, t)
                launch_days[utc(t)[:10]] += 1
        result["raw_launches"] = {
            "rows": nlaunch, "unique_mints": len(launch_mints),
            "duplicate_rows_beyond_first_mint": nlaunch - len(launch_mints),
            "first_seen": utc(first), "last_seen": utc(last),
            "columns": sorted(launch_keys), "rows_by_day_utc": dict(sorted(launch_days.items())),
        }

        # The deposit has legacy 8-column and new 11-column physical rows,
        # including unescaped commas inside symbols. Locate the enum field;
        # never shift a malformed row into a different semantic column silently.
        categories, outcome_rows = Counter(), Counter()
        outcome_mints = {}
        physical_rows = 0
        valid_rows = 0
        with gzip.open(z.open(PREFIX + "04_frozen_inputs/red_pump_2026_v1_outcomes.csv.gz"), "rt", encoding="utf-8-sig") as f:
            header = next(f).rstrip("\r\n").split(",")
            for line in f:
                physical_rows += 1
                fields = line.rstrip("\r\n").split(",")
                if not line.strip():
                    categories["blank_physical_line"] += 1
                    continue
                positions = [i for i, v in enumerate(fields) if v in LABELS and i >= 3]
                if len(positions) != 1:
                    categories[f"excluded_{len(fields)}fields_no_unique_label"] += 1
                    continue
                pos = positions[0]
                # After the outcome enum come 4 fields (legacy), or 7 (new).
                tail = len(fields) - pos - 1
                if tail not in (4, 7):
                    categories[f"excluded_{len(fields)}fields_wrong_tail"] += 1
                    continue
                schema = "V1_8field" if tail == 4 else "V2_11field"
                if pos > 3:
                    schema += "_comma_in_symbol"
                categories[schema] += 1
                valid_rows += 1
                label = fields[pos]
                mint = fields[1]
                outcome_rows[label] += 1
                outcome_mints[mint] = outcome_mints.get(mint, 0) | LABELS[label]
        unique_labels = Counter()
        for mask in outcome_mints.values():
            unique_labels["CONFLICT" if mask == 3 else "GRADUATED" if mask == 1 else "TIMEOUT"] += 1
        result["raw_outcomes"] = {
            "physical_data_lines": physical_rows, "valid_rows": valid_rows,
            "categories": dict(categories), "label_rows": dict(outcome_rows),
            "unique_mints": len(outcome_mints), "unique_mint_labels": dict(unique_labels),
            "duplicate_rows_beyond_first_mint": valid_rows - len(outcome_mints),
            "columns_in_header": header,
            "launch_mints_with_no_valid_terminal": len(launch_mints - outcome_mints.keys()),
            "terminal_mints_not_in_launches": len(outcome_mints.keys() - launch_mints),
        }
        # Separate sensitivity: unescaped line breaks in symbols split one
        # logical CSV record into a dated mint prefix and a label continuation.
        # Only join adjacent fragments when the prefix mint exists in launches,
        # the continuation enum is unambiguous, and the numeric tail has the
        # documented legacy/new width. Never describe the strict pass above as
        # a complete outcome census without this qualification.
        logical_mints, logical_rows = {}, Counter()
        recovered = Counter()
        pending = None
        with gzip.open(z.open(PREFIX + "04_frozen_inputs/red_pump_2026_v1_outcomes.csv.gz"), "rt", encoding="utf-8-sig") as f:
            next(f)
            for line in f:
                if not line.strip():
                    continue
                fields = line.rstrip("\r\n").split(",")
                if len(fields) == 3 and fields[1] in launch_mints and fields[0].startswith("2026-"):
                    pending = fields
                    continue
                positions = [i for i, v in enumerate(fields) if v in LABELS and (i == 1 or i >= 3)]
                if len(positions) != 1:
                    pending = None
                    continue
                pos = positions[0]
                tail = len(fields) - pos - 1
                if pos == 1 and pending is not None and tail in (4, 7):
                    mint = pending[1]
                    recovered["legacy" if tail == 4 else "new"] += 1
                elif pos >= 3 and tail in (4, 7) and fields[1] in launch_mints:
                    mint = fields[1]
                else:
                    pending = None
                    continue
                label = fields[pos]
                logical_rows[label] += 1
                logical_mints[mint] = logical_mints.get(mint, 0) | LABELS[label]
                pending = None
        logical_labels = Counter("CONFLICT" if v == 3 else "GRADUATED" if v == 1 else "TIMEOUT" for v in logical_mints.values())
        result["raw_outcomes_multiline_recovery_sensitivity"] = {
            "recovered_split_records": dict(recovered), "logical_label_rows": dict(logical_rows),
            "logical_rows": sum(logical_rows.values()), "unique_mints": len(logical_mints),
            "unique_mint_labels": dict(logical_labels),
            "launch_mints_with_no_recovered_terminal": len(launch_mints - logical_mints.keys()),
            "qualification": "Adjacent raw physical fragments joined conservatively; distinct from the author's frozen analytical cohort and not a platform-outcome census",
        }
        print("Raw records counted", flush=True)

        primary = read_table(z, "05_outputs/primary_cohort.parquet", [
            "mint", "t", "outcome", "Y", "dev_set_v2_3", "validation_set_v2_3",
            "observable_minutes", "recon_violation", "graduated_at_ms", "estimated_first_invisible_poll",
        ])
        cohort = {"rows": len(primary), "unique_mints": int(primary.mint.nunique()),
                  "labels": {str(k): int(v) for k, v in primary.outcome.value_counts().items()}}
        cohort["label_fraction"] = float(primary.Y.mean())
        cohort["inferred_observable_minutes_quantiles"] = {
            str(k): float(v) for k, v in primary.observable_minutes.quantile([0, .25, .5, .75, .9, .99, 1]).items()}
        violations = primary[primary.recon_violation]
        cohort["reconstruction_violations"] = len(violations)
        cohort["violation_graduation_recorded_at_first_invisible_poll"] = int(
            (violations.graduated_at_ms == violations.estimated_first_invisible_poll).sum())
        last24 = primary[primary.t >= last - 24 * 3600 * 1000]
        cohort["detected_in_collection_last_24h"] = {
            "threshold": utc(last - 24 * 3600 * 1000), "rows": len(last24),
            "labels": {str(k): int(v) for k, v in last24.outcome.value_counts().items()},
        }
        cohort["splits"] = {}
        for split, flag in [("development", "dev_set_v2_3"), ("validation", "validation_set_v2_3")]:
            s = primary[primary[flag]]
            cohort["splits"][split] = {"rows": len(s), "positive_labels": int(s.Y.sum()),
                                         "label_fraction": float(s.Y.mean())}
        result["deposited_primary_cohort_recount"] = cohort
        result["deposited_prediction_recalculation"] = {}
        for split in ("development", "validation"):
            pred = read_table(z, f"05_outputs/P1_{split}_predictions.parquet", ["mint", "Y", "p"])
            y, p = pred.Y.to_numpy(), pred.p.to_numpy()
            if not np.isfinite(p).all() or not ((0 <= p) & (p <= 1)).all():
                raise ValueError(f"Invalid probability in {split}")
            metric = {"rows": len(y), "positive_labels": int(y.sum()), "AUROC": auc(y, p),
                      "Brier": float(np.mean((p - y) ** 2)), "probabilities_below_1e-8": int((p < 1e-8).sum()),
                      "zero_probabilities": int((p == 0).sum())}
            if split == "validation":
                clean = ~pred.mint.isin(set(last24.mint)).to_numpy()
                metric["exclude_outcome_selected_last24h_sensitivity"] = {
                    "rows": int(clean.sum()), "positive_labels": int(y[clean].sum()),
                    "AUROC": auc(y[clean], p[clean]), "Brier": float(np.mean((p[clean] - y[clean]) ** 2)),
                }
            result["deposited_prediction_recalculation"][split] = metric
        result["not_rebuilt"] = ["model fitting", "500-replicate bootstrap", "true platform graduation ascertainment", "wallet cohorts", "survival curves"]
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.archive)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "primary_cohort": result["deposited_primary_cohort_recount"], "metrics": result["deposited_prediction_recalculation"]}, ensure_ascii=False), flush=True)
