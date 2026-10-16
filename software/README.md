# Software

The PV-SPI data path is **host MPEG-TS → SPI/READY reception → RP2350 BB framing, scrambling, BCH/LDPC, QPSK/PL framing → RRC pulse shaping → interleaved 14-bit I/Q → AFE7071**. The two cores share encoding and sample production for DMA/PIO output; resource allocation depends on the selected backend. A separate generic benchmark input accepts already coded QPSK symbols.

The current implementation lives in [RP2350_IQ_Benchmark](https://github.com/Rivercraft911/RP2350_IQ_Benchmark). Planning models used revision `354ff2d`. **No benchmark firmware is imported here yet.** The later import will select and review the clean implementation rather than copy experimental branches and logs.

## Timing and interfaces

PV-SPI v1 uses SPI mode 0, MSB first: GP17 SCK, GP18 MOSI and GP19 CS_N inward; GP22 READY outward. GP20 MISO is reserved/undriven and GP21 unused in that mode. Each 1332-byte transfer contains a 12-byte header, seven 188-byte TS slots/padding and a 4-byte CRC32. Check READY immediately before transfer and hold CS high at least 10 µs between messages. **READY means receive-slot admission, not RF readiness.** Packet continuity/PCR remain host responsibilities. See the benchmark [host-link](https://github.com/Rivercraft911/RP2350_IQ_Benchmark/blob/354ff2ddb0f83c0b7dc1d302e056a93b191298ec/docs/host-link.md) and [protocol](https://github.com/Rivercraft911/RP2350_IQ_Benchmark/blob/354ff2ddb0f83c0b7dc1d302e056a93b191298ec/docs/pv-spi-spec.md).

| Four-SPS profile | Symbol rate | DAC per channel | Interleaved bus | DDR DACCLK | Clock/writer divider at SYS128 |
|---|---:|---:|---:|---:|---:|
| IREC nominal | 8 Msym/s | 32 MS/s | 64 Mword/s | 32 MHz | 2 |
| Ground experiment | 16 Msym/s | 64 MS/s | 128 Mword/s | 64 MHz | 1 |

SYS is `12 × 128 / (6 × 2) = 128 MHz`. GPIO0–13 carry data; GPIO14 remains IQ_FLAG for diagnostics/fallback. In DDR the AFE captures I on rising DACCLK and Q on falling edges, bypassing its FIFO. GPIO16 CLK_IO is retained for fallback and stays high-impedance in DDR. GPIO15/SYNC_SLEEP is retained; DDR DSP synchronization can use SPI instead of an in-band pulse. Lower-rate satellite and two-SPS profiles need their own reviewed clock/filter settings.

The intended GP28 clock loop is `nop side 1; nop side 0`, with no FIFO/DMA dependency. Start its PIO0 state machine and the PIO2 writers together using the SDK's atomic cross-PIO enable/divider restart; use equal integer dividers and start with clock-high/I0. Prefill every writer FIFO and OSR and restore its complete PC/X state. Following a stall, disable SN65 before stopping the clock, quiesce DMA and rebuild the full stream; resume or `SM_RESTART` alone does not restore ordering. This integration is not yet implemented here.

PWM6A on GP28 remains an alternative: its 32/64 MHz rates fit, but a WAIT or self-training sequence needs qualified GPIO-feedback latency. Dual-input/FIFO mode remains a bring-up fallback with separate CLK_IO and twice-per-DAC-rate conversion clock; its initialization and cumulative slip limits do not apply to DDR. Receiver timing, analog enable/settling, partial power and RF remain unqualified.

The coded QPSK format packs 16 symbols per `uint32`: I bits [15:0], Q bits [31:16], with bit b mapping to 1−2b. Output slots contain signed 14-bit data in bits [13:0], IQ_FLAG in bit14 and reserved SYNC/control bit15. AFE reset selects offset binary (`0x2000` zero); explicitly select two's complement before using `0x0000` as zero. The examined four-writer allocation with the added clock fits 11/12 state machines; the clock adds two PIO words and no DMA channel. Other backends require their own allocation review.

Module control must initialize request pins low, service a meaningful watchdog early, configure/read back the AFE and clock while RF is inhibited, then release RF through a qualified arm sequence. Keep clock permission separate from the RF-amplifier supply enable. Hot sample streaming uses internal SRAM; PSRAM is optional. Host isolation, power faults and recovery still need board verification.

## Models

[Waveform levels](simulations/waveform_levels.py) requires Python 3, NumPy and a separate benchmark checkout:

```sh
python3 software/simulations/waveform_levels.py --benchmark /path/to/RP2350_IQ_Benchmark
```

It reads the supplied reference model, compares interpolation profiles, and reports mean/sample crest values plus the source hash and runtime versions. Verify the source against revision `354ff2d` before comparing with [saved planning results](simulations/waveform_levels_planning.json). These values describe digital samples before analog reconstruction.

Future software work belongs here: board definitions, reviewed sample/control implementation, host interface, tests and simulations. The pinned snapshot is a reference containing measurement records, not the flashed revision for every measurement. A new board profile and the continuous video mode need end-to-end timing, spectral and decoder verification; digital bench evidence does not establish Yapogee analog/RF performance or flight acceptance.
