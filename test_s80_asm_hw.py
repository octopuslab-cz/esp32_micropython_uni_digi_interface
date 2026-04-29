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
    run_hex_code(uP,hex_program,run_delay_ms=100)

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
; example_counter_s80
; C = limit (12), A = counter
; display A each step, stop when A > C
;
$limit = 6;

start:
    MOV_A,A
    MVI_C limit    ; C = limit
    MVI_A 0x0    ; A = 0  (counter)
;
loop:
    MOV_A,A      ; display A (spec. subrutina)
    ADI 1        ; A = A + 1
    CMP_C        ; A - C → nastav příznaky
    JC  loop     ; C=1 znamená A < C → pokračuj
    JZ  loop     ; Z=1 znamená A == C → pokračuj (chceme A > C)
;
finish:
    MOV_A,A      ; zobraz finální hodnotu
    HLT
end.
    """
print(asm)

run_test(f="",asm=asm)



"""
--- start ---
================================
[ system registers ]
a: 0 0x0 00000000
b: 0  | c: 0
h: 0  | l: 0
--------------------------------
|S|Z|0|C|0|P|1|C|
|0|1|0|0|0|0|1|0|
================================
ESP mem_free: 126976

start:
    MVI_A 0b00000111   ; a = 7 (dec)  | 0x07 (hex) 
    MVI_C 0b10101010   ; c = 170 (dec)| 0xAA (hex) 
    MOV_B,A    ; b <= ( a = 7 )
;              
loop1:
    NOP        ; test correct jump
    DCR_A      ; decrement
    JNZ loop1  ; jump if not zero   
loop2:
    MVI_A 0x09 ; a = 9 | 0x09 (hex)
    RLC  
    RLC
    RLC
    RRC
    RRC
    RRC
;    
    MVI_A 0xFF ; 255
    INR_A      ; 255+1 --> C = 1
    INR_A      ; 0+1   --> C = 0
    INR_A      ; 2
    INR_A      ; 3
    ADD_A 255  ; 3+255 = 257-256 = 2
    INR_A
    NOP
    
end.
    
[ clear_mem() ]
================================
--------------------------------

================================
- file name: 


log from terminal -->
--------------------------------


start:
    MVI_A 0b00000111   ; a = 7 (dec)  | 0x07 (hex) 
    MVI_C 0b10101010   ; c = 170 (dec)| 0xAA (hex) 
    MOV_B,A    ; b <= ( a = 7 )
;              
loop1:
    NOP        ; test correct jump
    DCR_A      ; decrement
    JNZ loop1  ; jump if not zero   
loop2:
    MVI_A 0x09 ; a = 9 | 0x09 (hex)
    RLC  
    RLC
    RLC
    RRC
    RRC
    RRC
;    
    MVI_A 0xFF ; 255
    INR_A      ; 255+1 --> C = 1
    INR_A      ; 0+1   --> C = 0
    INR_A      ; 2
    INR_A      ; 3
    ADD_A 255  ; 3+255 = 257-256 = 2
    INR_A
    NOP
    
end.
    

--------------------------------
[ two pass - translator ]
[---1---] first pass:
- temp_variables {}

