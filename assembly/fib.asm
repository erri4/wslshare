%include "./macros.asm"
global _start

section .text
fib: ; fib(rax) -> rbx
    mov rbx, 0
    mov r9, 1
    cmp rax, 0
    jg loop0_
    mov rbx, 0
    ret
    loop0_:
        dec rax
        mov rcx, r9
        add r9, rbx
        mov rbx, rcx
        push rax
        
        ; mod 1e9+7 for cses

        ;mov rax, r9
        ;xor rdx, rdx
        ;mov rcx, 1000000007
        ;div rcx
        ;mov r9, rdx

        pop rax
        cmp rax, 0
        jg loop0_
    ret

_start:
    call input
    call fib
    mov rax, rbx
    call print
    call exit