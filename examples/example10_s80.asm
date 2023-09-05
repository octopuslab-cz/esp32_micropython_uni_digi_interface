; example09 spec subroutine HW
    JMP start
;--------
show:
;--------
    OUT 0xF8  ;
    MOV_E,E   ; sleep
    RET
;============================
start:
    MVI_A 0xFF ; a = FFh
    NOP 
loop1:
    CALL show
    MOV_B,A
    IN 0xF9
    CALL show
    MOV_A,B
    
    DCR_A      ; decrement a-1
    JNZ loop1  ; jump if not zero
    ;-----------------------
    
    MVI_A 0x55
    MVI_B 0x05
    

end.