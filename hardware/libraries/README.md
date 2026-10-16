# Component library

Project-local KiCad assets for schematic capture: **114 symbols, 71 footprints and
64 model files**. The library includes 100 exact-part entries and fourteen generic
passive/debug/PCB-feature templates. The MCU and larger RF devices use functional symbol
units; supply pins and exposed pads remain explicit.

Open `hardware/devboard/board/Yapogee-Devboard` as a KiCad project. Its
`sym-lib-table` and `fp-lib-table` register the `Yapogee` library. Footprints resolve
models through `${KIPRJMOD}/../../../libraries/3dmodels/`; another project location
needs corresponding library/model paths. No global library installation is needed.

| Files | Contents |
|---|---|
| `Yapogee.kicad_sym` | MCU/flash, RF/clock, power, supervision, USB and interface symbols |
| `Yapogee.pretty/` | Selected package land patterns and generic passive/debug footprints |
| `3dmodels/` | Matching-package KiCad STEP models and drawing-derived VRML previews |
| [components.json](components.json) | Exact order codes, pin maps, source revisions/hashes, model provenance and package notes |

Pin maps, package drawings, pin/pad matching and KiCad 10 imports/exports have been
checked. The models are package previews, not guaranteed assembled-fit models;
some show only the maximum body envelope. Package and exposed-pad details are in
`components.json`. Thermal vias, paste/mask settings and assembly fit need review
on the actual board.

The main ICs and connector options below are covered. RF filters and the shield
still need selections and footprints. Generic resistor/capacitor templates
have no selected values, ratings or order codes; header templates have no final
signal assignments. The Abracon 3.3 µH entry is for the MCU internal regulator.

Place `Yapogee:SN65LVDM31DR` for the clock driver: a compact single-unit symbol
with all 16 pins visible and TI D0016A SOIC-16 reference lands. Pin mapping and
land dimensions are checked; no 3D model is linked. The proposed clock-interlock
ICs still need assets. Circuit timing and assembled fit remain to verify.

Capacitor symbols show the value, voltage, tolerance, dielectric and package in
the JLC style. These exact parts have manufacturer reflow lands and nominal STEP
package previews:

| Part | Value | Rated voltage | Package |
|---|---:|---:|---|
| `GCM155R71H104KE02D` | 100 nF X7R | 50 V | 0402 |
| `GCM188R71E105KA64D` | 1 µF X7R | 25 V | 0603 |
| `KAM15AR71A225KT` | 2.2 µF X7R | 10 V | 0603 |
| `KAM15CR70J475KT` | 4.7 µF X7R | 6.3 V | 0603 |
| `GRM155R60J475ME47D` | 4.7 µF X5R | 6.3 V | 0402 |
| `GCM1555C1H101JA16D` | 100 pF C0G | 50 V | 0402 |
| `GCM31CR71A226KE02L` | 22 µF X7R | 10 V | 1206 |
| `CGA6P3X7R1E226M250AB` | 22 µF X7R | 25 V | 1210 |
| `GCM1885C1H332JA16D` | 3.3 nF C0G | 50 V | 0603 |
| `GCM1885C1H103JA16D` | 10 nF C0G | 50 V | 0603 |
| `GCM1555C1H3R3CA16D` | 3.3 pF C0G, ±0.25 pF | 50 V | 0402 |

The 2.2 µF / 0603 option is for rails up to 5.5 V. Check effective capacitance
against each circuit's minimum. `GCM21BR71E225KA73L` (2.2 µF / 25 V / 0805) and
`CL31B106KAHVPNE` (10 µF / 25 V / 1206) are available alternatives. Exact source
drawings, order codes and model details are in `components.json`.

The local buck/AFE bulk part is `GCM31CR71A226KE02L`, with two per buck input and
output bank and one per AFE input/output bank. The 25 V TDK remains a separate
battery-bus option. The Murata has 1.05 × 1.60 mm reflow pads, a 1.90 mm gap and
a 4.50 × 2.30 mm courtyard. Its nominal STEP is a package preview; the hidden
maximum-body model is 3.40 × 1.80 × 1.80 mm.

Feedback resistor symbols use the same JLC drawing style as the 27 Ω USB part.
Place `Yapogee:0402,12kΩ,0.1%` and the matching 18 kΩ, 20 kΩ, 24 kΩ, 30 kΩ or
75 kΩ entry. These are Vishay TNPWe3, ±0.1%, 25 ppm/K, AEC-Q200, with exact
`TNPW0402…BEED` matte-tin order codes. The reference reflow footprint has
0.55 × 0.60 mm pads and a 0.40 mm gap. Supplier codes are omitted where unverified.

