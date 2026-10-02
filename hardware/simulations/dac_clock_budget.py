#!/usr/bin/env python3
"""Nominal PIO timing and clock-drift arithmetic; no SI/jitter qualification.

AFE7071 SLOS789C p.5: dual-input setup/hold >=1 ns, CLK_IO high >=3 ns.
Pages 25-26: equal-frequency CLK_IO/DACCLK, initial FIFO phase arbitrary,
subsequent movement up to +/-4 clock cycles. https://www.ti.com/lit/gpn/AFE7071
PIO launch convention: RP2350_IQ_Benchmark firmware/src/iqout.c at
904564589de68b2c8af1d67e5f8ad92a7fd48a27, build_programs().
https://github.com/Rivercraft911/RP2350_IQ_Benchmark

128 MHz SYS and cpw 2/4/8 are adopted planning settings. The 3 ns observed
setup/hold target is an engineering target, not a manufacturer requirement.
No package skew, pad delay, edge shape, probe error or RF noise is modeled.
"""
import argparse
import json
import math


def finite_nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be finite and nonnegative")
    return number


def budget(sys_hz, cpw, differential_ppm):
    tick_ns = 1e9 / sys_hz
    setup_ns = (cpw // 2) * tick_ns
    hold_ns = (cpw - cpw // 2) * tick_ns
    clock_hz = sys_hz / cpw
    # Extra/missing clock count grows at |f1-f2|. Four cycles is the
    # datasheet's phase-excursion scale, not a permitted stall or alarm delay.
    four_cycle_drift_s = (
        4 / (clock_hz * differential_ppm * 1e-6)
        if differential_ppm else None
    )
    return {
        "cpw": cpw,
        "CLK_IO_and_DACCLK_Hz": clock_hz,
        "sample_rate_per_IQ_channel_Hz": clock_hz / 2,
        "continuous_clock_PIO_integer_divider": cpw / 2,
        "nominal_setup_ns": setup_ns,
        "nominal_hold_and_CLK_IO_high_ns": hold_ns,
        "max_setup_loss_to_1ns_requirement_ns": setup_ns - 1,
        "max_hold_loss_to_1ns_requirement_ns": hold_ns - 1,
        "max_high_pulse_loss_to_3ns_requirement_ns": hold_ns - 3,
        "max_setup_loss_to_3ns_engineering_target_ns": setup_ns - 3,
        "max_hold_loss_to_3ns_engineering_target_ns": hold_ns - 3,
        "four_clock_cycles_ns": 4e9 / clock_hz,
        "four_cycle_drift_s_at_input_differential_ppm": four_cycle_drift_s,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--differential-ppm", type=finite_nonnegative, default=10,
                        help="relative frequency error of two clocks (default: 10 ppm)")
    args = parser.parse_args()
    print(json.dumps({
        "status": "Nominal analytical budget; receiver timing and RF performance unverified",
        "SYS_Hz": 128_000_000,
        "differential_ppm_scenario": args.differential_ppm,
        "zero_ppm_drift_result": "null means no deterministic drift in this ideal model",
        "sources": ["https://www.ti.com/lit/gpn/AFE7071",
                    "https://github.com/Rivercraft911/RP2350_IQ_Benchmark"],
        "profiles": {name: budget(128_000_000, cpw, args.differential_ppm)
                     for name, cpw in [("IREC", 2), ("video_candidate", 4),
                                      ("initial_satellite", 8)]},
    }, indent=2))


if __name__ == "__main__":
    main()
