# s80 Mikroassembler

> Zjednodušené výukové prostředí pro experimentování s principy assembleru a architektury mikroprocesorů. Projekt je součástí platformy **octopusLAB** a běží na zařízeních s **MicroPythonem** (ESP32 a kompatibilní). Není určen pro produkční nasazení — jde o nástroj pro výuku, testování a demonstraci strojového kódu.

---

## Architektura procesoru s80

Virtuální procesor s80 byl inspirován architekturou Intel 8080. Má 8bitové registry, jednoduchou paměť a příznakové bity.

### Registry

| Registr | Popis |
|---------|-------|
| `A` | Akumulátor – hlavní pracovní registr pro aritmetiku a logiku |
| `B`, `C` | Obecné registry, lze kombinovat jako 16bitový pár B:C |
| `H`, `L` | Adresní registry – pár H:L tvoří 16bitovou adresu (`H*256 + L`) |
| `E` | Obecný registr (také speciální subroutina `sleep`) |
| `D` | Obecný registr (display) |

### Příznakové bity (Flags)

| Příznak | Popis |
|---------|-------|
| `Z` | Zero – nastaven, pokud je výsledek 0 |
| `C` | Carry – nastaven, pokud výsledek přetekl přes 255 |
| `S` | Sign – znaménkový bit |
| `P` | Parity |

### Paměť

Paměť má celkem **300 bytů**:
- `0x00–0xFF` (0–255) — programová paměť (kód)
- `0x100+` (256+) — datová oblast (`#DATA` řetězce, RAM přes H:L)

---

## Syntaxe zdrojového souboru

### Komentáře

Komentáře začínají středníkem `;`. Vše za `;` na daném řádku je ignorováno.

```asm
MVI_A 0x07  ; toto je komentář
; celý řádek je komentář
```

### Instrukce a parametry

Každá instrukce je na samostatném řádku ve formátu:

```
INSTRUKCE [PARAMETR]  ; volitelný komentář
```

Parametry mohou být v libovolné číselné soustavě:

| Formát | Příklad | Popis |
|--------|---------|-------|
| Desítkový | `42` | Standartní celé číslo |
| Hexadecimální | `0x1F` | Prefix `0x` |
| Binární | `0b00001111` | Prefix `0b` |

### Návěští (Labels)

Návěští označují adresu v kódu. Definují se dvojtečkou za názvem, používají se jako parametr skokových instrukcí:

```asm
loop1:
    NOP
    DCR_A
    JNZ loop1   ; skočí zpět na loop1
```

Název návěští může být libovolný identifikátor bez mezer.

### Makro proměnné

Proměnné se definují na začátku souboru prefixem `$`. Slouží jako textová substituce (makro) před zpracováním kódu:

```asm
$pocet = 10
$adresa = 0xFF

    MVI_A $pocet    ; bude nahrazeno: MVI_A 10
```

### Datový řetězec (#DATA)

Direktiva `#DATA` uloží ASCII řetězec do datové paměti od adresy `0x0100` (256):

```asm
#DATA = "octopus test"
```

Řetězec je zakončen bajtem `0` (null terminator). Přistupuje se k němu přes registry H:L.

### Konec programu

Řádek `end.` je konvenční označení konce zdrojového souboru (není povinnou instrukcí, assembler jej ignoruje).

---

## Tři průchody assembleru

Překlad probíhá ve třech průchodech funkce `parse_file()`:

### Průchod 1 — Definice proměnných

Assembler prochází zdrojový soubor a hledá:
- Makro proměnné (`$var = hodnota`) — ukládá je do slovníku
- `#DATA = "..."` — ukládá ASCII řetězec do datové paměti procesoru

Po prvním průchodu jsou všechny výskyty názvů proměnných v kódu nahrazeny jejich hodnotami (textová substituce).

### Průchod 2 — Sběr návěští (relativní adresování)

Assembler znovu prochází kód (po substituci proměnných) a:
- Počítá pozici (PC — Program Counter) každé instrukce (instrukce mohou mít 1, 2 nebo 3 bajty)
- Ukládá každé nalezené návěští (`label:`) spolu s aktuální hodnotou PC do slovníku
- Sestavuje dočasnou reprezentaci programu — skokové instrukce zatím obsahují název návěští jako řetězec, ne adresu

### Průchod 3 — Finalizace strojového kódu (absolutní adresování)

Assembler prochází sestavenou reprezentaci programu a:
- Nahrazuje jména návěští jejich skutečnými absolutními adresami
- Zapisuje výsledné bajty do paměti procesoru (`uP.mem`)

Výsledkem je spustitelný strojový kód připravený k přímému vykonání třídou `Executor`.

