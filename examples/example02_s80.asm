; example02_s80 - test jumps
; org 0x00 ; (default)
;
start:
    MVI_A 0x07 ; note
    MOV_B,A
               ; b = 7
loop1:
    NOP
    DCR_A      ; decrement
    JNZ loop1  ; jump if not zero
    NOP
    MVI_A 0x01
    MVI_B 0x07
    ;
loop2:
    NOP ; 
    RLC
    DCR_B      ; decrement
    JNZ loop2  ; jump if not zero 
    NOP
    MVI_A 0x09 ; a = 9
;    
    NOP
end.
