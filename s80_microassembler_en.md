# s80 Microassembler

> A simplified educational environment for experimenting with the principles of assembly language and microprocessor architecture. The project is part of the **octopusLAB** platform and runs on devices with **MicroPython** (ESP32 and compatible). It is not intended for production use — it is a tool for learning, testing, and demonstrating machine code.

---

## s80 Processor Architecture

The s80 virtual processor is inspired by the Intel 8080 architecture. It has 8-bit registers, a simple memory model, and flag bits.

### Registers

| Register | Description |
|----------|-------------|
| `A` | Accumulator — the main working register for arithmetic and logic |
| `B`, `C` | General-purpose registers, can be combined as the 16-bit pair B:C |
| `H`, `L` | Address registers — the H:L pair forms a 16-bit address (`H*256 + L`) |
| `E` | General-purpose register (also used by the `sleep` special subroutine) |
| `D` | General-purpose register (display) |

### Flag Bits

| Flag | Description |
|------|-------------|
| `Z` | Zero — set if the result is 0 |
| `C` | Carry — set if the result overflowed past 255 |
| `S` | Sign bit |
| `P` | Parity |

### Memory

Total memory is **300 bytes**:
- `0x00–0xFF` (0–255) — program memory (code)
- `0x100+` (256+) — data area (`#DATA` strings, RAM accessed via H:L)

---

## Source File Syntax

### Comments

Comments start with a semicolon `;`. Everything after `;` on a given line is ignored.

```asm
MVI_A 0x07  ; this is a comment
; the entire line is a comment
```

### Instructions and Parameters

Each instruction is on its own line in the format:

```
INSTRUCTION [PARAMETER]  ; optional comment
```

Parameters can be written in any numeric base:

| Format | Example | Description |
|--------|---------|-------------|
| Decimal | `42` | Standard integer |
| Hexadecimal | `0x1F` | `0x` prefix |
| Binary | `0b00001111` | `0b` prefix |

### Labels

Labels mark an address in the code. They are defined with a colon after the name and used as parameters for jump instructions:

```asm
loop1:
    NOP
    DCR_A
    JNZ loop1   ; jump back to loop1
```

A label name can be any identifier without spaces.

### Macro Variables

Variables are defined at the top of the file with a `$` prefix. They act as text substitutions (macros) before the code is processed:

```asm
$count = 10
$address = 0xFF

    MVI_A $count    ; will be substituted: MVI_A 10
```

### Data String (#DATA)

The `#DATA` directive stores an ASCII string in data memory starting at address `0x0100` (256):

```asm
#DATA = "octopus test"
```

The string is terminated with a `0` byte (null terminator). It is accessed via the H:L registers.

### End of Program

The line `end.` is a conventional marker for the end of the source file (it is not a required instruction — the assembler ignores it).

---

## Three Assembler Passes

Translation is performed in three passes inside the `parse_file()` function:

### Pass 1 — Variable Definitions

The assembler scans the source file looking for:
- Macro variables (`$var = value`) — stores them in a dictionary
- `#DATA = "..."` — stores the ASCII string into the processor's data memory

After the first pass, all occurrences of variable names in the code are replaced with their values (text substitution).

### Pass 2 — Label Collection (Relative Addressing)

The assembler re-scans the code (after variable substitution) and:
- Tracks the position (PC — Program Counter) of each instruction (instructions can be 1, 2, or 3 bytes)
- Stores each found label (`label:`) along with the current PC value in a dictionary
- Builds a temporary program representation — jump instructions still hold the label name as a string, not an address

### Pass 3 — Machine Code Finalisation (Absolute Addressing)

The assembler walks the temporary program representation and:
- Replaces label names with their actual absolute addresses
- Writes the resulting bytes into the processor memory (`uP.mem`)

The output is executable machine code ready to be run directly by the `Executor` class.

```
.asm file
    │
    ▼
[Pass 1] → $variable substitution, #DATA loading
    │
    ▼
[Pass 2] → label collection, relative PC, program assembly
    │
    ▼
[Pass 3] → absolute address resolution, write to uP.mem
    │
    ▼
Machine code → run_hex_code()
```

