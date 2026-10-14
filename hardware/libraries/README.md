# Component library

Project-local KiCad assets for schematic capture: **53 symbols, 48 footprints and
44 model files**. The library includes 41 exact-part entries and twelve generic
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

The main ICs and connector options below are covered. RF filters, the dual-buck
inductor and shield still need selections and footprints. Generic resistor/capacitor templates
have no selected values, ratings or order codes; header templates have no final
signal assignments. The Abracon 3.3 µH entry is for the MCU internal regulator.

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