--------------------------------
[---2---] second pass:
0  pc: 0  instr: 0  pc+ 0  p1,p2  
---parts: ['MVI_A', '0b00000111']
1  pc: 2  instr: 0x3e  pc+ 2  p1,p2  
---parts: ['MVI_C', '0b10101010']
2  pc: 4  instr: 0xe  pc+ 2  p1,p2  
---parts: ['MOV_B,A']
3  pc: 5  instr: 0x47  pc+ 1  p1,p2  
4  pc: 5  instr: 0  pc+ 0  p1,p2  
---parts: ['NOP']
5  pc: 6  instr: 0x0  pc+ 1  p1,p2  
---parts: ['DCR_A']
6  pc: 7  instr: 0x3d  pc+ 1  p1,p2  
---parts: ['JNZ', 'loop1']
7  pc: 10  instr: 0xc2  pc+ 3  p1,p2  
8  pc: 10  instr: 0  pc+ 0  p1,p2  
---parts: ['MVI_A', '0x09']
9  pc: 12  instr: 0x3e  pc+ 2  p1,p2  
---parts: ['RLC']
10  pc: 13  instr: 0x7  pc+ 1  p1,p2  
---parts: ['RLC']
11  pc: 14  instr: 0x7  pc+ 1  p1,p2  
---parts: ['RLC']
12  pc: 15  instr: 0x7  pc+ 1  p1,p2  
---parts: ['RRC']
13  pc: 16  instr: 0xf  pc+ 1  p1,p2  
---parts: ['RRC']
14  pc: 17  instr: 0xf  pc+ 1  p1,p2  
---parts: ['RRC']
15  pc: 18  instr: 0xf  pc+ 1  p1,p2  
---parts: ['MVI_A', '0xFF']
16  pc: 20  instr: 0x3e  pc+ 2  p1,p2  
---parts: ['INR_A']
---parts: ['INR_A']
Err. No3
17  pc: 23  instr: 0xdb  pc+ 2  p1,p2  
---parts: ['INR_A']
---parts: ['INR_A']
Err. No3
18  pc: 26  instr: 0xdb  pc+ 2  p1,p2  
---parts: ['INR_A']
---parts: ['INR_A']
Err. No3
19  pc: 29  instr: 0xdb  pc+ 2  p1,p2  
---parts: ['INR_A']
---parts: ['INR_A']
Err. No3
20  pc: 32  instr: 0xdb  pc+ 2  p1,p2  
---parts: ['ADD_A', '255']
21  pc: 33  instr: 0x87  pc+ 1  p1,p2  
---parts: ['INR_A']
---parts: ['INR_A']
Err. No3
22  pc: 36  instr: 0xdb  pc+ 2  p1,p2  
---parts: ['NOP']
23  pc: 37  instr: 0x0  pc+ 1  p1,p2  
24  pc: 37  instr: 0  pc+ 0  p1,p2  
- temp_labels: {'loop2:': 10, 'loop1:': 5, 'start:': 0}
- temp_prog. : [62, '0b00000111', 14, '0b10101010', 71, 0, 61, 194, 'loop1', 0, 62, '0x09', 7, 7, 7, 15, 15, 15, 62, '0xFF', 60, 219, 0, 60, 219, 0, 60, 219, 0, 60, 219, 0, 135, 60, 219, 0, 0]
[---3---] third pass:
- replaces labels with addr.
---label--- loop1: 5
loop1 <--- 5
********************************
.:. function:  create_hex_program
--> duration (milis.) --> 1
--------------------------------
- program_num
[62, 7, 14, 170, 71, 0, 61, 194, 5, 0, 62, 9, 7, 7, 7, 15, 15, 15, 62, 255, 60, 219, 0, 60, 219, 0, 60, 219, 0, 60, 219, 0, 135, 60, 219, 0, 0]
- program_hex
3e 07 0e aa 47 00 3d c2 05 00 3e 09 07 07 07 0f 0f 0f 3e ff 3c db 00 3c db 00 3c db 00 3c db 00 87 3c db 00 00 
--------------------------------
- len(instr_set): 37
================================
1 0 {1} 3e   MVI_A 0x7
                      --->#1 |S0 Z0 C0| 00000111 | 7, 0x7 2 
2 2 {1} 0e   MVI_C 0xaa
                      --->#2 |S0 Z0 C0| 00000111 | 7, 0x7 4 
3 4 {0} 47   MOV_B,A
                      --->#3 |S0 Z0 C0| 00000111 | 7, 0x7 5 
4 5 {0} 00   NOP
                      --->#4 |S0 Z0 C0| 00000111 | 7, 0x7 6 
5 6 {0} 3d   DCR_A
                      --->#5 |S0 Z0 C0| 00000110 | 6, 0x6 7 
6 7 {2} c2   JNZ 05 00
                      --->#6 |S0 Z0 C0| 00000110 | 6, 0x6 5 
7 5 {0} 00   NOP
                      --->#7 |S0 Z0 C0| 00000110 | 6, 0x6 6 
8 6 {0} 3d   DCR_A
                      --->#8 |S0 Z0 C0| 00000101 | 5, 0x5 7 
9 7 {2} c2   JNZ 05 00
                      --->#9 |S0 Z0 C0| 00000101 | 5, 0x5 5 
10 5 {0} 00   NOP
                      --->#10 |S0 Z0 C0| 00000101 | 5, 0x5 6 
11 6 {0} 3d   DCR_A
                      --->#11 |S0 Z0 C0| 00000100 | 4, 0x4 7 
12 7 {2} c2   JNZ 05 00
                      --->#12 |S0 Z0 C0| 00000100 | 4, 0x4 5 
13 5 {0} 00   NOP
                      --->#13 |S0 Z0 C0| 00000100 | 4, 0x4 6 
14 6 {0} 3d   DCR_A
                      --->#14 |S0 Z0 C0| 00000011 | 3, 0x3 7 
15 7 {2} c2   JNZ 05 00
                      --->#15 |S0 Z0 C0| 00000011 | 3, 0x3 5 
16 5 {0} 00   NOP
                      --->#16 |S0 Z0 C0| 00000011 | 3, 0x3 6 
