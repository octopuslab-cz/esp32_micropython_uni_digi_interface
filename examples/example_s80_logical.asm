; example_s80_logical
;
start:
    MVI_A 0b01010101 ;
    ANI   0b00001111 ; and
    MOV_C,A     
    MVI_A 0b01010101 ;
    MVI_B 0b00001111 ; 
    MOV_A,A          ; spec.subroutine --> reg.info ABC
;
    MVI_A 0b01010101 ;
    MVI_B 0b00001111 ;
    ;ORI   0b00001111; or
    ORA_B            ; a = a or b
    MOV_C,A          ; c = a    
    MVI_A 0b01010101 ;     
    MOV_A,A          ; spec.subroutine --> reg.info ABC
;    
    MVI_A 0b01010101 ;
    XRI   0b00001111 ; xor
    MOV_C,A     
    MVI_A 0b01010101 ;
    MVI_B 0b00001111 ; 
    MOV_A,A          ; spec.subroutine --> reg.info ABC
; 
;
end.
