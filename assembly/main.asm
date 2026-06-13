default rel
global _start

section .data
    n dq 5

    question db "Use stored number? ", 0
    bad db "Please enter a number smaller than 21.", 10, 0

    digit db 0

section .text
breakpoint:
    ret

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

exit: ; exit with code 0
    mov rax, 60
    xor rdi, rdi
    syscall

print: ; print rax
    push rdi
    push rsi
    push rdx
    push r12
    push rax

    mov r12, 0
    mov rbx, 10
    loop1:
        mov rdx, 0 ; reminder

        div rbx
        push rdx
        inc r12
        cmp rax, 0
        jne loop1
    loop2:
        pop rax
        add al, '0'
        mov [digit], al
        mov rax, 1
        mov rdi, 1
        mov rsi, digit
        mov rdx, 1
        syscall
        dec r12
        cmp r12, 0
        jne loop2
    mov al, 10
    mov [digit], al
    mov rax, 1
    mov rdi, 1
    mov rsi, digit
    mov rdx, 1
    syscall

    pop rax
    pop r12
    pop rdx
    pop rsi
    pop rdi
    ret

printstr: ; print rsi
    push rcx
    push rdi
    push rdx
    push rbx
    mov rcx, 0
    mov rbx, rsi

    count_loop:
        cmp byte [rbx], 0
        je cont

        inc rbx
        inc rcx
        jmp count_loop
    cont:
        mov rdx, rcx
    mov rax, 1
    mov rdi, 1
    syscall
    
    pop rbx
    pop rdx
    pop rdi
    pop rcx
    ret

input_char: ; input 1 character into rax
    push rsi
    push rdi
    push rdx

    mov rax, 0
    mov rdi, 0
    mov rsi, digit
    mov rdx, 2
    syscall
    movzx rax, byte [digit]

    pop rdx
    pop rdi
    pop rsi
    ret

input: ; input a number into rbx
    push rdi
    push rsi
    push rdx
    push rbx

    mov rbx, 0
    mov rdx, 0
    loop0:
        mov rax, 0
        mov rdi, 0
        mov rsi, digit
        mov rdx, 1
        syscall ; input to digit
        cmp rax, 0
        jle dne

        mov dl, [digit]
        cmp dl, 10
        je dne
        cmp dl, 13
        je dne

        sub dl, '0'          
        imul rbx, 10
        add rbx, rdx

        jmp loop0
    dne:
        pop rbx
        pop rdx
        pop rsi
        pop rdi
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
        call breakpoint
        call fact
        call breakpoint
        call print
    call exit
    badinp:
        mov rsi, bad
        call printstr
    call exit