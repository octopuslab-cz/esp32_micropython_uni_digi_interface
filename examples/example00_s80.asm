; example00_s80 | first test - read parameters
; org 0x00 ; (default)
;
start:
                     ; INPUT:
    MVI_A 0b00000111 ; bin a = 7 (dec)  | 0x07 (hex) 
    MVI_B 0x08       ; hex b = 8
    MVI_C 9          ; dec c = 9
    NOP
    MOV_A,A          ; spec.subroutine --> reg.info ABC
    NOP
    ;
    HLT        ; halt (stop)
    MVI_A 0x03 ; a = 3 (will not be executed)
    NOP    
end.
;
;
; all lines ";" or COMM [PARAM] ; "note"
; numeric parameters: bin, hex, dec (ToDo macro variables $var)
; start: = label
; NOP    = No Operation
; HLT    = Halt | https://en.wikipedia.org/wiki/HLT_(x86_instruction)
; MVI_A / MVA A data | a = data
; DCR_A / DCR A (s80 / 8080) decrement | a = a - 1
;