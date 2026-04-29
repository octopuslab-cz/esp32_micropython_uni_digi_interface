\# S80 vs Intel 8080 / 8085 — Instruction Set Comparison



\## Legend

\- ✔ = implemented

\- \~ = partially implemented / simplified

\- ✖ = missing



\---



\## 1. Basic Instructions



| Instruction | 8080 | 8085 | S80 |

|------------|------|------|-----|

| NOP        | ✔    | ✔    | ✔   |

| HLT        | ✔    | ✔    | ✔   |

| EI         | ✔    | ✔    | ✖   |

| DI         | ✔    | ✔    | ✖   |

| SIM        | ✖    | ✔    | ✖   |

| RIM        | ✖    | ✔    | ✖   |



\---



\## 2. Data Transfer



| Instruction | 8080 | 8085 | S80 |

|------------|------|------|-----|

| MOV r,r    | ✔    | ✔    | ✔ (partial set) |

| MOV r,M    | ✔    | ✔    | ✔ |

| MOV M,r    | ✔    | ✔    | ✔ |

| MVI r      | ✔    | ✔    | ✔ |

| MVI M      | ✔    | ✔    | ✔ |

| LXI B/H    | ✔    | ✔    | ✔ |

| LXI D/SP   | ✔    | ✔    | ✖ |

| LDA        | ✔    | ✔    | ✔ |

| STA        | ✔    | ✔    | ✔ |

| LHLD       | ✔    | ✔    | ✖ |

| SHLD       | ✔    | ✔    | ✖ |

| LDAX       | ✔    | ✔    | ✖ |

| STAX       | ✔    | ✔    | ✖ |

| XCHG       | ✔    | ✔    | ✖ |



\---



\## 3. Arithmetic



| Instruction | 8080 | 8085 | S80 |

|------------|------|------|-----|

| ADD r      | ✔    | ✔    | ✔ |

| ADD M      | ✔    | ✔    | ✔ |

| ADI        | ✔    | ✔    | ✔ |

| ADC        | ✔    | ✔    | ✖ |

| SUB        | ✔    | ✔    | ✖ |

| SBB        | ✔    | ✔    | ✖ |

| INR        | ✔    | ✔    | ✔ |

| DCR        | ✔    | ✔    | ✔ |

| INX        | ✔    | ✔    | ✔ |

| DCX        | ✔    | ✔    | ✔ |

| DAD        | ✔    | ✔    | ✖ |

| DAA        | ✔    | ✔    | ✖ |



\---



\## 4. Logical Operations



| Instruction | 8080 | 8085 | S80 |

|------------|------|------|-----|

| ANA        | ✔    | ✔    | ✔ |

| ANI        | ✔    | ✔    | ✔ |

| ORA        | ✔    | ✔    | ✔ |

| ORI        | ✔    | ✔    | ✔ |

| XRA        | ✔    | ✔    | ✔ |

| XRI        | ✔    | ✔    | ✔ |

| CMP        | ✔    | ✔    | ✔ |

| CPI        | ✔    | ✔    | ✔ |

| CMA        | ✔    | ✔    | ✔ |

| CMC        | ✔    | ✔    | ✖ |

| STC        | ✔    | ✔    | ✖ |



\---



\## 5. Rotate Instructions



| Instruction | 8080 | 8085 | S80 |

|------------|------|------|-----|

| RLC        | ✔    | ✔    | ✔ |

| RRC        | ✔    | ✔    | ✔ |

| RAL        | ✔    | ✔    | ✖ |

| RAR        | ✔    | ✔    | ✖ |



\---



\## 6. Control Flow



| Instruction | 8080 | 8085 | S80 |

|------------|------|------|-----|

| JMP        | ✔    | ✔    | ✔ |

| JZ         | ✔    | ✔    | ✔ |

| JNZ        | ✔    | ✔    | ✔ |

| JC         | ✔    | ✔    | ✔ |

| JNC        | ✔    | ✔    | ✔ |

| JP         | ✔    | ✔    | ✖ |

| JM         | ✔    | ✔    | ✖ |

| CALL       | ✔    | ✔    | ✔ (simplified) |

| RET        | ✔    | ✔    | ✔ |

| Conditional CALL | ✔ | ✔ | ✖ |

| Conditional RET  | ✔ | ✔ | ✖ |

| RST        | ✔    | ✔    | ✖ |

| PCHL       | ✔    | ✔    | ✖ |



\---



\## 7. Stack \& I/O



| Instruction | 8080 | 8085 | S80 |

|------------|------|------|-----|

| PUSH       | ✔    | ✔    | ✖ |

| POP        | ✔    | ✔    | ✖ |

| SPHL       | ✔    | ✔    | ✖ |

| IN         | ✔    | ✔    | ✔ |

| OUT        | ✔    | ✔    | ✔ |



\---



\## 8. Flags Support



| Flag | 8080/8085 | S80 |

|------|----------|-----|

| Zero (Z) | ✔ | ✔ |

| Carry (C) | ✔ | ✔ |

| Sign (S) | ✔ | ✖ |

| Parity (P) | ✔ | ✖ |

| Aux Carry (AC) | ✔ | ✖ |



\---



\## 9. S80 Custom Extensions



| Instruction | Description |

|------------|------------|

| MOV\_A,A | Debug: print registers |

| MOV\_B,B | Dump memory |

| MOV\_C,C | Print program counter |

| MOV\_D,D | Display output |

| MOV\_E,E | Delay (sleep) |

| MOV\_H,H | LED ON |

| MOV\_L,L | LED OFF |



\---



\## Summary



\### Implemented Core

\- Arithmetic (basic)

\- Logical operations

\- Register/memory transfer

\- Basic branching (JMP, JZ, JNZ, JC, JNC)

\- Simple CALL/RET

\- I/O (IN/OUT)



\### Missing or Incomplete

\- Full stack support (PUSH/POP)

\- Carry-based arithmetic (ADC, SBB)

\- Advanced control flow (conditional CALL/RET, RST)

\- 16-bit arithmetic (DAD)

\- Flag completeness (S, P, AC)

\- Some data transfer instructions (LHLD, SHLD, LDAX, STAX)



\### Design Note

S80 is a simplified, partially compatible subset of 8080/8085 with added debugging and hardware-oriented pseudo-instructions, making it suitable for educational and embedded experimentation purposes.

