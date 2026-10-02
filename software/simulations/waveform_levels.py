#!/usr/bin/env python3
"""Recompute digital waveform levels using a supplied benchmark reference model.

Requires Python 3 and NumPy. Supply a separate benchmark checkout with
--benchmark. Planning reference revision is 354ff2d; no firmware/model is vendored.
This reads the benchmark and writes only the optional --output file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

sys.dont_write_bytecode = True

import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--benchmark", type=Path,
        required=True, help="Path to RP2350_IQ_Benchmark checkout (planning revision 354ff2d)",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    reference_model = args.benchmark.resolve() / "reference" / "iqlut.py"
    sys.path.insert(0, str(reference_model.parent))
    from iqlut import FULL_SCALE, Lut, lut_axis, unpack_bits, xorshift32

    symbols = 524288
    seed = 0xDEADBEEF
    ib, qb = unpack_bits(xorshift32(seed, symbols // 16))
    rows = []
    for sps, span in ((4, 12), (8, 8), (8, 10)):
        lut = Lut(alpha=0.2, sps=sps, L=span, kaiser_beta=1.0, headroom_db=1.0)
        table = lut.table.astype(np.float64)
        ensemble_mean = 2.0 * np.mean(table ** 2)
        # I and Q can independently select any history, at the same sample phase.
        phase_max = np.max(np.abs(table), axis=0)
        exact_peak = np.max(2.0 * phase_max ** 2)
        i = lut_axis(ib, lut).astype(np.float64)[span * sps:]
        q = lut_axis(qb, lut).astype(np.float64)[span * sps:]
        power = i ** 2 + q ** 2
        sample_mean = np.mean(power)
        rows.append({
            "samples_per_symbol": sps,
            "L": span,
            "kaiser_beta": 1.0,
            "headroom_db": 1.0,
            "random_seed_hex": "0xDEADBEEF",
            "random_symbols": symbols,
            "mean_db_relative_full_scale_complex_CW": float(10 * np.log10(ensemble_mean / FULL_SCALE ** 2)),
            "sampled_papr_1e_4_db": float(10 * np.log10(np.quantile(power, 0.9999) / sample_mean)),
            "sampled_max_papr_db": float(10 * np.log10(np.max(power) / sample_mean)),
            "exact_digital_sample_peak_re_exhaustive_mean_db": float(10 * np.log10(exact_peak / ensemble_mean)),
            "max_axis_code": int(np.max(np.abs(table))),
        })
    result = {
        "domain": "digital LUT samples before analog reconstruction; not RF measurement",
        "profiles": rows,
        "normalization": "A full-scale rotating complex CW has I=FS*cos(theta), Q=FS*sin(theta), hence total power FS^2. QPSK ensemble mean is 2*mean(axis^2). PAPR divides sample power by its sample mean; exact bound divides max sample power by exhaustive mean.",
        "reference": "RP2350_IQ_Benchmark/reference/iqlut.py",
        "planning_baseline_revision": "354ff2ddb0f83c0b7dc1d302e056a93b191298ec",
        "reference_model_sha256": hashlib.sha256(reference_model.read_bytes()).hexdigest(),
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
    }
    encoded = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
