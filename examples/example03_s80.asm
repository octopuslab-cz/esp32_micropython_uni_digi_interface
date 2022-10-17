; example03 - test CALL sub1 (subroutine)
; org 0x00 ; (default)
;
    JMP start
    NOP
sub1:
    NOP ; 1x nop = ok
    MVI_A 0xFF
    RET
    ;
start:
    NOP ; 2 x NOP = ok 
    NOP
    MVI_L 0x3 ; note RAM7
    MVI_H 0x1
    MVI_A 0x9
    MOV_M,A
    ;
    MVI_L 0x2 ; note RAM7
    ;MVI_H 0x1
    MVI_A 0x7
    MOV_M,A
    ;
    MVI_L 0x3 ; note RAM7
    ;MVI_H 0x1
    MOV_A,M
               ; b = 7
    CALL sub1
    ; 
    MVI_A 0xFE ; 36
end.
