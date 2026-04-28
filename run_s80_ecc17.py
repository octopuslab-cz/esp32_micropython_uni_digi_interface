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


print("instructions list:")
for i in instr.instructions:
    print(i, hex(instr.instructions[i]), end=" | ")
print()

# Test A
print("[ --- test A --- ]")
print("nop", hex(instr.instructions["NOP"]))  # 0x0
print("xxx", instr.instructions.get("xxx"))   # None
print("-"*30)

# Test B
print("[ --- test B --- ] OP-CODES")

opcodes = {}
for instruct, opcode in instr.instructions.items():
    opcodes[opcode] = instruct
    if DEBUG: print(opcodes[opcode], end=".")
instr = opcodes[0x00] # 'NOP'
print("instructions revers. (opcode/instr list:")    
print(instr)

# Test C ?x
"""
print("[ --- test C --- ]")

instr_set = [0x3e,0x7,0x0,0x3d,0xc2,0x0,0x3,0x0,0x3e,0x9,0x7,0x7,0x7,]
# create_hex_program(program, info = True)
hex_program = create_hex_program(program,prn=False)
print("- instr_set", instr_set)
print("len(instr_set):", len(hex_program))
run_hex_code(instr_set,run_delay_ms=100,run=False)
print("="*30)
run_hex_code(instr_set,run_delay_ms=100,run=True)
print("*"*30)
"""

# --- 2026 ok
#program = parse_file(uP, "example00_s80.asm") #******* 01,2,3,5,6,7
program = parse_file(uP, "ecc17.asm")
hex_program = create_hex_program(program,prn=False)

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
...
2350 252 {0} 7e   MOV_A,M
                      --->#2350 |S0 Z0 C1| 00001000 | 8, 0x8 253 
2351 253 {0} 47   MOV_B,A
                      --->#2351 |S0 Z0 C1| 00001000 | 8, 0x8 254 
2352 254 {1} 2e   MVI_L 0xa
                      --->#2352 |S0 Z0 C1| 00001000 | 8, 0x8 256 
2353 256 {0} 7e   MOV_A,M
                      --->#2353 |S0 Z0 C1| 00000011 | 3, 0x3 257 
2354 257 {0} 4f   MOV_C,A
                      --->#2354 |S0 Z0 C1| 00000011 | 3, 0x3 258 
2355 258 {0} 7f   MOV_A,A
--> R  DEC BIN    HEX (B_C)
    A:  3 00000011 03
    B:  8 00001000 08  (2051)
    C:  3 00000011 03  [266]
                      --->#2355 |S0 Z0 C1| 00000011 | 3, 0x3 259 
2356 259 {0} 76   HLT
                      --->#2356 |S0 Z0 C1| 00000011 | 3, 0x3 259 
.:. function:  run_hex_code
--> duration (milis.) --> 19022

------------------------------
mem_free: 72800
================================
[ system registers ]
a: 3 0x3 00000011
b: 8  | c: 3
h: 1  | l: 10
--------------------------------
|S|Z|0|C|0|P|1|C|
|0|0|0|0|0|0|1|1|
================================
"""