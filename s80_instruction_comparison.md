# Instruction Set Comparison: Intel 8080 / Intel 8085 / s80

> **s80** = simplified emulator subset (OctopusLAB 2015–26, MicroPython/ESP32)  
> ✅ = supported &nbsp; ➕ = added in 8085 &nbsp; 🔶 = partial / simplified &nbsp; ❌ = not implemented &nbsp; 🔁 = repurposed as special subroutine

---

## Data Transfer

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `MOV r1, r2` | ✅ | ✅ | ✅ | `0x40`–`0x7F` | Most pairs implemented |
| `MOV r, M` | ✅ | ✅ | ✅ | varies | HL used as address |
| `MOV M, r` | ✅ | ✅ | ✅ | varies | HL used as address |
| `MVI r, d8` | ✅ | ✅ | ✅ | `0x06`–`0x3E` | A B C H L M supported |
| `LXI rp, d16` | ✅ | ✅ | ✅ | `0x01` `0x21` | B and H pairs only |
| `LDA addr` | ✅ | ✅ | ✅ | `0x3A` | Load A from memory |
| `STA addr` | ✅ | ✅ | ✅ | `0x32` | Store A to memory |
| `LHLD addr` | ✅ | ✅ | ❌ | `0x2A` | Load HL direct |
| `SHLD addr` | ✅ | ✅ | ❌ | `0x22` | Store HL direct |
| `LDAX rp` | ✅ | ✅ | ❌ | `0x0A` `0x1A` | Load A indirect via BC/DE |
| `STAX rp` | ✅ | ✅ | ❌ | `0x02` `0x12` | Store A indirect via BC/DE |
| `XCHG` | ✅ | ✅ | ❌ | `0xEB` | Exchange DE ↔ HL |
| `RIM` | ❌ | ✅ | ❌ | `0x20` | Read Interrupt Mask (8085 only) |
| `SIM` | ❌ | ✅ | ❌ | `0x30` | Set Interrupt Mask (8085 only) |

---

## Arithmetic

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `ADD r` | ✅ | ✅ | ✅ | `0x80`–`0x87` | A B C H L; M partial |
| `ADD M` | ✅ | ✅ | ✅ | `0x86` | Add (HL) to A |
| `ADI d8` | ✅ | ✅ | ✅ | `0xC6` | Add immediate |
| `ADC r` | ✅ | ✅ | ✅ | `0x88`–`0x8F` | Add with carry |
| `ADC M` | ✅ | ✅ | ✅ | `0x8E` | Add (HL)+carry to A |
| `ACI d8` | ✅ | ✅ | ❌ | `0xCE` | Add immediate with carry |
| `SUB r` | ✅ | ✅ | ✅ | `0x90`–`0x97` | A B C H L M |
| `SUB M` | ✅ | ✅ | ✅ | `0x96` | Subtract (HL) from A |
| `SUI d8` | ✅ | ✅ | ❌ | `0xD6` | Subtract immediate |
| `SBB r` | ✅ | ✅ | ✅ | `0x98`–`0x9F` | Subtract with borrow |
| `SBB M` | ✅ | ✅ | ✅ | `0x9E` | Subtract (HL)+borrow from A |
| `SBI d8` | ✅ | ✅ | ❌ | `0xDE` | Subtract immediate with borrow |
| `INR r` | ✅ | ✅ | ✅ | varies | A B C H L supported |
| `INR M` | ✅ | ✅ | ❌ | `0x34` | Increment memory |
| `DCR r` | ✅ | ✅ | ✅ | varies | A B C H L supported |
| `DCR M` | ✅ | ✅ | ❌ | `0x35` | Decrement memory |
| `INX rp` | ✅ | ✅ | ✅ | `0x03` `0x23` | B and H pairs |
| `DCX rp` | ✅ | ✅ | ✅ | `0x0B` `0x2B` | B and H pairs |
| `DAD rp` | ✅ | ✅ | ❌ | `0x09`–`0x39` | Add register pair to HL |
| `DAA` | ✅ | ✅ | ❌ | `0x27` | Decimal adjust accumulator |

---

## Logical

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `ANA r` | ✅ | ✅ | ✅ | `0xA0`–`0xA7` | A B C D E H L M all done |
| `ANA M` | ✅ | ✅ | ✅ | `0xA6` | AND (HL) with A |
| `ANI d8` | ✅ | ✅ | ✅ | `0xE6` | AND immediate |
| `ORA r` | ✅ | ✅ | ✅ | `0xB0`–`0xB7` | A B C H L M |
| `ORA M` | ✅ | ✅ | ✅ | `0xB6` | OR (HL) with A |
| `ORI d8` | ✅ | ✅ | ✅ | `0xF6` | OR immediate |
| `XRA r` | ✅ | ✅ | ✅ | `0xA8`–`0xAF` | A B C H L M |
| `XRA M` | ✅ | ✅ | ✅ | `0xAE` | XOR (HL) with A |
| `XRI d8` | ✅ | ✅ | ✅ | `0xEE` | XOR immediate |
| `CMP r` | ✅ | ✅ | ✅ | `0xB8`–`0xBF` | A B C H L M |
| `CMP M` | ✅ | ✅ | ✅ | `0xBE` | Compare (HL) with A |
| `CPI d8` | ✅ | ✅ | ✅ | `0xFE` | Compare immediate |
| `CMA` | ✅ | ✅ | ✅ | `0x2F` | Complement A |
| `STC` | ✅ | ✅ | ❌ | `0x37` | Set carry flag |
| `CMC` | ✅ | ✅ | ❌ | `0x3F` | Complement carry flag |

