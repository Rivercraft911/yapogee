# Reused KiCad library data

KiCad-derived symbols, footprints and STEP models retain their upstream
CC-BY-SA 4.0 terms and KiCad design exception, supplied in [LICENSE.KiCad.md](LICENSE.KiCad.md).
The exception permits using library data in designs; it does not waive attribution
or share-alike terms for redistribution of the library collection itself. This
notice does not choose a license for the surrounding board/software project.

Upstream projects:

- [KiCad symbols](https://gitlab.com/kicad/libraries/kicad-symbols)
- [KiCad footprints](https://gitlab.com/kicad/libraries/kicad-footprints)
- [KiCad package models](https://gitlab.com/kicad/libraries/kicad-packages3D)

[components.json](components.json) records per-component sources and available
source hashes. Installed library inputs came from KiCad 10.0.0; downloaded STEP
models retain their embedded copyright headers. Upstream `master` links identify
their source projects; the recorded hashes identify the actual reused data.

Modifications include flattened symbol inheritance, functional pin grouping,
visible power/ground pads, exact-part fields, project-local model references and
selected land-pattern changes. The LMK1C1104 TSSOP footprint geometry is unchanged;
its STEP file retains the © 2025 KiCAD header. Generic package models are identified
as such rather than presented as vendor solids.

Original drawing-derived symbols, footprints and VRML envelopes use the factual
pin/land/body dimensions of the cited manufacturer drawings. Manufacturer source
PDFs, drawing screenshots and third-party web CAD downloads are not bundled.
