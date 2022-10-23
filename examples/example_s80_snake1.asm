; example_s80_snake1
; display TM1638 + RGB 8 x WS
;
MVI_A 0b10101010 ; intro:
MOV_A,A          ; show acc -> 10101010
MOV_E,E          ; sleep 1 sec.
CMA              ; complement / bit negation
MOV_A,A          ; show acc  -> 01010101
MOV_E,E          ; sleep
MOV_L,L          ; LED LOW / clear
;
    JMP start
;
display:         ; HW subroutines
    MOV_A,A      ; display pc and acc.
    MOV_E,E      ; sleep 1 sec.
    RET
;
start:
    MVI_A 0b00000001
loop:
    CALL display
    RLC          ; rotate left
    JNC loop     ; skip if carry
;
;
end.