---

## Instruction Set

### Control Instructions

| Instruction | Bytes | Description |
|-------------|-------|-------------|
| `NOP` | 1 | No Operation |
| `HLT` | 1 | Halt the processor |

### Data Moves (Move / Load Immediate)

| Instruction | Bytes | Description |
|-------------|-------|-------------|
| `MVI_A n` | 2 | A = n |
| `MVI_B n` | 2 | B = n |
| `MVI_C n` | 2 | C = n |
| `MVI_H n` | 2 | H = n |
| `MVI_L n` | 2 | L = n |
| `MVI_M n` | 2 | Memory[H:L] = n |
| `MOV_B,A` | 1 | B ← A |
| `MOV_A,B` | 1 | A ← B |
| `MOV_C,A` | 1 | C ← A |
| `MOV_A,C` | 1 | A ← C |
| `MOV_A,M` | 1 | A ← Memory[H:L] |
| `MOV_M,A` | 1 | Memory[H:L] ← A |
| `MOV_M,B` | 1 | Memory[H:L] ← B |
| `MOV_M,C` | 1 | Memory[H:L] ← C |
| `LXI_B lb hb` | 3 | BC ← (hb:lb) load register pair |
| `LXI_H lb hb` | 3 | HL ← (hb:lb) load register pair |
| `LDA lb hb` | 3 | A ← Memory[hb*256+lb] |
| `STA lb hb` | 3 | Memory[hb*256+lb] ← A |

### Arithmetic

| Instruction | Bytes | Description |
|-------------|-------|-------------|
| `INR_A` | 1 | A = A + 1 |
| `INR_B` | 1 | B = B + 1 |
| `INR_C` | 1 | C = C + 1 |
| `INR_H` | 1 | H = H + 1 |
| `INR_L` | 1 | L = L + 1 |
| `DCR_A` | 1 | A = A - 1, sets Z |
| `DCR_B` | 1 | B = B - 1, sets Z |
| `DCR_C` | 1 | C = C - 1, sets Z |
| `DCR_H` | 1 | H = H - 1, sets Z |
| `DCR_L` | 1 | L = L - 1, sets Z |
| `INX_B` | 1 | BC = BC + 1 (16-bit) |
| `INX_H` | 1 | HL = HL + 1 (16-bit) |
| `DCX_B` | 1 | BC = BC - 1 (16-bit) |
| `DCX_H` | 1 | HL = HL - 1 (16-bit) |
| `ADD_A` | 1 | A = A + A |
| `ADD_B` | 1 | A = A + B |
| `ADD_C` | 1 | A = A + C |
| `ADD_H` | 1 | A = A + H |
| `ADD_L` | 1 | A = A + L |
| `ADI n` | 2 | A = A + n (immediate) |
| `ADD_A n` | 2 | A = A + n (alias) |
| `CPI n` | 2 | Compare A with n, sets C/Z |

### Logic and Rotation

| Instruction | Bytes | Description |
|-------------|-------|-------------|
| `CMA` | 1 | A = ~A (bitwise complement) |
| `ANI n` | 2 | A = A AND n |
| `ORI n` | 2 | A = A OR n |
| `XRI n` | 2 | A = A XOR n |
| `ANA_B` | 1 | A = A AND B |
| `ANA_C` | 1 | A = A AND C |
| `ORA_B` | 1 | A = A OR B |
| `ORA_C` | 1 | A = A OR C |
| `XRA_B` | 1 | A = A XOR B |
| `XRA_C` | 1 | A = A XOR C |
| `RLC` | 1 | Rotate A left (through carry) |
| `RRC` | 1 | Rotate A right (through carry) |

### Jumps and Subroutines

| Instruction | Bytes | Description |
|-------------|-------|-------------|
| `JMP label` | 3 | Unconditional jump |
| `JNZ label` | 3 | Jump if Z = 0 (Not Zero) |
| `JZ label` | 3 | Jump if Z = 1 (Zero) |
| `JNC label` | 3 | Jump if C = 0 (No Carry) |
| `JC label` | 3 | Jump if C = 1 (Carry) |
| `CALL label` | 3 | Subroutine call (saves return address) |
| `RET` | 1 | Return from subroutine |

