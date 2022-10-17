# octopusLAB - core - simple_80 processor
__version__ = "0.3" # 2022/10/17

from time import sleep, sleep_ms
from utils.octopus_decor import octopus_duration
from octopus_digital import num_to_bin_str8, num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from components.microprocessor.s80 import instructions as instr
from components.microprocessor.s80 import table
from components.microprocessor.s80.table import get_instr_param

HW_COMPONETS = True

if HW_COMPONETS:
    from components.led import Led
    led = Led(2)

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
        self.debug = False
        
        self.vm = {} # virtual memory
        self.vm[255] = 0
        self.pc = 0  # programm counter
        self.sp = 0  # stack pointer - single
        
        # general registers
        self.a = 0  # acc
        self.b = 0  # reg b
        self.c = 0  # reg c
        self.d = 0  # reg d
        self.e = 0  # reg e
        self.l = 0
        self.h = 0
        
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
        print("[ system registers ]")
        print("a:",self.a, hex(self.a), bin(self.a))
        print("b:",self.b, " | c:",self.c)
        print("h:",self.h, " | l:",self.l)
        # print("d",self.d)
        # print("e",self.e)
        print("-"*32)
        print("|S|Z|0|C|0|P|1|C|")
        print(f"|{self.sb}|{self.zb}|0|{self.acb}|0|{self.pb}|1|{self.cb}|")
        print("="*32)
        
    def print_vm(self):
        print("[ virtual memory ] - (16/32 bytes)")
        vm_sorted = [0] * 16  # simple 16 Bytes
        # vm_sorted = dict(sorted(self.vm.items()))
        vm_offset = 256
        try:
            for addr,data in self.vm.items():
                 vm_sorted[addr-vm_offset] = data
       
            print(vm_sorted)
            print("--- hexa:")
            for ch in vm_sorted:
                print(hex(ch),end=" ")
            print()
            print("--- string:")
            for ch in vm_sorted:
            # print(ch)
            
                print(chr(ch),end="")
            print()
        except:
            print("vm.Err:")
            print("list index out of range")
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
                
        if inst=="INR_B":
            self.b += 1
            self.pc += 1
            if self.b > 255:
                self.b = 0
                self.cb = 1
                
        if inst=="INR_C":
            self.c += 1
            self.pc += 1
            if self.c > 255:
                self.c = 0
                self.cb = 1
                
        if inst=="INR_H":
            self.h += 1
            self.pc += 1
            if self.h > 255:
                self.h = 0
                self.cb = 1
                
        if inst=="INR_L":
            self.l += 1
            self.pc += 1
            if self.l > 255:
                self.l = 0
                self.cb = 1   
        
        if inst=="DCR_A":
            self.a -= 1
            self.pc += 1
            self.zb = 1 if self.a == 0 else 0            
        
        if inst=="DCR_B":
            self.b -= 1
            self.pc += 1
            self.zb = 1 if self.b == 0 else 0            
        
        if inst=="DCR_C":
            self.c -= 1
            self.pc += 1
            self.zb = 1 if self.c == 0 else 0
            
        if inst=="DCR_H":
            self.h -= 1
            self.pc += 1
            self.zb = 1 if self.h == 0 else 0
            
        if inst=="DCR_L":
            self.l -= 1
            self.pc += 1
            self.zb = 1 if self.l == 0 else 0
        
        if inst=="LDA":
            # [0]=H [1]=L   0x01 0x03 = 256+3
            addr = param[0]*256 + param[1]
            print("LDA addr test", param[0], param[1], "-->",addr, self.vm.get(addr))
            self.a = self.vm.get(addr)
            self.zb = 1 if self.a == 0 else 0
            self.pc += 3
            
        if inst=="STA":
            # [0]=H [1]=L   0x01 0x03 = 256+3
            addr = param[0]*256 + param[1]
            self.vm[addr] = self.a
            self.pc += 3
            
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
         
        if inst=="MVI_L":
            self.l = param
            self.pc += 2
            
        if inst=="MVI_H":
            self.h = param
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
                    
        if inst=="MOV_A,M":
            addr = self.h*256+self.l
            self.a = self.vm.get(addr)
            #print("MOV_A,M addr test", self.h, self.l, "-->",addr,self.vm.get(addr))
            self.pc += 1
            
        if inst=="MOV_M,A":
            self.vm[self.h*256+self.l] = self.a
            self.pc += 1
            
        if inst=="ADD":        
            self.a = self.a + param + self.cy
            
        if inst=="CPI":
            compare  = param - self.a
            self.zb = 1 if compare == 0 else 0
            self.cb = 1 if compare > 0 else 0
            self.pc += 2
        
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
            
        if inst=="JMP":
            self.pc = param[0]*256+param[1] # direct to addr: 0x00 0xFF
            if(self.debug):print("> JMP to ",self.pc)
                        
        if inst=="CALL":
            self.sp = self.pc + 3 # stack
            self.pc = param[0]*256+param[1]
            if(self.debug): print("> CALL from",self.sp,"to",self.pc)
                     
        if inst=="RET":
            self.pc = self.sp # stack
            if(self.debug): print("> RET to ",self.pc)
            self.sp = 0
            
        if inst=="JNZ":
            if self.zb == 0:
                self.pc = param[0]*256+param[1]
                if(self.debug): print("> jump to ",self.pc)
            else:
                self.pc += 3 
            
        if inst=="JZ":
            if self.zb == 1:
                self.pc = param[1] # 0x00 0xFF
                if(self.debug): print("> jump to ",self.pc)
            else:
                self.pc += 3
                
        if inst=="JNC":
            if self.cb == 0:
                self.pc = param[0]*256+param[1]
                if(self.debug): print("> jump to ",self.pc)
            else:
                self.pc += 3 
            
        if inst=="JC":
            if self.cb == 1:
                self.pc = param[1] # 0x00 0xFF
                if(self.debug): print("> jump to ",self.pc)
            else:
                self.pc += 3
                
        # ------------- spec subroutines --------
        if inst=="MOV_A,A":
            print("--> spec.sub. | acc:", self.a)
            self.pc += 1
            
        if inst=="MOV_B,B":
            print("--> spec.sub. | vitrual memory:", self.vm)
            self.pc += 1
            
        if inst=="MOV_C,C":
            print("--> spec.sub. | pc:", self.pc)
            self.pc += 1
            
        if inst=="MOV_D,D":
            print("--> spec.sub. | display (ToDo) ...")
            self.pc += 1
            
        if inst=="MOV_E,E":
            print("--> spec.sub. | sleep 1 sec. (slEEp)")
            sleep(1)
            self.pc += 1  
            
        if inst=="MOV_H,H":
            print("--> spec.sub. - LED_ON (High)")
            if HW_COMPONETS: led.value(1)
            self.pc += 1
            
        if inst=="MOV_L,L":
            print("--> spec.sub. - LED_OFF (Low)")
            if HW_COMPONETS: led.value(0)
            self.pc += 1  
            
        if(True): # /debug
            print(f"                      --->#{self.loop} |S{self.sb} Z{self.zb} C{self.cb}| {num_to_bin_str8(self.a)} | {self.a}, {hex(self.a)} {(self.pc)} ")

