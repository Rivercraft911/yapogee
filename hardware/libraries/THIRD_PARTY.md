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

The BLM15 ferrite entry uses KiCad's `Device:FerriteBead_Small` geometry and
the unchanged KiCad StepUp `L_0402_1005Metric.step` nominal package model.
Its reflow lands and hidden maximum-body envelope follow Murata's dimensional
drawing. The model is a representative package solid, not manufacturer CAD;
its embedded copyright and the KiCad terms above are retained.

The exact capacitor entries reuse the existing KiCad StepUp capacitor STEP
models for 0402, 0603, 0805, 1206 and 1210. The original © 2017 KiCad StepUp
headers and model bytes are unchanged. Exact manufacturer reference dimensions
were checked against the nominal body and colored termination faces; model
links use unity scale. These are representative package solids, not
manufacturer-authored CAD. The earlier drawing-derived maximum-body WRLs remain
linked as hidden clearance alternatives. Per-entry dimensions, source links and
hashes are recorded in `components.json`; the KiCad terms above apply to the
reused STEP files.

Seven support-part entries reuse reviewed CAD from the
[Pigeon Vision carrier library](https://github.com/stanford-ssi/PigeonVision/tree/5f18f65819614a4c84aacd40479237420e670fcd/hardware/libraries).
Their original KiCad-derived geometry and locally copied KiCad STEP models retain
the terms above. Drawing-derived TVS/header envelopes are identified as previews.
Changes here flatten inheritance, assign local footprint/model paths and preserve
exact order codes. The LiteOn LED uses KiCad's `Device:LED` symbol with the carrier's
audited LiteOn land pattern; it does not reuse the fitted Kento JLC-import asset.
Per-entry source paths, commit and hashes are recorded in `components.json`.

The RF connector symbols use KiCad's `Connector:Conn_Coaxial` geometry with exact
part fields. Three coaxial footprints and their STEP previews are copied from
KiCad 10.0.0; local model paths replace the global KiCad paths. The U.FL STEP is a
base-family community model checked against the exact (10) drawing. The two
solder-jumper symbols and shared open-pad footprint come from KiCad's Jumper
libraries. These additions retain the library terms above; manufacturer drawings
are referenced in the index and are not redistributed here.

The dual-mount module/carrier rows and Samtec header preview are original
drawing-derived assets. They use factual pitch, bore and body dimensions from
the cited Samtec/JLC documents and the Pico mounting precedent; no vendor CAD
or drawings are redistributed. The new RF choke/resistor VRML previews are
also authored mechanical representations. The 100 pF capacitor reuses the
licensed KiCad nominal model rather than adding another package solid.
