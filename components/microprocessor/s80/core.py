# octopusLAB - core - simple_80 processor
__version__ = "1.0.6" # 2023/10/25

from time import sleep, sleep_ms
from utils.octopus_decor import octopus_duration
from octopus_digital import num_to_bin_str8, num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from octopus_digital import hex_dump
from components.microprocessor.s80 import instructions as instr
from components.microprocessor.s80 import table
from components.microprocessor.s80.table import get_instr_param
from machine import Pin
from utils.pinout import set_pinout
pinout = set_pinout()
import gc
print("- init")
print("core: ESP mem_free",gc.mem_free())
gc.collect()
print("core: ESP mem_free",gc.mem_free())

# Hw components:
HW_LED = False
HW_RGB = True
DISPLAY8 = False
DISPLAY_TM = True
DISPLAY_LCD4 = False
EXP16_74LS374 = False

HW_DEBUG = True


if HW_LED: # Leds
    from components.led import Led
    led = Led(2)
    led.blink()
    
def rgb_fill(ws, c=(0,0,0)):
    for i in range(8):
        ws.color(c,i)
            
if HW_RGB: # Leds
    # from components.ws_rgb import Rgb
    from components.rgb import Rgb
    ws = Rgb(pinout.DEV1_PIN,8)
    # ws.rainbow_cycle()
    rgb_fill(ws,(100,0,0))
    sleep(0.3)
    rgb_fill(ws,(0,0,0))
 
if DISPLAY_LCD4:
    from components.udi_hw import i2c_init, lcd4_init, lcd4_show
    i2c = i2c_init()
    lcd = lcd4_init(i2c)
    #              "****************"
    lcd4_show(lcd, "start & init",3)
 
if DISPLAY8:
    from utils.octopus import disp7_init
    d8 = disp7_init()
    
if DISPLAY_TM:    
    from lib.tm1638 import TM1638
    tm = TM1638(stb=Pin(pinout.SPI_MOSI_PIN), clk=Pin(pinout.SPI_MISO_PIN), dio=Pin(pinout.SPI_CLK_PIN))
    tm.show2("0000  FF")
    # table1: matrix 4x4 - ABCD > K1 K2 K3 -
    btn_tab = {1:'E',2:'8',4:'4',8:'123',16:'C',32:'7',64:'3',128:'123',512:'0',1024:'6',2048:'2',8192:'9',16384:'5',32768:'1'}

if EXP16_74LS374:
    from octopus_digital import neg, reverse, int2bin, get_bit, set_bit
    from octopus_digital import num_to_bin_str8
    from universal_digital_interface import num_to_bytes2
    from components.udi_hw import exp16_init
    # expander instance, byty2 temp, clk 74LS374
    e16, b2, clk = exp16_init()
    PORT_REVERSE = False
    PORT_NEGATIVE = True


def port16rw(i):
   data = num_to_bytes2(neg(i),rev=PORT_REVERSE)
   data[0] = 255 # 8 bits for input SW
   """
   0-SW     1-LED
   76543210 76543210
   """
   r = e16.read()
   print(i, num_to_bin_str8(i), data, " --- ", neg(r), num_to_bin_str8(neg(r)))
   e16.write(data)
   clk.value(1)
   sleep_ms(10)
   clk.value(0)


def port16r(addr=0):
   r = e16.read()
   print("port16r - read", r, neg(r), num_to_bin_str8(neg(r)))
   return neg(r)


"""
from components.microprocesor.s80.core import Executor
uP = Executor() # microProcesor

from components.microprocesor.s80.core import Executor, create_hex_program, parse_file
program = parse_file(uP,"example01_s80.asm")
hex_program = create_hex_program(program,prn=False)
run_hex_code(uP,hex_program,run_delay_ms=10)
"""
MEM_MAX = 300