17 6 {0} 3d   DCR_A
                      --->#17 |S0 Z0 C0| 00000010 | 2, 0x2 7 
18 7 {2} c2   JNZ 05 00
                      --->#18 |S0 Z0 C0| 00000010 | 2, 0x2 5 
19 5 {0} 00   NOP
                      --->#19 |S0 Z0 C0| 00000010 | 2, 0x2 6 
20 6 {0} 3d   DCR_A
                      --->#20 |S0 Z0 C0| 00000001 | 1, 0x1 7 
21 7 {2} c2   JNZ 05 00
                      --->#21 |S0 Z0 C0| 00000001 | 1, 0x1 5 
22 5 {0} 00   NOP
                      --->#22 |S0 Z0 C0| 00000001 | 1, 0x1 6 
23 6 {0} 3d   DCR_A
                      --->#23 |S0 Z1 C0| 00000000 | 0, 0x0 7 
24 7 {2} c2   JNZ 05 00
                      --->#24 |S0 Z1 C0| 00000000 | 0, 0x0 10 
25 10 {1} 3e   MVI_A 0x9
                      --->#25 |S0 Z0 C0| 00001001 | 9, 0x9 12 
26 12 {0} 07   RLC
                      --->#26 |S0 Z0 C0| 00010010 | 18, 0x12 13 
27 13 {0} 07   RLC
                      --->#27 |S0 Z0 C0| 00100100 | 36, 0x24 14 
28 14 {0} 07   RLC
                      --->#28 |S0 Z0 C0| 01001000 | 72, 0x48 15 
29 15 {0} 0f   RRC
                      --->#29 |S0 Z0 C0| 00100100 | 36, 0x24 16 
30 16 {0} 0f   RRC
                      --->#30 |S0 Z0 C0| 00010010 | 18, 0x12 17 
31 17 {0} 0f   RRC
                      --->#31 |S0 Z0 C0| 00001001 | 9, 0x9 18 
32 18 {1} 3e   MVI_A 0xff
                      --->#32 |S0 Z0 C0| 11111111 | 255, 0xff 20 
33 20 {0} 3c   INR_A
                      --->#33 |S0 Z1 C1| 00000000 | 0, 0x0 21 
34 21 {1} db   IN 0x0
IN 0 0
                      --->#34 |S0 Z1 C1| 00000000 | 0, 0x0 23 
35 23 {0} 3c   INR_A
                      --->#35 |S0 Z0 C0| 00000001 | 1, 0x1 24 
36 24 {1} db   IN 0x0
IN 0 1
                      --->#36 |S0 Z0 C0| 00000001 | 1, 0x1 26 
37 26 {0} 3c   INR_A
                      --->#37 |S0 Z0 C0| 00000010 | 2, 0x2 27 
38 27 {1} db   IN 0x0
IN 0 2
                      --->#38 |S0 Z0 C0| 00000010 | 2, 0x2 29 
39 29 {0} 3c   INR_A
                      --->#39 |S0 Z0 C0| 00000011 | 3, 0x3 30 
40 30 {1} db   IN 0x0
IN 0 3
                      --->#40 |S0 Z0 C0| 00000011 | 3, 0x3 32 
41 32 {0} 87   ADD_A
                      --->#41 |S0 Z0 C0| 00000110 | 6, 0x6 33 
42 33 {0} 3c   INR_A
                      --->#42 |S0 Z0 C0| 00000111 | 7, 0x7 34 
43 34 {1} db   IN 0x0
IN 0 7
                      --->#43 |S0 Z0 C0| 00000111 | 7, 0x7 36 
44 36 {0} 00   NOP
                      --->#44 |S0 Z0 C0| 00000111 | 7, 0x7 37 
.:. function:  run_hex_code
--> duration (milis.) --> 323

--------------------------------
ESP mem_free: 106544
----------------regs
================================
[ system registers ]
a: 7 0x7 00000111
b: 7  | c: 170
h: 0  | l: 0
--------------------------------
|S|Z|0|C|0|P|1|C|
|0|0|0|0|0|0|1|0|
================================
----------------virtual mem.
================================
0000  3e  07  0e  aa  47  00  3d  c2  05  00  3e  09  07  07  07  0f  '>ªG.=Â.>	'
0010  0f  0f  3e  ff  3c  db  00  3c  db  00  3c  db  00  3c  db  00  '>ÿ<Û.<Û.<Û.<Û.'
0020  87  3c  db  00  00  00  00  00  00  00  00  00  00  00  00  00  '<Û.............'
0030  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  '................'
0040  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  '................'
0050  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  '................'
--------------------------------
asm file name: 
core_s80 ver. 0.3
"""

    