```
.asm soubor
    │
    ▼
[Průchod 1] → substituce $proměnných, načtení #DATA
    │
    ▼
[Průchod 2] → sběr návěští, relativní PC, sestavení programu
    │
    ▼
[Průchod 3] → dosazení absolutních adres, zápis do uP.mem
    │
    ▼
Strojový kód → run_hex_code()
```

---

## Instrukční sada

### Řídící instrukce

| Instrukce | Bajty | Popis |
|-----------|-------|-------|
| `NOP` | 1 | Žádná operace (No Operation) |
| `HLT` | 1 | Zastavení procesoru |

### Přesuny dat (Move / Load Immediate)

| Instrukce | Bajty | Popis |
|-----------|-------|-------|
| `MVI_A n` | 2 | A = n |
| `MVI_B n` | 2 | B = n |
| `MVI_C n` | 2 | C = n |
| `MVI_H n` | 2 | H = n |
| `MVI_L n` | 2 | L = n |
| `MVI_M n` | 2 | Paměť[H:L] = n |
| `MOV_B,A` | 1 | B ← A |
| `MOV_A,B` | 1 | A ← B |
| `MOV_C,A` | 1 | C ← A |
| `MOV_A,C` | 1 | A ← C |
| `MOV_A,M` | 1 | A ← Paměť[H:L] |
| `MOV_M,A` | 1 | Paměť[H:L] ← A |
| `MOV_M,B` | 1 | Paměť[H:L] ← B |
| `MOV_M,C` | 1 | Paměť[H:L] ← C |
| `LXI_B lb hb` | 3 | BC ← (hb:lb) načtení páru |
| `LXI_H lb hb` | 3 | HL ← (hb:lb) načtení páru |
| `LDA lb hb` | 3 | A ← Paměť[hb*256+lb] |
| `STA lb hb` | 3 | Paměť[hb*256+lb] ← A |

### Aritmetika

| Instrukce | Bajty | Popis |
|-----------|-------|-------|
| `INR_A` | 1 | A = A + 1 |
| `INR_B` | 1 | B = B + 1 |
| `INR_C` | 1 | C = C + 1 |
| `INR_H` | 1 | H = H + 1 |
| `INR_L` | 1 | L = L + 1 |
| `DCR_A` | 1 | A = A - 1, nastaví Z |
| `DCR_B` | 1 | B = B - 1, nastaví Z |
| `DCR_C` | 1 | C = C - 1, nastaví Z |
| `DCR_H` | 1 | H = H - 1, nastaví Z |
| `DCR_L` | 1 | L = L - 1, nastaví Z |
| `INX_B` | 1 | BC = BC + 1 (16bit) |
| `INX_H` | 1 | HL = HL + 1 (16bit) |
| `DCX_B` | 1 | BC = BC - 1 (16bit) |
| `DCX_H` | 1 | HL = HL - 1 (16bit) |
| `ADD_A` | 1 | A = A + A |
| `ADD_B` | 1 | A = A + B |
| `ADD_C` | 1 | A = A + C |
| `ADD_H` | 1 | A = A + H |
| `ADD_L` | 1 | A = A + L |
| `ADI n` | 2 | A = A + n (immediate) |
| `ADD_A n` | 2 | A = A + n (alias) |
| `CPI n` | 2 | Porovnání A s n, nastaví C/Z |

### Logika a rotace

| Instrukce | Bajty | Popis |
|-----------|-------|-------|
| `CMA` | 1 | A = ~A (bitový komplement) |
| `ANI n` | 2 | A = A AND n |
| `ORI n` | 2 | A = A OR n |
| `XRI n` | 2 | A = A XOR n |
| `ANA_B` | 1 | A = A AND B |
| `ANA_C` | 1 | A = A AND C |
| `ORA_B` | 1 | A = A OR B |
| `ORA_C` | 1 | A = A OR C |
| `XRA_B` | 1 | A = A XOR B |
| `XRA_C` | 1 | A = A XOR C |
| `RLC` | 1 | Rotace A vlevo (přes carry) |
| `RRC` | 1 | Rotace A vpravo (přes carry) |

### Skoky a podprogramy

| Instrukce | Bajty | Popis |
|-----------|-------|-------|
| `JMP label` | 3 | Nepodmíněný skok |
| `JNZ label` | 3 | Skok pokud Z = 0 (Not Zero) |
| `JZ label` | 3 | Skok pokud Z = 1 (Zero) |
| `JNC label` | 3 | Skok pokud C = 0 (No Carry) |
| `JC label` | 3 | Skok pokud C = 1 (Carry) |
| `CALL label` | 3 | Volání podprogramu (uloží návratovou adresu) |
| `RET` | 1 | Návrat z podprogramu |

