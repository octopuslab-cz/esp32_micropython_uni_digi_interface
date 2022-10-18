# octopusLAB UDI-22

(esp32_micropython_universal_digital_interface)

for revival / commissioning / **testing** / simulation / emulation / ... **8-bit computers**, **microprocesors**, RAM, ROM, I/O ports...

## 4-bit (Intel 4004 - 1970) version

https://github.com/octopuslab-cz/micropython_4004-emul


## 8-bit: 8008/8060/8080/8085/Z80 (intel/Zilog)
- Univac 8008 (1972)
- **Altair 8800** (1974)
- **MK14** (1977)
- ...
- 
## 8-bit: 6502 (Motorola)
- MOS Kim 1 - 6502 (1976)
- Apple 1 - 6502, 2/4kB (1976) 
- Atari 400/800 - 6502, 4/8kB (1979)
- ...
---

```
                             +-----------+         +-------------------+
  +--------------+           |           |         |  8-digit display  |
  |  addr 16-bit |-- A16 --->| I2C       |         |        SPI        |
  +--------------+           | expanders |         +-------------------+
                             |           |--I2C--->|   ** ESP32 **     |            
  +--------------+           |    LEDs   |         |  UART/USB serial  |
  |  data 8-bit  |-- D8 <--->|  2x8 + 8  |         |      WiFi/BLE     |
  +--------------+           |           |         |    ext.display    |
                             +-----------+         +-------------------+
                                    



--- address --- 16-bit (expander OUT - LED, conector)

A00-A07
A08-A15

--- data --- 8-bit (OUT/IN - LED/BTN, conector)

D00-D07

```




### udim.py

```
UDI Monitor 0.2 OctopusLAB 2016-22
> h
---------------------------------------
 Universal Digital Interface - Monitor
 HELP
---------------------------------------
Copy         C <start> <end> <dest>
Dump         D <start>
Go           G <address>
Help         H
Clear screen L
Info         I
Options      O
Read         R <address>
Write        W <address> <data>
---------------------------------------


UDI Monitor 0.2 OctopusLAB 2016-22
> d 0

0000  8b  e3  1f  d9  87  9d  7b  1f  71  6b  63  21  d5  fb  4b  e3
0010  ff  3d  fd  e7  fb  13  f1  0b  e3  fb  01  f3  e3  5f  73  6b
0020  8b  e3  1f  d9  87  9d  7b  1f  71  6b  63  21  d5  fb  4b  e3
0030  ff  3d  fd  e7  fb  13  f1  0b  e3  fb  01  f3  e3  5f  73  6b
0040  8b  e3  1f  d9  87  9d  7b  1f  71  6b  63  21  d5  fb  4b  e3
0050  ff  3d  fd  e7  fb  13  f1  0b  e3  fb  01  f3  e3  5f  73  6b
0060  8b  e3  1f  d9  87  9d  7b  1f  71  6b  63  21  d5  fb  4b  e3
0070  ff  3d  fd  e7  fb  13  f1  0b  e3  fb  01  f3  e3  5f  73  6b

```


### components/processor/s80 - emulator

```
s80
-----------------

+-----------+
|    P C    |   program counter
|    S P    |   stack pointer
+-----------+
+-----+
|  A  |  F      accumulator ↑ flags
+-----+-----+
|  B  |  C  |   system registers
+-----+-----+
|  H  |  L  |
+-----+-----+

-----------------
F - Flag:

| | | |A| | | | |
|S|Z|0|C|0|P|1|C|

sb S  State of Sign bit
zb Z  State of Zero bit
   0  always 0
AC    State of auxiliary Carry bit
   0  always 0
pb P  State of Parity bit
   1  always 1
cb C  State of Carry bit
```


---

## Inspitation and lins


https://github.com/GodTamIt/assembler

https://github.com/ept221/8085-Assembler

https://github.com/simonowen/pyz80

https://github.com/cburbridge/z80

https://github.com/dj-on-github/py6502

https://github.com/parasj/python-assembler

http://popolony2k.com.br/xtras/programming/asm/nemesis-lonestar/8080-z80-instruction-set.html

http://www.emulator101.com/reference/8080-by-opcode.html

https://wikijii.com/wiki/Intel_8080
