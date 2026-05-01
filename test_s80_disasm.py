# disasm_s80.py - disassembler tests
# OctopusLAB - MicroPython / ESP32

from components.microprocessor.s80.core import hex_str_to_bytes, print_disasm

print("[ test ] --- 1")
print_disasm(hex_str_to_bytes("00 3E FF C3 00 00"))

print("[ test ] --- 2")
print_disasm(hex_str_to_bytes("003EFFC32301"))
