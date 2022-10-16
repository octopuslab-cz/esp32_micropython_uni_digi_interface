; example00 simple test - note: fill all lines
start:
    MVI_A 0x07 ; note
    DCR_A 
    DCR_A 
    NOP
    INR_A
    INR_A
    INR_A
    MOV_B,A
; 
    MVI_A 0x09
    RLC
    RLC
    RLC
;
    MVI_A 0x0F
    RRC
    RRC
    RRC
    MOV_C,A
;
    NOP
end.
;
;temp_prog. : ['0x3e', '0x07', '0x3d', '0x3d', '0x0', '0x3c', '0x3c', '0x3c', '0x47', '0x3e', '0x09', '0x7', '0x7', '0x7', '0x3e', '0x0F', '0xf', '0xf', '0xf', '0x4f', '0x0']
;program_num [62, 7, 61, 61, 0, 60, 60, 60, 71, 62, 9, 7, 7, 7, 62, 15, 15, 15, 15, 79, 0]