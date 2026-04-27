# run_s80 - basic microprocessor s80 "simple80" 8080/85/z80 class

import gc
print("- init")
print("mem_free",gc.mem_free())

from time import sleep, sleep_ms
from octopus_decor import octopus_duration
from octopus_digital import num_to_bin_str8, num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from components.microprocessor.s80 import instructions as instr
from components.microprocessor.s80 import table
from components.microprocessor.s80.core import Executor, create_hex_program, parse_file, run_hex_code

# Test A

DEBUG = False
uP = Executor() # microProcesor

print("-"*30)
print("--- start ---")
uP.set_acc(0)
uP.print_regs()
print("mem_free:",gc.mem_free())

# --- 2026 ok
# program = parse_file(uP, "example01_s80.asm") ******* 01,2,3,5,6,7
program = parse_file(uP, "example21_s80_inv.asm")
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


"""
