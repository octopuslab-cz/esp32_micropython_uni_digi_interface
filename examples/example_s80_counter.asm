; example_s80_counter
; display TM1638 + RGB 8 x WS
; set: run_delay_ms=0
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
; ------------------------------------
display:         ; HW subroutines
    MOV_A,A      ; display pc and acc.
    RET
; ====================================
start:
    MVI_A 0
loop:
    INR_A        ; increment a = a + 1
    CALL display
    CPI 0xFF     ; compare
    JNC finish   ; is_greater 
    JMP loop
;
finish:
;
end.