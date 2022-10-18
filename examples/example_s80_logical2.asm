; example_s80_logical2
;
;
start:
; 
    MVI_A 0b11010111
    MOV_A,A
    CMA              ; ---1--- complement / bit negation
    MOV_A,A          ; -> 0b00101000
;
;                    
    MVI_B 1          ; ---2--- test Register B - is zero?
    MVI_A 0
    ORA_B            ; B or 0 -> Z.bit 0
    MOV_A,A
;
    MVI_B 0
    MVI_A 0
    ORA_B            ; B or 0 -> Z.bit 1
    MOV_A,A
;
;                    ; ---3--- mask bit 
    MVI_C 0b00110011 
                     
    MVI_A 0b00000100                 
    ANA_C            ; C and MASK (00000100)
    MOV_A,A          ; 1 -> Z.bit
;
    MVI_A 0b00000010 
    ANA_C            ; C and MASK (00000010)
    MOV_A,A          ; 0 -> Z.bit
;
;
end.
