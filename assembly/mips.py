from mips2cpp import mips2cpp
import argparse
import subprocess
import re
import os

def regify(x: str):
    return int(x[1:])

def readmem(addr: int):
    global mem
    b = mem[addr:addr+4]
    return (b[0] << 24) | (b[1] << 16) | (b[2] << 8) | b[3]

def writemem(addr: int, data: int):
    global mem
    mem[addr] = (data >> 24) & 0xFF
    mem[addr + 1] = (data >> 16) & 0xFF
    mem[addr + 2] = (data >> 8) & 0xFF
    mem[addr + 3] = data & 0xFF

def readarr(start: int, length: int):
    arr = []
    for i in range(length):
        arr.append(readmem(start + i * 4))
    return arr

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="MIPS interpreter.")
    parser.add_argument("script", help="Path to the MIPS script to run")
    parser.add_argument("-pc", help="PC of first command in program",default=0,type=int)
    parser.add_argument("--compile", "-c", help="Compile the program",action="store_true")
    parser.add_argument("--tocpp", "-tocpp", help="Transpile the program to C++",action="store_true")
    parser.add_argument("--load", help="Load a program to mem. PATH:ADDR",action="append",default=[],type=str)

    args = parser.parse_args()

    with open(args.script) as f:
        script = f.read()

    if args.compile or args.tocpp:
        dct = {}
        for load in args.load:
            if type(load) is str: # for type hints
                file, addr = load.split(':')
                dct[file] = int(addr)
        cpp_output = mips2cpp(script, dct)
        with open(os.path.basename(os.path.splitext(args.script)[0]) + '.cpp',"w") as f:
            f.write(cpp_output)
        if args.compile:
            subprocess.run(f'g++ -o {os.path.basename(os.path.splitext(args.script)[0])} {os.path.basename(os.path.splitext(args.script)[0]) + '.cpp'}')
        if not args.tocpp:
            os.remove(os.path.basename(os.path.splitext(args.script)[0]) + '.cpp')
    else:
        BTB = [1, 0]

        pc: int = args.pc
        regs = [0]*32
        mem = [0] * 4096

        for load in args.load:
            if type(load) is str: # for type hints
                file, addr = load.split(':')
                addr = int(addr)
                with open(file) as f:
                    rd = f.read()
                    for i in range(0, len(rd), 4):
                        if len(rd[i:i+4]) < 4:
                            rd += chr(0) * (4 - (len(rd[i:i+4])))
                        b = rd[i:i+4]
                        writemem(addr + i, (ord(b[0]) << 24) | (ord(b[1]) << 16) | (ord(b[2]) << 8) | ord(b[3]))

        BMP = 0
        IC = 0
        branch = 0
        jump = 0
        taken = 0
        labels = {}
        script = script.splitlines()
        for i in range(len(script)):
            if script[i].strip().endswith(':'):
                labels[script[i].strip()[:-1].lower()] = pc + 4 * i
        script = ['nop'] * (pc // 4) + script
        while pc < len(script)*4:
            command = script[pc // 4].lower().strip()
            if command.startswith('#') or command.endswith(':') or command.startswith('nop') or not command:
                if command.startswith('nop'): IC += 1
                pc += 4
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
                arguments[1] = 'r' + nums[1]
                arguments.append(nums[0])
            match command:
                case 'add':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] + regs[regify(arguments[2])]
                case 'sub':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] - regs[regify(arguments[2])]
                case 'addi':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] + imm
                case 'addu':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] + regs[regify(arguments[2])]
                case 'subu':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] - regs[regify(arguments[2])]
                case 'addiu':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] + imm
                case 'subi':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] - imm
                case 'and':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] & regs[regify(arguments[2])]
                case 'or':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] | regs[regify(arguments[2])]
                case 'andi':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] & imm
                case 'ori':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] | imm
                case 'sli':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] << imm
                case 'sri':
                    regs[regify(arguments[0])] = regs[regify(arguments[1])] >> imm
                case 'lw':
                    regs[regify(arguments[0])] = readmem(regs[regify(arguments[1])] + imm)
                case 'sw':
                    writemem(regs[regify(arguments[1])] + imm, regs[regify(arguments[0])])
                case 'beq':
                    branch += 1
                    BMP += (regs[regify(arguments[0])] == regs[regify(arguments[1])]) != BTB[0]
                    if regs[regify(arguments[0])] == regs[regify(arguments[1])]:
                        pc = labels[arguments[2]] - 4
                        taken += 1
                        match BTB:
                            case [0, 0]: BTB = [0, 1]
                            case [1, 0]: BTB = [1, 1]
                            case [0, 1]: BTB = [1, 0]
                            case [1, 1]: BTB = [1, 1]
                    else:
                        match BTB:
                            case [0, 0]: BTB = [0, 0]
                            case [1, 0]: BTB = [0, 1]
                            case [0, 1]: BTB = [0, 0]
                            case [1, 1]: BTB = [1, 0]
                case 'bne':
                    branch += 1
                    BMP += (regs[regify(arguments[0])] != regs[regify(arguments[1])]) != BTB[0]
                    if regs[regify(arguments[0])] != regs[regify(arguments[1])]:
                        pc = labels[arguments[2]] - 4
                        taken += 1
                        match BTB:
                            case [0, 0]: BTB = [0, 1]
                            case [1, 0]: BTB = [1, 1]
                            case [0, 1]: BTB = [1, 0]
                            case [1, 1]: BTB = [1, 1]
                    else:
                        match BTB:
                            case [0, 0]: BTB = [0, 0]
                            case [1, 0]: BTB = [0, 1]
                            case [0, 1]: BTB = [0, 0]
                            case [1, 1]: BTB = [1, 0]
                case 'slt':
                    regs[regify(arguments[0])] = int(regs[regify(arguments[1])] < regs[regify(arguments[2])])
                case 'j':
                    jump += 1
                    pc = labels[arguments[0]] - 4
                case 'jump':
                    jump += 1
                    pc = labels[arguments[0]] - 4
                case 'jal':
                    jump += 1
                    regs[31] = pc
                    pc = labels[arguments[0]] - 4
                case 'jr':
                    jump += 1
                    pc = regs[regify(arguments[0])]
                case 'syscall':
                    match int(arguments[1]):
                        case 0:
                            print(chr(regs[regify(arguments[0])] + int(arguments[2])),end='')
                        case 1:
                            regs[regify(arguments[0])] = ord(input()) + int(arguments[2])
                        case 2:
                            print(chr(readmem(regs[regify(arguments[0])]) + int(arguments[2])),end='')
                        case 3:
                            print(regs)
                        case 4:
                            print(regs[regify(arguments[0])])
                        case 5:
                            print(readarr(regs[regify(arguments[0])], int(arguments[2])))
                        case 6:
                            raise ValueError
                        case 7:
                            print(readmem(regs[regify(arguments[0])] + int(arguments[2])))
            IC += 1
            for i in range(len(regs)):
                regs[i] = (regs[i] + 2**31) % 2**32 - 2**31
            regs[0] = 0
            pc += 4