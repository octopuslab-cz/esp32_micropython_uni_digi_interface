# table for instructions s80

"""
zero_param_instr    1  INSTR 
single_param_instr  2  INSTR PARAM1 2: not 1 and not 3
double_param_instr  3  INSTR PARAM1 PARAM2
"""

zero_param_instr = {
 'NOP','HLT','RIM','SIM',
 'XCHG','XTHL','SPHL','PCHL',
 'RET','RC','RNC','RZ','RNZ','RP','RM',
 'RPE','RPO','RLC','RRC','RAL','RAR',
 'CMA','STC','CMC','DAA','EI','DI',
 'MOV_B,A','MOV_C,A','MOV_L,A','MOV_H,A','MOV_M,A',
 'MOV_A,B','MOV_C,B','MOV_L,B','MOV_H,B','MOV_M,B',
 'MOV_A,C','MOV_B,C','MOV_L,C','MOV_H,C','MOV_M,C','MOV_A,M',
 'MOV_A,A','MOV_B,B','MOV_C,C','MOV_D,D','MOV_E,E','MOV_L,L','MOV_H,H',
 'INR_A','INR_B','INR_C','INR_L','INR_H','INX_B','INX_H'
 'DCR_A','DCR_B','DCR_C','DCR_L','DCR_H','DCX_B','DCX_H',
 'ADC_A','ADC_B','ADC_C','ADC_H','ADC_L','ADC_M',
 'SUB_A','SUB_B','SUB_C','SUB_H','SUB_L','SUB_M',
 'SBB_A','SBB_B','SBB_C','SBB_H','SBB_L','SBB_M',
 'ANA_A','ANA_B','ANA_C','ANA_H','ANA_L','ANA_M',
 'XRA_A','XRA_B','XRA_C','XRA_H','XRA_L','XRA_M',
 'ORA_A','ORA_B','ORA_C','ORA_H','ORA_L','ORA_M', 
}

# 'ADD_A','ADD_B','ADD_C','ADD_H','ADD_L','ADD_M',


# instr: "address"
double_param_instr = {
 'STA','LDA','SHLD','LHLD','LXI_B','LXI_H',
 'JMP','JC','JNC','JZ','JNZ','JP','JM','JPE','JPO',
 'CALL','CC','CNC','CZ','CNZ','CP','CM','CPE','CPO'
}


def get_instr_param(instr):
    # if (instr not in double_param_instr) and (instr not in zero_param_instr): add_pc = 2
    add_pc = 2
    if instr in zero_param_instr: add_pc = 1
    if instr in double_param_instr: add_pc = 3
    return add_pc
