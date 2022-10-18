; example_s80_inx pair B_C / H_L
start:
    MVI_A 6
    MOV_A,A
    CMA
    MOV_A,A
;
    MVI_A 6          ; init loop1
    MVI_C 253  ;
loop1:               ; increment
    INX_B            ; B_C + 1
    MOV_A,A          ; spec.subroutine --> reg.info ABC
    NOP              ; test correct overflow
    ;
    DCR_A      ; 
    JNZ loop1
    ;
    MVI_A 6          ; init loop2
    ;
loop2:               ; decrement
    DCX_B            ; B_C - 1
    MOV_A,A          ; spec.subroutine --> reg.info ABC
    NOP              ; test correct overflow
    DCR_A      ; 
    JNZ loop2
    
;    
;
end.
