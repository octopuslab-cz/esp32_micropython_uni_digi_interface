# simple test - basic microprocessor s80 "simple80" 8080/85/z80 class

import gc
print("- init")
print("mem_free",gc.mem_free())

from time import sleep, sleep_ms
from utils.octopus_decor import octopus_duration
from octopus_digital import num_to_bin_str8, num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from components.microprocessor.s80 import instructions as instr
from components.microprocessor.s80 import table
from components.microprocessor.s80.core import __version__, Executor, create_hex_program, print_hex_program, parse_file, run_hex_code

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


print("-"*32)
print("ESP mem_free:",gc.mem_free())
print("--- start ---")
uP.set_acc(0)
uP.print_regs()
print("ESP mem_free:",gc.mem_free())
# instr = opcodes[0x00] # 'NOP'
##instr_set = [0x3e,0x7,0x0,0x3d,0xc2,0x0,0x3,0x0,0x3e,0x9,0x7,0x7,0x7,]
# create_hex_program(program, info = True)

def run_test(f="example05_s80.asm",asm=""):
    print("[ clear_mem() ]")
    uP.clear_mem()
    #program = parse_file("example00_s80.asm")
    print()
    print("="*32)
    print("- file name:",f)
    sleep(1)
    print()
    print()
    print("log from terminal -->")
    
    program = parse_file(uP,f,asm,print_asm=True)
    hex_program = create_hex_program(program,prn=False)

    print("-"*32)
    print("- program_num")
    print(hex_program)
    print("- program_hex")
    print_hex_program(hex_program)
    ##print("- instr_set", instr_set)
   
    print("-"*32)
        
    print("- len(instr_set):", len(hex_program))
    print("="*32)
    run_hex_code(uP,hex_program,run_delay_ms=0)

    print()
    print("-"*32)
    print("ESP mem_free:",gc.mem_free())
    
    print("-"*16 + "regs")
    uP.print_regs()
    print("-"*16 + "virtual mem.")
    #uP.print_vm()
    uP.print_mem()
    print("asm file name:",f)
    print("core_s80 ver.",__version__)
    sleep(5)
    

asm = """
    NOP
loop:
    MVI_A 0b00000101 ; intro:
    MOV_A,A          ; show acc -> 10101010
    MOV_B,B 
    
    MVI_A 65 ; ord("A")=65
    STA 0x00 0x01
    MVI_A 66 ; ord("B")=66
    STA 0x01 0x01
    MVI_A 67 ; ord("C")=66
    STA 0x02 0x01
    
    """
print(asm)

while True:
    run_test(f="",asm=asm)    
    
    run_test("example00_s80.asm")
    run_test("example01_s80.asm")
    run_test("example02_s80.asm")
    run_test("example03_s80.asm")
    run_test("example05_s80.asm")    
    run_test("example06_s80.asm")    
    run_test("test23_02.asm")
    """
    NOP
loop:
    MVI_A 0b10101010 ; intro:
    MOV_A,A          ; show acc -> 10101010
    MOV_E,E          ; sleep 1 sec.
    CMA              ; complement / bit negation
    MOV_A,A          ; show acc  -> 01010101
    MOV_E,E          ; sleep
;
    JMP loop
    """
    # 22: 00 3e aa 7f 5b 2f 7f 5b c3 00 01 00
    # 23: 00 3e aa 7f 5b 2f 7f 5b c3 01 00 00
    
    run_test("example_s80_counter.asm")
    run_test("example_s80_snake1.asm")


