# simple test - basic microprocessor s80 "simple80" 8080/85/z80 class

import gc
print("- init")
print("mem_free",gc.mem_free())

from time import sleep, sleep_ms
from octopus_decor import octopus_duration
from octopus_digital import num_to_bin_str8, num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from components.microprocessor.s80 import instructions as instr
from components.microprocessor.s80 import table
from components.microprocessor.s80.core import Executor, create_hex_program, parse_file, run_hex_code

DEBUG = False
uP = Executor() # microProcesor

print("--- start ---")
uP.set_acc(0)
uP.print_regs()
print("mem_free:",gc.mem_free())




# --- 2026 ok
#program = parse_file(uP, "example00_s80.asm") #******* 01,2,3,5,6,7
program = parse_file(uP, "ecc17_rgb.asm")
hex_program = create_hex_program(program,prn=False)

print("-"*30)
hex_str = " ".join(f"{b:02X}" for b in hex_program)
print("- program:",hex_str)
print("-"*30)

sleep(5)

print("len(instr_set):", len(hex_program))
print("="*30)
run_hex_code(uP,hex_program,5)

print()
print("-"*30)
print("mem_free:",gc.mem_free())

uP.print_regs()
uP.print_mem(18)


info ="""
-----------------
 1G = (15,13)
 2G = (2,10)
 3G = (8,3)
 5G = (6,6)
 6G = (5,8)
-----------------
-> result: (b, c)
"""
print(info)



"""
...

...
3137 256 {0} 7e   MOV_A,M
                      --->#3137 |S0 Z0 C1| 00000101 | 5, 0x5 257 
3138 257 {0} 47   MOV_B,A
                      --->#3138 |S0 Z0 C1| 00000101 | 5, 0x5 258 
3139 258 {1} 2e   MVI_L 0xa
                      --->#3139 |S0 Z0 C1| 00000101 | 5, 0x5 260 
3140 260 {0} 7e   MOV_A,M
                      --->#3140 |S0 Z0 C1| 00001000 | 8, 0x8 261 
3141 261 {0} 4f   MOV_C,A
                      --->#3141 |S0 Z0 C1| 00001000 | 8, 0x8 262 
3142 262 {0} 7f   MOV_A,A
--> R  DEC BIN    HEX (B_C)
    A:  8 00001000 08
    B:  5 00000101 05  (1288)
    C:  8 00001000 08  [266]
                      --->#3142 |S0 Z0 C1| 00001000 | 8, 0x8 263 
3143 263 {0} 76   HLT
                      --->#3143 |S0 Z0 C1| 00001000 | 8, 0x8 263 
.:. function:  run_hex_code
--> duration (milis.) --> 77046

------------------------------
mem_free: 97360
================================
[ system registers ]
a: 8 0x8 00001000
b: 5  | c: 8
h: 1  | l: 10
--------------------------------
|S|Z|0|C|0|P|1|C|
|0|0|0|0|0|0|1|1|
================================
================================
0000  c3  86  00  2e  07  3e  11  80  77  7f  2e  06  79  77  fe  00  'Ã..>w.ywþ.'
0010  ca  21  00  2e  07  7e  3d  77  2e  06  7e  3d  7f  77  c2  13  'Ê!..~=w.~=wÂ'
0020  00  2e  07  7e  fe  11  da  2b  00  c6  ef  c9  2e  07  36  00  '..~þÚ+.ÆïÉ.6.'

--------------------------------

-----------------
 1G = (15,13)
 2G = (2,10)
 3G = (8,3)
 5G = (6,6)
 6G = (5,8)
-----------------
-> result: (b, c)
"""