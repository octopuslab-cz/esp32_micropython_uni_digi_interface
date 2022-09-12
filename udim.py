"""
Universal Digital Interface - Monitor
(c) 2016-22 OctopusLab

"""
ver = "0.3" # basic - beta

from time import sleep, sleep_ms
from utils.bits import neg, reverse, get_bit, set_bit # int2bin
from universal_digital_interface import Universal_interface
from universal_digital_interface import bin_str2int, int2bin_str8, num_to_bytes, num_to_hex_str4, num_to_hex_str2
from mini_terminal import terminal_info, terminal_color, terminal_clear

ui = Universal_interface()

vM = [] # virual memory


"""    # i2c expanders:
#ui.write16(b'\xFF\xFF')
#ue.write16(num_to_bytes(0b1111111111111111))
#exp16.write(255)
bytes2 = num_to_bytes(i)
ui.i2c.writeto(39, bytes2)
print(loop2, i, num_to_hex_str4(i))

bytes2 = num_to_bytes(i)
ui.write16(bytes2)    
bin_str = int2bin_str8(i)
print(num_to_hex_str2(i), int2bin_str8(i), int2bin_str8(reverse(i)), bin_str2int(bin_str)) # num_to_bytes(i,rev=False))

bytes2 = num_to_bytes(i)
ui.write16(bytes2)
data8 = num_to_hex_str2(ui.read16d()[1])
    
print(i, num_to_hex_str4(i), data8, num_to_bytes(i,rev=False))
"""


# -------------------------------------
DEBUG = False
DISPLAY7 = True
terminal_run = True
PROCESOR = "Z80"
machine_code = () # table
    
    
if DISPLAY7:
    from utils.octopus import disp7_init
    d7 = disp7_init()


def parse_input(input_str):
    try:
        cmd = input_str.split()
        cmd0 = cmd[0].upper()
    except EOFError:
        print("debug: ERR split")
        
    try:
        cmd1 = cmd[1]
    except:
        cmd1 = "0"
        
    try:
        cmd2 = cmd[2]
    except:
        cmd2 = "0"
        
    return cmd0, cmd1, cmd2


def print_help():
    print("-"*39)
    print(" Universal Digital Interface - Monitor")
    print(" HELP")
    print("-"*39)
    print(" Copy         C <start> <end> <dest>")
    print(" Dump         D <start>")
    print(" Go           G <address>")
    print(" Help         H")
    print(" Clear screen L")
    print(" Info         I")
    print(" Options      O")
    print(" Procesor     P") # 4004, 8008, 8060, 8080, 8085, Z80, 6502, ...
    print(" Read         R <address>")
    print(" Write        W <address> <data>")
    print(" Quit         Q")
   
    print("-"*39)
    

# init vM  |  max size (for test) only 512 B
for i in range(512):
    vM.append(0)


# ===========================================
while terminal_run:
    terminal_clear()    
    print(f"UDI Monitor {ver} | OctopusLAB 2016-22")
    
    try:
       input_str = input(terminal_color("> ", 32))
    #except KeyboardInterrupt:
    #    print('^C')
    #    continue
    except EOFError:
        print("input ERR")
                
    cmd0, cmd1, cmd2 = parse_input(input_str)
    if DEBUG: print(cmd0, cmd1, cmd2)
    
    if cmd0 == "Q": terminal_run = False
    if cmd0 == "H": print_help()
    if cmd0 == "L": terminal_clear()
    if cmd0 == "T": terminal_info() # fix it
    if cmd0 == "I":
        print("--- info ---")
        print(f"UDI Monitor - version {ver} ")
        print("ESP32 | Micropython")
        
        print("emul.procesor:", PROCESOR)
        
    if cmd0.upper() == "P":
        PROCESOR = cmd1
    
    if cmd0.upper() == "R":
        addr = int(cmd1)
        
        bytes2 = num_to_bytes(addr)
        ui.i2c.writeto(39, bytes2)
        # data =  num_to_hex_str4(addr)
        data8 = num_to_hex_str2(ui.read16d()[1])
        print("read:", num_to_hex_str4(addr), data8)
        

    if cmd0 == "D":
        addr = int(cmd1)
        
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
        addr = int(cmd1)
        
        for r in range(8):
            print()
            print(num_to_hex_str4(addr+r*16), end="")
        
            for i in range(16):
                data8 = num_to_hex_str2(vM[addr+r*16+i])
                print(" ", data8, end="")

     
    if cmd0.upper() == "CV": # copy to virtual
        addr = int(cmd1)
        
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
        addr = int(cmd1)  # int or hexa: wv 256 d / ww 0xFF          
        data = cmd2       # hexa string DD: FF = 0xFF = 256 
        
        try:
            data_num = int("0x"+data)
            print("write:", addr, data_num)
            vM[addr] = data_num
        except:
            data = "ERR: input hexa data 00/ab/FF"
            

    if cmd0.upper() == "RV":
        addr = int(cmd1)
        
        data_num = vM[addr]
        data8 = num_to_hex_str2(data_num)
        print("read:", num_to_hex_str4(addr), data8)
