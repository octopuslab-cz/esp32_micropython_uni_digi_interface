; ╔══════════════════════════════════════════════════════════════╗
; ║  F17 ECC Point Addition  —  s80 microassembler              ║
; ║  G(15,13) + 2G(2,10) = 3G(8,3)   over GF(17), a=0          ║
; ║                                                             ║
; ║  MAPA PAMĚTI (0x01xx):                                      ║
; ║   0x100 P1X=15   0x101 P1Y=13                               ║
; ║   0x102 P2X=2    0x103 P2Y=10                               ║
; ║   0x104 num      0x105 den                                  ║
; ║   0x106 counter  0x107 mul_sum   (scratch subroutin)        ║
; ║   0x108 slope    0x109 x3                                   ║
; ║   0x10A y3                                                  ║
; ║                                                             ║
; ║  REGISTRY:                                                  ║
; ║   B = minuend / multiplicand (pevný v subroutině)           ║
; ║   C = subtrahend / multiplier / trial k                     ║
; ║   A = výsledek / scratch                                    ║
; ║   H = 0x01  (nastaveno jednou v start, nemění se)           ║
; ║   L = offset do datové oblasti                              ║
; ╚══════════════════════════════════════════════════════════════╝

$PMOD  = 17        ; modulus
$REDUCE = 239       ; 256 − 17 = 239  (trik: a−17 ≡ a+239 mod 256)

    JMP start    ; přeskočíme subroutiny

; ════════════════════════════════════════════════════════════════
;  sub_mod  —  A = (B − C) mod 17
;  Strategie: A = PM + B, pak dekrementujeme A celkem C-krát
;  Rozsahy:  B ∈ [0..16], C ∈ [0..16] → PM+B ∈ [17..33]
;            po odečtení C: [1..33], redukce na [0..16]
;  Ničí: A, L, mem[0x106], mem[0x107]
; ════════════════════════════════════════════════════════════════
sub_mod:
    MVI_L 0x07
    MVI_A PMOD
    ADD_B                   ; A = 17 + B  (carry nemůže nastat: max 33)
    MOV_M,A                 ; mem[0x107] = 17 + B
    MOV_A,A                 ; RGB

    MVI_L 0x06
    MOV_A,C
    MOV_M,A                 ; mem[0x106] = C  (počítadlo)
    CPI 0
    JZ sub_done             ; C=0 → výsledek je rovnou B

sub_loop:
    MVI_L 0x07
    MOV_A,M
    DCR_A
    MOV_M,A                 ; mem[0x107]--
    MVI_L 0x06
    MOV_A,M
    DCR_A
    MOV_A,A                 ; RGB 
    MOV_M,A                 ; counter--
    JNZ sub_loop

sub_done:
    MVI_L 0x07
    MOV_A,M                 ; A = 17 + B − C  ∈ [1..33]
    CPI PMOD
    JC sub_ret              ; A < 17 → hotovo
    ADI REDUCE                ; A − 17 = A + 239 mod 256
sub_ret:
    RET

; ════════════════════════════════════════════════════════════════
;  mul_mod  —  A = (B × C) mod 17
;  Opakované sčítání: sum=0, přičítáme B celkem C-krát
;  Max iterací: 16. Průběžná redukce: součet nikdy > 32
;  Ničí: A, L, mem[0x106], mem[0x107]
; ════════════════════════════════════════════════════════════════
mul_mod:
    MVI_L 0x07
    MVI_M 0                 ; sum = 0

    MVI_L 0x06
    MOV_A,C
    MOV_M,A                 ; counter = C
    CPI 0
    JZ mul_done             ; C=0 → výsledek 0

mul_loop:
    MVI_L 0x07
    MOV_A,M
    MOV_A,A                 ; RGB
    ADD_B                   ; A = sum + B  (max 16+16=32, no carry)
    CPI PMOD
    JC mul_no_red
    ADI REDUCE                ; A − 17
mul_no_red:
    MOV_M,A                 ; uložíme nový součet

    MVI_L 0x06
    MOV_A,M
    DCR_A
    MOV_M,A                 ; counter--
    JNZ mul_loop

mul_done:
    MVI_L 0x07
    MOV_A,M                 ; A = výsledek
    RET

; ════════════════════════════════════════════════════════════════
;  inv_mod  —  A = inv(A) mod 17
;  Trial: hledáme k∈[1..16] takové, že (A×k) mod 17 = 1
;  Násobení je inlinované (žádný CALL uvnitř CALL)
;  Max: 16 vnějších × 16 vnitřních = 256 kroků → velmi rychlé
;  Ničí: A, B (=x), C (=k), L, mem[0x106], mem[0x107]
; ════════════════════════════════════════════════════════════════
inv_mod:
    MOV_B,A                 ; B = x  (konstantní)
    MVI_C 1                 ; k = 1

inv_outer:
    MVI_L 0x07
    MVI_M 0                 ; sum = 0

    MVI_L 0x06
    MOV_A,C
    MOV_M,A                 ; counter = k  (kopie pro vnitřní smyčku)

inv_inner:
    MVI_L 0x07
    MOV_A,M
    ADD_B                   ; sum += x
    CPI PMOD
    JC inv_no_red
    ADI REDUCE
inv_no_red:
    MOV_M,A                 ; uložíme součet

    MVI_L 0x06
    MOV_A,M
    DCR_A
    MOV_M,A                 ; counter--
    JNZ inv_inner

    ; součin = (x × k) mod 17
    MVI_L 0x07
    MOV_A,M
    CPI 1
    JZ inv_found            ; součin = 1 → k je inverz!

    INR_C                   ; zkus další k
    JMP inv_outer           ; (pro prvočíselné p vždy najdeme)

