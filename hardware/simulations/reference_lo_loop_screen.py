#!/usr/bin/env python3
"""Ideal analog-loop screening, not a TI model, register export or qualification.

Topology: CPout and Vtune joined; C4 to ground in parallel with C2--R2 to
ground. Optional EVM R3/R4 links are zero and C1/C3 are absent. A real design
must include actual capacitor/charge-pump/VCO variation and PLLatinum Sim.

EVM passives and 6 GHz/100 MHz-PFD/66 MHz-VCO-gain nominal case: TI SNAU217B,
section 3.1.1, Table 1; topology in section 4.
https://www.ti.com/lit/ug/snau217b/snau217b.pdf
VCO4 gain interpolation: TI SNAS740B, section 8.1.3, Table 135, Equation 4.
https://www.ti.com/lit/ds/symlink/lmx2572.pdf
All other passives and 10/20 MHz-PFD operating points are planning candidates.
"""
import cmath
import json
import math


def screen(c2, c4, r2, icp, kvco_hz_per_v, n):
    def gain(frequency_hz):
        s = 2j * math.pi * frequency_hz
        impedance = (1 + s * r2 * c2) / (s * (c2 + c4 + s * r2 * c2 * c4))
        # CP gain Icp/(2*pi) A/rad times VCO 2*pi*Kvco rad/s/V,
        # integrating phase by 1/s and dividing feedback by N.
        return icp * kvco_hz_per_v / n * impedance / s

    low, high = 100.0, 1e6
    for _ in range(100):
        mid = math.sqrt(low * high)
        if abs(gain(mid)) > 1:
            low = mid
        else:
            high = mid
    crossover_hz = math.sqrt(low * high)
    return {
        "unity_crossover_hz": crossover_hz,
        "ideal_phase_margin_deg": 180 + math.degrees(cmath.phase(gain(crossover_hz))),
        "C2_F": c2, "C4_F": c4, "R2_ohm": r2, "Icp_A": icp,
        "Kvco_Hz_per_V": kvco_hz_per_v, "N": n,
    }


cases = [
    ("TI EVM nominal", 6e9, 100e6, 66e6),
    ("IREC 1280 MHz", 5.120e9, 20e6, 50e6 + (73e6 - 50e6) * (5.120 - 4.650) / (5.200 - 4.650)),
    ("S band 2400 MHz", 4.800e9, 20e6, 50e6 + (73e6 - 50e6) * (4.800 - 4.650) / (5.200 - 4.650)),
    ("S band 2405 MHz", 4.810e9, 10e6, 50e6 + (73e6 - 50e6) * (4.810 - 4.650) / (5.200 - 4.650)),
]
results = {
    "status": "Analytical screening only; does not include LMX nonidealities or validate a BOM",
    "model": "G(s) = Icp*Kvco/N * (1+s*R2*C2)/(s^2*(C2+C4+s*R2*C2*C4))",
    "sources": {
        "evm_nominal": "https://www.ti.com/lit/ug/snau217b/snau217b.pdf; section 3.1.1 Table 1",
        "vco_gain_interpolation": "https://www.ti.com/lit/ds/symlink/lmx2572.pdf; section 8.1.3 Table 135 Equation 4",
    },
    "EVM_network_reused_at_2p5mA": {},
    "candidate_for_TI_simulation_not_validated": {},
}
for name, fvco, fpfd, kvco in cases:
    results["EVM_network_reused_at_2p5mA"][name] = screen(15e-9, 2.2e-9, 330, .0025, kvco, fvco/fpfd)
    if name != "TI EVM nominal":
        icp = .006875 if fpfd == 10e6 else .005
        results["candidate_for_TI_simulation_not_validated"][name] = screen(22e-9, 2.2e-9, 430, icp, kvco, fvco/fpfd)
print(json.dumps(results, indent=2))
