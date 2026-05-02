# Instruction Set Comparison: Intel 8080 / Intel 8085 / s80

> **s80** = simplified emulator subset (OctopusLAB 2015–26, MicroPython/ESP32)  
> ✅ = fully implemented &nbsp; 🔶 = partial (in `instructions.py` / `table.py` but missing from `execute()`) &nbsp; ❌ = not implemented &nbsp; 🔁 = repurposed as s80 debug hook  
> ➕ = instruction added in 8085 only

*Last updated: 2026 — verified against `core.py`, `instructions.py`, `table.py`*

---

## Data Transfer

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `MOV A, B/C` | ✅ | ✅ | ✅ | `0x78` `0x79` | |
| `MOV A, H/L` | ✅ | ✅ | 🔶 | `0x7C` `0x7D` | In `instructions.py`; missing from `execute()` |
| `MOV A, M` | ✅ | ✅ | ✅ | `0x7E` | Load A from (HL) |
| `MOV B/C, A` | ✅ | ✅ | ✅ | `0x47` `0x4F` | |
| `MOV B, C/H/L/M` | ✅ | ✅ | 🔶 | `0x41`–`0x46` | In `instructions.py`; missing from `execute()` |
| `MOV C, B/H/L/M` | ✅ | ✅ | 🔶 | `0x48`–`0x4E` | In `instructions.py`; missing from `execute()` |
| `MOV H, A/B/C/L/M` | ✅ | ✅ | 🔶 | `0x60`–`0x67` | In `instructions.py`; missing from `execute()` |
| `MOV L, A/B/C/H/M` | ✅ | ✅ | 🔶 | `0x68`–`0x6F` | In `instructions.py`; missing from `execute()` |
| `MOV M, A/B/C` | ✅ | ✅ | ✅ | `0x77` `0x70` `0x71` | Write A/B/C to (HL) |
| `MOV M, H/L` | ✅ | ✅ | 🔶 | `0x74` `0x75` | In `instructions.py`; missing from `execute()` |
| `MVI r, d8` | ✅ | ✅ | ✅ | `0x06`–`0x3E` | A B C H L M all supported |
| `LXI B, d16` | ✅ | ✅ | ✅ | `0x01` | Load BC pair immediate |
| `LXI H, d16` | ✅ | ✅ | ✅ | `0x21` | Load HL pair immediate |
| `LDA addr` | ✅ | ✅ | ✅ | `0x3A` | Load A from memory address |
| `STA addr` | ✅ | ✅ | ✅ | `0x32` | Store A to memory address |
| `LHLD addr` | ✅ | ✅ | ❌ | `0x2A` | Load HL from direct address |
| `SHLD addr` | ✅ | ✅ | ❌ | `0x22` | Store HL to direct address |
| `LDAX B/D` | ✅ | ✅ | ❌ | `0x0A` `0x1A` | Load A indirect via BC or DE |
| `STAX B/D` | ✅ | ✅ | ❌ | `0x02` `0x12` | Store A indirect via BC or DE |
| `XCHG` | ✅ | ✅ | ❌ | `0xEB` | Exchange DE ↔ HL |
| `RIM` | ❌ | ➕ | ❌ | `0x20` | Read Interrupt Mask |
| `SIM` | ❌ | ➕ | ❌ | `0x30` | Set Interrupt Mask |

---

## Arithmetic

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `ADD A` | ✅ | ✅ | ✅ | `0x87` | A = A + A |
| `ADD B/C/H/L` | ✅ | ✅ | ✅ | `0x80`–`0x85` | |
| `ADD M` | ✅ | ✅ | 🔶 | `0x86` | In `instructions.py`; missing from `execute()` |
| `ADI d8` | ✅ | ✅ | ✅ | `0xC6` | Add immediate to A |
| `ADC r/M` | ✅ | ✅ | 🔶 | `0x88`–`0x8F` | In `instructions.py`; missing from `execute()` |
| `ACI d8` | ✅ | ✅ | ❌ | `0xCE` | Add immediate with carry |
| `SUB r/M` | ✅ | ✅ | 🔶 | `0x90`–`0x97` | In `instructions.py`; missing from `execute()` |
| `SUI d8` | ✅ | ✅ | ❌ | `0xD6` | Subtract immediate |
| `SBB r/M` | ✅ | ✅ | 🔶 | `0x98`–`0x9F` | In `instructions.py`; missing from `execute()` |
| `SBI d8` | ✅ | ✅ | ❌ | `0xDE` | Subtract immediate with borrow |
| `INR A/B/C/H/L` | ✅ | ✅ | ✅ | varies | All five registers |
| `INR M` | ✅ | ✅ | ❌ | `0x34` | Increment memory at (HL) |
| `DCR A/B/C/H/L` | ✅ | ✅ | ✅ | varies | All five registers |
| `DCR M` | ✅ | ✅ | ❌ | `0x35` | Decrement memory at (HL) |
| `INX B` | ✅ | ✅ | ✅ | `0x03` | Increment BC pair |
| `INX H` | ✅ | ✅ | ✅ | `0x23` | Increment HL pair |
| `DCX B` | ✅ | ✅ | ✅ | `0x0B` | Decrement BC pair |
| `DCX H` | ✅ | ✅ | ✅ | `0x2B` | Decrement HL pair |
| `DAD rp` | ✅ | ✅ | ❌ | `0x09`–`0x39` | Add register pair to HL |
| `DAA` | ✅ | ✅ | ❌ | `0x27` | Decimal adjust accumulator |

