%include "./macros.asm"
global _start

section .text
fib: ; fib(rax) -> rbx
    push rax
    mov rbx, 0 ; rbx = 0
    mov r9, 1 ; r9 = 1
    cmp rax, 0 ; if (rax > 0)
    jg loop0_ ; goto loop0_
    mov rbx, 0 ; rbx = 0
    ret ; return
    loop0_:
        dec rax ; rax--
        mov rcx, r9 ; rcx = r9
        add r9, rbx ; r9 += rbx
        mov rbx, rcx ; rbx = rcx
        
        ; mod 1e9+7 for cses

        ;mov rax, r9
        ;xor rdx, rdx
        ;mov rcx, 1000000007
        ;div rcx
        ;mov r9, rdx

        cmp rax, 0 ; if (rax > 0)
        jg loop0_ ; goto loop0_
    pop rax
    ret ; return

_start:
    call input
    call fib
    mov rax, rbx
    call print
    call exit