# simple test - basic microprocessor s80 "simple80" 8080/85/z80 class

import gc
print("- init")
print("mem_free",gc.mem_free())

from time import sleep, sleep_ms
from utils.octopus_decor import octopus_duration
from octopus_digital import num_to_bin_str8, num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from components.microprocessor.s80 import instructions as instr
from components.microprocessor.s80 import table
from components.microprocessor.s80.core import Executor, create_hex_program, parse_file, run_hex_code

"""
print("nop", hex(instr.instructions["NOP"]))  # 0x0
print("xxx", instr.instructions.get("xxx"))   # None
print("-"*30)
 
print("instructions list:")
for i in instr.instructions:
    print(i, hex(instr.instructions[i]), end=" | ")

"""    

# ===========================================================
DEBUG = False
uP = Executor() # microProcesor


print("-"*30)
print("mem_free:",gc.mem_free())
print("--- start ---")
uP.set_acc(0)
uP.print_regs()
print("mem_free:",gc.mem_free())
# instr = opcodes[0x00] # 'NOP'
##instr_set = [0x3e,0x7,0x0,0x3d,0xc2,0x0,0x3,0x0,0x3e,0x9,0x7,0x7,0x7,]
# create_hex_program(program, info = True)

#program = parse_file("example00_s80.asm")
program = parse_file("example05_s80.asm")
hex_program = create_hex_program(program,prn=False)

print("-"*30)
print("- program_num",hex_program)
##print("- instr_set", instr_set)
print("-"*30)
#print("RRC", hex(instr.instructions["RRC"]),instr.instructions["RRC"])
#print("RLC", hex(instr.instructions["RLC"]),instr.instructions["RLC"])

print("len(instr_set):", len(hex_program))
print("="*30)
run_hex_code(uP,hex_program,run_delay_ms=100)

print()
print("-"*30)
print("mem_free:",gc.mem_free())
uP.print_regs()
print("virtual memory:", uP.vm)
