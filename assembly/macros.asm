default rel
section .data
    digit db 0

section .text
breakpoint:
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

input: ; input a number into rax
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
        mov rax, rbx
        pop rbx
        pop rdx
        pop rsi
        pop rdi
        ret