class Executor:
    
    def __init__(self):
        self.debug = False
        
        ## self.vm = {} # virtual memory
        ## self.vm[255] = 0
        self.mem = [0] * MEM_MAX # 0-255 proram / 256-300 Data
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
        self.is_running = True

    
    def set_acc(self, value): # for test
        self.a = value
        self.zb = 1 if self.a == 0 else 0
        

    def set_z(self, data):
        self.zb = 1 if data == 0 else 0


    def set_c(self, data):
        self.cb = 1 if data > 255 else 0
                    
            
    def print_regs(self): # dec, hex, bin
        print("="*32)
        print("[ system registers ]")
        print("a:",self.a, hex(self.a), num_to_bin_str8(self.a))
        print("b:",self.b, " | c:",self.c)
        print("h:",self.h, " | l:",self.l)
        # print("d",self.d)
        # print("e",self.e)
        print("-"*32)
        print("|S|Z|0|C|0|P|1|C|")
        print(f"|{self.sb}|{self.zb}|0|{self.acb}|0|{self.pb}|1|{self.cb}|")
        print("="*32)
    
    def print_mem(self):
        print("="*32)
        hex_dump(self.mem,row=18)
        print("-"*32)
        
    def clear_mem(self):
        print("="*32)
        for i in range(MEM_MAX):
            self.mem[i] = 0
        print("-"*32)
        
    """   
    def print_vm(self):
        print("[ virtual memory ] - (16/32 bytes)")
                
        vm_values = list(self.vm.values())
        
        print("vm_values:")
        for it in vm_values:
            try:
                 #print(i, chr(self.vm[i]),end=" ")
                 print(it, end=" ")
            except:
                print("vm.Err values:")
        
        print()        
        print("vm_chars:")        
        for it in vm_values:
            try:
                 if it > 0:
                     print(chr(it), end=" ")
            except:
                print("vm.Err chars:")
                       
     """
    
    #------------------------------
    def execute(self, inst, param):
        self.loop += 1
        
        if inst=="NOP":
            self.pc += 1
                 
        if inst=="HLT":
            self.is_running = False
        
        if inst=="INR_A":
            self.a += 1
            #if self.a > 255:
            #    self.a = 0
            #    self.cb = 1
            self.set_c(self.a)
            if self.a > 255: self.a = 0
            
            self.set_z(self.a) #q#?
            self.pc += 1
            
        if inst=="INR_B":
            self.b += 1
            self.set_c(self.b)
            if self.b > 255: self.b = 0
            self.pc += 1
                
        if inst=="INR_C":
            self.c += 1
            self.set_c(self.c)
            if self.c > 255: self.c = 0
            self.pc += 1
                
        if inst=="INR_H":
            self.h += 1
            self.set_c(self.h)
            if self.h > 255: self.h = 0
            self.pc += 1
                
        if inst=="INR_L":
            self.l += 1
            self.set_c(self.l)
            if self.l > 255: self.l = 0
            self.pc += 1
        
        if inst=="INX_B":
            num = self.c + self.b*256 + 1
            self.b = int(num/256)
            self.c = num - self.b*256
            #self.set_c(self.b)
            #if self.b > 255: self.b = 0
            self.pc += 1

        if inst=="INX_H":
            num = self.l + self.h*256 + 1
            self.h = int(num/256)
            self.l = num - self.h*256
            #self.set_c(self.b)
            #if self.b > 255: self.b = 0
            self.pc += 1
        
        if inst=="DCR_A":
            self.a -= 1
            # self.zb = 1 if self.a == 0 else 0
            self.set_z(self.a)
            self.pc += 1            
        
        if inst=="DCR_B":
            self.b -= 1
            self.set_z(self.b)
            self.pc += 1
            
        if inst=="DCR_C":
            self.c -= 1
            self.set_z(self.c)
            self.pc += 1
            
        if inst=="DCR_H":
            self.h -= 1
            self.set_z(self.h)
            self.pc += 1
            
        if inst=="DCR_L":
            self.l -= 1
            self.set_z(self.l)
            self.pc += 1
            
        if inst=="DCX_B":
            num = self.c + self.b*256 - 1
            self.b = int(num/256)
            self.c = num - self.b*256
            #self.set_c(self.b)
            #if self.b > 255: self.b = 0
            self.pc += 1

        if inst=="DCX_H":
            num = self.l + self.h*256 - 1
            self.h = int(num/256)
            self.l = num - self.h*256
            #self.set_c(self.b)
            #if self.b > 255: self.b = 0
            self.pc += 1
                    
        if inst=="LDA": ## LDA a lb hb - Load A from memory
            # [0]=H [1]=L   0x01 0x03 = 256+3
            addr = param[0] + param[1]*256
            print("LDA addr test", param[0], param[1], "-->",addr, self.mem[addr])
            # self.a = self.vm.get(addr)
            try:
                self.a = self.mem[addr]
            except:
                self.a = "0xEE"
            self.zb = 1 if self.a == 0 else 0
            self.pc += 3
            
        if inst=="STA": ## STA a  lb hb - Store A to memory
            # [0]=H [1]=L   0x01 0x03 = 256+3
            addr = param[0] + param[1]*256
            # self.vm[addr] = self.a
            self.mem[addr] = self.a
            self.pc += 3

        if inst=="CMA": ## Compliment A / inverse
            self.a = self.a ^ 0xff
            self.pc += 1           
                     
        if inst=="ANI": ## AMD immediate with A
            self.a = self.a & param
            self.zb = 1 if self.a == 0 else 0
            self.pc += 2
            
        if inst=="ORI": ## OR immediate with A
            self.a = self.a | param
            self.zb = 1 if self.a == 0 else 0
            self.pc += 2
            
        if inst=="XRI": ## ExclusiveOR immediate with A
            self.a = self.a ^ param
            self.zb = 1 if self.a == 0 else 0
            self.pc += 2 
        
        if inst=="MVI_A": ## MVI r, - Move immediate to register
            self.a = param
            self.zb = 1 if self.a == 0 else 0
            self.pc += 2
                
        if inst=="MVI_B":
            self.b = param
            self.zb = 1 if self.b == 0 else 0
            self.pc += 2
            
        if inst=="MVI_C":
            self.c = param
            self.zb = 1 if self.c == 0 else 0
            self.pc += 2
            
        if inst=="MVI_L":
            self.l = param
            self.zb = 1 if self.l == 0 else 0
            self.pc += 2
            
        if inst=="MVI_H":
            self.h = param
            self.zb = 1 if self.h == 0 else 0
            self.pc += 2
            
        if inst=="MVI_M":
            self.vm[self.h*256+self.l] = param
            self.zb = 1 if param == 0 else 0
            self.pc += 2 
            
        if inst=="LXI_B": ## LXI RP (B_C),lb hb - Load register pair immediate
            self.c = param[0]
            self.b = param[1] 
            self.pc += 3
            
        if inst=="LXI_H": # H byte3 / L byte2 ??? I L H
            ## LXI RP (H_L),lb hb - Load register pair immediate
            self.l = param[0]
            self.h = param[1] 
            self.pc += 3
            
        if inst=="ANA_B": ## AND register with A
            self.a = self.a & self.b
            self.zb = 1 if self.a == 0 else 0
            self.pc += 1
            
        if inst=="ANA_C":
            print(self.c , self.a & self.c)
            self.a = self.a & self.c
            self.zb = 1 if self.a == 0 else 0
            self.pc += 1    
            
        if inst=="ORA_B": ## OR register with A
            self.a = self.a | self.b
            self.zb = 1 if self.a == 0 else 0
            self.pc += 1
            
        if inst=="ORA_C":
            self.a = self.a | self.c
            self.zb = 1 if self.a == 0 else 0
            self.pc += 1
            
        if inst=="XRA_B": ## ExclusiveOR register with A
            self.a = self.a ^ self.b
            self.zb = 1 if self.a == 0 else 0
            self.pc += 1
            
        if inst=="XRA_C":
            self.a = self.a ^ self.c
            self.zb = 1 if self.a == 0 else 0
            self.pc += 1    
            
        if inst=="MOV_B,A": ## B <- A
            self.b = self.a
            self.pc += 1
            
        if inst=="MOV_A,B": ## A <- B
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
            # ToDo: if addr > 300 ...
            # self.a = self.vm.get(addr)
            self.a = self.mem[addr]
            #print("MOV_A,M addr test", self.h, self.l, "-->",addr,self.vm.get(addr))
            self.pc += 1
            
        if inst=="MOV_M,A":
            addr = self.h*256+self.l
            # self.vm[self.h*256+self.l] = self.a
            self.mem[addr] = self.a 
            self.pc += 1
            
        if inst=="ADD_A":        
            #self.a = self.a + param + self.cy  #q#
            self.a = self.a + param
            self.set_c(self.a)
            if self.a > 255: self.a = self.a - 256 
            self.pc += 2
            
        if inst=="CPI": ## Compare immediate with A
            compare  = param - self.a
            #self.zb = 1 if compare == 0 else 0
            self.set_c(compare)
            self.cb = 1 if compare > 0 else 0
            self.pc += 2
            
        if inst=="RRC": ## Rotate A right (with carry)      
            self.a = self.a >> 1
            self.pc += 1
            """
            if self.a > 255:
                self.a = 0
                self.cb = 1
            """
                        
        if inst=="RLC": ## Rotate A left (with carry)       
            self.a = self.a << 1
            self.set_c(self.a)
            self.pc += 1
            
        #self.cy = self.acc >> 4
        #self.acc &= 0xF
            
        if inst=="JMP": ## Unconditional jump
            #self.pc = param[0]*256+param[1] # direct to addr: 0x00 0xFF
            self.pc = param[0]+param[1]*256 # 00 01 > 256 / 01 00 > 01  #v23.02
            if(self.debug):print("> JMP to ",self.pc)
                        
        if inst=="CALL": ## Unconditional subroutine call
            self.sp = self.pc + 3 # stack
            self.pc = param[0]+param[1]*256
            if(self.debug): print("> CALL from",self.sp,"to",self.pc)
                     
        if inst=="RET": ##  Unconditional return from subroutine
            self.pc = self.sp # stack
            if(self.debug): print("> RET to ",self.pc)
            self.sp = 0
            
        if inst=="JNZ": ## Conditional jump / not zerro
            if self.zb == 0:
                self.pc = param[0]+param[1]*256
                if(self.debug): print("> jump to ",self.pc)
            else:
                self.pc += 3
            
        if inst=="JZ": ## 
            if self.zb == 1:
                self.pc = param[0]+param[1]*256 # 0x00 0xFF
                if(self.debug): print("> jump to ",self.pc)
            else:
                self.pc += 3
                
        if inst=="JNC":
            if self.cb == 0:
                self.pc = param[0]+param[1]*256
                if(self.debug): print("> jump to ",self.pc)
            else:
                self.pc += 3
            
        if inst=="JC":
            if self.cb == 1:
                self.pc = param[0]+param[1]*256 # 0x00 0xFF
                if(self.debug): print("> jump to ",self.pc)
            else:
                self.pc += 3
                
        # ------------- spec subroutines --------
        if inst=="OUT":
            print("OUT",param,self.a)            
            if EXP16_74LS374:
                port16rw(self.a)
            self.pc += 2


        if inst=="IN":
            print("IN",param,self.a)            
            if EXP16_74LS374:
                data = port16r(param)
                self.a = data
            self.pc += 2
        
             
        if inst=="MOV_A,A": # Main info report / regs
            num_bc = self.c + self.b*256
            num_lh = self.l + self.h*256
            print("--> R ","DEC BIN    HEX (B_C)" )
            print("    A: ", self.a, num_to_bin_str8(self.a), num_to_hex_str2(self.a))
            print("    B: ", self.b, num_to_bin_str8(self.b), num_to_hex_str2(self.b), " ("+str(num_bc)+")")
            print("    C: ", self.c, num_to_bin_str8(self.c), num_to_hex_str2(self.c), " ["+str(num_lh)+"]")
            
            if HW_DEBUG and DISPLAY_TM:
                tm.show2(num_to_hex_str4(self.pc)+"  "+num_to_hex_str2(self.a))
                i = 0
                for a_bit in num_to_bin_str8(self.a):
                    if a_bit =="1": ws.color((100,0,0),7-i)
                    else: ws.color((0,0,0),7-i)
                    i += 1
                    if i > 7: i = 7
            self.pc += 1
            
        if inst=="MOV_B,B": # Virtual memory
            print("--> spec.sub. | vitrual memory:")
            self.print_mem()
            self.pc += 1
               
        if inst=="MOV_C,C": # C-counter
            print("--> spec.sub. | pc:", self.pc)
            self.pc += 1
            
        if inst=="MOV_D,D": # D-display
            print("--> spec.sub. | 7seg. display ")
            addr = self.h*256 + self.l
            data8 = num_to_hex_str2(self.vm.get(addr))
            print("[ "+num_to_hex_str4(addr)+ " | "+ data8+ " ]")
            if DISPLAY8:
               d8.show(num_to_hex_str4(addr)+"  "+data8)
               sleep(0.5)             
            self.pc += 1
            
        if inst=="MOV_E,E": # D-slEEp
            print("--> spec.sub. | sleep 1 sec. (slEEp)")
            sleep(1)
            self.pc += 1  
            
        if inst=="MOV_H,H":
            print("--> spec.sub. - LED_ON (High)")
            if HW_LED: led.value(1)
            self.pc += 1
            
        if inst=="MOV_L,L":
            print("--> spec.sub. - LED_OFF (Low)")
            if HW_LED: led.value(0)
            if HW_RGB: rgb_fill(ws)
            self.pc += 1
            
        if(True): # /debug
            print(f"                      --->#{self.loop} |S{self.sb} Z{self.zb} C{self.cb}| {num_to_bin_str8(self.a)} | {self.a}, {hex(self.a)} {(self.pc)} ")