---

## Rotate / Shift

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `RLC` | ✅ | ✅ | 🔶 | `0x07` | Rotate left; carry update missing |
| `RRC` | ✅ | ✅ | ✅ | `0x0F` | Rotate right through carry |
| `RAL` | ✅ | ✅ | ❌ | `0x17` | Rotate left through carry |
| `RAR` | ✅ | ✅ | ❌ | `0x1F` | Rotate right through carry |

---

## Branch

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `JMP addr` | ✅ | ✅ | ✅ | `0xC3` | Unconditional jump |
| `JZ addr` | ✅ | ✅ | ✅ | `0xCA` | Jump if zero |
| `JNZ addr` | ✅ | ✅ | ✅ | `0xC2` | Jump if not zero |
| `JC addr` | ✅ | ✅ | ✅ | `0xDA` | Jump if carry |
| `JNC addr` | ✅ | ✅ | ✅ | `0xD2` | Jump if no carry |
| `JP addr` | ✅ | ✅ | ❌ | `0xF2` | Jump if positive (S=0) |
| `JM addr` | ✅ | ✅ | ❌ | `0xFA` | Jump if minus (S=1) |
| `JPE addr` | ✅ | ✅ | ❌ | `0xEA` | Jump if parity even |
| `JPO addr` | ✅ | ✅ | ❌ | `0xE2` | Jump if parity odd |
| `PCHL` | ✅ | ✅ | ❌ | `0xE9` | Jump to address in HL |
| `CALL addr` | ✅ | ✅ | 🔶 | `0xCD` | Call; single SP (no real stack) |
| `RET` | ✅ | ✅ | 🔶 | `0xC9` | Return; single SP level only |
| `CZ / CNZ` | ✅ | ✅ | ❌ | `0xCC/0xC4` | Conditional call |
| `CC / CNC` | ✅ | ✅ | ❌ | `0xDC/0xD4` | Conditional call |
| `RZ / RNZ` | ✅ | ✅ | ❌ | `0xC8/0xC0` | Conditional return |
| `RC / RNC` | ✅ | ✅ | ❌ | `0xD8/0xD0` | Conditional return |

---

## Stack & Machine Control

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `PUSH rp` | ✅ | ✅ | ❌ | varies | No hardware stack |
| `POP rp` | ✅ | ✅ | ❌ | varies | No hardware stack |
| `XTHL` | ✅ | ✅ | ❌ | `0xE3` | Exchange top of stack with HL |
| `SPHL` | ✅ | ✅ | ❌ | `0xF9` | Load SP from HL |
| `NOP` | ✅ | ✅ | ✅ | `0x00` | No operation |
| `HLT` | ✅ | ✅ | ✅ | `0x76` | Halt |
| `EI` | ✅ | ✅ | ❌ | `0xFB` | Enable interrupts |
| `DI` | ✅ | ✅ | ❌ | `0xF3` | Disable interrupts |
| `RST n` | ✅ | ✅ | ❌ | varies | Restart (interrupt call) |

---

## I/O

| Mnemonic | 8080 | 8085 | s80 | Opcode | Notes |
|----------|:----:|:----:|:---:|:------:|-------|
| `IN port` | ✅ | ✅ | ✅ | `0xDB` | Read port → A; GPIO/expander hook |
| `OUT port` | ✅ | ✅ | ✅ | `0xD3` | Write A → port; GPIO/expander hook |

---

## s80 Special Subroutines (non-standard)

These reuse `MOV r,r` no-ops as debug/hardware hooks — not present in 8080/8085.

| s80 mnemonic | Opcode | Function |
|--------------|:------:|----------|
| `MOV A,A` | `0x7F` | Print registers A / B / C + show byte on RGB LED |
| `MOV B,B` | `0x40` | Dump virtual memory |
| `MOV C,C` | `0x49` | Print current PC |
| `MOV D,D` | `0x52` | Show value at HL address on 7-seg display |
| `MOV E,E` | `0x5B` | Sleep 1 second |
| `MOV H,H` | `0x64` | LED ON |
| `MOV L,L` | `0x6D` | LED OFF |

---

## Summary

| Category | 8080 total | 8085 adds | s80 ✅ | s80 ❌ missing |
|----------|:----------:|:---------:|:------:|:--------------:|
| Data transfer | 18 | +2 (RIM/SIM) | 10 | 10 |
| Arithmetic | 20 | — | 14 | 6 |
| Logical | 15 | — | 14 | 1 (STC/CMC) |
| Rotate | 4 | — | 2 | 2 (RAL/RAR) |
| Branch | 20 | — | 7 | 13 |
| Stack / control | 10 | — | 2 | 8 |
| I/O | 2 | — | 2 | 0 |
| **Total** | **~89** | **+2** | **~51** | **~40** |

> **Design intent:** s80 targets educational use on ESP32/MicroPython with tight RAM.  
> The missing instructions are either memory-heavy (full stack, interrupts) or rarely  
> needed for the target demo programs (DAD, DAA, conditional calls/returns).
