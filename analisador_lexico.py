class Token:
    def __init__(self, tipo, lexema, linha, coluna):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

    def __repr__(self):
        return self.tipo + " | " + self.lexema + " | L:" + str(self.linha) + " C:" + str(self.coluna)


class AFDPalavrasReservadas:
    # AFD pra reconhecer palavras reservadas da linguagem
    # Usa uma tabela hash com as palavras e seus tipos correspondentes
    def __init__(self):
        # Mapeamento das palavras reservadas pro tipo delas
        self.estados_finais = {
            'var': 'var',
            'fun': 'fun',
            'inteiro': 'inteiro',
            'flutuante': 'flutuante',
            'cadeia': 'cadeia',
            'logico': 'lógico',
            'if': 'if',
            'else': 'else',
            'for': 'for',
            'while': 'while',
            'write': 'write',
            'read': 'read',
            'verdadeiro': 'verdadeiro',
            'falso': 'falso',
            'inicio': 'inicio',
            'fim': 'fim'
        }
    
    def reconhecer(self, palavra):
        # Verifica se a palavra tá na tabela de reservadas
        # Se não tiver, é um identificador comum (id)
        if palavra in self.estados_finais:
            return self.estados_finais[palavra]
        return 'id'


class AFDOperadores:
    # AFD pra reconhecer operadores da linguagem
    # Trata operadores de 1 e 2 caracteres
    def __init__(self):
        # Operadores compostos (2 caracteres) - tem prioridade no reconhecimento
        self.op_2char = {
            '>=': 'ge',
            '<=': 'le',
            '==': 'eqeq',
            '!=': 'ne',
            '++': 'inc',
            '--': 'dec',
            '&&': 'e_logico'
        }
        
        # Operadores simples (1 caractere)
        self.op_1char = {
            '+': 'mais',
            '-': 'menos',
            '*': 'mult',
            '/': 'div',
            '(': 'ap',
            ')': 'fp',
            '{': 'ab',
            '}': 'fb',
            ',': 'v',
            ';': 'pv',
            '=': 'igual',
            '>': 'maior',
            '<': 'menor',
            '&': 'concat',
            ':': 'dois_pontos'
        }
    
    def reconhecer(self, c1, c2=None):
        # Estratégia greedy: tenta casar 2 chars primeiro, depois 1
        # Retorna uma tupla (tipo_token, tamanho_consumido)
        
        # Primeiro tenta operador de 2 caracteres
        if c2 is not None:
            dois = c1 + c2
            if dois in self.op_2char:
                return (self.op_2char[dois], 2)
        
        # Se não der, tenta operador de 1 caractere
        if c1 in self.op_1char:
            return (self.op_1char[c1], 1)
        
        # Operador desconhecido
        return ('desconhecido', 1)


