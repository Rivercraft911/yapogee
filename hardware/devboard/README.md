# Initial development board

Onboard RP2350B generates interleaved I/Q for AFE7071. A shared 12 MHz reference drives waveform timing and the full LMX2572 LO. GRF2013 supplies optional low-power drive; band PA/filter modules remain external. IREC 1240–1300 MHz is the first assembly; retain 2400–2450 MHz core coverage, with 2200–2290 MHz also within the selected devices' range.

![RF architecture](architecture/core-rf.svg)

[Editable architecture](architecture/architecture.drawio) · [Clock diagram](architecture/reference-clocks.svg) · [Power/interfaces](architecture/power-interfaces.svg)

## Components and references

| Function | Device / reference |
|---|---|
| MCU / flash | RP2350B A4 (SC1510-A4), W25Q128JVSIQ; [official minimal KiCad](https://pip.raspberrypi.com/documents/RP-010329-CA-RP2350B%20Minimal%20KiCAD.zip), [hardware guide](https://datasheets.raspberrypi.com/rp2350/hardware-design-with-rp2350.pdf) |
| Reference / fanout | ECS-TXO-2520MV-120-AN-TR, LMK1C1104PWR; [oscillator](https://ecsxtal.com/store/pdf/ECS-TXO-2520MV.pdf), [fanout](https://www.ti.com/lit/ds/symlink/lmk1c1104.pdf) |
| DAC / IQ modulator | AFE7071IRGZT; [datasheet/IBIS](https://www.ti.com/product/AFE7071), [EVM guide](https://www.ti.com/lit/ug/slou337a/slou337a.pdf) |
| LO | LMX2572RHAT; [datasheet](https://www.ti.com/lit/ds/symlink/lmx2572.pdf), [EVM schematic/BOM](https://www.ti.com/lit/ug/snau217b/snau217b.pdf) |
| Clock comparison | GPIO28 dedicated PIO or CDCE6214RGET; conditional LMK1D1204PRHDT frontend; [CDCE](https://www.ti.com/product/CDCE6214), [exact P buffer](https://www.ti.com/lit/ds/symlink/lmk1d1204p.pdf) |
| Driver | GRF2013; [reference circuit](https://www.guerrilla-rf.com/includes/prodFiles/2013/GRF2013DS.pdf) |
| Quiet rails | TPS7A2133PQWDRBRQ1 digital; 2×TPS7A9101DSKR AFE; 2×TPS7A9401DSCR LO/reference; [models/EVMs](https://www.ti.com/product/TPS7A94), [AFE LDO](https://www.ti.com/product/TPS7A91) |
| Input / reset | TPS259470LRPWR, TPS386000RGPR, 2×TPS389001DSER; [input](https://www.ti.com/lit/ds/symlink/tps25947.pdf), [supervisor](https://www.ti.com/lit/ds/symlink/tps386000.pdf), [AFE monitors](https://www.ti.com/lit/ds/symlink/tps3890.pdf) |

The board is in development; component choices describe the current design. Schematics, layout and a released BOM are not yet available.

## Interfaces

- **Power:** regulated 5 V, 4.75–5.25 V. The current analytical allocation is about 0.90 A / 4.5 W with the small driver enabled. Separate LDOs supply digital, AFE, LO and reference domains. USB-C power admission uses advertised source current; external 5 V also permits USB data/programming from lower-current hosts. The source-control circuit is still under development.
- **Host:** SPI SCK/MOSI/CS into module, READY outward, separate host I/O reference and default-off translation. Final pad numbers/timing are not released.
- **LO_OUT / LO_IN:** local LO → removable filter adapter → LO_IN, or an exclusively selected external generator. Isolate the inactive route at both roots. AFE-plane drive is −5 to +5 dBm; target +4 dBm and verify it at the AFE input. Common CMOS REF_IN is a separate 12 MHz interface.
- **RF:** exclusive raw-AFE or GRF2013 route with input-pad options. IREC evaluation PA is [GRF5613 EVB184](https://www.guerrilla-rf.com/includes/prodFiles/5613/GRF5613%20EVB184%201240-1420%20MHz.pdf); satellite low-power evaluation is [GRF5526 tune #180](https://www.guerrilla-rf.com/includes/prodFiles/5526/GRF5526%202200-2500MHz.pdf). Multi-watt video PA is separate. Each final PA has its own output filter, supply/bias, READY and local faults.
- **Mounting/debug:** solder-down module pads with multiple ground connections, optional digital headers, SWD/BOOTSEL/RUN, LEDs and test points. A removable shield is part of the intended module form; the mechanical design is not released. RF interfaces use controlled-impedance launches.

## Board and model status

`board/` is reserved for KiCad sources; none are released. Shared hardware models are in `../simulations/`: [link/payload budget](../simulations/link_budget.py) and [ideal LO-loop screen](../simulations/reference_lo_loop_screen.py). They are analytical planning models, not SPICE/RF validation. Real stackup, device models and measurements will accompany later SI, power, PLL and RF-network studies.

The [DAC clock budget](../simulations/dac_clock_budget.py) computes nominal launch margins and relative-frequency drift; it does not establish loaded receiver timing or jitter.

Run from the repository root with Python 3; all three use the standard library:

```sh
python3 hardware/simulations/link_budget.py
python3 hardware/simulations/reference_lo_loop_screen.py
python3 hardware/simulations/dac_clock_budget.py
```

The link model writes local `hardware/simulations/output/` tables/JSON. The loop screen and clock budget print JSON. Inputs and assumptions are recorded in the source and results.

## Clocking and control

The 12 MHz reference supplies the MCU and clock/LO synthesizers. At MCU SYS128 MHz, the interleaved data clock runs at 64/32/16 MHz for 32/16/8 MS/s per I/Q channel. A dedicated continuous PIO clock on GPIO28 is the proposed conversion-clock source; CDCE6214 provides a comparison source. The conversion clock is separate from the data strobe and remains frequency locked to it.

Rail supervision controls MCU reset and hardware permission. Clock enable operates independently of PA arm, allowing core configuration with RF muted. LO CE powers calibration; the RF path is enabled after configuration and path readiness. Destination-powered buffers isolate separately powered control domains.

The AFE differential clock interface and loaded PIO clock/RF performance remain unqualified. The models describe analytical behavior; hardware measurements will accompany the board files.
