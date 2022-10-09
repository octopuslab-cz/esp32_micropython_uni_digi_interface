# octopusLAB - universal digital interface for microprocesor / EEPROM / Etc.
__version__ = "0.2" # 2022/10/08

# from utils.bits import neg, reverse, int2bin, get_bit, set_bit

"""
hex_to_str(hex)
def char_to_hex(ch)
bin_str_to_int("1010101")         >>> 85
int_to_exp_1byte(i)
int_to_bin_str8(22)               >>> '00010110'
int_to_bin_str16(i)
num_to_bytes2(255)                >>> bytearray(b'\x00\xff')
num_to_bytes2(0b1111111111111111) >>> bytearray(b'\xff\xff')
num_to_hex_str4(1325)             >>> '052d'
num_to_hex_str2(i)

# bytearray
b = bytearray(2)
b[0] = 255 # int    # bytearray(b'\xff\x00')
str(hex(b[0]))[2:]  # "ff"

b = b'abc'
b.decode('utf-8')
"""

# num_to_bytes(reverse(b1))   >   '10011111'

PORT_REVERSE = False


def hex_to_str(h):
    return str(h)[2:]
    

def char_to_hex(ch):
    return hex(ord(ch))


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


#@micropython.viper
@micropython.native
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
