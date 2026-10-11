# Initial development board

Onboard RP2350B generates interleaved I/Q for AFE7071. A shared 12 MHz reference drives waveform timing and the full LMX2572 LO. GRF2013 supplies optional low-power drive; band PA/filter modules remain external. IREC 1240–1300 MHz is the first assembly; retain 2400–2450 MHz core coverage, with 2200–2290 MHz also within the selected devices' range.

![RF architecture](architecture/core-rf.svg)

[Editable architecture](architecture/architecture.drawio) · [Clock diagram](architecture/reference-clocks.svg) · [Power diagram](architecture/power-interfaces.svg)

## Components and references

| Function | Device / reference |
|---|---|
| MCU / flash | RP2350B A4 (SC1510-A4), W25Q128JVSIQ; [official minimal KiCad](https://pip.raspberrypi.com/documents/RP-010329-CA-RP2350B%20Minimal%20KiCAD.zip), [hardware guide](https://datasheets.raspberrypi.com/rp2350/hardware-design-with-rp2350.pdf) |
| Reference / fanout | ECS-TXO-2520MV-120-AN-TR, LMK1C1104PWR; [oscillator](https://ecsxtal.com/store/pdf/ECS-TXO-2520MV.pdf), [fanout](https://www.ti.com/lit/ds/symlink/lmk1c1104.pdf) |
| DAC / IQ modulator | AFE7071IRGZT; [datasheet/IBIS](https://www.ti.com/product/AFE7071), [EVM guide](https://www.ti.com/lit/ug/slou337a/slou337a.pdf) |
| LO | LMX2572RHAT; [datasheet](https://www.ti.com/lit/ds/symlink/lmx2572.pdf), [EVM schematic/BOM](https://www.ti.com/lit/ug/snau217b/snau217b.pdf) |
| DAC clock | GPIO28 dedicated PIO; conditional LMK1D1204PRHDT differential driver; [driver datasheet](https://www.ti.com/lit/ds/symlink/lmk1d1204p.pdf) |
| Driver | GRF2013; [reference circuit](https://www.guerrilla-rf.com/includes/prodFiles/2013/GRF2013DS.pdf) |
| Power | Candidate TPS62441QWRQRRQ1 dual buck (3.3 V digital and 2.5 V AFE preregulator), TPS7A8801QRTJRQ1 dual AFE LDO, 2×TPS7A2133PQWDRBRQ1 LO/reference LDOs; [buck](https://www.ti.com/lit/ds/symlink/tps62441-q1.pdf), [AFE LDO](https://www.ti.com/lit/ds/symlink/tps7a88-q1.pdf), [LO/reference LDO](https://www.ti.com/lit/ds/symlink/tps7a21-q1.pdf) |
| Input / reset | TUSB320LAIRWBR, TPS259470ARPW (auto-retry; same footprint as the library's TPS259470LRPWR), TPS386000RGPT, 2×TPS389001DSER; [USB-C CC](https://www.ti.com/lit/ds/symlink/tusb320lai.pdf), [eFuse](https://www.ti.com/lit/ds/symlink/tps25947.pdf), [supervisor](https://www.ti.com/lit/ds/symlink/tps386000.pdf), [AFE monitors](https://www.ti.com/lit/ds/symlink/tps389001.pdf) |

These are the current parts, with the DAC clock interface still being checked. There is no released BOM yet.

## Interfaces

- **Power:** USB-C 5 V. A CC controller admits only sources advertising at least 1.5 A, and one auto-retry eFuse limits inrush, current and overvoltage and blocks back-feed into the host. EXT_5V pads take bench or harness power through an exclusive link. A dual buck makes the 3.3 V digital rail and a 2.5 V preregulator for the AFE 1.8 V LDO; the 3.3 V AFE, LO and reference LDOs run from the protected 5 V.
- **Host:** SPI SCK/MOSI/CS in, READY out, with a host I/O reference and default-off level translation. Pin assignments are not final.
- **Reference / LO:** shared 12 MHz reference, with external-reference and external-LO injection options. An attenuator pad and onboard low-pass filter reduce LO harmonics before the AFE. Assembly links disconnect the unused source; the AFE LO input accepts −5 to +5 dBm.
- **RF:** raw AFE or GRF2013 driver output, selected with assembly links. Populate one output SMA first. Mission PA and output filter stay external.
- **Debug / mechanics:** SWD, BOOTSEL, RUN, LEDs, test points and DNP-isolated digital I/Q header positions. Leave room for a removable RF shield. Solder-down module pads come with the later compact board.

## Board and model status

[Open the KiCad project](board/Yapogee-Devboard/Yapogee-Devboard.kicad_pro). Its local tables load the [component library](../libraries/README.md), including symbols, footprints and package previews. The schematic and PCB are blank.

Three Python models cover [link/payload budget](../simulations/link_budget.py), [ideal LO-loop behavior](../simulations/reference_lo_loop_screen.py) and [DAC-clock timing](../simulations/dac_clock_budget.py). These are analytical models; they don't establish RF performance, loaded clock timing or board fit.

Run from the repository root with Python 3; all three use the standard library:

```sh
python3 hardware/simulations/link_budget.py
python3 hardware/simulations/reference_lo_loop_screen.py
python3 hardware/simulations/dac_clock_budget.py
```

The link model writes tables/JSON to `hardware/simulations/output/`; the other two print JSON. Inputs and assumptions are in the source and results.

## Clocking and control

The 12 MHz reference supplies the MCU and LO synthesizer. At MCU SYS128 MHz, the interleaved bus runs at 64/32/16 MHz for 32/16/8 MS/s per I/Q channel. A separate, continuous PIO loop on GPIO28 supplies the DAC conversion clock. Integer dividers keep the two clocks at the same nominal frequency. Screen the PIO source on existing hardware before layout; the differential receiver interface and final-board RF performance still need verification. There is no alternate DAC-clock input in this baseline.

Rail supervision holds reset and RF permission until power is valid. Clock enable is separate from PA arm so the core can be configured with RF muted. Destination-powered buffers isolate separately powered control domains.
