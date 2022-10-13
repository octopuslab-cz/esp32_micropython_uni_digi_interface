from components.microprocesor.i8085 import instructions as i8085
i8085.instructions["NOP"]

for i in i8085.instructions:
    print(i, hex(i8085.instructions[i]))
