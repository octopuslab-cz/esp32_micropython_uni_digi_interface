# s80: simple80 for microprocessor emulator (8080/85)
# --- OctopusLAB 2015-23
# only the most important commands

instructions = {
 'NOP':     0x00,
 'HLT':     0x76,
 'LDA':     0x3A,
 'STA':     0x32,
 'RLC':     0x07,
 'RRC':     0x0F,
 'LXI_B':   0x01,
 'OUT':     0xD3,
 'IN':      0xDB,
 'LXI_H':   0x21,
 'ADD_A':   0x87,
 'ADD_B':   0x80,
 'ADD_C':   0x81,
 'ADD_H':   0x84,
 'ADD_L':   0x85,
 'ADD_M':   0x86,
 'ADC_B':   0x88,
 'ADC_C':   0x89,
 'ADC_H':   0x8C,
 'ADC_L':   0x8D,
 'ADC_M':   0x8E,
 'ADC_A':   0x8F,
 'SUB_B':   0x90,
 'SUB_C':   0x91,
 'SUB_H':   0x94,
 'SUB_L':   0x95,
 'SUB_M':   0x96,
 'SUB_A':   0x97,
 'SBB_B':   0x98,
 'SBB_C':   0x99,
 'SBB_H':   0x9C,
 'SBB_L':   0x9D,
 'SBB_M':   0x9E,
 'SBB_A':   0x9F,
 'CMA':     0x2F,
 'ANI':     0xE6,
 'ANA_B':   0xA0,
 'ANA_C':   0xA1,
 'ANA_D':   0xA2,
 'ANA_E':   0xA3,
 'ANA_H':   0xA4,
 'ANA_L':   0xA5,
 'ANA_M':   0xA6,
 'ANA_A':   0xA7,
 'XRI':     0xEE,
 'XRA_B':   0xA8,
 'XRA_C':   0xA9,
 'XRA_H':   0xAC,
 'XRA_L':   0xAD,
 'XRA_M':   0xAE,
 'XRA_A':   0xAF,
 'ORI':     0xF6,
 'ORA_A':   0xB7,
 'ORA_B':   0xB0,
 'ORA_C':   0xB1,
 'ORA_H':   0xB4,
 'ORA_L':   0xB5,
 'ORA_M':   0xB6,
 'MVI_A':   0x3E,
 'MVI_B':   0x06,
 'MVI_C':   0x0E,
 'MVI_L':   0x2E,
 'MVI_H':   0x26,
 'MVI_M':   0x36,
 'DCR_A':   0x3D,
 'DCR_B':   0x05,
 'DCR_C':   0x0D,
 'DCR_H':   0x25,
 'DCR_L':   0x2D,
 'DCX_B':   0x0B,
 'DCX_H':   0x2B,
 'INR_A':   0x3C,
 'INR_B':   0x04,
 'INR_C':   0x0C,
 'INR_H':   0x24,
 'INR_L':   0x2C,
 'INX_B':   0x03,
 'INX_H':   0x23,
 'MOV_A,B': 0x78,
 'MOV_A,C': 0x79,
 'MOV_A,H': 0x7C,
 'MOV_A,L': 0x7D,
 'MOV_A,M': 0x7E,
 'MOV_B,A': 0x47,
 'MOV_B,C': 0x41,
 'MOV_B,H': 0x44,
 'MOV_B,L': 0x45,
 'MOV_B,M': 0x46,
 'MOV_C,A': 0x4F,
 'MOV_C,B': 0x48,
 'MOV_C,H': 0x4C,
 'MOV_C,L': 0x4D,
 'MOV_C,M': 0x4E,
 'MOV_H,B': 0x60,
 'MOV_H,C': 0x61,
 'MOV_H,H': 0x64,
 'MOV_H,L': 0x65,
 'MOV_H,M': 0x66,
 'MOV_H,A': 0x67,
 'MOV_L,A': 0x6F,
 'MOV_L,B': 0x68,
 'MOV_L,C': 0x69,
 'MOV_L,H': 0x6C,
 'MOV_L,M': 0x6E,
 'MOV_M,A': 0x77,
 'MOV_M,B': 0x70,
 'MOV_M,C': 0x71,
 'MOV_M,H': 0x74,
 'MOV_M,L': 0x75,
 'JMP':     0xC3,
 'JZ':      0xCA,
 'JNZ':     0xC2,
 'JC':      0xDA,
 'JNC':     0xD2,
 'CALL':    0xCD,
 'RET':     0xC9,
 'MOV_A,A': 0x7F,
 'MOV_B,B': 0x40,
 'MOV_C,C': 0x49,
 'MOV_D,D': 0x52,
 'MOV_E,E': 0x5B,
 'MOV_L,L': 0x6D,
 'MOV_H,H': 0x64,
 'CMP_A':   0xBF,
 'CMP_B':   0xB8,
 'CMP_C':   0xB9,
 'CMP_H':   0xBC,
 'CMP_L':   0xBD,
 'CMP_M':   0xBE,
 'CPI':     0xFE,    
 }