inv_found:
    MOV_A,C                 ; A = k  (hledaný inverz)
    RET

; ════════════════════════════════════════════════════════════════
;  MAIN  —  G(15,13) + 2G(2,10)  // 5G = (6,6)
; ════════════════════════════════════════════════════════════════
start:
    MVI_H 0x01              ; H=1 zůstane navždy, L budeme měnit

    ; — uložení vstupních bodů —
    MVI_L 0x00
    MVI_A 15
    MOV_M,A                 ; mem[0x100] = P1X = 15
    INR_L
    MVI_A 13
    MOV_M,A                 ; mem[0x101] = P1Y = 13
    INR_L
    MVI_A 6
    MOV_M,A                 ; mem[0x102] = P2X = 2 / 6
    INR_L
    MVI_A 6
    MOV_M,A                 ; mem[0x103] = P2Y = 10 6

    ; ── [1] num = (P2Y − P1Y) mod 17  →  (10−13)=14 ─────────
    MVI_L 0x03
    MOV_A,M                 ; A = P2Y = 10
    MOV_B,A                 ; B = 10
    MVI_L 0x01
    MOV_A,M                 ; A = P1Y = 13
    MOV_C,A                 ; C = 13
    CALL sub_mod            ; A = (10−13) mod 17 = 14
    MVI_L 0x04
    MOV_M,A                 ; mem[0x104] = num = 14

    ; ── [2] den = (P2X − P1X) mod 17  →  (2−15)=4 ───────────
    MVI_L 0x02
    MOV_A,M                 ; A = P2X = 2
    MOV_B,A                 ; B = 2
    MVI_L 0x00
    MOV_A,M                 ; A = P1X = 15
    MOV_C,A                 ; C = 15
    CALL sub_mod            ; A = (2−15) mod 17 = 4
    MVI_L 0x05
    MOV_M,A                 ; mem[0x105] = den = 4

    ; ── [3] inv_den = inv(4) mod 17  →  13 ───────────────────
    MVI_L 0x05
    MOV_A,M                 ; A = 4  (reload L! sub_mod mění L)
    CALL inv_mod            ; A = 13
    MOV_B,A                 ; B = inv_den = 13 (pro mul)

    ; ── [4] slope = num × inv_den mod 17  →  14×13=12 ────────
    MVI_L 0x04
    MOV_A,M                 ; A = num = 14
    MOV_C,A                 ; C = 14
    ; B = 13 (z kroku 3)
    CALL mul_mod            ; A = 14×13 mod 17 = 12
    MVI_L 0x08
    MOV_M,A                 ; mem[0x108] = slope = 12

    ; ── [5a] slope² mod 17  →  12×12=8 ───────────────────────
    MOV_B,A                 ; B = 12
    MOV_C,A                 ; C = 12
    CALL mul_mod            ; A = 12×12 mod 17 = 8

    ; ── [5b] tmp = slope² − P1X  →  8−15=10 (mod 17) ─────────
    MOV_B,A                 ; B = 8
    MVI_L 0x00
    MOV_A,M                 ; A = P1X = 15
    MOV_C,A                 ; C = 15
    CALL sub_mod            ; A = (8−15) mod 17 = 10

    ; ── [5c] x3 = tmp − P2X  →  10−2=8 (mod 17) ─────────────
    MOV_B,A                 ; B = 10
    MVI_L 0x02
    MOV_A,M                 ; A = P2X = 2
    MOV_C,A                 ; C = 2
    CALL sub_mod            ; A = (10−2) mod 17 = 8
    MVI_L 0x09
    MOV_M,A                 ; mem[0x109] = x3 = 8

    ; ── [6a] diff = P1X − x3  →  15−8=7 ──────────────────────
    MVI_L 0x00
    MOV_A,M                 ; A = P1X = 15
    MOV_B,A                 ; B = 15
    MVI_L 0x09
    MOV_A,M                 ; A = x3 = 8
    MOV_C,A                 ; C = 8
    CALL sub_mod            ; A = (15−8) mod 17 = 7

    ; ── [6b] slope × diff  →  12×7=16 (mod 17) ───────────────
    MOV_C,A                 ; C = diff = 7
    MVI_L 0x08
    MOV_A,M                 ; A = slope = 12
    MOV_B,A                 ; B = 12
    CALL mul_mod            ; A = 12×7 mod 17 = 16

    ; ── [6c] y3 = mul_result − P1Y  →  16−13=3 ───────────────
    MOV_B,A                 ; B = 16
    MVI_L 0x01
    MOV_A,M                 ; A = P1Y = 13
    MOV_C,A                 ; C = 13
    CALL sub_mod            ; A = (16−13) mod 17 = 3
    MVI_L 0x0A
    MOV_M,A                 ; mem[0x10A] = y3 = 3

    ; ── VÝSLEDEK: 3G = (x3, y3) = (8, 3) ─────────────────────
    MVI_L 0x09
    MOV_A,M                 ; A = x3 = 8
    MOV_B,A                 ; B = 8
    MVI_L 0x0A
    MOV_A,M                 ; A = y3 = 3
    MOV_C,A                 ; C = 3
    MOV_A,A     ; DEBUG → tiskne: A=3  B=8  C=3
                ;                  y3     x3

    HLT
end.