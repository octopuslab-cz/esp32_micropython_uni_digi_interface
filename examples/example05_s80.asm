; example05 spec subroutines / 2x call
; org 0x00
;
    JMP start
    NOP
sub1:
    MOV_A,A ; print acc
    RET
    ;
sub2:
    MOV_E,E ; print vm
    RET
    ;
sub3:
    MOV_B,B ; 
    RET
    ;
start:
    NOP
    MVI_L 0x1 ; note RAM9
    MVI_H 0x1
    MVI_A 0x9
    MOV_M,A
    CALL sub1
    ;
    MVI_L 0x2 ; note RAM7
    MVI_H 0x1
    MVI_A 0x7
    MOV_M,A
    CALL sub1
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
