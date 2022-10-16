#  test assembler s80

# from components.microprocesor.s80 import instructions as instr
# from components.microprocesor.s80 import table
# from components.microprocesor.s80.table import get_instr_param
from components.microprocessor.s80.core import create_hex_program, parse_file

"""
instructions - one word
MVI A --> MVI_A 
label: <-- [:]
only 255 lines max --> jmp addr (0, addr8)

"""


# ===============================================

program = parse_file("example01_s80.asm")
print("="*30)
print("parse_file->program",program)
print()
print("="*30)
print()

hex_program = create_hex_program(program)

print()
print("hex_program",hex_program)
