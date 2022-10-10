from machine import Pin, I2C
from time import sleep, sleep_ms
from micropython import const
from octopus_digital import bin_str_to_int, int_to_bin_str8, hex_to_str
from octopus_digital import num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from octopus_digital import char_to_hex


data_256 = bytearray(256)
print(data_256)
str_result = ""

"""
def hex2str(h):
    return str(h)[2:]
    

def ch2hex(ch):
    return hex(ord(ch))
"""

def i2c_init(HW_or_SW=0,freq=100000):
    # from utils.pinout import set_pinout
    # pinout = set_pinout()
    I2C_SDA_PIN, I2C_SCL_PIN = const(21), const(22)
    # HW_or_SW: HW 0 | SW 1
    i2c = I2C(HW_or_SW, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=freq)
    return i2c

print("i2c_init")
i2c = i2c_init()
print(i2c.scan())
# [80, 81, 82, 83, 84, 85, 86, 87]
# 34 expander / 73 therm. / 84 eeprom

"""
_bmp_addr = self._bmp_addr
self._bmp_i2c = i2c_bus
self._bmp_i2c.start()
self.chip_id = self._bmp_i2c.readfrom_mem(_bmp_addr, 0xD0, 2)
# read calibration data from EEPROM
self._AC1 = unp('>h', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xAA, 2))[0]

self._bmp_i2c.writeto_mem(self._bmp_addr, 0xF4, bytearray([0x2E]))

"""
EEPROM_ADDR = 87


def eeprom_write(addr, data):
    i2c.writeto_mem(EEPROM_ADDR, addr, data)
    sleep_ms(5)


def eeprom_read(addr):
    data = i2c.readfrom_mem(EEPROM_ADDR, addr, 1)
    return data


def eeprom_read_block(addr, num=8):
    data = i2c.readfrom_mem(EEPROM_ADDR, addr, num)
    return data

def eeprom_read_256():
    global data_256
    for i in range(2): # 256/8
        data = i2c.readfrom_mem(EEPROM_ADDR, i*8, 8)
        a = 0
        for byte in data:
            # print(i+a,hex(byte))
            data_256[i*8+a] = byte
            a += 1


"""
print("test read")
test_data = i2c.readfrom_mem(EEPROM_ADDR, 0x00, 2)
print(test_data)
sleep(0.5)
"""

"""
print("test write")
new_data0 = bytearray([0x01])
new_data1 = bytearray([0x02])
#i2c.writeto_mem(EEPROM_ADDR, 0x00, new_data0)
eeprom_write(0x0a, new_data0)
eeprom_write(0x0b, new_data1)
"""

"""
print("test read")
#test_data = i2c.readfrom_mem(EEPROM_ADDR, 0x00, 8)
test_data = eeprom_read_block(0x00, 2)
print(test_data)
sleep(0.5)
"""


"""
i = 0 # index  
for ch in range(48,128):
    hex_result[i] = ch
    # print(chr(ch), end="")
    str_result += chr(ch)
    # hex2str(hex(chr(ch)))
    i += 1

print("str_result", str_result)
print("hex_result", str(hex_result))


print("test hex dump")
s = "abc abc 123456789 ěščřžýááííé .,-*/-"


print("-"*30)

for x in str_result:
    print(x, int(ch2hex(x)), hex2str(ch2hex(x)))
"""
print("> eeprom_read_256()")
eeprom_read_256()
#print(data_256)

print()
print("> hex_dump")
addr = 0

for r in range(16):
    print()
    print(num_to_hex_str4(addr+r*16), end="")
        
    for i in range(16):
        bytes2 = num_to_bytes2(addr+r*16+i)
        #ui.i2c.writeto(39, bytes2)
        data8 = hex_to_str(hex(data_256[r*16+i])) #num_to_hex_str2(ui.read16d()[1])
        print(" ", data8, end="")