---

## Logical

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `ANA A` | ✅ | ✅ | ✅ | `0xA7` | A & A — sets flags only |
| `ANA B/C/H/L/M` | ✅ | ✅ | ✅ | `0xA0`–`0xA6` | AND register/memory with A |
| `ANA D/E` | ✅ | ✅ | 🔶 | `0xA2` `0xA3` | In `instructions.py`; missing from `execute()` |
| `ANI d8` | ✅ | ✅ | ✅ | `0xE6` | AND immediate with A |
| `ORA B/C` | ✅ | ✅ | ✅ | `0xB0` `0xB1` | OR register with A |
| `ORA A/H/L/M` | ✅ | ✅ | 🔶 | `0xB7` `0xB4`–`0xB6` | In `instructions.py`; missing from `execute()` |
| `ORI d8` | ✅ | ✅ | ✅ | `0xF6` | OR immediate with A |
| `XRA A` | ✅ | ✅ | ✅ | `0xAF` | A = 0 — classic zero idiom |
| `XRA B/C/H/L/M` | ✅ | ✅ | ✅ | `0xA8`–`0xAE` | XOR register/memory with A |
| `XRI d8` | ✅ | ✅ | ✅ | `0xEE` | XOR immediate with A |
| `CMP B/C/H/L` | ✅ | ✅ | ✅ | `0xB8`–`0xBD` | Compare register with A; sets Z and C |
| `CMP A/M` | ✅ | ✅ | 🔶 | `0xBF` `0xBE` | In `instructions.py`; missing from `execute()` |
| `CPI d8` | ✅ | ✅ | ✅ | `0xFE` | Compare immediate with A |
| `CMA` | ✅ | ✅ | ✅ | `0x2F` | Complement A (bitwise NOT) |
| `STC` | ✅ | ✅ | ❌ | `0x37` | Set carry flag |
| `CMC` | ✅ | ✅ | ❌ | `0x3F` | Complement carry flag |

---

## Rotate / Shift

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `RLC` | ✅ | ✅ | 🔶 | `0x07` | Shifts left but does not wrap bit 7 → bit 0 |
| `RRC` | ✅ | ✅ | ✅ | `0x0F` | Rotate right; bit 0 wraps to bit 7 |
| `RAL` | ✅ | ✅ | ❌ | `0x17` | Rotate left through carry |
| `RAR` | ✅ | ✅ | ❌ | `0x1F` | Rotate right through carry |

---

## Branch

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `JMP addr` | ✅ | ✅ | ✅ | `0xC3` | Unconditional jump |
| `JZ addr` | ✅ | ✅ | ✅ | `0xCA` | Jump if zero (Z=1) |
| `JNZ addr` | ✅ | ✅ | ✅ | `0xC2` | Jump if not zero (Z=0) |
| `JC addr` | ✅ | ✅ | ✅ | `0xDA` | Jump if carry (C=1) |
| `JNC addr` | ✅ | ✅ | ✅ | `0xD2` | Jump if no carry (C=0) |
| `JP addr` | ✅ | ✅ | ❌ | `0xF2` | Jump if positive (S=0) |
| `JM addr` | ✅ | ✅ | ❌ | `0xFA` | Jump if minus (S=1) |
| `JPE addr` | ✅ | ✅ | ❌ | `0xEA` | Jump if parity even |
| `JPO addr` | ✅ | ✅ | ❌ | `0xE2` | Jump if parity odd |
| `PCHL` | ✅ | ✅ | ❌ | `0xE9` | Jump to address in HL |
| `CALL addr` | ✅ | ✅ | ✅ | `0xCD` | Call; list-based stack, up to 16 levels deep |
| `RET` | ✅ | ✅ | ✅ | `0xC9` | Return; pops return address from stack list |
| `CZ / CNZ` | ✅ | ✅ | ❌ | `0xCC` `0xC4` | Conditional call |
| `CC / CNC` | ✅ | ✅ | ❌ | `0xDC` `0xD4` | Conditional call |
| `RZ / RNZ` | ✅ | ✅ | ❌ | `0xC8` `0xC0` | Conditional return |
| `RC / RNC` | ✅ | ✅ | ❌ | `0xD8` `0xD0` | Conditional return |

