# core simple_80 processor

from utils.octopus_decor import octopus_duration
from octopus_digital import num_to_bin_str8
from components.microprocessor.s80 import instructions as instr
from components.microprocessor.s80 import table
from components.microprocessor.s80.table import get_instr_param

"""
from components.microprocesor.s80.core import Executor
uP = Executor() # microProcesor

from components.microprocesor.s80.core import Executor, create_hex_program, parse_file
program = parse_file("example01_s80.asm")
hex_program = create_hex_program(program,prn=False)

----------------------------

| | | |A| | | | |
|S|Z|0|C|0|P|1|C|

sb S  State of Sign bit
zb Z  State of Zero bit
   0  always 0
AC    State of auxiliary Carry bit
   0  always 0
pb P  State of Parity bit
   1  always 1
cb C  State of Carry bit

"""

#class Executor(object):
class Executor:
    
    def __init__(self):
        self.debug = True
        
        
        self.pc = 0 # programm counter
        self.sp = 0 # stack
        
        # general registers
        self.a = 0  # acc
        self.b = 0  # reg b
        self.c = 0  # reg c
        self.d = 0  # reg d
        self.e = 0  # reg e
        
        #self.regs = [0] * 16
        #self.memory = [0] * 256
        
        self.sb = 0
        self.zb = 0
        self.acb = 0
        self.pb = 0
        self.cb = 0
        
        #self.stack = []
        #self.cycles = 0
        self.loop = 0

    def set_acc(self, value): # for test
        self.a = value
        self.zb = 1 if self.a == 0 else 0
            
            
    def print_regs(self): # dec, hex, bin
        print("="*32)
        print("a",self.a, hex(self.a), bin(self.a))
        print("b",self.b)
        print("c",self.c)
        print("d",self.d)
        print("e",self.e)
        print("-"*32)
        print("|S|Z|0|C|0|P|1|C|")
        print(f"|{self.sb}|{self.zb}|0|{self.acb}|0|{self.pb}|1|{self.cb}|")
        print("="*32)

    """
    def run(self, prg):
        self.prg = prg
        while self.ip in prg:
            self.step(prg[self.ip])


    def step(self, line):
        self.ip += line.size
        cmd = getattr(self, 'i_' + line.opcode)
        cmd(line.params)
        self.cycles += line.size


    def jump(self, param):
        if type(param) != int:
            raise Exception('Label address not resolved: ' + str(param))
        self.ip = param
    """
    
    #----------------------------------------------------------
    def execute(self, inst, param):
        self.loop += 1
        
        if inst=="NOP":
            self.pc += 1
            pass
        
        if inst=="INR_A":
            self.a += 1
            self.pc += 1
            if self.a > 255:
                self.a = 0
                self.cb = 1            
            
        if inst=="DCR_A":
            self.a -= 1
            self.pc += 1
            self.zb = 1 if self.a == 0 else 0            
        
        if inst=="MVI_A":
            self.a = param
            self.zb = 1 if self.a == 0 else 0
            self.pc += 2
            
        if inst=="MVI_B":
            self.b = param
            self.pc += 2
    
        if inst=="MVI_C":
            self.c = param
            self.pc += 2
         
        if inst=="MOV_B,A":
            self.b = self.a
            self.pc += 1
            
        if inst=="MOV_A,B":
            self.a = self.b
            self.pc += 1
    
        if inst=="MOV_C,A":
            self.c = self.a
            self.pc += 1
    
        if inst=="MOV_A,C":
            self.a = self.c
            self.pc += 1
            
        if inst=="ADD":        
            self.a = self.a + param + self.cy
        
        if inst=="RRC":        
            self.a = self.a >> 1
            self.pc += 1
            """
            if self.a > 255:
                self.a = 0
                self.cb = 1
            """
            
        if inst=="RLC":        
            self.a = self.a << 1
            self.pc += 1
        
        #self.cy = self.acc >> 4
        #self.acc &= 0xF
            
        if inst=="JNZ":
            if self.zb == 0:
                self.pc = param[0]*255+param[1] # 0x00 0xFF
                if(self.debug):
                     print("> jump to ",self.pc)
            else:
                self.pc += 3 
            
        if inst=="JZ":
            if self.zb == 1:
                self.pc = param[1] # 0x00 0xFF
                if(self.debug):
                     print("> jump to ",self.pc)
            else:
                self.pc += 3 
            
        if(self.debug):
            print(f"                        --->#{self.loop} |S{self.sb} Z{self.zb} C{self.cb}| {num_to_bin_str8(self.a)} | {self.a}, {hex(self.a)} {(self.pc)} ")

# ----------------------------------------------
def parse_file(file_name):
    pc = 0
    labels = {}
    program = []
    print("- open file:", file_name)
           
    # f = open("data/" + file)
    f = open("examples/"+file_name)
    fs = f.read()
    f.close()
    
    l=0
    for line in fs.splitlines():
        
        # clean up    
        clean_line = line.split(";")[0].strip()
        if len(clean_line) > 0:
            i_pc, i_hex, i_p1, i_p2 = 0,0,"",""
            for i1 in instr.instructions:
                if i1 in clean_line:
                    parts = clean_line.split(" ")
                    print("---parts",parts)
                    i_pc = get_instr_param(i1)
                    pc += i_pc
                    i_hex = hex(instr.instructions[i1])
                    program.append(hex(int(i_hex)))
                    try:
                        if i_pc > 2:
                            print("---jmp---add 0x00")
                            program.append(0x0) # simple jmp to (0 addr)
                        if i_pc > 1:
                            i_p1 = parts[1]
                            #if i_p1+":" in labels
                            program.append(i_p1)
                    except:
                        print("Err. No3")
                        program.append(0)
                    #if i_pc > 2: i_p2 = parts[2]
                    
            # find label
            label = "-"
            if line.count(":") == 1:
                ## labels.append(line.split(" ")[0])
                labels[line.split(" ")[0]] = pc+1 # dict test init (next pc)
                     
            print(l, pc, clean_line, i_hex,"*",i_pc, i_p1, i_p2)
            l += 1
    
    print("temp_labels:",labels)
    print("temp_prog. :",program)
    
    i=0
    
    for part1 in program:
        if str(part1)+":" in labels:
            print("---label---",part1+":",labels[part1+":"])
            program[i] = labels[part1+":"] # todo addr 2 bytes
        i += 1
  
    return program


def create_hex_program(p, prn=True, info=False):
    hex_program = []
    if info:
        print("-"*30)
        print("source: ", p)
        print("-"*30)

    if prn: print("[", end="")
    for hex_i in p:
        try:                      
            if info:
                print(hex(int(hex_i)),"(",int(hex_i),")", end=",")
            else:
                if prn: print(hex(int(hex_i)), end=",")
                #hex_program.append(hex(int(hex_i))) # hex
                hex_program.append((int(hex_i)))      # int
        except:
            print(str(hex_i)+"??? ", end=",")
    if prn: print("]", end="")
    return hex_program
