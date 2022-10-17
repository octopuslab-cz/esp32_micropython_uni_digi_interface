; example08 spec subroutine HW
    JMP start
;--------
blink:
;--------
    MOV_A,A   ; print acc
    MOV_H,H   ; led H
    MOV_E,E   ; sleep
    MOV_L,L   ; led L
    MOV_E,E   ; sleep
    RET
;============================
start:
    MVI_A 0x07 ; a = 7
    NOP 
loop1:
    CALL blink
    DCR_A      ; decrement a-1
    JNZ loop1  ; jump if not zero
    ;
    NOP        ; finish  
end.