# Component library

Project-local KiCad assets for schematic capture: **38 symbols, 37 footprints and
34 model files**. The library includes 28 exact-part entries and ten generic
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

Pin maps, package drawings, pin/pad matching and KiCad 10 imports/exports have been
checked. The models are package previews, not guaranteed assembled-fit models;
some show only the maximum body envelope. Package and exposed-pad details are in
`components.json`. Thermal vias, paste/mask settings and assembly fit need review
on the actual board.

The main ICs are covered. RF filters, RF connectors, the dual-buck inductor and
shield still need selections and footprints. Generic resistor/capacitor templates
have no selected values, ratings or order codes; header templates have no final
signal assignments. The Abracon 3.3 µH entry is for the MCU internal regulator.

Both LMX entries use TI's current RHA0040Y land
([MPQF974](https://www.ti.com/lit/ml/mpqf974/mpqf974.pdf), 4233329/A): a 3.1 mm
exposed pad with four 1.35 mm paste windows. The older RHA0040H drawing in the
datasheet addenda has a 4.5 mm pad; the perimeter lands are identical. The smaller
land also suits H parts, while the larger one could print paste close to the
terminals of a Y part. Confirm the drawing for the purchased lot.

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
