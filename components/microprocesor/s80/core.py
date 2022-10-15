# core simple_80 processor

from utils.octopus_decor import octopus_duration
from octopus_digital import num_to_bin_str8

"""
from components.microprocesor.s80.core import Executor
uP = Executor() # microProcesor

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
        
        if inst=="INR A":
            self.a += 1
            if self.a > 255:
                self.a = 0
                self.cb = 1
            self.pc += 1
            
        if inst=="DCR A":
            self.a -= 1
            self.zb = 1 if self.a == 0 else 0
            self.pc += 1
        
        if inst=="MVI A":
            self.a = param
            self.zb = 1 if self.a == 0 else 0
            self.pc += 2
            
        if inst=="MVI B":
            self.b = param
            self.pc += 2
    
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

      
    """
    def i_add4(self, params):
        p = params[0]
        self.acc = self.acc + self.regs[p] + self.cy
        self.cy = self.acc >> 4
        self.acc &= 0xF
    def i_adm(self, params):
        self.acc = self.acc + self.memory[self.dp] + self.cy
        self.cy = self.acc >> 4
        self.acc &= 0xF
        
    def i_bbl(self, params):
        self.jump(self.stack.pop())
        self.acc = params[0] & 0xF
    
    def i_clb(self, params):
        self.acc = 0
        self.cy = 0
        
    def i_clc(self, params):
        self.cy = 0
        
    def i_cma(self, params):
        self.acc ^= 0xF
        
    def i_cmc(self, params):
        self.cy ^= 1
    
    def i_daa(self, params):
        if self.acc >= 10 or self.cy:
            self.acc += 6
        if self.acc >= 16:
            self.cy = 1
            self.acc -= 16
    
    def i_dac(self, params):
        self.acc = (self.acc - 1) & 0xF
        self.cy = 1 if self.acc != 15 else 0
    
    def i_fim(self, params):
        p = params[0] & 0xE
        v = params[1]
        self.regs[p] = (v >> 4) & 0xF
        self.regs[p + 1] = v & 0xF
    
    def i_fin(self, params):
        p = params[0] & 0xE
        addr = 'd' + str(self.regs[0] * 16 + self.regs[1])
        if addr in self.prg:
            v = self.prg[addr]
            self.regs[p] = (v >> 4) & 0xF
            self.regs[p + 1] = v & 0xF
            self.cycles += 1
        else:
            raise Exception("Attempt to read the data from uninitialized ROM address %s" % addr[1:])
            
    def i_iac(self, params):
        self.acc = (self.acc + 1) & 0xF
        self.cy = 1 if self.acc == 0 else 0
    
    def i_jcn(self, params):
        op = params[0]
        if op not in ['c0', 'c1', 'az', 'an']:
            raise Exception("Unknown jump condition '%s'!" % op);
        if op[0] == 'c':
            if str(self.cy) != op[1]:
                return
        elif op == 'az' and self.acc != 0:
            return
        elif op == 'an' and self.acc == 0:
            return
        self.jump(params[1])
    
    def i_jms(self, params):
        addr = params[0]
        if type(addr) != int:
            raise Exception('Subroutine address not resolved: ' + str(addr))
        if addr < 0x300:
            self.stack.append(self.ip)
            self.jump(params[0])
        else:
            try:
                subr = getattr(self, "c_%0.3x" % addr)
            except AttributeError:
                raise Exception("No custom subroutine for address %0.3x was defined!" % addr)
            subr()
    
    def i_jun(self, params):
        self.jump(params[0])
    
    def i_inc(self, params):
        p = params[0]
        self.regs[p] = (self.regs[p] + 1) & 0xF
    
    def i_isz(self, params):
        p = params[0]
        self.regs[p] = (self.regs[p] + 1) & 0xF
        if self.regs[p] != 0:
            self.jump(params[1])
    
    def i_ld(self, params):
        self.acc = self.regs[params[0]]
        
    def i_ldm(self, params):
        self.acc = params[0] & 0xF
    
    
    def i_ral(self, params):
        self.acc = (self.acc << 1) + self.cy
        self.cy = self.acc >> 4
        self.acc &= 0xF
    
    def i_rar(self, params):
        cy = self.acc & 1
        self.acc = (self.acc >> 1) + (self.cy << 3)
        self.cy = cy
    
    def i_rdm(self, params):
        self.acc = self.memory[self.dp]
    
    def i_src(self, params):
        p = params[0] & 0xE
        self.dp = (self.regs[p] << 4) + self.regs[p + 1]
    
    def i_stc(self, params):
        self.cy = 1
    
    def i_sub(self, params):
        p = params[0]
        self.acc = self.acc + self.cy + (self.regs[p] ^ 0xF)
        self.cy = self.acc >> 4
        self.acc &= 0xF
    
    def i_sbm(self, params):
        self.acc = self.acc + 16 - self.memory[self.dp] - self.cy
        self.cy = self.acc >> 4
        self.acc &= 0xF
    
    def i_tcc(self, params):
        self.acc = self.cy
        self.cy = 0
    
    def i_tcs(self, params):
        self.acc = 9 + self.cy
        self.cy = 0
    
    def i_wrm(self, params):
        self.memory[self.dp] = self.acc
    
    def i_xch(self, params):
        p = params[0]
        self.regs[p], self.acc = self.acc, self.regs[p]
"""
    
"""    
#  =================================================
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
"""
