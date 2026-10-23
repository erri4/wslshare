addi R4, R0, 0
# m stack at 1000
addi R5, R0, 0
# mult stack at 2000
addi R6, R0, 0
# jal stack at 3000


j EXIT

MULT:
# R1 * R2
slt R7, R1, R2
beq R7, R0, GOODSIZE
addi R8, R2, 0
addi R2, R1, 0
addi R1, R8, 0
GOODSIZE:
sw R31, 3000(R6)
addi R6, R6, 4
beq R2, R0, CASE0
sw R2, 1000(R4)
addi R4, R4, 4
sri R2, R2, 1
jal MULT
subi R4, R4, 4
lw R2, 1000(R4)
subi R5, R5, 4
lw R3, 2000(R5)
sli R3, R3, 1
andi R2, R2, 1
beq R2, R0, PUSH
add R3, R3, R1
PUSH:
sw R3, 2000(R5)
addi R5, R5, 4
subi R6, R6, 4
lw R31, 3000(R6)
jr R31
CASE0:
sw R0, 2000(R5)
addi R5, R5, 4
subi R6, R6, 4
lw R31, 3000(R6)
jr R31

EXIT:

addi R1, R0, 456
addi R2, R0, 123
jal MULT
subi R5, R5, 4
lw R3, 2000(R5)
syscall R3, 4, 0