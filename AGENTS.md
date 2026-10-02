# Yapogee engineering and collaboration

Yapogee is an RP2350B-based USB-C/SPI transmitter module. IREC development is the first schedule priority; preserve useful reuse for 2.4 GHz satellite work. Read the README and relevant hardware/software documentation before changing the design.

## Engineering

- Reason from first principles. Start with physical behavior, requirements and constraints, then derive the equations. Check units, signs, reference planes, current paths and limiting cases.
- Preserve derivations and calculations with inputs, units, assumptions, input provenance, tolerances, operating conditions, tool versions and conclusions. Keep them simple and traceable; unexplained GOOD/PASS labels do not substitute for reasoning.
- Prefer primary manufacturer documentation, textbooks and reproducible measurements. Verify exact order codes, package pins, footprints, device errata and actual connections. Do not trust a familiar-looking symbol or distributor parametric match.
- Distinguish facts, user reports, adopted requirements, assumptions, estimates and unknowns. Separate recommended operating conditions from absolute maximum ratings.
- Distinguish analytical predictions, simulations and measurements. State model limits and how the claim will be checked on hardware. A digital benchmark does not establish RF performance or link closure.
- Derive margins, derating and verification from the mission and component evidence. Do not turn unexplained rules of thumb into universal requirements.
- Make design intent reviewable: hierarchy, power domains, interfaces, startup, shutdown, partial-power behavior, faults, calibration, test access, assembly and manufacturing constraints.
- Audit full power-off and intermediate brownout behavior. Ioff, a reset label, AC coupling or a lock indicator alone does not establish a complete safe interface.
- Preserve calculations and simulation inputs with the design. Record exact source/model revisions, hashes where useful, software versions, run instructions and the relevant results.
- Point out errors and questionable assumptions directly, including prior work and your own conclusions. Recheck disputed findings independently and correct them when evidence changes.

## Collaboration and communication

- **Ask for clarification when a requirement, intended action or constraint is unclear.** State what is uncertain and why the answer matters; continue useful work that does not depend on it. Do not silently guess mission-critical requirements.
- Lead with the finding or result. Use concrete technical language, clear prose, definitions, derivations and figures that explain the physical design.
- State what was checked and what remains unverified. Do not present a proposal as a released circuit or a simulation as board qualification.
- Avoid filler, sales language, forced enthusiasm and stock AI phrasing. Explain tradeoffs without inventing an inferior alternative to contrast against.
- Cite the exact revision, section or page only when checked. Never invent a citation or imply a document was read in full when it was not.

## Files and changes

- Preserve existing work and user edits. Inspect dependencies before moving files; do not delete backups as incidental cleanup.
- Keep generated previews and QA artifacts in their local `output/` directories. Keep published SVG previews beside editable diagram sources; regenerate both when changing a diagram.
- Use repository-relative paths and scripts that work after moving or cloning the repo. Do not publish private workspace paths, personal notes, transcripts, credentials or unsupported vendor redistribution.
- Keep proposed engineering work separate from immutable manufacturing releases. No release tag without an exact BOM, reviewed connectivity/layout, actual stackup and recorded checks.
- Run checks appropriate to the change. Do not add tests that merely mirror documentation or implementation; verify meaningful calculations, connectivity, model inputs and measured behavior.
- Preserve third-party provenance and terms. Do not change project licensing or ownership without an explicit maintainer decision.
- Do not add AI co-author trailers or “Generated with” lines to commits or pull requests.
