; example06 - simple data_string
     #DATA = "octopus test"
; fix virtual RAM addr: 256+ (0x01,0x00+)
;------------------------
start:
    MVI_L 0x00 ; 
    MVI_H 0x01
    MOV_A,M
    INR_L
    MOV_A,M
    INR_L
    MOV_A,M
;
    LDA 0x01 0x00 ; note
    LDA 0x01 0x01
    LDA 0x01 0x02
    NOP
    MVI_A 45 ; ord("-")=45
    STA 0x01 0x0C
; 
    NOP
end.
;