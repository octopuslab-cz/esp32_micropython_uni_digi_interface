; example03 test
    JMP start
    NOP
sub1:
    NOP; ???
    NOP
    MVI_A 0xFF
    RET
    NOP
    ;
start:
    NOP; ??? pc +/- 1
    NOP
    NOP
    MVI_L 0x1 ; note RAM7
    MVI_H 0x3
    MVI_A 0x9
    MOV_M,A
    ;
    MVI_L 0x2 ; note RAM7
    MVI_H 0x3
    MVI_A 0x7
    MOV_M,A
    ;
    MVI_L 0x1 ; note RAM7
    MVI_H 0x3
    MOV_A,M
               ; b = 7
    NOP
    CALL sub1
    ; 
    MVI_A 0xFE ; 36
    NOP
end.

;['0x3e','0x07','0x47','0x0','0x3d','0xc2',0,'loop1','0x0','0x3e','0x09','0x7','0x7','0x7','0xf','0xf', '0xf', '0x0']
; program_num [62, 7, 71, 0, 61, 194, 0, 4, 0, 62, 9, 7, 7, 7, 15, 15, 15, 0]