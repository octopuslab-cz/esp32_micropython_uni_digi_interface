# simple test - basic microprocessor s80 "simple80" 8080/85/z80 class

from time import sleep, sleep_ms
from utils.octopus_decor import octopus_duration
from octopus_digital import num_to_bin_str8, num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from components.microprocessor.s80 import instructions as instr
from components.microprocessor.s80 import table
from components.microprocessor.s80.core import Executor, create_hex_program, parse_file


DEBUG = True
uP = Executor() # microProcesor

"""
print("nop", hex(instr.instructions["NOP"]))  # 0x0
print("xxx", instr.instructions.get("xxx"))   # None
print("-"*30)
 
print("instructions list:")
for i in instr.instructions:
    print(i, hex(instr.instructions[i]), end=" | ")

"""    

# ===========================================================
print("- init")
print("instructions rev. (opcode/instr list:")
opcodes = {}
for instruct, opcode in instr.instructions.items():
    # print(hex(opcode), instruct)
    opcodes[opcode] = instruct
# instr = opcodes[0x00] # 'NOP'
print("-"*30)

## pc = 0 # index / program counter

#  for ins_op in instr_test:
# for i in range(len(instr_set)):

@octopus_duration(DEBUG)
def run_hex_code(instr_set, run_delay_ms=1, run=True):
    run_code = True
    pc, uP.pc = 0, 0
    while run_code: # max loop
        if run: pc = uP.pc
        instr = opcodes.get(int(instr_set[pc]))
        if instr:
            # try:
            hex_i0 = num_to_hex_str2(int(instr_set[pc]))+"  "
            if instr in table.zero_param_instr:
                print("(0)",pc,hex_i0, instr)
                add_pc = 1
                param = ""

            if instr in table.double_param_instr:
                param1 = instr_set[pc+1]
                param2 = instr_set[pc+2]
                print("(2)",pc,hex_i0 , instr, num_to_hex_str2(param1), num_to_hex_str2(param2))
                add_pc = 3
                param = param1, param2
                
            if (instr not in table.double_param_instr) and (instr not in table.zero_param_instr):
                param = instr_set[pc+1]
                print("(1)",pc,hex_i0 , instr, hex(param))
                add_pc = 2
                
            if run:
                uP.execute(instr, param)
            else:
                pc += add_pc
                uP.pc = pc
            # except:
            # Err = "list index out of range"
        else:
            print(hex(instr_set[pc]), "???")
            # pc += 1
        ##print("> uP.pc:", uP.pc, len(instr_set))
        if uP.pc >= len(instr_set):
            run_code = False
        sleep_ms(run_delay_ms)


print("--- start ---")

##instr_set = [0x3e,0x7,0x0,0x3d,0xc2,0x0,0x3,0x0,0x3e,0x9,0x7,0x7,0x7,]
# create_hex_program(program, info = True)

program = parse_file("example01_s80.asm")
hex_program = create_hex_program(program,prn=False)

print("-"*30)
print("- hex_program",hex_program)
##print("- instr_set", instr_set)
print("-"*30)

print("len(instr_set):", len(hex_program))
##run_hex_code(instr_set,run_delay_ms=100,run=False)
##print("="*30)
##run_hex_code(instr_set,run_delay_ms=100,run=True)
print("="*30)
run_hex_code(hex_program,run_delay_ms=100,run=True)

print()
print("-"*30)
uP.set_acc(0)
uP.print_regs()
