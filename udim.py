"""
Universal Digital Interface - Monitor
(c) 2016-23 OctopusLab
"""
ver = "0.3.1 | 2026-05" # basic - beta

from time import sleep, sleep_ms
from universal_digital_interface import Universal_interface
from octopus_digital import neg, reverse, get_bit, set_bit # int2bin
from octopus_digital import num_to_bin_str8, num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from octopus_digital import bin_str_to_int, hex_dump, ascii_table
from mini_terminal import terminal_info, terminal_color, terminal_clear
from components.microprocessor.s80.core import __version__, Executor, create_hex_program, print_hex_program, parse_file, run_hex_code

from gc import mem_free

ui = Universal_interface()

vM = []     # 512 B virual memory
vMtemp = [] # 256 B virual memory - temporary

VM_SIZE = 256
VM_TEMP_SIZE = 128

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
DISPLAY8 = False
terminal_run = True
PROCESOR = "s80"
machine_code = () # table
address = 0

uP = Executor()

# init vM  |  max size (for test) only 512 B
for i in range(256):
    vM.append(0)
    
uP.memory = vM

for i in range(256):
    vMtemp.append(0)
    
if DISPLAY8:
    from components.display8 import Display8
    d8 = Display8() #disp7_init()


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
    print(" ASCII table  A")
    print(" Copy         C <start> <end> <dest>")
    print(" Dump         D <start>")
    print(" Go           G <address>")
    print(" Executr      E")
    print(" Help         H")
    print(" Clear screen L")
    print(" Info         I")
    print(" Options      O")
    print(" Procesor     P") # 4004, 8008, 8060, 8080, 8085, Z80, 6502, ...
    print(" Read         R <address>")
    print(" Write        W <address> <data>")
    print(" Quit         Q")
    print("-"*39)
    print(" Dump VM      DV <start> (Virtual memory)")
    print(" Read VM      RV <address>")
    print(" Write VM     WV <address> <data>")
    print(" Write next   WN <data> (address+1)")
    print("-"*39)    
    print("              save filename.hex") # 256 B from virtual memory
    print("              load filename.hex") # 256 B to virtual memory
    print("-"*39)


def print_ascii_table():
    ascii_table(1)