class Lexico:
    def __init__(self):
        self.codigo = ""
        self.pos = 0
        self.linha = 1
        self.coluna = 1
        
        # Instancia os AFDs que vão fazer o reconhecimento
        self.afd_palavras = AFDPalavrasReservadas()
        self.afd_ops = AFDOperadores()

    def definir_entrada(self, codigo):
        self.codigo = codigo
        self.pos = 0
        self.linha = 1
        self.coluna = 1

    def char_atual(self):
        # Pega o caractere na posição atual, ou None se chegou no fim
        if self.pos < len(self.codigo):
            return self.codigo[self.pos]
        return None
    
    def proximo_char(self):
        # Olha o próximo caractere sem avançar a posição
        if self.pos + 1 < len(self.codigo):
            return self.codigo[self.pos + 1]
        return None
    
    def avancar(self):
        # Move pro próximo caractere e atualiza linha/coluna
        c = self.char_atual()
        if c is not None:
            self.pos += 1
            if c == '\n':
                self.linha += 1
                self.coluna = 1
            else:
                self.coluna += 1

    def proximo_token(self):
        # Ignora espaços em branco
        while self.char_atual() is not None and self.char_atual() in ' \t\r\n':
            self.avancar()
        
        c = self.char_atual()
        if c is None:
            return Token('$', '$', self.linha, self.coluna)
        
        lin = self.linha
        col = self.coluna

        # Comentário de linha (//)
        if c == '/' and self.proximo_char() == '/':
            while self.char_atual() is not None and self.char_atual() != '\n':
                self.avancar()
            return self.proximo_token()

        # String literal entre aspas
        if c == '"':
            return self.ler_string(lin, col)

        # Literal numérico
        if self.eh_digito(c):
            return self.ler_numero(lin, col)

        # Identificador ou palavra reservada
        if self.eh_letra(c) or c == '_':
            return self.ler_identificador(lin, col)

        # Operador
        if c in '+-*/(){},;=!><&:':
            return self.ler_operador(lin, col)

        # Caractere inválido
        raise Exception("Char invalido: '" + c + "' em L" + str(self.linha) + " C" + str(self.coluna))

    def eh_digito(self, c):
        if c is None:
            return False
        return '0' <= c <= '9'
    
    def eh_letra(self, c):
        if c is None:
            return False
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z')
    
    def eh_alfanum(self, c):
        return self.eh_letra(c) or self.eh_digito(c) or c == '_'

    def ler_string(self, lin, col):
        # Lê uma string literal do código
        # Trata caracteres de escape também
        lex = ""
        lex += self.char_atual()  # aspas de abertura
        self.avancar()

        while self.char_atual() is not None:
            c = self.char_atual()

            # Caractere de escape (barra invertida)
            if c == '\\':
                lex += c
                self.avancar()
                if self.char_atual() is not None:
                    lex += self.char_atual()
                    self.avancar()
                continue

            # Fecha a string
            if c == '"':
                lex += c
                self.avancar()
                return Token('CADEIA', lex, lin, col)

            lex += c
            self.avancar()

        raise Exception("String nao fechada em L" + str(lin) + " C" + str(col))

    def ler_numero(self, lin, col):
        # Lê um número (inteiro ou ponto flutuante)
        lex = ""
        
        # Parte inteira
        while self.char_atual() is not None and self.eh_digito(self.char_atual()):
            lex += self.char_atual()
            self.avancar()
        
        # Parte decimal (se existir)
        if self.char_atual() == '.':
            lex += self.char_atual()
            self.avancar()
            while self.char_atual() is not None and self.eh_digito(self.char_atual()):
                lex += self.char_atual()
                self.avancar()
        
        return Token('num', lex, lin, col)

    def ler_identificador(self, lin, col):
        # Lê um identificador ou palavra reservada
        lex = ""
        
        # Primeiro caractere (letra ou underscore)
        lex += self.char_atual()
        self.avancar()
        
        # Resto do identificador (letras, dígitos ou underscore)
        while self.char_atual() is not None and self.eh_alfanum(self.char_atual()):
            lex += self.char_atual()
            self.avancar()
        
        # Consulta o AFD pra saber se e palavra reservada ou ID comum
        tipo = self.afd_palavras.reconhecer(lex)
        return Token(tipo, lex, lin, col)

    def ler_operador(self, lin, col):
        # Lê um operador usando estratégia greedy (tomando sempre a melhor decisão local disponível no momento)
        c1 = self.char_atual()
        c2 = self.proximo_char()
        
        # AFD retorna o tipo e quantos caracteres consumir
        tipo, tam = self.afd_ops.reconhecer(c1, c2)
        
        lex = c1
        self.avancar()
        
        if tam == 2 and c2 is not None:
            lex += c2
            self.avancar()
        
        return Token(tipo, lex, lin, col)

    def analisar(self, codigo):
        self.definir_entrada(codigo)
        tokens = []
        erros = []

        while True:
            try:
                tk = self.proximo_token()
                if tk.tipo == '$':
                    break
                tokens.append(tk)
            except Exception as e:
                erros.append(str(e))
                self.avancar()

        return tokens, erros
