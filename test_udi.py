from time import sleep, sleep_ms
from random import randint
# from components.i2c_expander import Expander16
from utils.bits import neg, reverse, int2bin, get_bit, set_bit
from universal_digital_interface import Universal_interface
from universal_digital_interface import i2c_init, num_to_bytes, num_to_hex_str


ui = Universal_interface()

#i2c = i2c_init()
#print("init exp16")
#exp16 = Expander16(39)

print("test1") # ?!: xFF / 0xFF
for loop in range(3):
    #ue.i2c.writeto(39, b'\xFF\xFF')
    ui.write16(b'\xFF\xFF')
    #ue.write16(num_to_bytes(0b1111111111111111))
    #exp16.write(255)
    sleep(0.3)
    ui.write16(b'\x00\x00')
    #ue.write16(num_to_bytes(0))
    sleep(0.3)
    print(loop)


print("test2")
print(num_to_bytes(0))


for loop in range(5):
    ui.write16(num_to_bytes(0b0000111100001111))
    sleep_ms(300)
    ui.write16(num_to_bytes(0b1111000011110000))
    sleep_ms(300)
    print(loop)    
    

for loop in range(5):
    i = 1
    for loop2 in range(16):
        bytes2 = num_to_bytes(i)
        ui.i2c.writeto(39, bytes2)
        sleep_ms(50)
        i = i << 1
        print(loop2, i)


for loop in range(32):
    i = randint(0,65536)
    bytes2 = num_to_bytes(i)
    ui.i2c.writeto(39, bytes2)
    sleep_ms(200)


for i in range(2**16): # 65536
    bytes2 = num_to_bytes(i)
    ui.write16(bytes2)
    
    # max speed / "REM"
    hex_str = num_to_hex_str(i)
    print(i, hex(i), hex_str, num_to_bytes(i,rev=False))
    # sleep_ms(1000)

