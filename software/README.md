# Software

The PV-SPI data path is **host MPEG-TS → SPI/READY reception → RP2350 BB framing, scrambling, BCH/LDPC, QPSK/PL framing → RRC pulse shaping → interleaved 14-bit I/Q → AFE7071**. Core 1 performs DVB-S2 encoding; core 0 generates samples for chained DMA/PIO output. A separate generic benchmark input accepts already coded QPSK symbols.

The current implementation lives in [RP2350_IQ_Benchmark](https://github.com/Rivercraft911/RP2350_IQ_Benchmark). Planning models used revision `354ff2d`. **No benchmark firmware is imported here yet.** The later import will select and review the clean implementation rather than copy experimental branches and logs.

## Timing and interfaces

PV-SPI v1 uses SPI mode 0, MSB first: GP17 SCK, GP18 MOSI and GP19 CS_N inward; GP22 READY outward. GP20 MISO is reserved/undriven and GP21 unused in that mode. Each 1332-byte transfer contains a 12-byte header, seven 188-byte TS slots/padding and a 4-byte CRC32. Check READY immediately before transfer and hold CS high at least 10 µs between messages. **READY means receive-slot admission, not RF readiness.** Packet continuity/PCR remain host responsibilities. See the benchmark [host-link](https://github.com/Rivercraft911/RP2350_IQ_Benchmark/blob/354ff2ddb0f83c0b7dc1d302e056a93b191298ec/docs/host-link.md) and [protocol](https://github.com/Rivercraft911/RP2350_IQ_Benchmark/blob/354ff2ddb0f83c0b7dc1d302e056a93b191298ec/docs/pv-spi-spec.md).

| Profile | Symbol rate | DAC per I/Q channel | Interleaved bus / continuous DACCLK | SYS / cpw |
|---|---:|---:|---:|---|
| IREC initial | 8 Msym/s | 32 MS/s | 64 MHz | 128 MHz / 2 |
| Satellite initial | 1 Msym/s | 8 MS/s | 16 MHz | 128 MHz / 8 |
| Satellite video candidate | 4 Msym/s | 16 MS/s | 32 MHz | 128 MHz / 4 |

SYS is `12 × 128 / (6 × 2) = 128 MHz`. GPIO0–13 carry data; GPIO14 is IQ_FLAG and GPIO16 CLK_IO. GPIO15 is spare in the benchmark and proposed for module SYNC_SLEEP. The data strobe may stall. A separate FIFO-free PIO loop on GPIO28 with integer divider 1/2/4 is the proposed continuous 64/32/16 MHz DAC clock; compare against CDCE6214 before adopting it. Receiver swing/bias and startup/rate-change synchronization remain hardware gates.

The internal coded-symbol format packs 16 QPSK symbols per `uint32`: I bits [15:0], Q bits [31:16], with bit b mapping to 1−2b. Output slots contain signed 14-bit data in bits [13:0], IQ_FLAG in bit 14 (I=1, Q=0) and bit 15=0. Benchmark output uses two PIO0 state machines and three DMA channels; PV-SPI claims three PIO2 state machines and three DMA channels. A spare PIO0 state machine is available for the proposed continuous clock.

Module control must initialize request pins low, service a meaningful watchdog early, perform AFE/clock/FIFO setup while RF is muted, sequence PA request→PA_READY→LO calibration→RF release, and handle bounded faults/recovery. Hot sample streaming uses internal SRAM; PSRAM is optional. New host isolation and partial-power behavior need board verification.

## Models

[Waveform levels](simulations/waveform_levels.py) requires Python 3, NumPy and a separate benchmark checkout:

```sh
python3 software/simulations/waveform_levels.py --benchmark /path/to/RP2350_IQ_Benchmark
```

It reads the supplied reference model, compares interpolation profiles, and reports mean/sample crest values plus the source hash and runtime versions. Verify the source against revision `354ff2d` before comparing with [saved planning results](simulations/waveform_levels_planning.json). These values describe digital samples before analog reconstruction.

Future software work belongs here: board definitions, reviewed sample/control implementation, host interface, tests and simulations. The pinned snapshot is a reference containing measurement records, not the flashed revision for every measurement. A new board profile and the continuous video mode need end-to-end timing, spectral and decoder verification; digital bench evidence does not establish Yapogee analog/RF performance or flight acceptance.
