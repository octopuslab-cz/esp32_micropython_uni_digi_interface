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
    MVI_A 0x0a ; a = Ah
    NOP 
loop1:
    CALL show
    DCR_A      ; decrement a-1
    JNZ loop1  ; jump if not zero
    ;-----------------------
    
    MVI_A 0x55
    MVI_B 0x05
    
loop2:    
    CALL show
    CMA        ; RAR/RAL/RRC...
    DCR_B      ; decrement b-1
    JNZ loop2  ; jump if not zero
    ;-----------------------
    
    MVI_A 255
    MVI_B 0x09
    
loop3:    
    CALL show
    RRC        ; RAR/RAL/RRC...
    DCR_B      ; decrement b-1
    JNZ loop3  ; jump if not zero

end.