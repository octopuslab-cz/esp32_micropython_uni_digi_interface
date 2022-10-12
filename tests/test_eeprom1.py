from machine import Pin, I2C
from time import sleep, sleep_ms
from micropython import const
from octopus_digital import bin_str_to_int, num_to_bin_str8, hex_to_str
from octopus_digital import num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from octopus_digital import char_to_hex, hex_dump


data_256 = bytearray(256)
print(data_256)
str_result = ""


def i2c_init(HW_or_SW=0,freq=100000):
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
self._AC1 = unp('>h', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xAA, 2))[0]
self._bmp_i2c.writeto_mem(self._bmp_addr, 0xF4, bytearray([0x2E]))
"""

EEPROM_ADDR = 80


def eeprom_write(addr, data):
    i2c.writeto_mem(EEPROM_ADDR, addr, data)
    sleep_ms(10)


def eeprom_read(addr):
    data = i2c.readfrom_mem(EEPROM_ADDR, addr, 1)
    return data


def eeprom_read_block(addr, num=8):
    data = i2c.readfrom_mem(EEPROM_ADDR, addr, num)
    return data

def eeprom_read_256():
    global data_256
    for i in range(16): # 8*8=64 // 16*8=128 //
        ### data = i2c.readfrom_mem(EEPROM_ADDR, i*8, 8)
        data = eeprom_read_block(i*8,8)
        # byte =  eeprom_read(i)
        # data_256[i] = byte
        a = 0
        for byte in data:
            ##print(i*8+a,hex(byte))
            data_256[i*8+a] = byte
            a += 1
        

def eeprom_write_string1(s2w):
    i=0
    for s in s2w:
        addr = i
        data = bytearray([ord(s)]) # bytearray([30+i*2])
        eeprom_write(addr, data)
        print(addr,data)
        i += 1

"""
print("test read")
test_data = i2c.readfrom_mem(EEPROM_ADDR, 0x00, 2)
print(test_data)
sleep(0.5)
"""


"""
print("test read")
#test_data = i2c.readfrom_mem(EEPROM_ADDR, 0x00, 8)
test_data = eeprom_read_block(0x00, 2)
print(test_data)
sleep(0.5)
"""

"""
print("test write 32")
#i2c.writeto_mem(EEPROM_ADDR, 0x00, new_data0)
for i in range(32):
    addr = i
    data = bytearray([30+i*2])
    eeprom_write(addr, data)
    print(addr,data)
"""

"""
print("eeprom_write_string1")
#     "01234567890123456789012345678901" //32
s2w = "tr3ti zapis nejakeho retezce 123" # string to write // s2w

eeprom_write_string1(s2w)
"""

print("test read 32")
#i2c.writeto_mem(EEPROM_ADDR, 0x00, new_data0)
for addr in range(32):
    print(addr,eeprom_read(addr))

print("> eeprom_read_256()")
eeprom_read_256()

print()
print("> hex_dump")
hex_dump(data_256, show_ascii=True)