The clock-filter parts are `Yapogee:BLM15PX121SH1D` and `Yapogee:0402,1.5Ω`
(`CRCW04021R50FKED`). The bead has Murata's 0402 reflow lands and a nominal
STEP preview; the resistor reuses the CRCW0402 lands and model. The matching
`KAM15AR71A225KT` 2.2 µF and `GCM155R71H104KE02D` 100 nF entries are ready too.

Clock-network passives also include `0402,2.2kΩ`, `0402,47Ω` and
`0402,24.3kΩ,0.1%`. The 47 Ω / 3.3 pF damping pair and 24.3 kΩ detector-divider
part are tuning/protection candidates; their presence does not select a fitted
circuit. Set DNP on schematic instances, not on reusable library symbols.

LMX loop assets are `GRM2165C1H333JA01D` (33 nF C0G/0805),
`GRM1555C1H222GA01D` (2.2 nF C0G/0402) and `0402,470Ω`
(`CRCW0402470RFKED`). The 33 nF part has its own checked GRM21 reflow lands.
Bias/termination assets add `GCM188R71E474KA64D` (470 nF X7R/0603),
`GCM21BR71A106KE22L` (10 µF X7R/0805) and `0402,49.9Ω`
(`CRCW040249R9FKED`). Package checks do not qualify the connected PLL or RF path.

For the dual buck, place `Yapogee:XGL3520-681MEC`: Coilcraft's 0.68 µH ±20%
AEC-Q200 shielded inductor. `Coilcraft_XGL3520_RefReflow` uses its recommended
0.81 × 3.2 mm lands at 1.80 mm centres. Pad 1 denotes the marked short-lead end;
connect it to SW for the manufacturer's preferred EMI orientation. The VRML is
a drawing-derived body/terminal preview. Check hot inductance and assembled fit.

For the RP2350 core output, `GRM155R60J475ME47D` follows the official R4-S1
4.7 µF reference, with its regulator-specific wide lands and an enclosing
courtyard. It is general-purpose X5R rated to 85°C. The X7R/AEC
`KAM15CR70J475KT` is an input/filter candidate with its own wider-pad KAM15C
footprint; it is not a qualified core-output replacement. The MCU inductor's
marked pad 1 goes to core1V1, pad 2 to VREG_LX.

For GRF2013 bias, `0402DC-33NXGRW` supplies the Coilcraft 33 nH choke lands;
`0603,499Ω,0.1%` is Vishay `TNPW0603499RBEEA`. The 100 pF C0G DC blocks reuse
the existing GCM15 footprint and nominal STEP. E24 pad choices are
`0402,18Ω` / `0402,300Ω` and `0402,36Ω` / `0402,150Ω`, with exact CRCW order
codes and manufacturer reflow lands. Their mounted GHz behavior remains to check.

The capacitor STEP files are representative KiCad models with rounded ceramic
bodies and metallic termination faces, not manufacturer CAD. Their nominal
length, width, height and termination spans were checked against the exact part
drawings; each uses unity scale and sits at the footprint origin. Nominal heights
are 0.50 mm for GCM15, 0.80 mm for GCM18/KAM15, 1.25 mm for GCM21, 1.60 mm for
GCM31/CL31 and 2.50 mm for CGA6. Each footprint also retains its maximum-body WRL as a
hidden model: switch visibility in KiCad for clearance review. Neither preview
includes solder fillets or assembly standoff. Existing board instances need a
library footprint update to receive the new model links.

## RF connectors and power jumper

| Place from `Yapogee:` | Use |
|---|---|
| `132134-10` | Top-mounted SMT SMA for dev-board RF output |
| `U.FL-R-SMT-1(10)` | Compact top-mounted external-LO connector; mark DNP initially |
| `132289` | Edge-launch SMA alternative for a nominal 1.57 mm PCB; requires bottom solder joints |
| `SolderJumper_2_Bridged` | Normally soldered USB power link |
| `SolderJumper_2_Open` | Same pads, shown open on the schematic |

The jumper uses `Yapogee:SolderJumper-2_P1.3mm_Open_Pad1.0x1.5mm`: two
1 × 1.5 mm pads with a 0.3 mm gap and no paste apertures. Manually bridge it for
USB power and wick it open before using EXT_5V with USB attached. EXT_5V remains
live during USB-powered operation. This is a PCB feature, with no purchase MPN,
3D component model or catalog current rating. Check bridge loss/heating during bring-up.

The first two connectors keep all solder joints on top. The vertical SMA is 8.84 mm
tall and needs cable strain relief; U.FL is for occasional testing. Connector STEP
models are KiCad community previews checked against manufacturer drawings.
The RF launch still depends on the chosen PCB stackup. Keep compact 0 Ω assembly
links for LO selection; the larger power solder jumper belongs outside the RF path.

