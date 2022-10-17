# table for instructions s80

"""
zero_param_instr    1  INSTR 
single_param_instr  2  INSTR PARAM1
double_param_instr  3  INSTR PARAM1 PARAM2

"""

zero_param_instr = {
 'XCHG','XTHL','SPHL','PCHL',
 'RET','RC','RNC','RZ','RNZ','RP','RM',
 'RPE','RPO','RLC','RRC','RAL','RAR',
 'CMA','STC','CMC','DAA','EI','DI',
 'NOP','HLT','RIM','SIM',
 'INR_A', 'INR_B', 'INR_C', 'INR_L','INR_H','DCR_A', 'DCR_B', 'DCR_C','DCR_L','DCR_H',
 'MOV_B,A','MOV_C,A','MOV_L,A','MOV_H,A','MOV_M,A',
 'MOV_A,B','MOV_C,B','MOV_L,B','MOV_H,B','MOV_M,B',
 'MOV_A,C','MOV_B,C','MOV_L,C','MOV_H,C','MOV_M,C',
 'MOV_A,A','MOV_B,B','MOV_C,C','MOV_D,D','MOV_E,E','MOV_L,L','MOV_H,H','MOV_A,M',
}


# instr: "address"
double_param_instr = {
 'STA','LDA','SHLD','LHLD',
 'JMP','JC','JNC','JZ','JNZ','JP','JM','JPE','JPO',
 'CALL','CC','CNC','CZ','CNZ','CP','CM','CPE','CPO',
}


def get_instr_param(instr):
    # if (instr not in double_param_instr) and (instr not in zero_param_instr): add_pc = 2
    add_pc = 2
    if instr in zero_param_instr: add_pc = 1
    if instr in double_param_instr: add_pc = 3
    return add_pc
