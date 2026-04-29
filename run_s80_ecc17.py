# simple test - basic microprocessor s80 "simple80" 8080/85/z80 class

import gc
print("- init")
print("mem_free",gc.mem_free())

from time import sleep, sleep_ms
from octopus_decor import octopus_duration
from octopus_digital import num_to_bin_str8, num_to_bytes2, num_to_hex_str4, num_to_hex_str2
from components.microprocessor.s80 import instructions as instr
from components.microprocessor.s80 import table
from components.microprocessor.s80.core import Executor, create_hex_program, parse_file, run_hex_code

DEBUG = False
uP = Executor() # microProcesor

print("--- start ---")
uP.set_acc(0)
uP.print_regs()
print("mem_free:",gc.mem_free())




# --- 2026 ok
#program = parse_file(uP, "example00_s80.asm") #******* 01,2,3,5,6,7
program = parse_file(uP, "ecc17_rgb.asm")
hex_program = create_hex_program(program,prn=False)

print("-"*30)
print("- program_num",hex_program)
print("-"*30)

print("len(instr_set):", len(hex_program))
print("="*30)
run_hex_code(uP,hex_program,1)

print()
print("-"*30)
print("mem_free:",gc.mem_free())

uP.print_regs()
uP.print_mem(18)


info ="""
-----------------
 1G = (15,13)
 2G = (2,10)
 3G = (8,3)
 5G = (6,6)
 6G = (5,8)
-----------------
-> result: (b, c)
"""
print(info)

