;example00_s80 - all lines ";" or COMM [PARAM] ; note
; org 0x00 ; (default)
;
start:
    MVI_A 0x07 ; a = 7
    DCR_A      ; a = a - 1
    DCR_A      ; a = a - 1 --> 5 
    NOP
    NOP
end.
;