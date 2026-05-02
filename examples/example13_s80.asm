; example13_s80.asm
; Nested CALL demo â€” 3 levels deep
; Function: multiply B * C  â†’ result in A, stored to RAM[0x0103]
;
; call stack at deepest point:
;
;   main --CALL--–ş multiply          stack: [ retâ†’HLT        ]
;                    â””-CALL--–ş add_step    stack: [ retâ†’HLT, retâ†’DCR_C   ]
;                                â””-CALL--–ş save_result
;                                           stack: [ retâ†’HLT, retâ†’DCR_C, retâ†’RET ]
;
; registers:
;   B = multiplicand  (fixed value, not modified)
;   C = loop counter  (counts down from multiplier to 0)
;   A = running total (accumulates B each iteration)
;   H,L = pointer to result in RAM (set inside save_result)

    JMP start

;----------------------------------------------------
; LEVEL 3 â€” save running total to RAM[0x0103]
;           stack depth here: 3
save_result:
    MVI_H 0x01
    MVI_L 0x03
    MOV_M,A         ; mem[0x0103] = A  (intermediate result)
    RET

;-----------------------------------------------------
; LEVEL 2 â€” add B to running total, then save
;           stack depth here: 2
add_step:
    ADD_B           ; A = A + B
    CALL save_result
    RET

;-----------------------------------------------------
; LEVEL 1 â€” loop C times, accumulate B into A
;           stack depth here: 1
multiply:
    MVI_A 0x00      ; running total = 0
mul_loop:
    CALL add_step   ; A += B  (and save snapshot to RAM)
    DCR_C           ; loop counter--
    JNZ mul_loop    ; repeat until C == 0
    RET

;-----------------------------------------------------
start:
    MVI_B 0x03      ; multiplicand  =  3
    MVI_C 0x04      ; multiplier    =  4
    CALL multiply   ; result: A = 3 * 4 = 12 = 0x0C
    MOV_B,A         ; copy result to B (for display)
    MOV_A,A         ; [s80 debug hook] print A / B / C + LED
    HLT
