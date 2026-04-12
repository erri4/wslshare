import sys
import os
import subprocess
token_map = {
    '>': "step_fwd",
    '<': "step_bk",
    '+': "add 1",
    '-': "add -1",
    '.': "out",
    ';': "outint",
    ',': "in",
    '[': "jmp_if_zero",
    ']': "jmp_if_nonzero",
    '#': "debug",
    '!': "debug",
}
 
def parse(code):
    valid_commands = {'>', '<', '+', '-', '.', ',', '[', ']', ';', '#', '!'}
    return ''.join([char for char in code if char in valid_commands])
 
def tokenize(parsed_code):
    return list(parsed_code)

def compile_to_c(tokens):
    c_program = []
    indent_level = 1  
    
    def indent():
        return "    " * indent_level
    
   
    c_program.append("#include <stdio.h>")
    c_program.append("int main() {")
    c_program.append("    unsigned char memory[30000] = {0};")
    c_program.append("    int used = 0;")
    c_program.append("    unsigned char *pointer = memory;")
 
   
    for token in tokens:
        if token == '>':
            c_program.append(indent() + f"pointer++;/* OP {token_map[token]}*/")
            c_program.append(indent() + "used++;")
        elif token == '<':
            c_program.append(indent() + f"pointer--;/* OP {token_map[token]}*/")
        elif token == '+':
            c_program.append(indent() + f"(*pointer)++;/* OP {token_map[token]}*/")
        elif token == '-':
            c_program.append(indent() + f"(*pointer)--;/* OP {token_map[token]}*/")
        elif token == '.':
            c_program.append(indent() +f"putchar(*pointer);/* OP {token_map[token]}*/")
        elif token == ';':
            c_program.append(indent() +f'printf("%d", *pointer);/* OP {token_map[token]}*/')
        elif token == ',':
            c_program.append(indent() + f"*pointer = getchar();/* OP {token_map[token]}*/")
        elif token == '[':
            c_program.append(indent() + "/* OP JZ*/while (*pointer) {")
            indent_level += 1
        elif token == ']':
            indent_level -= 1
            c_program.append(indent() + "}/* OP JNZ*/")
        elif token == '#' and '--debug' in sys.argv:
            c_program.append(indent() + "printf(\"[\");")
            c_program.append(indent() + "for(int i = 0; i < used; i++) {")
            c_program.append(indent() + "    printf(\"%u, \", memory[i]);")
            c_program.append(indent() + "}")
            c_program.append(indent() + "printf(\"%u]\", memory[used]);")
        elif token == '!' and '--debug' in sys.argv:
            c_program.append(indent() + "printf(\"%u\", pointer - memory);")
    
   
    c_program.append("    return 0;")
    c_program.append("}")
    
    return "\n".join(c_program)
 
 
def brainfuck_to_c(code):
    parsed_code = parse(code)
    tokens = tokenize(parsed_code)
    return compile_to_c(tokens)

with open(sys.argv[1],'r') as f: brainfuck_code = f.read()    
c_output = brainfuck_to_c(brainfuck_code)
with open(os.path.basename(os.path.splitext(sys.argv[1])[0]) + '.c',"w") as f:
    f.write(c_output)