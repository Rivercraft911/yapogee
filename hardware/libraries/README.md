# Component library

Project-local KiCad assets for schematic capture: **37 symbols, 37 footprints and
34 model files**. The library includes 27 exact-part entries and ten generic
passive/debug templates. The MCU and larger RF devices use functional symbol
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

These are draft component assets. Pin/function and package drawings were checked,
symbol pin identifiers were matched to footprint pads, and KiCad 10 imports/exports
were exercised. STEP package models are not manufacturer-certified solids. VRML
previews use drawing dimensions; several represent only maximum body envelopes,
without leads. Neither type establishes final assembled fit.

The AFE clock frontend remains conditional. TPS62441 analog-preregulator headroom,
effective output passives and the complete USB power path remain circuit decisions.
Generic capacitors/resistors have no selected value, voltage rating or order code.
No shield outline, RF connector, output-buck inductor or final header pinout is
frozen by this library. The Abracon 3.3 µH entry is for the MCU internal regulator.

Package details recorded in the index include the AFE7071 and LMX2572 exposed-pad
sizes, unnumbered CDCE6214/TPS7A88 corner lands, the local GRF2013 exposed-pad number,
USB contact pairs sharing copper, and MCU/inductor land-pattern choices. Review
these before connecting nets. Thermal vias, paste/mask process, circuit ERC, routed
board DRC and mechanical/assembly review belong to the board design.

Run the portable integrity check from the repository root:

```sh
python3 hardware/libraries/check_assets.py
```

It checks library/table/model resolution, indexed file hashes and pin/pad identity.
It does not check circuit behavior. [Third-party provenance](THIRD_PARTY.md) covers
reused KiCad data; source datasheet PDFs and local QA fixtures are not redistributed.