# -----------------------------------------
def parse_file(uP, file_name, debug = True):
    pc = 0
    labels = {}
    program = []
    print("[ two-pass translator ]")
    print("- open file:", file_name)
           
    # f = open("data/" + file)
    f = open("examples/"+file_name)
    fs = f.read()
    f.close()
    
    l=0
    for line in fs.splitlines():
        
        # clean up    
        clean_line = line.split(";")[0].strip()
        
        # data_string
        index_vm = 256  # start data virtual memory FF+1
        if clean_line.count("#DATA"): 
            parts = clean_line.split("=")
            data_string=parts[1].strip().replace('"','')
            print("data_string:",data_string)
            for ch in data_string:
                uP.vm[index_vm] = ord(ch)
                index_vm += 1
            uP.vm[index_vm] = 0 # last "0" = stop
        
        if len(clean_line) > 0:
            i_pc, i_hex, i_p1, i_p2 = 0,0,"",""
            for i1 in instr.instructions:
                if i1 in clean_line:
                    parts = clean_line.split(" ")
                    print("---parts:",parts)
                    i_pc = get_instr_param(i1)
                    pc += i_pc
                    i_hex = hex(instr.instructions[i1])
                    program.append(hex(int(i_hex)))
                    
                    if i1 =="LDA" or i1 =="STA":
                        print("-LD/ST-A-add",parts[1],parts[2])
                        # program.append(0x0) # simple jmp to (0 addr)
                        program.append(parts[1])
                        program.append(parts[2])
                    else:
                        try:                            
                            if i_pc > 2:                                
                                print("---jmp---add 0x00")
                                program.append(0x0) # simple jmp to (0 addr)
                            if i_pc > 1:
                                i_p1 = parts[1]
                                #if i_p1+":" in labels
                                program.append(i_p1)
                    
                        #if i_pc > 2: i_p2 = parts[2]
                            
                        
                        except:
                            print("Err. No3")
                            program.append(0)
                    
            # find label
            label = "-"
            if line.count(":") == 1:
                ## labels.append(line.split(" ")[0])
                labels[line.split(" ")[0]] = pc # dict test init (next pc)
                     
            print(l, " pc:",pc, " instr:", i_hex," pc+",i_pc," p1,p2", i_p1, i_p2)
            l += 1
    
    print("- temp_labels:",labels)
    print("- temp_prog. :",program)
    print("[ the second pass replaces labels with addr. ]")
    
    i=0
    
    for part1 in program:
        if str(part1)+":" in labels:
            print("---label---",part1+":",labels[part1+":"])
            print(program[i],"<---",labels[part1+":"])
            program[i] = labels[part1+":"] # todo addr 2 bytes
        i += 1
  
    return program


DEBUG = False

print("- instructions revers. (opcode/instr list)")
opcodes = {}
for instruct, opcode in instr.instructions.items():
    opcodes[opcode] = instruct
    if DEBUG: print(opcodes[opcode], end=".")


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


@octopus_duration(True)
def run_hex_code(uP, instr_set, run_delay_ms=1, run=True):
    
    run_code = True
    pc, uP.pc = 0, 0
    while run_code: # max loop
        if run: pc = uP.pc
        instr = opcodes.get(int(instr_set[pc]))
        if DEBUG: print("instr:", instr)
        if instr:
            # try:
            hex_i0 = num_to_hex_str2(int(instr_set[pc]))+"  "
            if instr in table.zero_param_instr:
                print(pc,"{0}",hex_i0, instr)
                add_pc = 1
                param = ""

            if instr in table.double_param_instr:
                param1 = instr_set[pc+1]
                param2 = instr_set[pc+2]
                print(pc,"{2}",hex_i0 , instr, num_to_hex_str2(param1), num_to_hex_str2(param2))
                add_pc = 3
                param = param1, param2
                
            if (instr not in table.double_param_instr) and (instr not in table.zero_param_instr):
                param = instr_set[pc+1]
                print(pc,"{1}",hex_i0 , instr, hex(param))
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