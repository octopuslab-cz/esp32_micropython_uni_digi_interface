"""
Universal Digital Interface - Monitor
(c) 2016-22 OctopusLab

"""

from time import sleep, sleep_ms
from utils.bits import neg, reverse, get_bit, set_bit # int2bin
from universal_digital_interface import Universal_interface
from universal_digital_interface import bin_str2int, int2bin_str8, num_to_bytes, num_to_hex_str4, num_to_hex_str2
from mini_terminal import terminal_info, terminal_color, terminal_clear

ui = Universal_interface()

vM = [] # virual memory


# -------------------------------------
DISPLAY7 = True
    
if DISPLAY7:
    from utils.octopus import disp7_init
    d7 = disp7_init()

def print_help():
    print("-"*39)
    print(" Universal Digital Interface - Monitor")
    print(" HELP")
    print("-"*39)
    print("Copy         C <start> <end> <dest>")
    print("Dump         D <start>")
    print("Go           G <address>")
    print("Help         H")
    print("Clear screen L")
    print("Info         I")
    print("Options      O")
    print("Read         R <address>")
    print("Write        W <address> <data>")
    
    print("-"*39)
    

# init vM   ------------------ max size (for test) only 512 B
for i in range(512):
    vM.append(0)


# =======================================================
while True:
    terminal_clear()
    print("UDI Monitor 0.2 OctopusLAB 2016-22")
    
    try:
       input_str = input(terminal_color("> ", 32))
    except KeyboardInterrupt:
        print('^C')
        continue
    except EOFError:
        print()
                
    try:
        cmd = input_str.split()
        cmd0 = cmd[0]
    except EOFError:
        print("debug: ERR split")
        
    if cmd0.upper() == "H": print_help()
    if cmd0.upper() == "L": terminal_clear()
    if cmd0.upper() == "T": terminal_info() # fix it
    
    if cmd0.upper() == "R":
        addr = int(cmd[1])
        
        bytes2 = num_to_bytes(addr)
        ui.i2c.writeto(39, bytes2)
        # data =  num_to_hex_str4(addr)
        data8 = num_to_hex_str2(ui.read16d()[1])
        print("read", num_to_hex_str4(addr), data8)
        

    if cmd0.upper() == "D":
        try:
            addr = int(cmd[1])
        except:
            addr = 0
        
        for r in range(8):
            print()
            print(num_to_hex_str4(addr+r*16), end="")
        
            for i in range(16):
                bytes2 = num_to_bytes(addr+r*16+i)
                ui.i2c.writeto(39, bytes2)
                data8 = num_to_hex_str2(ui.read16d()[1])
                print(" ", data8, end="")

     
    # --------------- virtual memory
    if cmd0.upper() == "ZV": # reset vM to ZERO
        for i in range(256):
            vM[i] = 0
            
            
    if cmd0.upper() == "DV":
        try:
            addr = int(cmd[1])
        except:
            addr = 0
        
        for r in range(8):
            print()
            print(num_to_hex_str4(addr+r*16), end="")
        
            for i in range(16):
                data8 = num_to_hex_str2(vM[addr+r*16+i])
                print(" ", data8, end="")

     
    if cmd0.upper() == "CV": # copy to virtual
        try:
            addr = int(cmd[1])
        except:
            addr = 0
        
        for r in range(8):
            print()
            print(num_to_hex_str4(addr+r*16), end="")
        
            for i in range(16):
                bytes2 = num_to_bytes(addr+r*16+i)
                ui.i2c.writeto(39, bytes2)
                data_num = ui.read16d()[1]
                data8 = num_to_hex_str2(data_num)
                vM[addr+r*16+i] = data_num
                print(" ", data8, end="")
                
                
    if cmd0.upper() == "WV": # write byte to virtual
        try:
            addr = int(cmd[1])
        except:
            addr = 0
            
        try:
            data = cmd[2]
        except:
            data = "00"
        
        try:
            data_num = int("0x"+data)
            print("write", addr, data_num)
            vM[addr] = data_num
        except:
            data = "ERR: input hexa data 00/ab/FF"
      
            
                
"""
#ui.write16(b'\xFF\xFF')
#ue.write16(num_to_bytes(0b1111111111111111))
#exp16.write(255)
bytes2 = num_to_bytes(i)
ui.i2c.writeto(39, bytes2)
print(loop2, i, num_to_hex_str4(i))


for loop3 in range(32):
    i = randint(0,65536)
    bytes2 = num_to_bytes(i)
    ui.i2c.writeto(39, bytes2)
    print(loop3, num_to_hex_str4(i), i)
    sleep_ms(200)


print("--- test 256 --- loop")
for i in range(2**8): # 256
    bytes2 = num_to_bytes(i)
    ui.write16(bytes2)    
    bin_str = int2bin_str8(i)
    print(num_to_hex_str2(i), int2bin_str8(i), int2bin_str8(reverse(i)), bin_str2int(bin_str)) # num_to_bytes(i,rev=False))
    sleep_ms(10)


sleep(2)
print("--- test 64k --- and read data8")
for i in range(2**16): # 65536
    bytes2 = num_to_bytes(i)
    ui.write16(bytes2)
    data8 = num_to_hex_str2(ui.read16d()[1])
    
    # max speed / "REM"
    # num_to_hex_str(i) # hex(int("0xaa"))
    print(i, num_to_hex_str4(i), data8, num_to_bytes(i,rev=False))
    # sleep_ms(1000)
    if DISPLAY7:
        d7.show(num_to_hex_str4(i)+"  "+data8)
    sleep(0.3)
"""