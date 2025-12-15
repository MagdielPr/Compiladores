.data

.text
.globl main
main:
    addi $sp, $sp, -24
    li $t0, 10
    sw $t0, 4($sp)
    li $t0, 3.14
    sw $t0, 8($sp)
    lw $t0, 4($sp)
    li $t1, 3
    sgt $t0, $t0, $t1
    beq $t0, $zero, ELSE_MAIOR_3
    li $v0, 1
    syscall
    j FIM_IF_MAIOR_3
ELSE_MAIOR_3:
    li $v0, 1
    syscall
FIM_IF_MAIOR_3:
    lw $t0, 4($sp)
    li $t1, 10
    beq $t0, $zero, ELSE_MAIOR_3
    li $v0, 1
    syscall
    j FIM_IF_MAIOR_3
ELSE_MAIOR_3:
FIM_IF_MAIOR_3:
    lw $t0, 8($sp)
    li $t1, 5.0
    beq $t0, $zero, ELSE_MAIOR_3
    li $v0, 1
    syscall
    j FIM_IF_MAIOR_3
ELSE_MAIOR_3:
FIM_IF_MAIOR_3:
    lw $t0, 4($sp)
    li $t1, 5
    beq $t0, $zero, ELSE_MAIOR_3
    li $v0, 1
    syscall
    j FIM_IF_MAIOR_3
ELSE_MAIOR_3:
FIM_IF_MAIOR_3:
INICIO_FOR:
    lw $t0, 24($sp)
    li $t1, 5
    slt $t0, $t0, $t1
    beq $t0, $zero, FIM_FOR
    j CORPO_FOR
INCREMENTO_FOR:
    j INICIO_FOR
CORPO_FOR:
    li $v0, 1
    syscall
    lw $a0, 24($sp)
    li $v0, 1
    syscall
    j INCREMENTO_FOR
FIM_FOR:
INICIO_WHILE:
    lw $t0, 16($sp)
    beq $t0, $zero, FIM_WHILE
    j INICIO_WHILE
FIM_WHILE:
    li $v0, 5
    syscall
    sw $v0, 4($sp)
    lw $t0, 4($sp)
    lw $t1, 8($sp)
    add $t0, $t0, $t1
    sw $t0, 20($sp)
    lw $t0, 4($sp)
    lw $t1, 8($sp)
    sub $t0, $t0, $t1
    sw $t0, 20($sp)
    lw $t0, 4($sp)
    li $t1, 2
    mul $t0, $t0, $t1
    sw $t0, 20($sp)
    lw $t0, 4($sp)
    li $t1, 2
    div $t0, $t1
    mflo $t0
    sw $t0, 20($sp)
    addi $sp, $sp, 24
    li $v0, 10
    syscall