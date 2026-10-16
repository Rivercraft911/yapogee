# Hardware

The dev board puts RP2350B, AFE7071, the reference and LO on one PCB. USB-C handles power and programming; SPI takes data from the carrier. The optional small driver feeds an external PA and band filter.

| Board | Contents / status |
|---|---|
| [Yapogee Rev A](devboard/README.md) | Compact module with bring-up pads and solder-down/header mounting; schematic capture underway |
| [Transmitter board](transmitter/) | Empty workspace for the later integrated IREC/mission board |

The intended clock interface is GP28 continuous PIO → SN65LVDM31DR → AFE differential DDR, at 32/64 MHz for the 8/16 Msym/s four-SPS targets. Clock and data start together; phase alignment adds no PCB parts. Retain CLK_IO for dual-input bring-up. The reference fanout remains LMK1C1104PWR.

The [link budget](simulations/link_budget.py), [LO loop](simulations/reference_lo_loop_screen.py) and [dual-input fallback timing](simulations/dac_clock_budget.py) models run with Python 3 and no extra packages. The last model describes the older SDR/FIFO path, not DDR startup. These are calculations; measured results will follow.

IREC comes first. Rev A is also the Yapogee module: test it on the bench, then solder the same board onto the carrier and feed it regulated 5 V. Later mission boards can integrate the proven circuit. Satellite work can reuse tested blocks with its own PA and filter. Yapling will likely have its own repo.
