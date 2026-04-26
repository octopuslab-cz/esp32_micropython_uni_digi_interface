; example12_s80 - doubles in memory
; 1,2,4,8,...,128 smyčkou, 256 a 512 ručně
; big-endian 16-bit, data od adresy 0x100
;
start:
    MVI_H 0x1    ; HL = 0x100 (oblast dat)
    MVI_L 0x0
    MVI_B 0x0    ; B = high byte = 0
    MVI_A 0x1    ; A = low byte = 1
    MVI_C 0x8    ; C = počítadlo = 8
loop:
    MOV_M,B      ; [HL]   = high byte (B)
    INX_H        ; HL++
    MOV_M,A      ; [HL]   = low byte (A)
    INX_H        ; HL++
    ADD_A        ; A = A * 2
    DCR_C        ; C--
    JNZ loop     ; pokud C != 0, opakuj
    ; --- 256 = 0x01 0x00 ---
    MVI_A 0x1
    MOV_M,A
    INX_H
    MVI_A 0x0
    MOV_M,A
    INX_H
    ; --- 512 = 0x02 0x00 ---
    MVI_A 0x2
    MOV_M,A
    INX_H
    MVI_A 0x0
    MOV_M,A
    MOV_B,B      ; výpis paměti
    HLT
end.