# -----------------------------------------
def parse_file(uP, file_name="", asm="",print_asm=True, debug = True):
    pc = 0
    labels = {}
    variables = {}
    program = []
               
    gc.collect()
    if len(file_name) > 2:
        print("---", file_name, "---")
        f = open("examples/"+file_name)
        fs = f.read()
        f.close()
    else:
        fs = asm
     
    if print_asm:
        print("-"*32)
        print()
        print(fs)
        print()
        print("-"*32)
        
    print("[ two pass - translator ]")
    print("[---1---] first pass:")
    
    for line in fs.splitlines():
        clean_line = line.split(";")[0].strip()
        
        # data_string
        index_vm = 256  # start data virtual memory FF+1
        if clean_line.count("#DATA"): 
            parts = clean_line.split("=")
            data_string=parts[1].strip().replace('"','')
            print("data_string:",data_string)
            for ch in data_string:
                # uP.vm[index_vm] = ord(ch)
                uP.mem[index_vm] = ord(ch)
                index_vm += 1
            uP.mem[index_vm] = 0 # last "0" = stop
            
        # ToDo: #SUBPROC? load simple rutines for CALL with RET
        # maybe RAM/ROM or all self.mem?
        
        # variables  $var = 123 ---> var: 123
        if clean_line.count("$"):
            var_parts = clean_line.split(";")[0].split("=")
            variables[var_parts[0].strip().replace("$","")] = var_parts[1].strip()
        
    print("- temp_variables",variables)
       
    for var_name,var in variables.items():
        print("replace", var_name, var) # variables[var_name]
        fs = fs.replace(var_name,var)
    print()
    print("-"*32)
        
    print("[---2---] second pass:")
    l=0
    for line in fs.splitlines():
        
        # clean up    
        clean_line = line.split(";")[0].strip()
        clean_line = clean_line.replace('   ',' ')  # 123456 > 12 | 12345 > 123 | 1234 > 12
        clean_line = clean_line.replace('  ',' ')   # 123 > 12
        clean_line = clean_line.replace('  ',' ')
              
                    
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
                    
                    if i1 =="LDA" or i1 =="STA" or i1 == "LXI_B" or i1 == "LXI_H": # ToDo in list
                        print("-LD/ST-A-add",parts[1],parts[2])
                        # program.append(0x0) # simple jmp to (0 addr)
                        program.append(parts[1])
                        program.append(parts[2])
                    else:
                        try:
                            #22: JMP 00 01 > 01 / xx addr / 01
                            #23: JMP 01 00 > 01 / addr xx / addr --- ToDo > 255 program space
                            if i_pc > 2:                                
                                ## print("---jmp---add 0x00")
                                program.append("0x11") # tempor. place for 8080 compatibility
                                print("--- 23 JMP --- temp ") # third: 11 aa -> aa 00
                            if i_pc > 1:
                                i_p1 = parts[1]
                                #if i_p1+":" in labels
                                program.append(i_p1)
                                #23: program.append(0x0)
                    
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
    print("[---3---] third pass:")
    print("- replaces labels with addr.")
    
    i=0
    
    for part1 in program:
        if str(part1)+":" in labels:
            print("---label---",part1+":",labels[part1+":"])
            print(program[i],"<---",labels[part1+":"])
            program[i-1] = labels[part1+":"] # addr 2 bytes : temp addr -> addr 0 // limit: max 256 B program
            program[i] = "0x00"
        i += 1
    
    print("*"*32)
    #print("len(program)",len(program))
    #for i in range(255,260):
    #    print(i,uP.mem[i])       
           
    for i in range(len(program)):
        # print(i,program[i])
        uP.mem[i] = int(program[i])
    
    return program

DEBUG = False

print("- instructions revers. (opcode/instr list)")
opcodes = {}
for instruct, opcode in instr.instructions.items():
    opcodes[opcode] = instruct
    if DEBUG: print(opcodes[opcode], end=".")


@octopus_duration(True)
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


def print_hex_program(p): # really hex )
    for h in p:
        print(num_to_hex_str2(h),end=" ")
    print()


@octopus_duration(True)
def run_hex_code(uP, instr_set, run_delay_ms=1, run=True):
    pc, run_code = 0,True
    uP.pc, uP.is_running = 0, True
    
    while run_code and uP.is_running: # max loop
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