---

## Stack & Machine Control

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `PUSH B` | ✅ | ✅ | ✅ | `0xC5` | Push BC pair as tuple onto stack list |
| `PUSH D` | ✅ | ✅ | ✅ | `0xD5` | Push DE pair as tuple onto stack list |
| `PUSH H` | ✅ | ✅ | ✅ | `0xE5` | Push HL pair as tuple onto stack list |
| `PUSH PSW` | ✅ | ✅ | ✅ | `0xF5` | Push A + packed flags onto stack list |
| `POP B` | ✅ | ✅ | ✅ | `0xC1` | Pop tuple → restore BC |
| `POP D` | ✅ | ✅ | ✅ | `0xD1` | Pop tuple → restore DE |
| `POP H` | ✅ | ✅ | ✅ | `0xE1` | Pop tuple → restore HL |
| `POP PSW` | ✅ | ✅ | ✅ | `0xF1` | Pop tuple → restore A and flags |
| `XTHL` | ✅ | ✅ | ✅ | `0xE3` | Exchange HL with top of stack (tuple or int) |
| `SPHL` | ✅ | ✅ | ✅ | `0xF9` | s80: truncate stack to depth L (H ignored) |
| `NOP` | ✅ | ✅ | ✅ | `0x00` | No operation |
| `HLT` | ✅ | ✅ | ✅ | `0x76` | Halt execution |
| `EI` | ✅ | ✅ | ❌ | `0xFB` | Enable interrupts |
| `DI` | ✅ | ✅ | ❌ | `0xF3` | Disable interrupts |
| `RST n` | ✅ | ✅ | ❌ | varies | Restart / software interrupt |

---

## I/O

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `IN port` | ✅ | ✅ | ✅ | `0xDB` | Read port → A; GPIO / 74LS374 expander hook |
| `OUT port` | ✅ | ✅ | ✅ | `0xD3` | Write A → port; GPIO / 74LS374 expander hook |

---

## s80 Special Subroutines (non-standard)

Unused `MOV r,r` no-ops repurposed as debug and hardware hooks.  
Not present in 8080 / 8085.

| Mnemonic | Opcode | Function |
|----------|:------:|----------|
| `MOV A,A` | `0x7F` | Print registers A / B / C in dec, hex, bin; show A on RGB LED |
| `MOV B,B` | `0x40` | Dump virtual memory (hex dump) |
| `MOV C,C` | `0x49` | Print current program counter (PC) |
| `MOV D,D` | `0x52` | Show value at (HL) on 7-segment display |
| `MOV E,E` | `0x5B` | Sleep 1 second |
| `MOV H,H` | `0x64` | LED ON |
| `MOV L,L` | `0x6D` | LED OFF |

---

## s80 Stack Model

Unlike the hardware 8080/8085 (which uses a RAM-backed SP register), s80 uses a
Python list as a mixed-type stack — supporting up to `STACK_SIZE = 16` entries.

| Item type | Pushed by | Popped by | Content |
|-----------|-----------|-----------|---------|
| `int` | `CALL` | `RET` | Return address (PC + 3) |
| `tuple (hi, lo)` | `PUSH_B/D/H` | `POP_B/D/H` | Register pair |
| `tuple (A, flags)` | `PUSH_PSW` | `POP_PSW` | Accumulator + packed flags |

`SPHL` truncates the stack list to depth `L` (H ignored — s80 extension).  
`XTHL` swaps HL with the top item, handling both `int` and `tuple` transparently.

---

## Summary

| Category | 8080 | 8085 adds | s80 ✅ | s80 🔶 partial | s80 ❌ missing |
|----------|:----:|:---------:|:------:|:--------------:|:--------------:|
| Data transfer | 18 | +2 | 9 | 6 | 5 |
| Arithmetic | 20 | — | 12 | 4 | 4 |
| Logical | 15 | — | 11 | 4 | 2 |
| Rotate | 4 | — | 1 | 1 | 2 |
| Branch | 20 | — | 7 | — | 13 |
| Stack / control | 14 | — | 12 | — | 3 |
| I/O | 2 | — | 2 | — | 0 |
| **Total** | **~93** | **+2** | **~54** | **~15** | **~29** |

> **🔶 partial** means the instruction is defined in `instructions.py` and `table.py`  
> (the assembler recognises and encodes it correctly) but the `execute()` method  
> does not yet handle it — the emulator will silently skip it without advancing PC,  
> causing an **infinite loop** if encountered at runtime.
>
> **Design intent:** s80 targets educational use on ESP32/MicroPython with tight RAM.  
> Missing instructions are either memory-heavy (interrupts, full hardware stack)  
> or rarely needed for the target demo programs (DAD, DAA, conditional calls/returns).
