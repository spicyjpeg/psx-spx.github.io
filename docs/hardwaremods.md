
# Hardware Mods

- [Nocash BIOS "chipless" modchip](#nocash-bios-chipless-modchip)
- [Nocash PAL/NTSC composite color fixes](#nocash-palntsc-composite-color-fixes)

## Nocash BIOS "chipless" modchip

_Credit: Martin Korth / nocash_

The nocash kernel clone outputs a SCEX signal via A20 and A21 address lines,
(so one won't need a separate modchip/microprocessor):

```
  A20 = the normal SCEX signal (inverted ASCII, eg. "A" = BEh)   ;all boards
  A21 = uninverted SCEX signal (uninverted ASCII, eg. "A" = 41h) ;PU-7..PU-20
  A21 = always 1 during SCEX output                              ;PU-22 and up
```

When using the clone bios as internal ROM replacement, A20 can be used with
simple wires/diodes. Doing that with external expansion ROMs would cause the
console to stop working when unplugging the ROM, hence needing a slightly more
complex circuit with transistors/logic chips.

### External Expansion ROM version, for older boards (PU-7 through PU-20)

```
              .--------.-.                 .--------.-.
  GATE--------|C  NPN  |  .    DATA--------|C  NPN  |  .
  A20--[10K]--|B  BC   |  |    A21--[10K]--|B  BC   |  |
  GND---------|E  547  |  '    GND---------|E  547  |  '
              '--------'-'                 '--------'-'
```

### External Expansion ROM version, for newer boards (PU-22)

```
         .-------------------.
  A21----|OE1,OE2            |
  A20----|IN1   74HC126  OUT1|--- DATA
  WFCK---|IN2            OUT2|--- SYNC
         '-------------------'
```

### Internal Kernel ROM version, for older boards (PU-7 through PU-20):

```
  GATE---------GND
  DATA---------A20
```

### Internal Kernel ROM version, for newer boards (PU-22 through PM-41(2))

```
  SYNC--------WFCK
  DATA---|>|---A20
```

### What pin is where...

```
  GATE is IC703.Pin2  (?) (8pin chip with marking "082B")   ;PU-7? .. PU-16
  GATE is IC706.Pin7/10   (16pin "118" uPC5023GR-118)       ;PU-18 .. PU-20
  SYNC is IC723.Pin17(TEO)(20pin "SONY CXA2575N")           ;PU-22 .. PM-41(2)
  DATA is IC???.Pin7 (CG) (8pin chip with marking "2903")   ;PU-7? .. PU-16
  DATA is IC706.Pin1 (CG) (16pin "118" uPC5023GR-118)       ;PU-18 .. PU-20
  DATA is HC05.Pin17 (CG) (52pin "SONY SC4309xxPB")         ;PU-7 .. EARLY-PU-8
  DATA is HC05.Pin32 (CG) (80pin "SONY E35D, 4246xx 185")   ;LATE-PU-8 .. PU-20
  DATA is SPU.Pin42 (CEI) (208pin "SONY CXD2938Q")          ;PU-22 .. PM-41
  DATA is SPU.Pin36?(CEI) (176pin "SONY CXD2941R")          ;PM-41(2)
  WFCK is SPU.Pin5 (WFCK) (208pin "SONY CXD2938Q")          ;PU-22 .. PM-41
  WFCK is SPU.Pin84(WFCK) (176pin "SONY CXD2941R")          ;PM-41(2)
  A20  is CPU.Pin149(A20) (208-pin CPU CXD8530 or CXD8606)  ;PU-7 .. PM-41(2)
  A20  is EXP.Pin28 (A20) (68-pin Expansion Port)           ;PU-7 .. PU-22
  A21  is CPU.Pin150(A21) (208-pin CPU CXD8530 or CXD8606)  ;PU-7 .. PM-41(2)
  A21  is EXP.Pin62 (A21) (68-pin Expansion Port)           ;PU-7 .. PU-22
```

- GATE on PU-18 is usually IC706.Pin7 (but IC706.Pin10 reportedly works, too).
- GATE on PU-20 is usually IC706.Pin10 (but IC706.Pin7 might work, too).

## Nocash PSX-XBOO Upload

### Component List

```
  32pin socket for EPROM
  EPROM (or FLASH)
  74HC541 (8-bit 3-state noninverting buffer/line driver)
  1N4148 diode (for reset signal)
  1N4148 diode (for optional "modchip" feature)
  36pin Centronics socket for printer cable (or 25pin dsub)
```

### Nocash PSX-XBOO Connection (required)

```
  GND (BOARD)       --------- GND    (SUBD.18-25, CNTR.19-30)
  A16 (ROM.2)       --------- SLCT   (SUBD.13, CNTR.13)     ;\
  A17 (ROM.30)      --------- PE     (SUBD.12, CNTR.12)     ; 4bit.dta.out
  A18 (ROM.31)      --------- /ACK   (SUBD.10, CNTR.10)     ;
  A19 (ROM.1)       --------- BUSY   (SUBD.11, CNTR.11)     ;/
  /RESET            ---|>|--- /INIT  (SUBD.16, CNTR.31)     ;-reset.in
  D0..D7 (74HC541)  --------- DATA   (SUBD.2-9, CNTR.2-9)   ;\
  Y0..Y7 (74HC541)  --------- D0..D7 (ROM.13-15,17-21)      ; 7bit.dta.in, and
  /OE1 (74HC541.1)  --------- /EXP   (CPU.98)               ; 1bit.dta.clk.in
  /OE2 (74HC541.19) --------- /OE    (ROM.24)               ;
  GND  (74HC541.10) --------- GND    (BOARD)                ;
  VCC  (74HC541.20) --------- +5V    (BOARD)                ;/
```

### Nocash PSX-BIOS Connection (required)

```
  A0..A19 (ROM) --------- A0..A19 (EPROM)
  D0..D7  (ROM) --------- D0..D7  (EPROM)
  /BIOS (CPU.97)--------- /CS  (EPROM.22)
  /OE (ROM.24)  --------- /OE  (EPROM.24)
  +5V (BOARD)   --------- VCC  (EPROM.32)
  GND (BOARD)   --------- GND  (EPROM.16)
  /CS (ROM.22)  --/cut/-- /BIOS (CPU.97)
  /CS (ROM.22)  --------- +5V  (BOARD) (direct, or via 100k ohm)
```

### PSX-XBOO Upload BIOS

The required BIOS is contained in no$psx (built-in in the no$psx.exe file), the
Utility menu contains a function for creating a standalone ROM-image (file
PSX-XBOO.ROM in no$psx folder; which can be then burned to FLASH or EPROM).

### Pinouts

```
              ______  ______                      ____  ____
             |      \/      |                    |    \/    |
  A19,VPP12  | 1         32 |  VCC6         /OE1 |1       20| VCC
        A16  | 2         31 |  A18,/PGM       D0 |2       19| /OE2
        A15  | 3         30 |  A17            D1 |3       18| Y0
        A12  | 4         29 |  A14            D2 |4       17| Y1
         A7  | 5         28 |  A13            D3 |5 74541 16| Y2
         A6  | 6         27 |  A8             D4 |6       15| Y3
         A5  | 7         26 |  A9,IDENT12     D5 |7       14| Y4
         A4  | 8         25 |  A11            D6 |8       13| Y5
         A3  | 9         24 |  /OE,VPP12      D7 |9       12| Y6
         A2  | 10        23 |  A10           GND |10      11| Y7
         A1  | 11        22 |  /CE,(/PGM)        |__________|
         A0  | 12        21 |  D7
         D0  | 13        20 |  D6
         D1  | 14        19 |  D5
         D2  | 15        18 |  D4
        GND  | 16        17 |  D3
             |______________|
```

### Note

Instead of the above internal mod, the nocash kernel clone can be also
installed on cheat devices, which do also include DB25 connectors for parallel
port uploads, too.

For DB25 parallel port uploads, do the following mods to the cheat device:

```
 - Datel: use the FiveWire mod to get it parallel port compatible
 - Xplorer: simply wire DB25./INIT to EXP./RESET (with diode, if needed)
```

## Nocash PAL/NTSC composite color fixes

_Credit: Martin Korth / nocash_

The PSX hardware is more or less capable of generating both PAL and NTSC
signals. However, it's having the bad habbit to do this automatically depending
on the game's frame rate. And worse, it's doing it regardless of whether the
board is having matching oscillators installed (eg. a PAL board in 60Hz mode
will produce NTSC encoding with faulty NTSC color clock).

```
  color encoding    PAL             NTSC
  color clock       4.43361875MHz   3.579545MHz
  frame rate        50Hz            60Hz
```

### RGB Cables

RGB cables don't rely on composite PAL/NTSC color encoding, and thus don't need
any color mods (except, see the caution on GNDed pins for missing
53.20MHz/53.69MHz oscillators below).

### Newer Consoles (PU-22, PU-23, PM-41, PM-41(2))

These consoles have 17.734MHz (PAL) or 14.318MHz (NTSC) oscillators with
constant dividers, so the color clock will be always constant, and one does
only need to change the color encoding:

```
  /PAL (IC502.pin13) ---/cut/--- /PAL (GPU.pin157)
  /PAL (IC502.pin13) ----------- GND (PAL) or VCC (NTSC)
```

This forces the console to be always producing the desired composite color
format (regardless of whether the GPU is in 50Hz or 60Hz mode).

That works for NTSC games on PAL consoles (and vice-versa). However, it won't
work for NTSC consoles with PAL TV Sets (for that case it'd be easiest to
install an extra oscillator, as done on older consoles).

### Older Consoles (PU-7, PU-8, PU-16, PU-18, PU-20)

These consoles have 53.20MHz (PAL) or 53.69MHz (NTSC) oscillators and the GPU
does try to change the clock divider depending on the frame rate (thereby
producing a nonsense clock signal that's neither PAL nor NTSC). Best workaround
is to install an extra 4.43361875MHz (PAL) or 3.579545MHz (NTSC) oscillator
(with internal amplifier, ie. in 4pin package, which resembles DIP14, hence the
pin 1,7,8,14 numbering):

```
  GPU ------------------/cut/--- CXA1645M.pin6  SCIN
  GPU ------------------/cut/--- CXA1645M.pin7  /PAL
  Osc.pin14 VCC ---------------- CXA1645M.pin12 VCC (5V)
  Osc.pin7  GND ---------------- CXA1645M.pin1  GND
  Osc.pin8  OUT ---------------- CXA1645M.pin6  SCIN
  Osc.pin1  NC  --
  GND (PAL) or VCC (NTSC) ------ CXA1645M.pin7  /PAL
```

Caution: Many mainboards have solder pads for both 53.20MHz and 53.69MHz
oscillators, the missing oscillator is either GNDed or shortcut with the
installed oscillator (varies from board to board, usually via 0 ohm resistors
on PCB bottom side). If it's GNDed, remove that connection, and instead have it
shortcut with the installed oscillator.

Alternately, instead of the above mods, one could also install the missing
oscillator (and remove its 0 ohm resistor), so the board will have both
53.20MHz and 53.69MHz installed; that will produce perfect PAL and NTSC signals
in 50Hz and 60Hz mode accordingly, but works only if the TV Set recognizes both
PAL and NTSC signals.

### Notes

External 4.433MHz/3.579MHz osciallors won't be synchronized with the GPU frame
rate (normally you don't want them to be synchronized, but there's some small
risk that they might get close to running in sync, which could result in static
or crawling color artifacts).

For the CXA1645 chip modded to a different console region, one should also
change one of the resistors (see datasheet), there's no noticable difference on
the TV picture though.

### Region Checks

Some kernel versions contain regions checks (additionally to the SCEx check),
particulary for preventing NTSC games to run on PAL consoles, or non-japanese
games on japanese consoles. Some PAL modchips can bypass that check (by
patching the region byte in BIOS). Expansions ROMs or nocash kernel clone could
be also used to avoid such checks.
