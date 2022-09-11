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
