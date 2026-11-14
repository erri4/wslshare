addi R4, R0, 0
# m stack at 1000
addi R5, R0, 0
# mult stack at 2000
addi R6, R0, 0
# jal stack at 3000

addi R9, R0, 3500
addi R10, R0, 3600
syscall R9, 8, "Enter first number"
syscall R10, 8, "Enter second number"
# use 58 after

addi R11, R0, 3700
addi R12, R0, 3800
syscall R11, 8, "*"
syscall R12, 8, "="
# use 32 after


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
syscall R9, 9, 58
syscall R0, 0, 32

addi R1, R0, 0
addi R2, R0, 0
addi R3, R0, 0
INPr1:
sli R2, R1, 1
sli R3, R1, 3
syscall R1, 1, 0
beq R1, R0, ENDINPr1
subi R1, R1, 48
add R1, R1, R2
add R1, R1, R3
j INPr1
ENDINPr1:
sri R1, R2, 1

syscall R10, 9, 58
syscall R0, 0, 32

addi R4, R0, 0
addi R2, R0, 0
addi R3, R0, 0
INPr2:
sli R2, R4, 1
sli R3, R4, 3
syscall R4, 1, 0
beq R4, R0, ENDINPr2
subi R4, R4, 48
add R4, R4, R2
add R4, R4, R3
j INPr2
ENDINPr2:
sri R4, R2, 1
addi R2, R4, 0

addi R3, R0, 0
addi R4, R0, 0
addi R5, R0, 0
addi R6, R0, 0

addi R15, R1, 0
addi R16, R2, 0

jal MULT
subi R5, R5, 4
lw R3, 2000(R5)
syscall R15, 4, 32
syscall R11, 9, 32
syscall R16, 4, 32
syscall R12, 9, 32
syscall R3, 4, 0