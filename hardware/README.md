# Hardware

Start with the development board: an onboard RP2350B, AFE7071 DAC/IQ modulator, shared reference, wideband LO and optional small driver. IREC comes first; the core also supports satellite development with a different external PA and output filter.

| Board | Contents / status |
|---|---|
| [Initial dev board](devboard/README.md) | Detailed architecture, component references, interfaces and bring-up requirements; KiCad sources come next |
| [Transmitter board](transmitter/) | Empty workspace for the later integrated IREC/mission board |

Shared [link-budget](simulations/link_budget.py), [LO-loop](simulations/reference_lo_loop_screen.py) and [DAC-clock timing](simulations/dac_clock_budget.py) models live in `simulations/`. They record analytical assumptions; device-level simulations and measured results will follow the board work.

The dev board provides USB-C, SPI, external regulated 5 V, test access and a removable shield option. The later transmitter board can reuse qualified circuit blocks on its own PCB. Yapling will likely live in a separate repository.
