# AFE clock interface

The first board uses AFE7071 **dual-input clock mode**. The frequency plan is established and nominal parallel-bus timing is derived; the differential receiver circuit remains conditional. This sheet is a schematic design contract, not a qualified circuit or fabrication release.

## Frequency and data path

The shared 12 MHz reference drives the MCU and comparison synthesizer. With MCU SYS128 MHz:

| Profile | CLK_IO and DACCLK | Sample rate per I/Q channel | Data PIO cpw | Continuous-clock PIO divider |
|---|---:|---:|---:|---:|
| IREC | 64 MHz | 32 MS/s | 2 | 1 |
| Video candidate | 32 MHz | 16 MS/s | 4 | 2 |
| Initial satellite | 16 MHz | 8 MS/s | 8 | 4 |

GPIO0–13 carry D0–13; GPIO14 is IQ_FLAG, GPIO15 is synchronous SYNC_SLEEP, and GPIO16 is CLK_IO. Share DIG3V3 with AFE IOVDD. GPIO28 is reserved for a separate FIFO-free continuous PIO clock. The proposed source needs board firmware and measurements. Retain CDCE6214RGET as the comparison/recovery source for the first board. CLK_IO can stall with the data state machine and must not be the only conversion-clock source.

AFE DACCLKP/N are pins 1/2 and refer to CLKVDD18, pin 3. In the chosen mode, DACCLK and CLK_IO must be frequency locked; the FIFO absorbs initial phase, not sustained frequency error. SYNC_SLEEP requires a synchronous pulse encoded by the data PIO, since GPIO15 is part of its output word. Keep alarm/readback on its own GPIO31 net. ALARM_SDO is active-low in alarm mode; four-pin SPI repurposes it as SDO. [AFE7071 pin, timing, register and clock descriptions](https://www.ti.com/lit/gpn/AFE7071).

## Differential frontend decision

**Do not freeze LMK1D1204PRHDT as the production driver yet.** Its individual hardware OE and 1.8 V operation suit the power/inhibit architecture. Its specified 250–450 mV VOD, however, means 500–900 mV differential peak-to-peak. AFE clock duty must be 40–60%. The AFE's 0.4–1 V row does not define which amplitude convention it uses or give a supported common-mode range. The EVM guide uses LVPECL and a 100 Ω differential termination, but the detailed EVM clock schematic has not been recovered. Old IBIS thresholds do not supply a receiver-bias guarantee. [Exact P buffer](https://www.ti.com/lit/ds/symlink/lmk1d1204p.pdf), [AFE EVM guide](https://www.ti.com/lit/ug/slou337a/slou337a.pdf).

Draft the frontend as an explicitly conditional sheet with:

- Exclusive PIO/CDCE source selection and short inactive branches. No wired clock-output junction.
- Receiver-side 100 Ω termination and space for a selected coupling/bias network. DNP options are experiments; neither AC coupling nor a guessed midpoint proves compatibility.
- A destination-powered inhibit stage. The conditional P buffer and its OE logic share the **same physical CLKVDD18 domain** as the AFE. Avoid independently held-up clock islands.
- Hardware-low actual OE at boot/reset/fault; destination-powered logic translates 3.3 V requests into the 1.8 V control domain. Disable unused outputs explicitly.
- Coherent external-clock access through the reviewed frontend where possible, and short ground-referenced probe pads near the AFE. Direct receiver injection is a powered-only laboratory path requiring its own electrical review.

Changing to an LVPECL driver is not automatically a solution: its supply, termination, common mode, startup and power-off behavior must also be closed. Receiver testing or recovered manufacturer circuit evidence must select the actual driver and population before fabrication. A fixture result establishes the tested operating conditions; it does not create a missing manufacturer guarantee.

## Timing and startup

At the fastest profile the current PIO launch convention gives nominal 7.8125 ns setup and hold. AFE requires at least 1 ns of each and a 3 ns CLK_IO high pulse. The combined pad/package/route/edge/jitter error must fit that budget. The adopted receiver measurement target is at least 3 ns setup/hold; this is engineering margin. Source damping and actual-stackup SI analysis choose resistor values and routing limits.

The [timing calculator](../simulations/dac_clock_budget.py) reproduces the nominal arithmetic and relative-frequency drift. At 10 ppm differential error, four cycles accumulate in only 6.25 ms at 64 MHz. External injection must be truly coherent with the MCU data clock. The four-cycle FIFO scale is not a permitted data-stall interval.

Keep RF muted and AFE reset during source configuration. Establish a valid continuous clock and idle data, configure the AFE, synchronize its FIFO and clear/check alarms before permitting RF. Rate/source changes and stalls require mute and resynchronization. Clock permission is independent of PA arm so the core can be configured with the PA absent.

Before selecting the production population, compare PIO/CDCE at equal receiver waveform and RF settings. Check differential/common-mode voltage, duty, setup/hold, startup and partial-power waveforms, then decoded errors, EVM, spurs and output mask under real host/USB/flash activity. Retain the same short core topology on later boards; remove comparison hardware only after these measurements justify it.
