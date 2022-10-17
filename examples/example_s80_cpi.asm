; example_tempor.ary
#DATA = "--- octopus"
;
start:
    MVI_L 0x01 ; init LH
    MVI_H 0x01
    MVI_A 88 ; "X"
    MOV_M,A
;   e=69 g=71 s=83 x=88
    MVI_A 0x07 ; note
    CPI 0x07 
    NOP
; |S|Z|0|C|0|P|1|C|
; |0|1|0|0|0|0|1|0| cp = a (z)
;
    CPI 0x08 
    NOP
; |S|Z|0|C|0|P|1|C|
; |0|0|0|0|0|0|1|1| cp > a (c)
;
   JC is_greater 
   JZ is_equal
   JMP end
;
is_greater:
    MVI_A 71 ; "G"
    MOV_M,A
    JMP end
;
is_equal:
    MVI_A 69 ; "E"
    MOV_M,A
    JMP end
;
smaller:
;
end:
;