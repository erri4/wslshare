import re
import json

def mips2c(script: str, files: dict[str, str | int]) -> str:
    ret = 0
    jr = '''#define jr(R) {\\
        switch (R){\\
            '''
    res = '''#include <stdio.h>
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
    if (buffer[idx] == '\\0' || idx == 100){
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

int main(){\n'''
    for file, addr in files.items():
        res += f'FILE* file{addr} = fopen({json.dumps(file)}, "rb");\n'
        res += f'if (!file{addr})' + '{\nprintf("Unable to open file\\n");\nreturn 1;\n}\n'
        res += '''char buffer[5] = {'\\0', '\\0', '\\0', '\\0', '\\0'};

int i = 0;
size_t bytesRead;
while ((bytesRead = fread(buffer, 1, 4, file''' + str(addr) + ''')) > 0) {
    writemem(''' + str(addr) + ''' + i, ((unsigned char)buffer[0] << 24) | ((unsigned char)buffer[1] << 16) | ((unsigned char)buffer[2] << 8) | (unsigned char)buffer[3]);
    buffer[0] = '\\0';
    buffer[1] = '\\0';
    buffer[2] = '\\0';
    buffer[3] = '\\0';
    i += 4;
}\n'''
        res += f"fclose(file{addr});\n"

    res += "\n\n// Start of MIPS assembly (transpiled to C) code\n\n"
    for command in script.splitlines():
        command = command.strip()
        if not command:
            res += '\n'
            continue
        if command.startswith('#') or command.startswith('nop'):
            res += '//' + command + '\n'
            continue
        if command.endswith(':'):
            res += command + '\n'
            continue
        arguments = [x.strip() for x in command[command.find(' ')+1:].split(',')]
        if '' in arguments: arguments.remove('')
        command = command[:command.find(' ')] if command.find(' ') != -1 else command
        try:
            imm = int(arguments[-1])
        except ValueError, IndexError:
            imm = None
        if command == 'lw' or command == 'sw':
            nums = re.findall(r'\d+', arguments[1])
            imm = int(nums[0])
            arguments[1] = 'R' + nums[1]
            arguments.append(nums[0])
        match command:
            case 'add':
                res += f'{arguments[0]} = {arguments[1]} + {arguments[2]}'
            case 'sub':
                res += f'{arguments[0]} = {arguments[1]} - {arguments[2]}'
            case 'addi':
                res += f'{arguments[0]} = {arguments[1]} + {imm}'
            case 'subi':
                res += f'{arguments[0]} = {arguments[1]} - {imm}'
            case 'and':
                res += f'{arguments[0]} = {arguments[1]} & {arguments[2]}'
            case 'or':
                res += f'{arguments[0]} = {arguments[1]} | {arguments[2]}'
            case 'xor':
                res += f'{arguments[0]} = {arguments[1]} ^ {arguments[2]}'
            case 'xori':
                res += f'{arguments[0]} = {arguments[1]} ^ {imm}'
            case 'andi':
                res += f'{arguments[0]} = {arguments[1]} & {imm}'
            case 'ori':
                res += f'{arguments[0]} = {arguments[1]} | {imm}'
            case 'sli':
                res += f'{arguments[0]} = {arguments[1]} << {imm}'
            case 'sri':
                res += f'{arguments[0]} = {arguments[1]} >> {imm}'
            case 'lw':
                res += f'{arguments[0]} = readmem({arguments[1]} + {imm})'
            case 'sw':
                res += f'writemem({arguments[1]} + {imm}, {arguments[0]})'
            case 'beq':
                res += f'if ({arguments[0]} == {arguments[1]}) goto {arguments[2]}'
            case 'bne':
                res += f'if ({arguments[0]} != {arguments[1]}) goto {arguments[2]}'
            case 'slt':
                res += f'if ({arguments[1]} < {arguments[2]}) {arguments[0]} = 1;\nelse {arguments[0]} = 0'
            case 'j':
                res += f'goto {arguments[0]}'
            case 'jump':
                res += f'goto {arguments[0]}'
            case 'jal':
                res += f'R31 = {ret};\ngoto {arguments[0]};\nRET{ret}:'
                jr += f'''case {ret}:\\
                goto RET{ret};\\
                break;\\\n            '''
                ret += 1
            case 'jr':
                res += f'jr({arguments[0]})'
            case 'syscall':
                match int(arguments[1]):
                    case 0:
                        res += f'printf("%c", (char)({arguments[0]} + {imm}))'
                    case 1:
                        res += f'{arguments[0]} = scan() + {imm}'
                    case 2:
                        res += f'printf("%c", (char)(readmem({arguments[0]}) + {imm}))'
                    case 3:
                        res += 'printf'
                        fmt = " ".join(["%d"] * 32)
                        args_list = ", ".join([f"R{i}" for i in range(32)])
                        res += f'("{fmt}", {args_list})'
                    case 4:
                        res += f'printf("%d", {arguments[0]})'
                    case 5:
                        res += f"""int* temp_arr_{ret} = readarr({arguments[0]}, {imm});
if (temp_arr_{ret} != NULL) {{
    for (int idx_{ret} = 0; idx_{ret} < {imm}; idx_{ret}++) {{
        printf("%d ", temp_arr_{ret}[idx_{ret}]);
    }}
    free(temp_arr_{ret});
}}"""
                    case 6:
                        res += f'return {imm} + {arguments[0]}'
                    case 7:
                        res += f'printf("%d", readmem({arguments[0]} + {imm}))'

        res += ';\n'
    jr += '''default:\\
                break;\\
        }\\
    }\n'''
    res = jr + res + '\n\n//End of MIPS assembly code\nreturn 0;}'
    return res