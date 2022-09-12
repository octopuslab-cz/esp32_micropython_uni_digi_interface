# octopusLAB UDI

(esp32_micropython_universal_digital_interface)

for revival / commissioning / **testing** / simulation / emulation / ... **8-bit computers**, **microprocesors**, RAM, ROM, I/O ports...

## 8060/8080/8085/Z80 (intel/Zilog)
- Univac 8008 (1972)
- **Altair 8800** (1974)
- **MK14** (1977)
- ...
- 
## 6502 (Motorola)
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
