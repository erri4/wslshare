%include "macros.asm"
global _start

section .data
    n dq 5

    question db "Use stored number? ", 0
    bad db "Please enter a number smaller than 21.", 10, 0

section .text
fact: ; factorial of rdi -> rax
    cmp rdi, 0
    je base
    push rdi
    dec rdi
    call fact
    pop rdi
    imul rax, rdi
    ret
    base:
        mov rax, 1
        ret


_start:
    mov rsi, question
    call printstr
    call input_char
    cmp rax, "n"
    je inp
    mov rdi, [n]
    jmp run
    inp:
        call input
        cmp rbx, 21
        jge badinp
        mov rdi, rbx
    run:
        mov rdi, rax
        call fact
        call print
    call exit
    badinp:
        mov rsi, bad
        call printstr
    call exit