; example00_s80 - all lines ";" or COMM [PARAM] ; note
; org 0x00 ; (default)
;
start:
    MVI_A 0x07 ; a = 7
    DCR_A      ; a = a - 1
    DCR_A      ; a = a - 1 --> 5 
    NOP
    NOP
    ;
    HLT        ; halt (stop)
    MVI_A 0x07 ; a = 3 (will not be executed)
    NOP    
end.
;
;
; start: = label
; NOP    = No Operation
; HLT    = Halt | https://en.wikipedia.org/wiki/HLT_(x86_instruction)
; MVI_A / MVA A data | a = data
; DCR_A / DCR A (s80 / 8080) decrement | a = a - 1
;