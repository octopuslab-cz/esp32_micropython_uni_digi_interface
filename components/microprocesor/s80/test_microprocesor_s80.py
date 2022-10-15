# from components.microprocesor.i8085 import instructions as i8085
from components.microprocesor.s80 import instructions as instr
from components.microprocesor.s80 import table

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

instr_set = [0x00,0xC3,0x11,0x22,0x11,0x20,0x30,0x40,0x50,0x60]

pc = 0 # index / program counter
#  for ins_op in instr_test:
for i in range(len(instr_set)):
    instr = opcodes.get(instr_set[pc])
    if instr:
        try:
            if instr in table.zero_param_instr:
                print(hex(instr_set[pc]), instr)
                pc += 1

            if instr in table.double_param_instr:
                param1 = instr_set[pc+1]
                param2 = instr_set[pc+2]
                print(hex(instr_set[pc]), instr, hex(param1), hex(param2))
                pc += 3
                
            if (instr not in table.double_param_instr) and (instr not in table.zero_param_instr):
                param = instr_set[pc+1]
                print(hex(instr_set[pc]), instr, hex(param))
                pc += 2
            
        except:
            Err = "list index out of range"
    else:
        print(hex(instr_set[pc]), "???")
        pc += 1