# ===========================================
while terminal_run:
    terminal_clear()    
    print(f"UDI Monitor {ver} | OctopusLAB 2016-26")
    
    try:
       input_str = input(terminal_color("> ", 32))
    #except KeyboardInterrupt:
    #    print('^C')
    #    continue
    except EOFError:
        print("input ERR")
                
    cmd0, cmd1, cmd2 = parse_input(input_str)
    if DEBUG: print(cmd0, cmd1, cmd2)
    
    if cmd0 == "A": print_ascii_table()
    if cmd0 == "Q": terminal_run = False
    if cmd0 == "H": print_help()
    if cmd0 == "L": terminal_clear()
    if cmd0 == "T": terminal_info() # fix it
    if cmd0 == "I":
        print("--- info ---")
        print(f"UDI Monitor - version {ver} ")
        print("ESP32 | Micropython")
        print(f"--> RAM free {mem_free()}")
        print(f"--> VM_SIZE {VM_SIZE} (virtual memory)")
        print(f"--> VM_TEMP_SIZE {VM_TEMP_SIZE}")
        VM_TEMP_SIZE
        print("emul.procesor:", PROCESOR)
        print("address:", address)
        
    if cmd0.upper() == "P": PROCESOR = cmd1

    if cmd0.upper() == "R":
        addr = int(cmd1)
        
        bytes2 = num_to_bytes2(addr)
        ui.i2c.writeto(39, bytes2)
        # data =  num_to_hex_str4(addr)
        data8 = num_to_hex_str2(ui.read16d()[1])
        print("read:", num_to_hex_str4(addr), data8)
        if DISPLAY8:
            d8.show(num_to_hex_str4(addr)+"  "+data8)
  
    if cmd0 == "D":
        addr = int(cmd1)
        
        for r in range(16):
            print()
            print(num_to_hex_str4(addr+r*16), end="")
        
            for i in range(16):
                bytes2 = num_to_bytes2(addr+r*16+i)
                ui.i2c.writeto(39, bytes2)
                data8 = num_to_hex_str2(ui.read16d()[1])
                print(" ", data8, end="")
                
    if cmd0 == "E":
        # Check if there is anything in memory to run
        # We check the first few bytes, or use sum()
        if all(v == 0 for v in vM[:16]):
            print("Warning: Memory at 0x0000 is empty (NOPs). Load a program first.")
        else:
            # Get start address from cmd1 (default 0)
            try:
                start_addr = int(cmd1, 0)
            except:
                start_addr = 0
                
            print(f"Executing from address: {num_to_hex_str4(start_addr)}...")
            print("-" * 30)
            
            try:
                # Reset CPU state before run
                uP.pc = start_addr
                uP.is_running = True
                
                # We pass vM as the instruction set
                # uP will execute instructions one by one
                run_hex_code(uP, vM, run_delay_ms=1)
                
                print("-" * 30)
                print("Execution finished.")
                # Show final state of registers for debugging
                print(f"Final state: A:{uP.a:02x} B:{uP.b:02x} C:{uP.c:02x} HL:{uP.h:02x}{uP.l:02x} PC:{uP.pc:04x}")
            
            except Exception as e:
                print(f"Runtime Error: {e}")
                if DEBUG: raise e # Show full traceback only in debug mode
        
        uP.print_regs()
        print("-"*16 + "virtual mem.")
        uP.print_mem()
     
    # --------------- virtual memory
    if cmd0.upper() == "ZV": # reset vM to ZERO
        for i in range(256):
            vM[i] = 0
            
            
    if cmd0.upper() == "DV":
        addr = int(cmd1)
        
        hex_dump(vM)
     
    if cmd0.upper() == "CV": # copy to virtual
        addr = int(cmd1)
        
        for r in range(16): # 16 * 16 = 256
            print()
            print(num_to_hex_str4(addr+r*16), end="")
        
            for i in range(16):
                bytes2 = num_to_bytes2(addr+r*16+i)
                ui.i2c.writeto(39, bytes2)
                data_num = ui.read16d()[1]
                data8 = num_to_hex_str2(data_num)
                vM[addr+r*16+i] = data_num
                print(" ", data8, end="")
                
                
    if cmd0.upper() == "WV": # write byte to virtual
        addr = int(cmd1)  # int or hexa: wv 256 d / ww 0xFF
        address = addr
        data = cmd2       # hexa string DD: FF = 0xFF = 256 
        
        try:
            data_num = int("0x"+data)
            print("write:", addr, data_num)
            vM[addr] = data_num
        except:
            data = "ERR: input hexa data 00/ab/FF"
            
    if cmd0.upper() == "WN": # write byte to virtual to next addres
        address += 1
        data = cmd1       # hexa string DD: FF = 0xFF = 256 
        
        try:
            data_num = int("0x"+data)
            print("write:", address, data_num)
            vM[address] = data_num
        except:
            data = "ERR: input hexa data 00/ab/FF"
            

    if cmd0.upper() == "RV":
        addr = int(cmd1)
        
        data_num = vM[addr]
        data8 = num_to_hex_str2(data_num)
        print("read:", num_to_hex_str4(addr), data8)
        
    # ------------------- hex file ---- test only 256 B
    if cmd0.upper() == "SAVE": # subdir /data
        file = cmd1
        if len(file)<3:
            file = "test.hex"
          
        str_temp =""
        for i in range(256):
            str_temp += num_to_hex_str2(vM[i])
            
        f = open("data/" + file, 'w')
        f.write(str_temp)
        f.close()
        
  
    if cmd0.upper() == "LOAD": # todo: if file dont exist
        filename = cmd1
        if len(filename) < 3: 
            filename = "test.hex"
            
        try:
            # Attempt to open the file from the data/ subdirectory
            with open("data/" + filename, "r") as f:
                fs_raw = f.read()
            
            # 1. Remove all whitespace (spaces, tabs, newlines)
            # This creates a clean hex string like "2e002601..."
            fs = "".join(fs_raw.split()) 
            
            print(f"Loading {filename}...")
            if DEBUG: print("Clean hex string:", fs)
            
            # 2. Determine the number of pairs (bytes) to load
            # Floor division (// 2) automatically ignores a trailing odd character
            num_bytes = len(fs) // 2
            bytes_to_load = min(256, num_bytes)
            
            # 3. Load data into virtual memory (vM)
            for i in range(bytes_to_load):
                byte_str = fs[i*2 : i*2+2]
                try:
                    vM[i] = int(byte_str, 16)
                except ValueError:
                    print(f"ERR: '{byte_str}' at position {i} is not a valid hex!")
                    break
            
            print(f"Done. Loaded {bytes_to_load} bytes.")

        except OSError:
            # File not found or cannot be opened - warning only, no crash
            print(f"Warning: File 'data/{filename}' not found.")
