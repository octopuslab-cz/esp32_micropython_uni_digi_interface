; example07 spec operation HW
    JMP start
    NOP
print_acc:
    MOV_A,A ; 
    RET
led0:
    MOV_L,L ; 
    RET
    ;
led1:
    MOV_H,H ; 
    RET
    ;
sleep1:
    MOV_E,E ; 
    RET
    ;
start:
    NOP
    CALL led1
    CALL sleep1
    CALL led0
    CALL sleep1
    NOP
    CALL led1
    CALL sleep1
    CALL led0
    CALL sleep1 
    ;
    NOP ; end    
end.
