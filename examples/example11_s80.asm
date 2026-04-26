; example11_s80 - multiplication B * C
; result: A = B * C = 9 * 7 = 63 = 0x3F
; method: repeated addition  A += B  (C times)
;
start:
    MVI_B 0x9  ; B = 9  (multiplicand)
    MVI_C 0x7  ; C = 7  (counter / multiplier)
    MVI_A 0x0  ; A = 0  (accumulator)
;
loop:
    ADD_B      ; A = A + B
    DCR_C      ; C--
    JNZ loop   ; if C != 0 --> repeat
;
; A = 63 = 0x3F = 0b00111111
    NOP
end.


# 