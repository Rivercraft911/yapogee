#!/usr/bin/env python3
"""Planning calculations only; no measured receiver/antenna/PA performance is claimed.

Run: python3 hardware/simulations/link_budget.py
Writes hardware/simulations/output/results.json and tables.md; standard library only.
Every RF power is average wanted-channel power at the connector AFTER the final
PA output filter. Filter loss is not subtracted a second time in the link.

Decoder thresholds: ETSI EN 302 307-1 V1.4.1, section 6, Table 13 (normal
frames, ideal synchronization, AWGN, 50 LDPC iterations). Frame sizes and
overhead: Tables 5a/5b and section 5.5. Receiver/link allocations are assumptions.
https://www.etsi.org/deliver/etsi_en/302300_302399/30230701/01.04.01_60/en_30230701v010401p.pdf
"""
import json
import math
from pathlib import Path

C = 299792458.0
K = 1.380649e-23
EARTH_RADIUS_KM = 6371.0
SERVICE_FACTOR = (184 / 188) * 0.95  # TS header, then provisional extra mux allocation
MODES = {
    "1/2": {"kbch": 32208, "esn0_ideal_db": 1.00},
    "2/3": {"kbch": 43040, "esn0_ideal_db": 3.10},
    "3/4": {"kbch": 48408, "esn0_ideal_db": 4.03},
}
PLFRAME_SYMBOLS = 32400 + 90 + 36 * ((360 - 1) // 16)
for mode in MODES.values():
    mode["datafield_bits"] = mode["kbch"] - 80
    mode["datafield_bits_per_symbol"] = mode["datafield_bits"] / PLFRAME_SYMBOLS
    mode["video_bits_per_symbol"] = mode["datafield_bits_per_symbol"] * SERVICE_FACTOR

def db(value):
    return 10 * math.log10(value)

def fspl_db(distance_km, frequency_hz):
    return 20 * math.log10(4 * math.pi * distance_km * 1000 * frequency_hz / C)

def slant_km(altitude_km, elevation_deg):
    e = math.radians(elevation_deg)
    return math.sqrt((EARTH_RADIUS_KM + altitude_km) ** 2 -
                     (EARTH_RADIUS_KM * math.cos(e)) ** 2) - EARTH_RADIUS_KM * math.sin(e)

def dish_gain_db(diameter_m, frequency_hz, efficiency=0.55):
    return db(efficiency * (math.pi * diameter_m * frequency_hz / C) ** 2)

# At the ground antenna feed plane. The pre-LNA cable's signal attenuation and
# its thermal noise are already represented in Tsys and hence G/T.
GROUND = {"antenna_noise_k": 80, "feeder_loss_db": 0.5,
          "feeder_temperature_k": 290, "lna_nf_db": 0.7,
          "aperture_efficiency": 0.55}
L = 10 ** (GROUND["feeder_loss_db"] / 10)
F = 10 ** (GROUND["lna_nf_db"] / 10)
GROUND["tsys_k"] = GROUND["antenna_noise_k"] + (L - 1) * 290 + L * (F - 1) * 290
SAT_LOSSES = {"flight_feeder_db": 0.7, "flight_radome_db": 0.3,
              "ground_radome_db": 0.2, "polarization_db": 0.5,
              "ground_pointing_db": 0.5}
SAT_ATMOSPHERE = {90: 0.1, 30: 0.2, 10: 0.4}
SAT_IMPLEMENTATION_DB = 2.0
SAT_FADE_RESERVE_DB = 6.0

def satellite(power_w, h_km, elev_deg, dish_m, gain_db, mode_name, rs_hz,
              frequency_hz=2.2e9, tsys_k=None, extra_path_loss_db=0.0):
    slant = slant_km(h_km, elev_deg)
    gain = dish_gain_db(dish_m, frequency_hz)
    tsys_k = GROUND["tsys_k"] if tsys_k is None else tsys_k
    gt = gain - db(tsys_k)
    flight_pointing = 1.0 if gain_db > 0 else 0.0
    losses = sum(SAT_LOSSES.values()) + SAT_ATMOSPHERE[elev_deg] + flight_pointing + extra_path_loss_db
    cn0 = db(power_w) + gain_db - losses - fspl_db(slant, frequency_hz) + gt - db(K)
    ideal = db(rs_hz) + MODES[mode_name]["esn0_ideal_db"]
    nominal = cn0 - ideal
    residual = nominal - SAT_IMPLEMENTATION_DB - SAT_FADE_RESERVE_DB
    return {"power_after_filter_w": power_w, "altitude_km": h_km,
            "elevation_deg": elev_deg, "slant_km": slant, "frequency_hz": frequency_hz,
            "dish_m": dish_m, "dish_gain_dbi": gain, "gt_db_per_k": gt,
            "ground_system_temperature_k": tsys_k, "extra_path_loss_db": extra_path_loss_db,
            "flight_gain_dbi": gain_db, "flight_pointing_loss_db": flight_pointing,
            "other_losses_db": losses - flight_pointing, "mode": mode_name,
            "symbol_rate_hz": rs_hz, "cn0_db_hz": cn0, "ideal_required_cn0_db_hz": ideal,
            "nominal_margin_db": nominal, "implementation_penalty_db": SAT_IMPLEMENTATION_DB,
            "fade_reserve_db": SAT_FADE_RESERVE_DB, "residual_margin_db": residual,
            "minimum_power_after_filter_w": power_w * 10 ** (-residual / 10)}

IREC_LOSSES = {"flight_feeder_db": 0.7, "flight_radome_db": 0.5,
               "ground_feeder_db": 1.0, "ground_preselector_db": 1.0,
               "polarization_db": 0.5, "ground_pointing_db": 1.0}
def irec(power_w, height_ft, horizontal_km, nf_db=8.0,
         flight_gain_db=0.0, ground_gain_db=13.0, implementation_db=2.0):
    h_km = height_ft * 0.3048 / 1000
    slant = math.hypot(h_km, horizontal_km)
    fspl = fspl_db(slant, 1.28e9)
    received = db(power_w) + 30 + flight_gain_db + ground_gain_db - sum(IREC_LOSSES.values()) - fspl
    # SDR threshold at SDR connector, so receiver-side feeder/preselector are
    # signal losses above; NF is the SDR-only figure at this same reference plane.
    threshold_ideal = db(K * 290 * 8e6) + 30 + nf_db + MODES["2/3"]["esn0_ideal_db"]
    nominal = received - threshold_ideal
    residual = nominal - implementation_db - 10.0
    return {"power_after_filter_w": power_w, "height_agl_ft": height_ft,
            "horizontal_offset_km": horizontal_km, "slant_km": slant,
            "fspl_db": fspl, "received_at_sdr_dbm": received,
            "nf_sdr_db": nf_db, "flight_gain_dbi": flight_gain_db,
            "ground_gain_dbi": ground_gain_db, "ideal_threshold_dbm": threshold_ideal,
            "nominal_margin_db": nominal, "implementation_penalty_db": implementation_db,
            "fade_reserve_db": 10.0, "residual_margin_db": residual,
            "minimum_power_after_filter_w": power_w * 10 ** (-residual / 10)}

rates = []
for mode_name, mode in MODES.items():
    for video_mbps in [1, 5, 10]:
        rs = video_mbps * 1e6 / mode["video_bits_per_symbol"]
        rates.append({"mode": mode_name, "video_mbps": video_mbps,
                      "required_symbol_rate_hz": rs, "occupied_bandwidth_hz": 1.2 * rs,
                      "dac_sample_rate_n4_hz": 4 * rs, "bus_word_rate_n4_hz": 8 * rs})
sat_cases = []
for frequency in [2.2e9, 2.4e9]:
    for h in [500, 550]:
        for elev in [90, 30, 10]:
            for dish in [1.2, 1.9, 3.5]:
                for flight_gain in [0, 6]:
                    for power in [0.1, 0.25, 1, 2, 5, 10]:
                        for mode_name in ["1/2", "2/3"]:
                            for video_mbps in [1, 5, 10]:
                                rs = video_mbps * 1e6 / MODES[mode_name]["video_bits_per_symbol"]
                                item = satellite(power, h, elev, dish, flight_gain, mode_name, rs, frequency)
                                item["video_mbps"] = video_mbps
                                sat_cases.append(item)
candidate = [satellite(p, h, e, 1.9, g, "3/4", 4e6)
             for h in [500, 550] for e in [90, 30, 10]
             for g in [0, 6] for p in [0.1, 0.25, 1, 2, 5, 10]]
irec_cases = [irec(p, h, offset, nf) for p in [0.01, 0.02, 0.05, 0.1, 0.25, 0.5]
              for h in [10000, 30000] for offset in [0.1, 5.0] for nf in [3, 5, 8]]
out = {"status": "Analytical planning; adopted assumptions remain unmeasured",
       "generated_from": "link_budget.py, standard library",
       "standard_source": {"document": "ETSI EN 302 307-1 V1.4.1",
                           "thresholds": "section 6, Table 13, normal frames, ideal AWGN",
                           "url": "https://www.etsi.org/deliver/etsi_en/302300_302399/30230701/01.04.01_60/en_30230701v010401p.pdf"},
       "constants": {"c_m_per_s": C, "k_w_per_k_hz": K, "earth_radius_km": EARTH_RADIUS_KM},
       "modes": MODES, "plframe_symbols": PLFRAME_SYMBOLS, "service_factor": SERVICE_FACTOR,
       "ground_receiver_assumptions": GROUND, "satellite_loss_allocations": SAT_LOSSES,
       "satellite_atmosphere_allocations": SAT_ATMOSPHERE, "irec_loss_allocations": IREC_LOSSES,
       "rates": rates, "satellite_payload_sweep": sat_cases,
       "satellite_4msym_qpsk3_4_candidate": candidate, "irec_sweep": irec_cases,
       "satellite_station_path_sensitivity": [
           satellite(5, 550, 10, 1.9, 6, "3/4", 4e6, tsys_k=temp, extra_path_loss_db=extra)
           for temp in [GROUND["tsys_k"], 300] for extra in [0, 3]],
       "large_pa_compression_screen": [
           {"rf_after_filter_w": p, "filter_loss_db": 1, "provisional_crest_db": 5.5,
            "compression_separation_db": 2,
            "pa_average_before_filter_w": p * 10 ** 0.1,
            "cw_op1db_screen_w": p * 10 ** ((1 + 5.5 + 2) / 10)}
           for p in [5, 10]],
       "thermal_efficiency_sensitivity": [{"rf_after_filter_w": p, "filter_loss_db": 1,
              "assumed_pa_efficiency": eff, "pa_output_before_filter_w": p * 10 ** 0.1,
              "pa_dc_w": p * 10 ** 0.1 / eff,
              "pa_heat_w": p * 10 ** 0.1 * (1 / eff - 1)}
              for p in [1, 2, 5, 10] for eff in [0.2, 0.3, 0.4, 0.5]]}

# Limiting-case / independent algebra checks, not claims about real hardware.
assert PLFRAME_SYMBOLS == 33282
assert abs(slant_km(550, 90) - 550) < 1e-9
case_22 = satellite(1, 550, 10, 1.9, 0, "3/4", 4e6, 2.2e9)
case_24 = satellite(1, 550, 10, 1.9, 0, "3/4", 4e6, 2.4e9)
assert abs(case_22["cn0_db_hz"] - case_24["cn0_db_hz"]) < 1e-9
assert abs(satellite(2, 550, 10, 1.9, 0, "3/4", 4e6)["cn0_db_hz"] -
           case_22["cn0_db_hz"] - db(2)) < 1e-9
assert abs(irec(0.25, 10000, 0.1)["received_at_sdr_dbm"] -
           irec(0.25, 30000, 0.1)["received_at_sdr_dbm"] - 9.53827) < 0.01

folder = Path(__file__).resolve().parent / "output"
folder.mkdir(exist_ok=True)
(folder / "results.json").write_text(json.dumps(out, indent=2) + "\n")
lines = ["# Calculated planning tables", "", f"Tsys = {GROUND['tsys_k']:.3f} K; service factor = {SERVICE_FACTOR:.6f}.", "",
         "## Payload rates", "", "| QPSK code | Video Mb/s | Required Rs Msym/s | Width MHz |", "|---|---:|---:|---:|"]
for r in rates:
    lines.append(f"| {r['mode']} | {r['video_mbps']} | {r['required_symbol_rate_hz']/1e6:.3f} | {r['occupied_bandwidth_hz']/1e6:.3f} |")
lines += ["", "## 5 Mb/s video profile candidate: 4 Msym/s QPSK 3/4; 1.9 m dish", "",
          "| Altitude km | Elevation deg | Range km | Min W, flight 0 dBi | Min W, patch 6 dBi with 1 dB pointing |", "|---:|---:|---:|---:|---:|"]
for h in [500, 550]:
    for e in [90, 30, 10]:
        a = satellite(1, h, e, 1.9, 0, "3/4", 4e6)
        b = satellite(1, h, e, 1.9, 6, "3/4", 4e6)
        lines.append(f"| {h} | {e} | {a['slant_km']:.1f} | {a['minimum_power_after_filter_w']:.3f} | {b['minimum_power_after_filter_w']:.3f} |")
lines += ["", "## Satellite candidate residual margin at 550 km", "",
          "| W after filter | 90 deg, 0 dBi | 30 deg, 0 dBi | 10 deg, 0 dBi | 90 deg, patch | 30 deg, patch | 10 deg, patch |", "|---:|---:|---:|---:|---:|---:|---:|"]
for p in [0.1, 0.25, 1, 2, 5, 10]:
    vals = [satellite(p, 550, e, 1.9, g, "3/4", 4e6)["residual_margin_db"]
            for g in [0, 6] for e in [90, 30, 10]]
    lines.append("| " + str(p) + " | " + " | ".join(f"{v:+.2f}" for v in vals) + " |")
lines += ["", "## IREC 8 Msym/s QPSK 2/3; NF 8 dB; 0 dBi flight, 13 dBic ground", "",
          "| W after filter | 10k ft / 0.1 km offset residual dB | 30k ft / 0.1 km offset residual dB |", "|---:|---:|---:|"]
for p in [0.01, 0.02, 0.05, 0.1, 0.25, 0.5]:
    a = irec(p, 10000, 0.1)["residual_margin_db"]
    b = irec(p, 30000, 0.1)["residual_margin_db"]
    lines.append(f"| {p} | {a:+.2f} | {b:+.2f} |")
lines += ["", "## Satellite station and path sensitivity: 5 W delivered, 550 km, 10 deg, directed antenna", "",
          "| Tsys K | Extra loss dB | Minimum W after filter | Residual margin dB |",
          "|---:|---:|---:|---:|"]
for item in out["satellite_station_path_sensitivity"]:
    lines.append(f"| {item['ground_system_temperature_k']:.2f} | {item['extra_path_loss_db']:.1f} | {item['minimum_power_after_filter_w']:.3f} | {item['residual_margin_db']:+.2f} |")
(folder / "tables.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
print(f"\nWrote {folder / 'results.json'}")
