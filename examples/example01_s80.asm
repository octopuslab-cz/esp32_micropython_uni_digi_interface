; example01_s80 - test correct JUMP
; org 0x00 ; (default)
;
start:
    MVI_A 0x07 ; note
    MOV_B,A
               ; b = 7
loop1:
    NOP        ; test correct jump
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
