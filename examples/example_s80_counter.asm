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

display:
    MOV_A,A
    RET

start:
    MVI_A 0
loop:
    CALL display  ; zobraz (0..255)
    ADI 1         ; A = A + 1  (sets Z=1 při přetečení 255→0)
    JZ finish     ; přeteklo → hotovo
    JMP loop

finish:
    HLT

end.