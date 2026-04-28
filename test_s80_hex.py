# simple test - basic microprocessor s80 "simple80" 8080/85/z80 class

import gc
print("- init")
print("mem_free",gc.mem_free())

from time import sleep, sleep_ms
from octopus_decor import octopus_duration
from octopus_digital import num_to_bin_str8, num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from components.microprocessor.s80 import instructions as instr
from components.microprocessor.s80 import table
from components.microprocessor.s80.core import Executor, convert_hex_to_nums, print_hex_program, run_hex_code

DEBUG = True
uP = Executor() # microProcesor

print("--- start ---")
uP.set_acc(0)
uP.print_regs()
print("mem_free:",gc.mem_free())


# --- 2026 ok
# data/test.hex:
# 2e 00 26 01 7e 2c db 00 7e 2c db 00 7e 01 00 01 01 01 02 00 3e 2d 01 0c 00

filename = "test.hex"
try:
    with open("data/" + filename, "r") as f:
        raw_data = f.read()
    if DEBUG: print("Program loaded:", raw_data)
    
    hex_program = convert_hex_to_nums(raw_data)
    
    if DEBUG: print(f"Program {filename} loaded:")
    print_hex_program(hex_program)
   
  
except OSError:
   print(f"Warning: File 'data/{filename}' not found.")
except ValueError:
   print("Error: File contains invalid hexadecimal characters.")


print("-"*30)
print("- program_num",hex_program)
print("-"*30)

print("len(instr_set):", len(hex_program))
print("="*30)
run_hex_code(uP,hex_program,1)

print()
print("-"*30)
print("mem_free:",gc.mem_free())
uP.print_regs()


"""
--- start ---
================================
[ system registers ]
a: 0 0x0 00000000
b: 0  | c: 0
h: 0  | l: 0
--------------------------------
|S|Z|0|C|0|P|1|C|
|0|1|0|0|0|0|1|0|
================================
mem_free: 126736
Program loaded: 2e 00 26 01 7e 2c db 00 7e 2c db 00 7e 01 00 01 01 01 02 00 3e 2d 01 0c 00
Program test.hex loaded:
2e 00 26 01 7e 2c db 00 7e 2c db 00 7e 01 00 01 01 01 02 00 3e 2d 01 0c 00 
------------------------------
- program_num [46, 0, 38, 1, 126, 44, 219, 0, 126, 44, 219, 0, 126, 1, 0, 1, 1, 1, 2, 0, 62, 45, 1, 12, 0]
------------------------------
len(instr_set): 25
==============================
1 0 {1} 2e   MVI_L 0x0
                      --->#1 |S0 Z1 C0| 00000000 | 0, 0x0 2 
2 2 {1} 26   MVI_H 0x1
                      --->#2 |S0 Z0 C0| 00000000 | 0, 0x0 4 
3 4 {0} 7e   MOV_A,M
                      --->#3 |S0 Z0 C0| 00000000 | 0, 0x0 5 
4 5 {0} 2c   INR_L
                      --->#4 |S0 Z0 C0| 00000000 | 0, 0x0 6 
5 6 {1} db   IN 0x0
IN 0 0
                      --->#5 |S0 Z0 C0| 00000000 | 0, 0x0 8 
6 8 {0} 7e   MOV_A,M
                      --->#6 |S0 Z0 C0| 00000000 | 0, 0x0 9 
7 9 {0} 2c   INR_L
                      --->#7 |S0 Z0 C0| 00000000 | 0, 0x0 10 
8 10 {1} db   IN 0x0
IN 0 0
                      --->#8 |S0 Z0 C0| 00000000 | 0, 0x0 12 
9 12 {0} 7e   MOV_A,M
                      --->#9 |S0 Z0 C0| 00000000 | 0, 0x0 13 
10 13 {2} 01   LXI_B 00 01
                      --->#10 |S0 Z0 C0| 00000000 | 0, 0x0 16 
11 16 {2} 01   LXI_B 01 02
                      --->#11 |S0 Z0 C0| 00000000 | 0, 0x0 19 
12 19 {0} 00   NOP
                      --->#12 |S0 Z0 C0| 00000000 | 0, 0x0 20 
13 20 {1} 3e   MVI_A 0x2d
                      --->#13 |S0 Z0 C0| 00101101 | 45, 0x2d 22 
14 22 {2} 01   LXI_B 0c 00
                      --->#14 |S0 Z0 C0| 00101101 | 45, 0x2d 25 
.:. function:  run_hex_code
--> duration (milis.) --> 106

------------------------------
mem_free: 119328
================================
[ system registers ]
a: 45 0x2d 00101101
b: 0  | c: 12
h: 1  | l: 2
--------------------------------
|S|Z|0|C|0|P|1|C|
|0|0|0|0|0|0|1|0|
================================
"""