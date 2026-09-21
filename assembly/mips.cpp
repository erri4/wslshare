#define jr(R) {\
        switch (R){\
            case 0:\
                goto RET0;\
                break;\
            case 1:\
                goto RET1;\
                break;\
            default:\
                break;\
        }\
    }
#include <bits/stdc++.h>
using namespace std;
const int R0 = 0;
int R1 = 0;
int R2 = 0;
int R3 = 0;
int R4 = 0;
int R5 = 0;
int R6 = 0;
int R7 = 0;
int R8 = 0;
int R9 = 0;
int R10 = 0;
int R11 = 0;
int R12 = 0;
int R13 = 0;
int R14 = 0;
int R15 = 0;
int R16 = 0;
int R17 = 0;
int R18 = 0;
int R19 = 0;
int R20 = 0;
int R21 = 0;
int R22 = 0;
int R23 = 0;
int R24 = 0;
int R25 = 0;
int R26 = 0;
int R27 = 0;
int R28 = 0;
int R29 = 0;
int R30 = 0;
int R31 = 0;
char inp;
vector<int> mem(4096, 0);

int readmem(int addr){
    return (mem[addr+0] << 24) | (mem[addr+1] << 16) | (mem[addr+2] << 8) | mem[addr+3];
}

void writemem(int addr, int data){
    mem[addr] = (data >> 24) & 0xFF;
    mem[addr + 1] = (data >> 16) & 0xFF;
    mem[addr + 2] = (data >> 8) & 0xFF;
    mem[addr + 3] = data & 0xFF;
}

vector<int> readarr(int start, int length){
    vector<int> arr;
    for (int i = 0; i < length; i++){
        arr.push_back(readmem(start + i * 4));
    }
    return arr;
}

int main(){
ifstream file1000(".\\testasm.bf");
if (!file1000){
cout << "Unable to open file";
return 1;
}
char buffer[5] = {'\0', '\0', '\0', '\0', '\0'};

int i = 0;
while (file1000.read(buffer, 4) || file1000.gcount() > 0) {
    writemem(1000 + i, (buffer[0] << 24) | (buffer[1] << 16) | (buffer[2] << 8) | buffer[3]);
    buffer[0] = '\0';
    buffer[1] = '\0';
    buffer[2] = '\0';
    buffer[3] = '\0';
    i += 4;
}
file1000.close();
R1 = R0 + 0;
//# ptr

R2 = R0 + 0;
//# current cell

R3 = R0 + 0;
//# pc

R4 = R0 + 0;
//# top of stack
//# (stack is at 2000)

R5 = R0 + 3;
//# command byte

R21 = R0 + 1;
R22 = R0 + 2;
R23 = R0 + 3;

R11 = R0 + 43;
//# +
R12 = R0 + 45;
//# -
R13 = R0 + 91;
//# [
R14 = R0 + 93;
//# ]
R15 = R0 + 60;
//# <
R16 = R0 + 62;
//# >
R17 = R0 + 44;
//# ,
R18 = R0 + 46;
//# .
//# consts

LOOP:
R31 = 0;
goto READ;
RET0:;
R2 = readmem(R1 + 0);

if (R6 == R12) goto CASEMN;
if (R6 == R13) goto CASEOP;
if (R6 == R14) goto CASECL;
if (R6 == R15) goto CASELEFT;
if (R6 == R16) goto CASERIGHT;
if (R6 == R17) goto CASEINP;
if (R6 == R18) goto CASEPR;
if (R6 != R11) goto CASENOP;

CASEPL:
R2 = R2 + 1;
goto CASENOP;

CASEMN:
R2 = R2 - 1;
goto CASENOP;

CASEOP:
//# if enter:
//# push pc
//# else:
//# skip loop
if (R2 != R0) goto ENTER;
goto SKIP;
ENTER:
R3 = R3 << 2;
R3 = R3 + R5;
writemem(R4 + 2000, R3);
R3 = R3 >> 2;
R4 = R4 + 4;
goto CASENOP;
SKIP:
R7 = R0 + 1;
//# depth
LOOP2:
R31 = 1;
goto READ;
RET1:;
if (R6 == R14) goto OUT;
if (R6 == R13) goto IN;
goto ALWAYS;
IN:
R7 = R7 + 1;
goto ALWAYS;
OUT:
R7 = R7 - 1;
ALWAYS:
if (R7 != R0) goto LOOP2;
goto CASENOP;

CASECL:
//# if repeat:
//# read stack
//# jump there
//# else:
//# pop stack
if (R2 != R0) goto REPEAT;
goto CONT;
REPEAT:
R4 = R4 - 4;
R3 = readmem(R4 + 2000);
R5 = R3 & 3;
R3 = R3 >> 2;
R4 = R4 + 4;
goto CASENOP;
CONT:
R4 = R4 - 4;
goto CASENOP;

CASELEFT:
R1 = R1 - 4;
R2 = readmem(R1 + 0);
goto CASENOP;

CASERIGHT:
R1 = R1 + 4;
R2 = readmem(R1 + 0);
goto CASENOP;

CASEINP:
cin >> inp; R2 = (int)inp + 0;
//# input
goto CASENOP;

CASEPR:
cout << (char)(R2 + 0);
//# print

CASENOP:

R2 = R2 & 255;
writemem(R1 + 0, R2);

goto LOOP;

READ:
R6 = readmem(R3 + 1000);
if (R6 == R0) goto END;

if (R5 == R21) goto CASE1;
if (R5 == R22) goto CASE2;
if (R5 == R23) goto CASE3;

CASE0:
R6 = R6 & 255;
R5 = R0 + 3;
R3 = R3 + 4;
goto ENDCASES1;

CASE1:
R6 = R6 & 65280;
R6 = R6 >> 8;
R5 = R0 + 0;
goto ENDCASES1;

CASE2:
R6 = R6 & 16711680;
R6 = R6 >> 16;
R5 = R0 + 1;
goto ENDCASES1;

CASE3:
R6 = R6 & 4278190080;
R6 = R6 >> 24;
R5 = R0 + 2;

ENDCASES1:
jr(R31);

END:
return 0;}