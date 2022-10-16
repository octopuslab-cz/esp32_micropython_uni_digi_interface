; example01 test
start:
    MVI_A 0x07 ; note
    MOV_B,A
               ; b = 7
loop1:
    NOP
    DCR_A      ; decrement
    JNZ loop1  ; jump if not zero   
loop2:
    NOP 
    MVI_A 0x09 ; a = 9
    RLC  
    RLC
    RLC
    RRC
    RRC
    RRC
;    
    NOP
end.

;['0x3e','0x07','0x47','0x0','0x3d','0xc2',0,'loop1','0x0','0x3e','0x09','0x7','0x7','0x7','0xf','0xf', '0xf', '0x0']
; program_num [62, 7, 71, 0, 61, 194, 0, 4, 0, 62, 9, 7, 7, 7, 15, 15, 15, 0]