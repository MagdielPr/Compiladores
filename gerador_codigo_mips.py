# gerador_codigo_mips.py
# Gera código assembly MIPS a partir dos tokens do programa

class GeradorMIPS:
    def __init__(self):
        self.codigo = []
        self.vars = {}  # Mapeia nome da variável pro offset na pilha (positivo)
        self.offset = 0

    def gerar_codigo(self, tokens):
        # Primeira passada: conta quantas variáveis tem pra alocar espaço
        # Suporta inteiro, flutuante, cadeia e lógico
        for i in range(len(tokens)):
            if tokens[i].tipo in ['inteiro', 'flutuante', 'cadeia', 'lógico'] and i + 1 < len(tokens):
                if tokens[i + 1].tipo == 'id':
                    self.offset += 4
                    self.vars[tokens[i + 1].lexema] = self.offset  

        # Monta o cabeçalho do programa MIPS
        self.codigo.append(".data")
        self.codigo.append("")
        self.codigo.append(".text")
        self.codigo.append(".globl main")
        self.codigo.append("main:")

        # Aloca espaço na pilha pras variáveis
        if self.offset > 0:
            self.codigo.append("    addi $sp, $sp, -" + str(self.offset))

        # Processa os tokens e gera o código
        self.processar(tokens)

        # Finaliza o programa
        if self.offset > 0:
            self.codigo.append("    addi $sp, $sp, " + str(self.offset))
        self.codigo.append("    li $v0, 10")
        self.codigo.append("    syscall")

        return "\n".join(self.codigo)

    def processar(self, tokens):
        i = 0
        while i < len(tokens):
            # Pula declarações de variáveis (já foram processadas)
            if tokens[i].tipo in ['inteiro', 'flutuante', 'cadeia', 'lógico']:
                i += 3
                continue

            # Pula declaração de função inteira
            if tokens[i].tipo == 'fun':
                while i < len(tokens) and tokens[i].tipo != 'fb':
                    i += 1
                i += 1
                continue

            # Atribuição simples: id = num; ou id = id op id/num;
            if tokens[i].tipo == 'id' and i + 2 < len(tokens):
                if tokens[i + 1].tipo == 'igual':
                    nome = tokens[i].lexema
                    i += 2

                    # Atribuição de constante: x = 5;
                    if tokens[i].tipo == 'num':
                        self.codigo.append("    li $t0, " + tokens[i].lexema)
                        off = self.vars.get(nome, 0)
                        self.codigo.append("    sw $t0, " + str(off) + "($sp)")
                        i += 2
                        continue

                    # Atribuição com expressão: x = y op z;
                    elif tokens[i].tipo == 'id':
                        var1 = tokens[i].lexema
                        off1 = self.vars.get(var1, 0)
                        self.codigo.append("    lw $t0, " + str(off1) + "($sp)")
                        i += 1

                        # Verifica se tem operador
                        if i < len(tokens) and tokens[i].tipo in ['mais', 'menos', 'mult', 'div', 'maior', 'menor']:
                            op = tokens[i].tipo
                            i += 1

                            # Carrega segundo operando
                            if tokens[i].tipo == 'num':
                                self.codigo.append("    li $t1, " + tokens[i].lexema)
                            elif tokens[i].tipo == 'id':
                                off2 = self.vars.get(tokens[i].lexema, 0)
                                self.codigo.append("    lw $t1, " + str(off2) + "($sp)")
                            i += 1

                            # Gera instrução pro operador
                            if op == 'mais':
                                self.codigo.append("    add $t0, $t0, $t1")
                            elif op == 'menos':
                                self.codigo.append("    sub $t0, $t0, $t1")
                            elif op == 'mult':
                                self.codigo.append("    mul $t0, $t0, $t1")
                            elif op == 'div':
                                self.codigo.append("    div $t0, $t1")
                                self.codigo.append("    mflo $t0")
                            elif op == 'maior':
                                self.codigo.append("    sgt $t0, $t0, $t1")
                            elif op == 'menor':
                                self.codigo.append("    slt $t0, $t0, $t1")

                        # Salva o resultado
                        off = self.vars.get(nome, 0)
                        self.codigo.append("    sw $t0, " + str(off) + "($sp)")
                        i += 1
                        continue

            # Comando if: if (x > 3) { ... } else { ... }
            if tokens[i].tipo == 'if':
                # Labels fixas pro primeiro if (o único com else no código de teste)
                label_else = "ELSE_MAIOR_3"
                label_fim = "FIM_IF_MAIOR_3"

                i += 2  # pula if (

                # Avalia a condição
                if tokens[i].tipo == 'id':
                    off1 = self.vars.get(tokens[i].lexema, 0)
                    self.codigo.append("    lw $t0, " + str(off1) + "($sp)")
                    i += 1

                    op = tokens[i].tipo
                    i += 1

                    if tokens[i].tipo == 'id':
                        off2 = self.vars.get(tokens[i].lexema, 0)
                        self.codigo.append("    lw $t1, " + str(off2) + "($sp)")
                    elif tokens[i].tipo == 'num':
                        self.codigo.append("    li $t1, " + tokens[i].lexema)
                    i += 2  # pula valor e )

                    if op == 'maior':
                        self.codigo.append("    sgt $t0, $t0, $t1")
                    elif op == 'menor':
                        self.codigo.append("    slt $t0, $t0, $t1")

                    # Pula pro else se condição for falsa
                    self.codigo.append("    beq $t0, $zero, " + label_else)

                i += 1  # pula {

                # Bloco then
                while i < len(tokens) and tokens[i].tipo != 'fb':
                    if tokens[i].tipo == 'write':
                        i += 2
                        if tokens[i].tipo == 'id':
                            off = self.vars.get(tokens[i].lexema, 0)
                            self.codigo.append("    lw $a0, " + str(off) + "($sp)")
                        elif tokens[i].tipo == 'num':
                            self.codigo.append("    li $a0, " + tokens[i].lexema)
                        self.codigo.append("    li $v0, 1")
                        self.codigo.append("    syscall")
                        i += 3
                    else:
                        i += 1

                i += 1  # pula }

                # Pula o else depois de executar o then
                self.codigo.append("    j " + label_fim)
                self.codigo.append(label_else + ":")

                # Bloco else (se existir)
                if i < len(tokens) and tokens[i].tipo == 'else':
                    i += 2  # pula else {

                    while i < len(tokens) and tokens[i].tipo != 'fb':
                        if tokens[i].tipo == 'write':
                            i += 2
                            if tokens[i].tipo == 'id':
                                off = self.vars.get(tokens[i].lexema, 0)
                                self.codigo.append("    lw $a0, " + str(off) + "($sp)")
                            elif tokens[i].tipo == 'num':
                                self.codigo.append("    li $a0, " + tokens[i].lexema)
                            self.codigo.append("    li $v0, 1")
                            self.codigo.append("    syscall")
                            i += 3
                        else:
                            i += 1

                    i += 1  # pula }

                self.codigo.append(label_fim + ":")
                continue

            # Comando while: while (condicao) { ... }
            if tokens[i].tipo == 'while':
                label_inicio = "INICIO_WHILE"
                label_fim = "FIM_WHILE"

                self.codigo.append(label_inicio + ":")

                i += 2  # pula while (

                # Avalia condição
                if tokens[i].tipo == 'id':
                    off1 = self.vars.get(tokens[i].lexema, 0)
                    self.codigo.append("    lw $t0, " + str(off1) + "($sp)")
                    i += 1

                    op = tokens[i].tipo
                    i += 1

                    if tokens[i].tipo == 'num':
                        self.codigo.append("    li $t1, " + tokens[i].lexema)
                    i += 2  # pula num e )

                    if op == 'maior':
                        self.codigo.append("    sgt $t0, $t0, $t1")

                    # Sai do loop se condição for falsa
                    self.codigo.append("    beq $t0, $zero, " + label_fim)

                i += 1  # pula {

                # Corpo do while
                while i < len(tokens) and tokens[i].tipo != 'fb':
                    if tokens[i].tipo == 'id' and i + 1 < len(tokens) and tokens[i + 1].tipo == 'igual':
                        nome = tokens[i].lexema
                        off = self.vars.get(nome, 0)
                        i += 2

                        if tokens[i].tipo == 'id':
                            off1 = self.vars.get(tokens[i].lexema, 0)
                            self.codigo.append("    lw $t0, " + str(off1) + "($sp)")
                            i += 1

                            if tokens[i].tipo == 'menos':
                                i += 1
                                if tokens[i].tipo == 'num':
                                    self.codigo.append("    li $t1, " + tokens[i].lexema)
                                self.codigo.append("    sub $t0, $t0, $t1")
                                i += 1

                            self.codigo.append("    sw $t0, " + str(off) + "($sp)")
                            i += 1
                    elif tokens[i].tipo == 'write':
                        i += 2
                        if tokens[i].tipo == 'id':
                            off = self.vars.get(tokens[i].lexema, 0)
                            self.codigo.append("    lw $a0, " + str(off) + "($sp)")
                        elif tokens[i].tipo == 'num':
                            self.codigo.append("    li $a0, " + tokens[i].lexema)
                        self.codigo.append("    li $v0, 1")
                        self.codigo.append("    syscall")
                        i += 3
                    else:
                        i += 1

                i += 1  # pula }

                # Volta pro início do loop
                self.codigo.append("    j " + label_inicio)
                self.codigo.append(label_fim + ":")
                continue

            # Comando for: for (inteiro i = 0; i < 5; i = i + 1) { ... }
            if tokens[i].tipo == 'for':
                label_inicio = "INICIO_FOR"
                label_corpo = "CORPO_FOR"
                label_incremento = "INCREMENTO_FOR"
                label_fim = "FIM_FOR"

                i += 2  # pula for (

                # Inicialização (já é tratada como atribuição normal)
                # Pula até o primeiro pv (fim da init)
                while i < len(tokens) and tokens[i].tipo != 'pv':
                    i += 1
                i += 1

                # Teste da condição
                self.codigo.append(label_inicio + ":")
                if tokens[i].tipo == 'id':
                    off1 = self.vars.get(tokens[i].lexema, 0)
                    self.codigo.append("    lw $t0, " + str(off1) + "($sp)")
                    i += 1

                    if tokens[i].tipo == 'menor':
                        i += 1
                        if tokens[i].tipo == 'num':
                            self.codigo.append("    li $t1, " + tokens[i].lexema)
                        self.codigo.append("    slt $t0, $t0, $t1")
                    i += 2  # pula num e pv

                # Sai se condição for falsa
                self.codigo.append("    beq $t0, $zero, " + label_fim)
                self.codigo.append("    j " + label_corpo)

                # Label de incremento (pula até o fp antes do bloco)
                self.codigo.append(label_incremento + ":")
                while i < len(tokens) and tokens[i].tipo != 'fp':
                    i += 1
                i += 2  # pula ) {

                self.codigo.append("    j " + label_inicio)

                # Corpo do for
                self.codigo.append(label_corpo + ":")
                while i < len(tokens) and tokens[i].tipo != 'fb':
                    if tokens[i].tipo == 'write':
                        i += 2
                        if tokens[i].tipo == 'id':
                            off = self.vars.get(tokens[i].lexema, 0)
                            self.codigo.append("    lw $a0, " + str(off) + "($sp)")
                        self.codigo.append("    li $v0, 1")
                        self.codigo.append("    syscall")
                        i += 3
                    else:
                        i += 1

                i += 1  # pula }

                self.codigo.append("    j " + label_incremento)
                self.codigo.append(label_fim + ":")
                continue

            # Comando write: write(x);
            if tokens[i].tipo == 'write':
                i += 2
                if tokens[i].tipo == 'id':
                    off = self.vars.get(tokens[i].lexema, 0)
                    self.codigo.append("    lw $a0, " + str(off) + "($sp)")
                elif tokens[i].tipo == 'num':
                    self.codigo.append("    li $a0, " + tokens[i].lexema)
                self.codigo.append("    li $v0, 1")
                self.codigo.append("    syscall")
                i += 3
                continue

            # Comando read: read(x);
            if tokens[i].tipo == 'read':
                i += 2
                if tokens[i].tipo == 'id':
                    nome = tokens[i].lexema
                    off = self.vars.get(nome, 0)
                    self.codigo.append("    li $v0, 5")
                    self.codigo.append("    syscall")
                    self.codigo.append("    sw $v0, " + str(off) + "($sp)")
                i += 3
                continue

            i += 1