# octopusLAB - universal digital interface for microprocesor / EEPROM / Etc.
__version__ = "0.2.1" #

from machine import Pin, I2C
from time import sleep, sleep_ms
from micropython import const
from octopus_digital import neg, reverse, int2bin, get_bit, set_bit

"""
num_to_hex_str4(1325)     # '052d'
int_to_bin_str8(22)       # '00010110'
bin_str_to_int("1010101") # 85
num_to_bytes2(255)        # bytearray(b'\x00\xff')
num_to_bytes2(0b1111111111111111) # bytearray(b'\xff\xff')
"""

PORT_REVERSE = True
# Expander: PCF8574 - 8-bit
# Expander: PCF8575 - 16-bit

# addr16: 000 = 39
# e8 = Expander8(addr) addr default 000 > 0x20
# from utils.i2c_expander import Expander8

# num_to_bytes(reverse(b1))   >   '10011111'

"""
# bytearray
b = bytearray(2)
b[0] = 255 # int    # bytearray(b'\xff\x00')
str(hex(b[0]))[2:]  # "ff"

b = b'abc'
b.decode('utf-8')
"""

# -------------------------------
class Universal_interface:
    def __init__(self, hw=1):
        self.hw = hw # hw ver 1+ / 2config
        self.i2c = i2c_init()
        
        # ===== pinouts =====             
        self.sensor = None
        
        # ===== expander address =====
        self.ADDR08 = const(55)  # 555
        self.ADDR16 = const(39)  # 000 addr
        self.ADDR16d = const(38) # 001 data
    
    def set_temp1(self, value):
        self.temp1 = value
    
    
    def write16(self,bytes2):
        self.i2c.writeto(self.ADDR16, bytes2)
        
        
    def read16(self):
        #self.i2c.writeto(self.ADDR16, bytes2)
        bytes2 = None
        return bytes2
    
    
    def read16d(self):
        bytes2 = self.i2c.readfrom(self.ADDR16d,2) # bus size 16 bits = 2 Bytes
        return bytes2
    

# -----------------------------------
def i2c_init(HW_or_SW=0,freq=300000): # 2000000 ok
    # from utils.pinout import set_pinout
    # pinout = set_pinout()
    I2C_SDA_PIN, I2C_SCL_PIN = const(21), const(22)
    # HW_or_SW: HW 0 | SW 1
    i2c = I2C(HW_or_SW, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=freq)
    return i2c


def int_to_exp_1byte(i): # expander
    tmp = bytearray(2)    
    #b = str(hex(reverse(i)))[1:]
    #print(f'{(1):02d}')    
    a = reverse(i+256)    
    #int("{0:#0{1}x}".format(11,4))
    #b = "{0:#0{1}x}".format(i,4)
                     
    # return b.encode()
    tmp[1] = a
    return tmp


def int_to_bin_str8(i):
    # bin8_str = bin(num)[2:]
    return f"{i:08b}"


def int_to_bin_str16(i):
    return f"{i:16b}"


def bin_str_to_int(s):
    bs = "0b"+s
    return(int(bs))


@micropython.native
#@micropython.viper
def num_to_bytes2(i,rev=PORT_REVERSE):
    tmp = bytearray(16 // 8) # 2
    if rev:
        if i >= 256: tmp[0] = reverse(i // 256)     
        a = reverse(i+256)
    else:
        if i >= 256: tmp[0] = i // 256    
        a = i+256
        
    tmp[1] = a
    return tmp


def num_to_hex_str4(i):
    # hex_str = str(hex(i))[2:]
    return f"{i:04x}"


def num_to_hex_str2(i): 
    # data 8bit / 1 byte / XX
    return f"{i:02x}"