"""
MPY: soft reboot
- init
mem_free 174128
- init
core: ESP mem_free 135504
core: ESP mem_free 145600
- instructions revers. (opcode/instr list)
--- decorator --- @octopus_duration:
--- decorator --- @octopus_duration:
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
mem_free: 139232
instructions list:
MOV_H,C 0x61 | MOV_H,H 0x64 | SBB_H 0x9c | ORI 0xf6 | MOV_C,H 0x4c | SBB_M 0x9e | SBB_L 0x9d | MOV_C,L 0x4d | MOV_C,M 0x4e | SBB_A 0x9f | INX_B 0x3 | RLC 0x7 | SBB_B 0x98 | SBB_C 0x99 | DCX_B 0xb | MOV_H,L 0x65 | INR_L 0x2c | INX_H 0x23 | MOV_H,M 0x66 | MOV_H,A 0x67 | DCX_H 0x2b | INR_H 0x24 | MOV_M,A 0x77 | MOV_M,B 0x70 | MOV_M,C 0x71 | INR_C 0xc | INR_B 0x4 | INR_A 0x3c | MOV_M,H 0x74 | MOV_M,L 0x75 | JMP 0xc3 | LDA 0x3a | JZ 0xca | JC 0xda | LXI_B 0x1 | RET 0xc9 | MOV_C,C 0x49 | MOV_D,D 0x52 | CMP_A 0xbf | CMP_B 0xb8 | MOV_E,E 0x5b | CMP_C 0xb9 | CMP_H 0xbc | JNC 0xd2 | LXI_H 0x21 | MVI_H 0x26 | MOV_L,M 0x6e | MOV_L,L 0x6d | CMP_L 0xbd | MVI_L 0x2e | MVI_M 0x36 | MOV_L,H 0x6c | CMP_M 0xbe | CPI 0xfe | MVI_A 0x3e | MVI_B 0x6 | SUB_L 0x95 | SUB_M 0x96 | MVI_C 0xe | MOV_L,A 0x6f | SUB_H 0x94 | ADI 0xc6 | MOV_L,B 0x68 | MOV_L,C 0x69 | CALL 0xcd | SUB_B 0x90 | SUB_C 0x91 | JNZ 0xc2 | SUB_A 0x97 | MOV_B,A 0x47 | MOV_B,C 0x41 | RRC 0xf | CMA 0x2f | MOV_A,B 0x78 | MOV_A,C 0x79 | MOV_B,H 0x44 | MOV_A,A 0x7f | MOV_B,B 0x40 | ANA_D 0xa2 | ANA_E 0xa3 | HLT 0x76 | XRI 0xee | MOV_B,L 0x45 | ANA_A 0xa7 | ADD_H 0x84 | ANA_B 0xa0 | ANA_C 0xa1 | ADD_M 0x86 | ADD_L 0x85 | OUT 0xd3 | ADD_B 0x80 | ADD_A 0x87 | ADD_C 0x81 | ANA_H 0xa4 | ANA_L 0xa5 | ANA_M 0xa6 | ORA_A 0xb7 | ORA_B 0xb0 | ORA_C 0xb1 | ORA_H 0xb4 | ORA_L 0xb5 | ORA_M 0xb6 | DCR_A 0x3d | DCR_B 0x5 | XRA_A 0xaf | ADC_L 0x8d | ADC_M 0x8e | XRA_B 0xa8 | XRA_C 0xa9 | ADC_H 0x8c | DCR_C 0xd | DCR_H 0x25 | DCR_L 0x2d | XRA_H 0xac | MOV_A,H 0x7c | ANI 0xe6 | XRA_M 0xae | XRA_L 0xad | ADC_A 0x8f | ADC_B 0x88 | ADC_C 0x89 | MOV_A,L 0x7d | MOV_A,M 0x7e | MOV_B,M 0x46 | NOP 0x0 | MOV_C,A 0x4f | MOV_C,B 0x48 | STA 0x32 | MOV_H,B 0x60 | IN 0xdb | 
[ --- test A --- ]
nop 0x0
xxx None
------------------------------
[ --- test B --- ] OP-CODES
instructions revers. (opcode/instr list:
NOP
--- example00_s80.asm ---
--------------------------------

; example00_s80 | first test - read parameters
; org 0x00 ; (default)
;
start:
                     ; INPUT:
    MVI_A 0b00000111 ; bin a = 7 (dec)  | 0x07 (hex) 
    MVI_B 0x08       ; hex b = 8
    MVI_C 9          ; dec c = 9
    NOP
    MOV_A,A          ; spec.subroutine --> reg.info ABC
    NOP
    ;
    HLT        ; halt (stop)
    MVI_A 0x03 ; a = 3 (will not be executed)
    NOP    
end.
;
;
; all lines ";" or COMM [PARAM] ; "note"
; numeric parameters: bin, hex, dec (ToDo macro variables $var)
; start: = label
; NOP    = No Operation
; HLT    = Halt | https://en.wikipedia.org/wiki/HLT_(x86_instruction)
; MVI_A / MVA A data | a = data
; DCR_A / DCR A (s80 / 8080) decrement | a = a - 1
;

--------------------------------
[ two pass - translator ]
[---1---] first pass:
- temp_variables {}

--------------------------------
[---2---] second pass:
0  pc: 0  instr: 0  pc+ 0  p1,p2  
---parts: ['MVI_A', '0b00000111']
1  pc: 2  instr: 0x3e  pc+ 2  p1,p2  
---parts: ['MVI_B', '0x08']
2  pc: 4  instr: 0x6  pc+ 2  p1,p2  
---parts: ['MVI_C', '9']
3  pc: 6  instr: 0xe  pc+ 2  p1,p2  
---parts: ['NOP']
4  pc: 7  instr: 0x0  pc+ 1  p1,p2  
---parts: ['MOV_A,A']
5  pc: 8  instr: 0x7f  pc+ 1  p1,p2  
---parts: ['NOP']
6  pc: 9  instr: 0x0  pc+ 1  p1,p2  
---parts: ['HLT']
7  pc: 10  instr: 0x76  pc+ 1  p1,p2  
---parts: ['MVI_A', '0x03']
8  pc: 12  instr: 0x3e  pc+ 2  p1,p2  
---parts: ['NOP']
9  pc: 13  instr: 0x0  pc+ 1  p1,p2  
10  pc: 13  instr: 0  pc+ 0  p1,p2  
- temp_labels: {'start:': 0}
- temp_prog. : [62, '0b00000111', 6, '0x08', 14, '9', 0, 127, 0, 118, 62, '0x03', 0]
[---3---] third pass:
- replaces labels with addr.
********************************
.:. function:  create_hex_program
--> duration (milis.) --> 0
------------------------------
- program_num [62, 7, 6, 8, 14, 9, 0, 127, 0, 118, 62, 3, 0]
------------------------------
len(instr_set): 13
==============================
0 {1} 3e   MVI_A 0x7
                      --->#1 |S0 Z0 C0| 00000111 | 7, 0x7 2 
2 {1} 06   MVI_B 0x8
                      --->#2 |S0 Z0 C0| 00000111 | 7, 0x7 4 
4 {1} 0e   MVI_C 0x9
                      --->#3 |S0 Z0 C0| 00000111 | 7, 0x7 6 
6 {0} 00   NOP
                      --->#4 |S0 Z0 C0| 00000111 | 7, 0x7 7 
7 {0} 7f   MOV_A,A
--> R  DEC BIN    HEX (B_C)
    A:  7 00000111 07
    B:  8 00001000 08  (2057)
    C:  9 00001001 09  [0]
                      --->#5 |S0 Z0 C0| 00000111 | 7, 0x7 8 
8 {0} 00   NOP
                      --->#6 |S0 Z0 C0| 00000111 | 7, 0x7 9 
9 {0} 76   HLT
                      --->#7 |S0 Z0 C0| 00000111 | 7, 0x7 9 
.:. function:  run_hex_code
--> duration (milis.) --> 734

------------------------------
mem_free: 128672
================================
[ system registers ]
a: 7 0x7 00000111
b: 8  | c: 9
h: 0  | l: 0
--------------------------------
|S|Z|0|C|0|P|1|C|
|0|0|0|0|0|0|1|0|
================================
"""