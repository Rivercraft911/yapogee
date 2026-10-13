# Hardware

The dev board puts RP2350B, AFE7071, the reference and LO on one PCB. USB-C handles power and programming; SPI takes data from the carrier. The optional small driver feeds an external PA and band filter.

| Board | Contents / status |
|---|---|
| [Initial dev board](devboard/README.md) | RF, clock and power diagrams, current parts and KiCad project; schematic capture underway |
| [Transmitter board](transmitter/) | Empty workspace for the later integrated IREC/mission board |

The [link budget](simulations/link_budget.py), [LO loop](simulations/reference_lo_loop_screen.py) and [DAC-clock timing](simulations/dac_clock_budget.py) models run with Python 3 and no extra packages. Inputs and assumptions live in the scripts. These are calculations; measured results will follow.

IREC comes first. After validation, the dev board can run from the carrier's regulated 5 V; a compact transmitter PCB comes later. Satellite work can reuse tested blocks with its own PA and filter. Yapling will likely have its own repo.
