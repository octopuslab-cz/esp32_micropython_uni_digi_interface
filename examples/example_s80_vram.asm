; example_s80_vram - virtual RAM pair H_L
#DATA = "----- octopus"
;
;
start:
    LXI_B 0x03 0x02   ; 
    MOV_A,A
    ;
    ;
    MVI_L 0x1   ; L = 1
    MVI_H 0x1   ; H = 1
    MVI_A 49    ; "1" = 49 ASCII
    MOV_M,A     ; (HL)<-A
    ;
    MOV_B,B     ; spec.suroutine - print vm
    ;
    LXI_H 2 1   ; L=2 H=1 # H byte3 / L byte2 :: I L H
    MOV_A,A
    MVI_M 50    ; "2"
    INX_H       ; H_L + 1  
    MVI_M 51    ; "3"
    ;
    MOV_B,B     ; spec.suroutine - print vm
    ;
;
end.
