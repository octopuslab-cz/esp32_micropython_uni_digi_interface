; example01_s80 - test correct JUMP
; org 0x00 ; (default)
;
start:
    MVI_A 0b00000111   ; a = 7 (dec)  | 0x07 (hex) 
    MVI_C 0b10101010   ; c = 170 (dec)| 0xAA (hex) 
    MOV_B,A    ; b <= ( a = 7 )
;              
loop1:
    NOP        ; test correct jump
    DCR_A      ; decrement
    JNZ loop1  ; jump if not zero   
loop2:
    MVI_A 0x09 ; a = 9 | 0x09 (hex)
    RLC  
    RLC
    RLC
    RRC
    RRC
    RRC
;    
    MVI_A 0xFF ; 255
    INR_A      ; 255+1 --> C = 1
    INR_A      ; 0+1   --> C = 0
    INR_A      ; 2
    INR_A      ; 3
    ADD_A 255  ; 3+255 = 257-256 = 2
    INR_A
    NOP
    
end.
