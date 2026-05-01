# Example/Test I2C EEPROM 24C02
# (c) OctopusLAB 2016-26 - MIT


from octopus_lib import i2c_init
from components.i2c_eeprom_24xxx import EEPROM24x
from octopus_digital import hex_dump

i2c = i2c_init()
memory = EEPROM24x(i2c, 80, "24x02")
TEST_WRITE = False

# ── KROK 1: zápis (spusť jednou, pak zakomentuj) ──────────
save_string = "test 2026 abc xyz"
print("[--- write ---]")
print("TEST_WRITE:",TEST_WRITE)

for addr, ch in enumerate(save_string):
    if TEST_WRITE:
        memory.write_byte(addr, ord(ch))
    print(f"  [{addr:03d}] '{ch}' = 0x{ord(ch):02x}")

# ── KROK 2: čtení zpět jako string ────────────────────────
print("[--- read string ---]")
result = ""
for i in range(len(save_string)):
    b = memory.read_byte(i)
    val = b[0] if isinstance(b, (bytes, bytearray)) else ord(b)
    result += chr(val)
print("->", result)

# ── KROK 3: hex_dump prvních 48 bajtů (3 řádky) ──────────
print("[--- hex_dump ---]")
buf = []
for i in range(48):
    raw = memory.read_byte(i)
    buf.append(raw[0] if isinstance(raw, (bytes, bytearray)) else ord(raw))
hex_dump(buf, row=3, addr=0, show_ascii=True)


"""
[--- write ---]
TEST_WRITE: False
  [000] 't' = 0x74
  [001] 'e' = 0x65
  [002] 's' = 0x73
  [003] 't' = 0x74
  [004] ' ' = 0x20
  [005] '2' = 0x32
  [006] '0' = 0x30
  [007] '2' = 0x32
  [008] '6' = 0x36
  [009] ' ' = 0x20
  [010] 'a' = 0x61
  [011] 'b' = 0x62
  [012] 'c' = 0x63
  [013] ' ' = 0x20
  [014] 'x' = 0x78
  [015] 'y' = 0x79
  [016] 'z' = 0x7a
[--- read string ---]
-> test 2026 abcxy G
[--- hex_dump ---]
0000  74  65  73  74  20  32  30  32  36  20  61  62  63  78  79  20  'test 2026 abcxy '
0010  47  42  41  52  20  47  4c  43  56  20  4f  45  42  50  20  3f  'GBAR GLCV OEBP ?'
0020  65  74  63  20  ff  ff  ff  ff  ff  ff  ff  ff  ff  ff  ff  ff  'etc ÿÿÿÿÿÿÿÿÿÿÿÿ'
"""