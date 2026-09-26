import re
import json

def mips2cpp(script: str, files: dict[str, str | int]) -> str:
    ret = 0
    jr = '''#define jr(R) {\\
        switch (R){\\
            '''
    res = '''#include <bits/stdc++.h>
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

int main(){\n'''
    for file, addr in files.items():
        res += f'ifstream file{addr}({json.dumps(file)});\n'
        res += f'if (!file{addr})' + '{\ncout << "Unable to open file";\nreturn 1;\n}\n'
        res += '''char buffer[5] = {'\\0', '\\0', '\\0', '\\0', '\\0'};

int i = 0;
while (file''' + str(addr) + '.read(buffer, 4) || file' + str(addr) + '''.gcount() > 0) {
    writemem(''' + str(addr) + ''' + i, (buffer[0] << 24) | (buffer[1] << 16) | (buffer[2] << 8) | buffer[3]);
    buffer[0] = '\\0';
    buffer[1] = '\\0';
    buffer[2] = '\\0';
    buffer[3] = '\\0';
    i += 4;
}\n'''
        res += f'file{addr}.close();\n'
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
                        res += f"cout << (char)({arguments[0]} + {arguments[2]}) << '\\n'"
                    case 1:
                        res += f'cin >> inp; {arguments[0]} = (int)inp + {arguments[2]}'
                    case 2:
                        res += f"cout << (char)(readmem({arguments[0]}) + {arguments[2]}) << '\\n'"
                    case 3:
                        res += 'cout'
                        for i in range(32):
                            res += f" << R{i} << ' '"
                        res += " << '\\n'"
                    case 4:
                        res += f'cout << {arguments[0]}'
                    case 5:
                        res += f"for (int n : readarr({arguments[0]}, {arguments[2]})) cout << n << ' ';\ncout << '\\n'"
                    case 6:
                        res += f'return {arguments[2]}'
                    case 7:
                        res += f"cout << (readmem({arguments[0]} + {arguments[2]})) << '\\n'"

        res += ';\n'
    jr += '''default:\\
                break;\\
        }\\
    }\n'''
    res = jr + res + 'return 0;}'
    return res