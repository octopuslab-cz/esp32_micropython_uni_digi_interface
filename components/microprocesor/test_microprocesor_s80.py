# from components.microprocesor.i8085 import instructions as i8085
from time import sleep, sleep_ms
from utils.octopus_decor import octopus_duration
from octopus_digital import num_to_bin_str8, num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from components.microprocesor.s80 import instructions as instr
from components.microprocesor.s80 import table
from components.microprocesor.s80.core import Executor


DEBUG = True
uP = Executor() # microProcesor

print("nop", hex(instr.instructions["NOP"]))  # 0x0
print("xxx", instr.instructions.get("xxx"))   # None
print("-"*30)
 
print("instructions list:")
for i in instr.instructions:
    print(i, hex(instr.instructions[i]), end=" | ")

print("instructions rev. (opcode/instr list:")
opcodes = {}
for instruct, opcode in instr.instructions.items():
    # print(hex(opcode), instruct)
    opcodes[opcode] = instruct
    


# ===========================================================
# instr = opcodes[0x00] # 'NOP'
print("-"*30)
#                  MVI 11   RRC            INR        DCR       JNZ
instr_set0 = [0x00,0x3E,0x11,0x0F,0x0F,0x0F,0x3C,0x07,0x07,0x00,0xC2,0x00,0x05,0x00,0x00]

#                  MVI 07   DCR A(3d)   JNZ
instr_set = [0x00,0x3E,0x07,0x3D,0x00,0xC2,0x00,0x03,0x00,0x00,0x00,0x00,0x00]
## pc = 0 # index / program counter

#  for ins_op in instr_test:
# for i in range(len(instr_set)):

@octopus_duration(DEBUG)
def run_hex_code(instr_set, run_delay_ms=1):
    run_code = True
    while run_code: # max loop
        pc = uP.pc
        instr = opcodes.get(instr_set[pc])
        if instr:
            # try:
            hex_i0 = num_to_hex_str2(instr_set[pc])+"  "
            if instr in table.zero_param_instr:
                print("(0)",pc,hex_i0, instr)
                # pc += 1
                param = ""

            if instr in table.double_param_instr:
                param1 = instr_set[pc+1]
                param2 = instr_set[pc+2]
                print("(2)",pc,hex_i0 , instr, num_to_hex_str2(param1), num_to_hex_str2(param2))
                # pc += 3
                param = param1, param2
                
            if (instr not in table.double_param_instr) and (instr not in table.zero_param_instr):
                param = instr_set[pc+1]
                print("(1)",pc,hex_i0 , instr, hex(param))
                # pc += 2
                
            uP.execute(instr, param)
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
print("len(instr_set):", len(instr_set))
run_hex_code(instr_set)


print()
print("-"*30)
uP.set_acc(0)
uP.print_regs()









