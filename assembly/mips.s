addi R1, R0, 0
# ptr

addi R2, R0, 0
# current cell

addi R3, R0, 0
# pc

addi R4, R0, 0
# top of stack
# (stack is at 2000)

addi R5, R0, 3
# command byte

addi R21, R0, 1
addi R22, R0, 2
addi R23, R0, 3

addi R11, R0, 43
# +
addi R12, R0, 45
# -
addi R13, R0, 91
# [
addi R14, R0, 93
# ]
addi R15, R0, 60
# <
addi R16, R0, 62
# >
addi R17, R0, 44
# ,
addi R18, R0, 46
# .
# consts

LOOP:
jal READ
lw R2, 0(R1)

beq R6, R12, CASEMN
beq R6, R13, CASEOP
beq R6, R14, CASECL
beq R6, R15, CASELEFT
beq R6, R16, CASERIGHT
beq R6, R17, CASEINP
beq R6, R18, CASEPR
bne R6, R11, CASENOP

CASEPL:
addi R2, R2, 1
j CASENOP

CASEMN:
subi R2, R2, 1
j CASENOP

CASEOP:
# if enter:
# push pc
# else:
# skip loop
bne R2, R0, ENTER
j SKIP
ENTER:
sli R3, R3, 2
add R3, R3, R5
sw R3, 2000(R4)
sri R3, R3, 2
addi R4, R4, 4
j CASENOP
SKIP:
addi R7, R0, 1
# depth
LOOP2:
jal READ
beq R6, R14, OUT
beq R6, R13, IN
j ALWAYS
IN:
addi R7, R7, 1
j ALWAYS
OUT:
subi R7, R7, 1
ALWAYS:
bne R7, R0, LOOP2
j CASENOP

CASECL:
# if repeat:
# read stack
# jump there
# else:
# pop stack
bne R2, R0, REPEAT
j CONT
REPEAT:
subi R4, R4, 4
lw R3, 2000(R4)
andi R5, R3, 3
sri R3, R3, 2
addi R4, R4, 4
j CASENOP
CONT:
subi R4, R4, 4
j CASENOP

CASELEFT:
subi R1, R1, 4
lw R2, 0(R1)
j CASENOP

CASERIGHT:
addi R1, R1, 4
lw R2, 0(R1)
j CASENOP

CASEINP:
syscall R2, 1, 0
j CASENOP

CASEPR:
syscall R2, 0, 0

CASENOP:

andi R2, R2, 255
sw R2, 0(R1)

j LOOP

READ:
    lw R6, 1000(R3)
    beq R6, R0, END

    beq R5, R21, CASE1
    beq R5, R22, CASE2
    beq R5, R23, CASE3

    CASE0:
    andi R6, R6, 255
    addi R5, R0, 3
    addi R3, R3, 4
    j ENDCASES1

    CASE1:
    andi R6, R6, 65280
    sri R6, R6, 8
    addi R5, R0, 0
    j ENDCASES1

    CASE2:
    andi R6, R6, 16711680
    sri R6, R6, 16
    addi R5, R0, 1
    j ENDCASES1

    CASE3:
    andi R6, R6, 4278190080
    sri R6, R6, 24
    addi R5, R0, 2

    ENDCASES1:
    jr R31

END: