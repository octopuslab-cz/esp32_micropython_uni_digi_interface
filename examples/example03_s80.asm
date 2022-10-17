; example03 - test CALL sub1 (subroutine)
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