For USB D+/D− series resistors, place **`Yapogee:0402,27Ω`**: Vishay
CRCW040227R0FKED, 27 Ω ±1%, JLC/LCSC **C482122**. It uses
`Yapogee:R_0402_1005Metric` and the existing package model. The symbol matches the
JLC resistor style, with the value inside the rectangle and purchasing fields hidden.

The same ordinary support family also includes `0402,0Ω`, `0402,22Ω`,
`0402,33Ω`, `0402,100Ω`, `0402,1kΩ`, `0402,4.7kΩ` and `0402,10kΩ`.
Choose damping from each route; availability in this library does not set a
termination value. Unverified supplier IDs are omitted.

## Solder-down and header rows

`PCB_DualMount_EdgeRow_1x12` has separate 0.80 mm edge castellations and
1.10 mm full header holes at 2.54 mm pitch, joined by masked copper.
`PCB_Carrier_DualRow_1x12` provides matching carrier lands and full holes.
These are bare PCB features excluded from purchasing/position files. Align
the board-owned edge to the module footprint's `Dwgs.User` guide.

`Samtec_HTSW_1x12` selects `HTSW-112-07-L-S`, a high-temperature vertical
header. It uses the same holes as an assembly alternative; do not overlay its
footprint on the PCB row. The header model is a drawing-derived nominal preview.
The dual-mount interface is intended for Rev A as well as later revisions.
The 12-contact row does not freeze the final contact count. It is not a complete
module footprint: outline, row spacing, signal
assignments, paste, mounting and contact-current qualification remain open.
Keep RF on a dedicated launch.

Reusable [Pigeon Vision carrier](https://github.com/stanford-ssi/PigeonVision)
parts are available under `Yapogee:` too. These are library options; adding them
doesn't change the fitted transmitter circuit.

| Symbol | Use |
|---|---|
| `TPD1E05U06DYAR` | Single-line ESD protection |
| `TPD4E05U06DQAR` | Four-line ESD protection |
| `PTS636_SK25_SMTR_LFS` | BOOT/RUN pushbutton |
| `BSS138BK,215` | Small control MOSFET |
| `Samtec_TSM-102-01-L-SV-P-TR` | Two-pin recovery/shunt header |
| `INA226AIDGSR` | Optional current and bus-voltage measurement |
| `LTST-C170KGKT` | Green status LED; carrier's audited alternate |

The TPD4E05U06's opposite NC pads need external copper for through-routing.
The single-line ESD diode isn't a precision clamp for USB hot-plug ringing.
The LED is the LiteOn alternate, not the carrier's fitted KT-0805G/C2297.
Choose its resistor and the INA226's shunt for the actual circuit.

For USB-C, place **`Yapogee:USB4105-GF-A-060`**: GCT's USB 2.0 receptacle,
JLC/LCSC **C3025063**. It uses the existing `Yapogee:USB4105-GF-A` footprint;
GCT drawing B3 gives the same lands for both stake lengths. The `-060` part has
0.60 mm shell stakes; the unsuffixed part has 0.95 mm stakes. The shared STEP is a
family preview. Check the shell joints, board edge and plug clearance during layout.
The symbol uses KiCad's USB-C graphics with nine connections along the right.
VBUS, GND, D+ and D− each join their matching contacts internally; all physical
pin numbers remain mapped to the footprint. CC1, CC2, SBU1, SBU2 and shield stay
separate. Leave the unused SBU connections explicitly unconnected for USB 2.0.

Place **`Yapogee:TPS259470ARPWR`** for the auto-retry eFuse. It shares the existing
`TPS259470LRPWR`-named footprint and body preview; the separate symbol keeps the
order code and fault behavior explicit. The L symbol remains the latch-off option.

Both LMX entries use TI's current RHA0040Y land
([MPQF974](https://www.ti.com/lit/ml/mpqf974/mpqf974.pdf), 4233329/A): a 3.1 mm
exposed pad with four 1.35 mm paste windows. The older RHA0040H drawing in the
datasheet addenda has a 4.5 mm pad; the perimeter lands are identical. Confirm the
package drawing and paste pattern for the purchased lot. Matching perimeter lands
alone do not establish solderability across the two exposed-pad variants.

LMX2572LPRHAT is an IREC-only alternate using the same footprint.
Its 2 GHz output limit excludes 2.4 GHz satellite operation. Registers, loop filter,
decoupling and output drive need checking for that variant. The full LMX2572 remains
the shared-band choice; the alternate entry doesn't change the fitted part.

Run the portable integrity check from the repository root:

```sh
python3 hardware/libraries/check_assets.py
```

It checks library/table/model resolution, indexed file hashes, pin/pad identity and
that copper belonging to different pins doesn't overlap. It does not replace circuit ERC, board DRC or hardware testing. [Third-party provenance](THIRD_PARTY.md) covers
reused KiCad data; source datasheet PDFs and local QA fixtures are not redistributed.
