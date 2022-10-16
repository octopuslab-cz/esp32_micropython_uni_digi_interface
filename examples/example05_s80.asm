; example05 spec operation / 2x call
    JMP start
    NOP
sub1:
    NOP; ???
    MOV_A,A ; print acc
    RET
    ;
sub2:
    NOP; ???
    MOV_E,E ; print vm
    RET
    ;
start:
    NOP; ??? pc +/- 1
    NOP
    MVI_L 0x1 ; note RAM9
    MVI_H 0x1
    MVI_A 0x9
    MOV_M,A
    ;
    MVI_L 0x2 ; note RAM7
    MVI_H 0x1
    MVI_A 0x7
    MOV_M,A
    ;
    MVI_L 0x1 ; note RAM9
    MVI_H 0x1
    MOV_A,M
               ; b = 7
    CALL sub1
    MVI_A 0xFE ; 36
    CALL sub2
    NOP
end.
