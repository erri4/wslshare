#define jr(R) {\
        switch (R){\
            default:\
                break;\
        }\
    }
#include <stdio.h>
#include <stdlib.h>
const int R0 = 0;
int R1;
int R2;
int R3;
int R4;
int R5;
int R6;
int R7;
int R8;
int R9;
int R10;
int R11;
int R12;
int R13;
int R14;
int R15;
int R16;
int R17;
int R18;
int R19;
int R20;
int R21;
int R22;
int R23;
int R24;
int R25;
int R26;
int R27;
int R28;
int R29;
int R30;
int R31;
char buffer[100];
int idx = 0;
int needs_input = 1;
unsigned char mem[4096] = {0};

int scan(){
    if (needs_input){
        scanf("%99s", buffer);
        needs_input = 0;
        idx = 0;
    }
    if (buffer[idx] == '\0' || idx == 100){
        needs_input = 1;
        return 0;
    }
    
    char res = buffer[idx];
    idx++;
    
    return (int)res;
}

int readmem(int addr){
    return ((int)mem[addr+0] << 24) | ((int)mem[addr+1] << 16) | ((int)mem[addr+2] << 8) | mem[addr+3];
}

void writemem(int addr, int data){
    mem[addr] = (data >> 24) & 0xFF;
    mem[addr + 1] = (data >> 16) & 0xFF;
    mem[addr + 2] = (data >> 8) & 0xFF;
    mem[addr + 3] = data & 0xFF;
}

int* readarr(int start, int length){
    int* arr = (int*)malloc(length * sizeof(int));
    if (arr == NULL) return NULL;
    for (int i = 0; i < length; i++){
        arr[i] = readmem(start + i * 4);
    }
    return arr;
}

int main(){


// Start of MIPS assembly (transpiled to C) code

R1 = R0 + 0;
R2 = R0 + 0;
R3 = R0 + 0;
INP:
R2 = R1 << 1;
R3 = R1 << 3;
R1 = scan() + 0;
if (R1 == R0) goto ENDINP;
R1 = R1 - 48;
R1 = R1 + R2;
R1 = R1 + R3;
goto INP;
ENDINP:
R1 = R2 >> 1;

R2 = R0 + 0;
R3 = R0 + 0;
R4 = R0 + 1;
FIBLOOP:
if (R2 == R1) goto ENDFIB;
R5 = R3 + R4;
R3 = R4 + 0;
R4 = R5 + 0;
R2 = R2 + 1;
if (R2 != R1) goto FIBLOOP;
ENDFIB:
printf("%d", R3);


//End of MIPS assembly code
return 0;}