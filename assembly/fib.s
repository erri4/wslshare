addi R1, R0, 0
addi R2, R0, 0
addi R3, R0, 0
INP:
sli R2, R1, 1
sli R3, R1, 3
syscall R1, 1, 0
beq R1, R0, ENDINP
subi R1, R1, 48
add R1, R1, R2
add R1, R1, R3
j INP
ENDINP:
sri R1, R2, 1

addi R2, R0, 0
addi R3, R0, 0
addi R4, R0, 1
FIBLOOP:
    beq R2, R1, ENDFIB
    add R5, R3, R4
    addi R3, R4, 0
    addi R4, R5, 0
    addi R2, R2, 1
    bne R2, R1, FIBLOOP
ENDFIB:
syscall R3, 4, 0
