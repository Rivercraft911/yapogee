# Yapogee

Welcome, welcome, welcome! I went looking for a small, affordable QPSK transmitter and couldn't find what I wanted. So we're making one. Meet Yapogee: a little USB-C/SPI board that is ready to yap.

The plan: RP2350B handles DVB-S2 encoding and, through the power of PIO, sends I/Q samples to an AFE7071. A shared reference, LMX2572 LO and optional small driver get us to RF. IREC at 1.28 GHz comes first; 2.4 GHz satellite work reuses the core with a different external PA and filter.

![System overview](hardware/architecture/system-overview.svg)

Dashed lines are assembly options. GPIO28 feeds the AFE through the SN65LVDM31DR capture target: DDR at 32/64 MHz for 8/16 Msym/s with four samples per symbol. Loaded timing, startup and power-loss behavior still need verification. See the [dev-board guide](hardware/devboard/README.md).

For N samples per symbol, `f_IQ = N × R_s` and the interleaved bus runs at `f_bus = 2 × f_IQ`. The intended interface is continuous PIO + DDR: at SYS128 and N=4, 8/16 Msym/s uses 32/64 MHz DACCLK and 64/128 Mwords/s. Clock and data writers start atomically. This costs one internal state machine and two instructions, with no added phase hardware. PWM remains a same-pin experiment; module firmware and loaded AFE operation are unqualified.

| Area | Contents |
|---|---|
| [Hardware](hardware/README.md) | Initial dev board, future transmitter board and hardware models |
| [Software](software/README.md) | Data path, timing, reference models and future cleaned firmware |

Schematic capture is underway in [KiCad](hardware/devboard/board/Yapogee-Devboard/Yapogee-Devboard.kicad_pro), with a local [component library](hardware/libraries/README.md). Firmware will come from a cleaned import of the [digital benchmark](https://github.com/Rivercraft911/RP2350_IQ_Benchmark). The RF board hasn't been built yet.
