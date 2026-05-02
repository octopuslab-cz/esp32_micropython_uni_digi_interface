; example06_s80.asm
; Copy 16 bytes from 0x0050 → 0x0030
; HL = source, DE = destination, C = counter

    JMP start

start:
    #DATA = "octopus test  "  ; → mem[0x0050..0x005F], 16 chars

    LXI_H 0x0050       ; HL = source address
    LXI_D 0x0030       ; DE = destination address
    MVI_C 0x10         ; C  = 16 (byte counter)

copy_loop:
    MOV_A,M            ; A = mem[HL]
    STAX_D             ; mem[DE] = A
    INX_H              ; HL++
    INX_D              ; DE++
    DCR_C              ; C--
    JNZ copy_loop      ; repeat while C != 0

    ; verify: read first copied byte back
    LXI_H 0x0030       ; HL = destination
    MOV_A,M            ; A = mem[0x0030]  should be 'o' = 0x6F
    MOV_A,A            ; [debug hook] print A/B/C
    HLT
 end.