> **Note:** The stack is simple in the current version (a single SP register). Nested `CALL` invocations are not supported.

### I/O Instructions

| Instruction | Bytes | Description |
|-------------|-------|-------------|
| `OUT port` | 2 | Output A to HW port (74LS374) |
| `IN port` | 2 | Input from HW port into A |

---

## Special Subroutines (HW Extensions)

Some `MOV r,r` instructions (where both operands are the same register) are redirected to hardware or diagnostic operations. These are called *special subroutines* — internally they are regular instructions, but their side effect is used for I/O:

| Instruction | Effect |
|-------------|--------|
| `MOV_A,A` | Print register state (A, B, C) to console |
| `MOV_B,B` | Print memory contents (hex dump) |
| `MOV_C,C` | Print current PC value |
| `MOV_E,E` | `sleep(1)` — wait 1 second (**slEEp**) |
| `MOV_H,H` | LED on (`led.value(1)`) — **H**igh |
| `MOV_L,L` | LED off (`led.value(0)`) — **L**ow |
| `MOV_D,D` | Display data on the 7-segment display |

These subroutines allow simple hardware experiments (LED blinking, delays) directly from assembler source code without writing separate driver routines.

---

## Example Programs

### Simple Counter with Conditional Jump

```asm
; example01 - countdown and jump
start:
    MVI_A 0b00000111   ; A = 7
    MVI_C 0b10101010   ; C = 0xAA
    MOV_B,A            ; B = A

loop1:
    NOP
    DCR_A              ; A = A - 1, sets Z
    JNZ loop1          ; jump to loop1 while A != 0

    HLT
end.
```

### Subroutine (CALL / RET)

```asm
; example03 - subroutine call
    JMP start

sub1:
    MVI_A 0xFF
    RET

start:
    NOP
    CALL sub1          ; call sub1, A = 0xFF
    MVI_A 0xFE
end.
```

### Memory Access via H:L

```asm
; write and read using the H:L address pair
    MVI_H 0x01         ; address: H=1
    MVI_L 0x03         ;          L=3 -> mem[0x103]
    MVI_A 0x42
    MOV_M,A            ; mem[0x103] = 0x42

    MOV_A,M            ; A = mem[0x103]
end.
```

### Data String

```asm
; example06 - reading text from memory
    #DATA = "octopus test"

start:
    MVI_H 0x01
    MVI_L 0x00
    MOV_A,M            ; A = 'o' (first character)
    INR_L
    MOV_A,M            ; A = 'c'
    NOP
end.
```

### HW LED Blinking

```asm
; example08 - LED blinking via special subroutines
    JMP start

blink:
    MOV_H,H   ; LED on
    MOV_E,E   ; sleep 1s
    MOV_L,L   ; LED off
    MOV_E,E   ; sleep 1s
    RET

start:
    MVI_A 0x03    ; number of blinks
loop1:
    CALL blink
    DCR_A
    JNZ loop1
    NOP
end.
```

---

## Usage in MicroPython

```python
from components.microprocessor.s80.core import Executor, parse_file, create_hex_program, run_hex_code

uP = Executor()                                    # create processor instance

program = parse_file(uP, "example01_s80.asm")     # translate (3 passes)
hex_program = create_hex_program(program)          # prepare hex representation

run_hex_code(uP, hex_program, run_delay_ms=10)    # run
```

Alternatively, the source code can be passed directly as a string (the `asm=` parameter):

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

## Limitations and Planned Development (ToDo)

- The stack is simple (a single SP) — nested `CALL` invocations are not safe
- The `#DATA` directive currently supports only one string per file
- The translator does not support multi-level macro expansion
- Planned: `#SUBPROC` for shared subroutines (ROM routines)
- Planned: extension of the address space beyond 255 bytes for larger programs

---

*s80 microassembler · octopusLAB · MicroPython · v2.1 · 2026*
