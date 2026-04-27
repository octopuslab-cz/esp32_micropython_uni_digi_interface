; ╔══════════════════════════════════════════════════════════╗
; ║  ESS251 – inv_mod rutina pro s80 microassembler          ║
; ║  Algoritmus: trial multiplication                        ║
; ║  Hledáme k∈[1..250] splňující (x·k) mod 251 == 1        ║
; ║                                                          ║
; ║  MAPA PAMĚTI (data area 0x01xx):                         ║
; ║   0x100 P1X  0x101 P1Y  0x102 P2X  0x103 P2Y            ║
; ║   0x104 inv_vstup       0x105 inv_vysledek               ║
; ║   0x106 pocitadlo (kopie k pro vnitřní smyčku)           ║
; ║   0x107 soucet   (akumulátor součinu mod p)              ║
; ╚══════════════════════════════════════════════════════════╝

$PM = 251   ; modulus
$REDUCE = 5     ; 256 - 251 = 5  (trik redukce)

start:

; ── MAIN ─────────────────────────────────────────────────────

    MVI_H 0x01          ; H = 0x01 (high byte datové oblasti)
    MVI_L 0x00

    MVI_A 10            ; P1X = 10   → G_x
    MOV_M,A
    INR_L
    MVI_A 76            ; P1Y = 76   → G_y
    MOV_M,A
    INR_L
    MVI_A 201           ; P2X = 201  → 2G_x  (spočítáme později)
    MOV_M,A
    INR_L
    MVI_A 16            ; P2Y = 16   → 2G_y
    MOV_M,A

; ── TEST 1: inv_mod(2) → očekáváme 126  (2 × 126 = 252 ≡ 1) ─

    MVI_L 0x04
    MVI_A 2
    MOV_M,A             ; mem[0x104] = 2
    CALL inv_mod
    MVI_L 0x05
    MOV_M,A             ; mem[0x105] = výsledek
    MOV_A,A             ; DEBUG: tiskne A (= 126), B (= 2), C (= 126)

; ── TEST 2: inv_mod(3) → očekáváme 84   (3 × 84  = 252 ≡ 1) ─

    MVI_L 0x04
    MVI_A 3
    MOV_M,A
    CALL inv_mod
    MVI_L 0x05
    MOV_M,A
    MOV_A,A             ; DEBUG: tiskne A (= 84), B (= 3), C (= 84)

    HLT

; ═══════════════════════════════════════════════════════════
;  SUBROUTINE: inv_mod
;  Vstup:  mem[0x104] = x  (1..250)
;  Výstup: A = x⁻¹ mod 251,  nebo 0 pokud inverz neexistuje
;  Ničí:   A, B (= x), C (= k), H (= 0x01), L
;
;  Přiřazení registrů:
;    B  = x  (konstantní, proto máme ADD_B)
;    C  = k  (vnější čítač, 1..250, MOV_A,C + INR_C)
;    A  = scratch (mezisoučet, porovnání)
;    H:L = adresování paměti (H=0x01 pevné po inicializaci)
;
;  Klíčový trik — redukce mod 251 bez instrukce SUB:
;    256 − 251 = 5,  tedy  a − 251 ≡ a + 5  (mod 256)
;    • carry z ADD_B → A_reálné = A + 256 → výsledek = A + 5
;    • bez carry, A ≥ 251           → výsledek = A + 5
;    • bez carry, A < 251           → beze změny
;
;  Složitost: O(p²) iterací, max ~31 500 kroků pro p=251
; ═══════════════════════════════════════════════════════════

inv_mod:
    MVI_H 0x01
    MVI_L 0x04
    MOV_A,M             ; A = x
    MOV_B,A             ; B = x  (konstantní po celou dobu)
    MVI_C 1             ; C = k = 1

inv_outer:
    ; ulož k jako počítadlo vnitřní smyčky
    MOV_A,C
    MVI_L 0x06
    MOV_M,A             ; mem[0x106] = k

    ; vynuluj akumulátor součinu
    MVI_L 0x07
    MVI_M 0             ; mem[0x107] = 0

inv_inner:
    MVI_L 0x07
    MOV_A,M             ; A = aktuální součet
    ADD_B               ; A = součet + x   (carry možný)

    ; ── redukce mod 251 ──────────────────────────────
    JC inv_carry        ; přeteklo → A_reálné = A + 256
    CPI $PM             ; bez carry: A < 251 ?
    JC inv_ok           ; ano → hotovo
    ADI $REDUCE         ; A ≥ 251 → A = A − 251 = A + 5 (mod 256)
    JMP inv_ok
inv_carry:
    ADI $REDUCE         ; A_reálné − 251 = A + 256 − 251 = A + 5
inv_ok:
    ; ─────────────────────────────────────────────────
    MVI_L 0x07
    MOV_M,A             ; mem[0x107] = nový součet

    MVI_L 0x06
    MOV_A,M
    DCR_A               ; counter--  (nastaví Z pokud = 0)
    MOV_M,A             ; mem[0x106] = counter  (MOV neruší Z)
    JNZ inv_inner       ; pokračuj dokud counter != 0

    ; ── konec vnitřní smyčky: A = (x · k) mod 251 ───
    MVI_L 0x07
    MOV_A,M             ; načti výsledný součin
    CPI 1
    JZ inv_found        ; součin == 1 → k je inverz!

    INR_C               ; k++
    MOV_A,C
    CPI $PM             ; k == 251? (pro p prvočíslo nenastane pro x ≠ 0)
    JZ inv_none
    JMP inv_outer

inv_found:
    MOV_A,C             ; A = k  (hledaný inverz)
    RET

inv_none:
    MVI_A 0             ; A = 0  (inverz neexistuje)
    RET

end.