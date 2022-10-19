; example_s80_vars: macro variables
;
$var1 = 123               ; note
$var2 = 0b10101010
$virtual_label = label2:  ; poznamka2
;
start:
    MVI_B var2
    MVI_A var1
    MOV_A,A
    CMA
    MOV_A,A
;
; 
virtual_label ; variable
;
end.
