# Yapogee Rev A

RP2350B makes I/Q samples; AFE7071 turns them into RF using the LMX2572 LO. A shared 12 MHz reference ties the timing together. GRF2013 adds optional low-power drive, with the mission PA and band filter outside the board. IREC at 1.28 GHz comes first; the core also covers 2.4 GHz.

![RF signal path](architecture/core-rf.svg)

[Editable diagrams](architecture/architecture.drawio) · [Clocks](architecture/reference-clocks.svg) · [Power tree](architecture/power-interfaces.svg)

The clock diagram shows the intended DDR interface; the dashed GPIO16/CLK_IO connection is a retained dual-input fallback.

## Parts

| Function | Current device |
|---|---|
| MCU / flash | RP2350B A4 (SC1510-A4), W25Q128JVSIQ; [RP2350 hardware guide](https://datasheets.raspberrypi.com/rp2350/hardware-design-with-rp2350.pdf) |
| Reference / fanout | ECS-TXO-2520MV-120-AN-TR, LMK1C1104PWR |
| DAC / IQ modulator | [AFE7071IRGZT](https://www.ti.com/product/AFE7071) |
| LO | [LMX2572RHAT](https://www.ti.com/lit/ds/symlink/lmx2572.pdf) |
| DAC clock | GPIO28 continuous PIO → SN65LVDM31DR on AFE3V3; intended DDR32/64 MHz |
| RF driver | GRF2013, optional |
| Input | GCT USB4105-GF-A-060, TPS25940ARVCR eFuse |
| Buck | TPS62441QWRQRRQ1: DIG3V3 and PRE2V5 |
| Quiet supplies | TPS7A8801QRTJRQ1: AFE3V3 / AFE1V8; 2×TPS7A2133PQWDRBRQ1: LO3V3 / REF3V3 |
| Reset / watchdog | TPS386000RGPT planned, not captured; RGPR differs only in reel quantity |
| RF driver supply | TPS22810TDBVRQ1 load switch; separate from DAC-clock enable |

This first PCB is also the compact Yapogee module. Castellated contacts and small top-side solder pads provide carrier attachment and bring-up access. Contact layout and underside clearance are still open. These are the working parts, not a released BOM. The [KiCad project](board/Yapogee-Devboard/Yapogee-Devboard.kicad_pro) loads the local [symbols, footprints and models](../libraries/README.md). Capture is underway; layout and hardware testing are still ahead.

## How it fits together

**Power:** USB-C or EXT_5V → eFuse → protected 5 V. The dual buck makes DIG3V3 and PRE2V5; PRE2V5 feeds the AFE's 1.8 V LDO. The three quiet 3.3 V outputs come from protected 5 V. Reset/watchdog and clock interlocks remain to capture; AFE LDO power-good alone does not qualify clock permission. Rail test points and the eFuse current signal support bring-up.

Use a verified 5 V / 3 A source for this eval board. The eFuse retries automatically; reverse-polarity protection is not provided. Each CC pin has a 5.1 kΩ pull-down; available USB current is not detected. A removable solder bridge disconnects USB VBUS when EXT_5V powers the board.

**MCU:** SPI carries payload data; USB handles programming and test access. The benchmark uses GPIO17 SCK, 18 MOSI, 19 CS_N and 22 READY; the board interface is still being captured. SWD, BOOTSEL, RUN and LEDs support bring-up, with isolated I/Q pads planned.

**LO and clocks:** keep the 12 MHz TCXO/LMK1C1104 fanout and full LMX2572. At SYS128, 8/16 Msym/s at four SPS uses DDR32/64 MHz on GP28 and 64/128 Mword/s on the bus. Start the independent PIO clock and writers atomically; the AFE FIFO is bypassed and CLK_IO stays unused in DDR. Preserve CLK_IO and optional GP16/HSTX links for bring-up, with one clock source fitted. PWM remains a same-GP28 trial. Loaded timing, startup, power loss and jitter remain to verify. External reference/LO injection and the LO pad/filter remain assembly options.

**Clock support:** capture the SN65's 100 Ω termination before two 10 nF coupling caps, 1 kΩ across the AFE clock pins after them, disabled-source prebias and DNP damping pads. Use a separate default-off clock request/interlock; `DRIVER_EN` controls the GRF supply. The receiver network and interlock are intended evaluation circuitry, not qualified hardware. Recount AFE3V3 current with the SN65 before freezing the BOM; CDCE and its dedicated I²C isolation remain omitted.

**IQ and RF:** assembly links select raw AFE output or the GRF2013 driver. Populate one top-mounted SMA first; the compact external-LO connector stays DNP. Leave space for a removable shield and accessible bodge pads. Castellated edges attach the module to its carrier; the outline and contact assignments are still open.

The project separates USB, RF/LO, clocks, I/Q, SPI, flash, power and sensitive analog nets. Impedance intent is 90 Ω differential for USB and 50 Ω for RF/LO and controlled CMOS routes; the conditional DAC-clock pair has its own 100 Ω class. Geometry awaits the stackup. CMOS source damping is separate from trace impedance.

## Models

Run from the repo root with Python 3:

```sh
python3 hardware/simulations/link_budget.py
python3 hardware/simulations/reference_lo_loop_screen.py
python3 hardware/simulations/dac_clock_budget.py
```

The link model writes tables and JSON to `hardware/simulations/output/`; the other two print JSON. The DAC-clock calculator covers the retained dual-input SDR/FIFO model. These calculations do not establish DDR startup, measured RF performance or loaded clock timing.
