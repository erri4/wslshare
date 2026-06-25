%include "./macros.asm"
global _start

section .text
_start:
    push -1
    loop0_:
        mov rax, 0
        mov rdi, 0
        mov rsi, digit
        mov rdx, 1
        syscall ; input to digit
        cmp rax, 0
        jle loop1_

        movzx rdx, byte [digit]
        cmp dl, 10
        je loop1_
        cmp dl, 13
        je loop1_

        push rdx
        jmp loop0_
    loop1_:
        pop rsi
        cmp rsi, -1
        je dne_
        mov [digit], sil
        mov rax, 1
        mov rdi, 1
        mov rsi, digit
        mov rdx, 1
        syscall

        jmp loop1_
    dne_:
        mov byte [digit], 10
        mov rax, 1
        mov rdi, 1
        mov rsi, digit
        mov rdx, 1
        syscall
        call exit