> **Poznámka:** Zásobník je v aktuální verzi jednoduchý (jednobytový SP). Vnořená volání `CALL` nejsou podporována.

### I/O instrukce

| Instrukce | Bajty | Popis |
|-----------|-------|-------|
| `OUT port` | 2 | Výstup A na HW port (74LS374) |
| `IN port` | 2 | Vstup z HW portu do A |

---

## Speciální subroutiny (HW rozšíření)

Některé instrukce `MOV r,r` (kde jsou oba operandy stejné) jsou přesměrovány na hardwarové nebo diagnostické operace. Jde o tzv. *spec. subroutiny* — interně jsou to regulérní instrukce, ale jejich vedlejší efekt je využit pro I/O:

| Instrukce | Efekt |
|-----------|-------|
| `MOV_A,A` | Výpis stavu registrů A, B, C do konzole |
| `MOV_B,B` | Výpis obsahu paměti (hex dump) |
| `MOV_C,C` | Výpis hodnoty PC |
| `MOV_E,E` | `sleep(1)` — čekání 1 sekundu (**slEEp**) |
| `MOV_H,H` | LED zapnout (`led.value(1)`) — **H**igh |
| `MOV_L,L` | LED vypnout (`led.value(0)`) — **L**ow |
| `MOV_D,D` | Zobrazení dat na 7segmentovém displeji |

Tyto subroutiny umožňují jednoduché HW experimenty (blikání LED, čekání) přímo ze zdrojového kódu assembleru bez nutnosti psát obslužné rutiny.

---

## Ukázky programů

### Jednoduchý čítač s podmíněným skokem

```asm
; example01 - odpočet a skok
start:
    MVI_A 0b00000111   ; A = 7
    MVI_C 0b10101010   ; C = 0xAA
    MOV_B,A            ; B = A

loop1:
    NOP
    DCR_A              ; A = A - 1, nastaví Z
    JNZ loop1          ; skočí na loop1, dokud A != 0

    HLT
end.
```

### Podprogram (CALL / RET)

```asm
; example03 - volání podprogramu
    JMP start

sub1:
    MVI_A 0xFF
    RET

start:
    NOP
    CALL sub1          ; zavolá sub1, A = 0xFF
    MVI_A 0xFE
end.
```

### Práce s pamětí přes H:L

```asm
; zápis a čtení přes adresní pár H:L
    MVI_H 0x01         ; adresa: H=1
    MVI_L 0x03         ;         L=3 -> mem[0x103]
    MVI_A 0x42
    MOV_M,A            ; mem[0x103] = 0x42

    MOV_A,M            ; A = mem[0x103]
end.
```

### Datový řetězec

```asm
; example06 - načtení textu z paměti
    #DATA = "octopus test"

start:
    MVI_H 0x01
    MVI_L 0x00
    MOV_A,M            ; A = 'o' (první znak)
    INR_L
    MOV_A,M            ; A = 'c'
    NOP
end.
```

### HW blikání LED

```asm
; example08 - blikání LED přes spec. subroutiny
    JMP start

blink:
    MOV_H,H   ; LED zapnout
    MOV_E,E   ; sleep 1s
    MOV_L,L   ; LED vypnout
    MOV_E,E   ; sleep 1s
    RET

start:
    MVI_A 0x03    ; počet bliknutí
loop1:
    CALL blink
    DCR_A
    JNZ loop1
    NOP
end.
```

---

## Použití v MicroPythonu

```python
from components.microprocessor.s80.core import Executor, parse_file, create_hex_program, run_hex_code

uP = Executor()                              # vytvoření instance procesoru

program = parse_file(uP, "example01_s80.asm")  # překlad (3 průchody)
hex_program = create_hex_program(program)       # příprava hex reprezentace

run_hex_code(uP, hex_program, run_delay_ms=10)  # spuštění
```

Alternativně lze předat kód jako řetězec přímo (parametr `asm=`):

```python
src = """
    MVI_A 0x05
loop:
    DCR_A
    JNZ loop
    HLT
end.
"""
program = parse_file(uP, asm=src)
```

---

## Limity a plánovaný rozvoj (ToDo)

- Zásobník je jednoduchý (jeden SP) — vnořená volání `CALL` nejsou bezpečná
- `#DATA` direktiva zatím podporuje pouze jeden řetězec na soubor
- Překlad nepodporuje víceúrovňové makro expanze
- Plánováno: `#SUBPROC` pro sdílené podprogramy (ROM rutiny)
- Plánováno: rozšíření adresového prostoru nad 255 bajtů pro větší programy

---

*s80 mikroassembler · octopusLAB · MicroPython · v2.1 · 2026*
