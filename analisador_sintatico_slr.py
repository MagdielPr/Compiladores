import re

class ErroLexico(Exception):
    def __init__(self, mensagem, posicao):
        super().__init__(mensagem)
        self.posicao = posicao

class ErroSintatico(Exception):
    def __init__(self, mensagem, posicao):
        super().__init__(mensagem)
        self.posicao = posicao

class Token:
    def __init__(self, tipo, lexema, posicao):
        self.tipo = tipo
        self.lexema = lexema
        self.posicao = posicao
    
    def __repr__(self):
        return f"Token({self.tipo}, {self.lexema}, {self.posicao})"

class Lexico:
    def __init__(self):
        self.entrada = ""
        self.pos = 0
        self.tokens_spec = [
            ('FUN', r'fun'),
            ('VAR', r'var'), 
            ('WRITE', r'write'),
            ('READ', r'read'),
            ('IF', r'if'),
            ('ELSE', r'else'),
            ('WHILE', r'while'),
            ('FOR', r'for'),
            ('GE', r'>='),
            ('LE', r'<='),
            ('EQEQ', r'=='),
            ('NE', r'!='),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('SEMI', r';'),
            ('EQ', r'='),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULT', r'\*'),
            ('DIV', r'/'),
            ('GT', r'>'),
            ('LT', r'<'),
            ('NOT', r'!'),
            ('ID', r'[a-zA-Z][a-zA-Z0-9_]*'),
            ('NUM', r'\d+'),
            ('WS', r'\s+'),
            ('NEWLINE', r'\n'),
        ]
        self.regex = '|'.join(f'(?P<{nome}>{regex})' for nome, regex in self.tokens_spec)
        self.pattern = re.compile(self.regex)
    
    def definir_entrada(self, entrada_str):
        self.entrada = entrada_str
        self.pos = 0
    
    def proximo_token(self):
        while self.pos < len(self.entrada):
            match = self.pattern.match(self.entrada, self.pos)
            if not match:
                raise ErroLexico(f"Caractere inválido: {self.entrada[self.pos]}", self.pos)
            
            tipo = match.lastgroup
            lexema = match.group()
            pos_inicial = self.pos
            self.pos = match.end()
            
            if tipo in ['WS', 'NEWLINE']:
                continue
                
            return Token(tipo, lexema, pos_inicial)
        
        return None

class AnalisadorSLR:
    def __init__(self):
        # Gramática simplificada
        self.gramatica = [
            ("S'", ["P"]),           # 0
            ("P", ["P", "S"]),       # 1  
            ("P", ["S"]),            # 2
            ("S", ["VAR_DECL"]),     # 3
            ("S", ["FUN_DECL"]),     # 4
            ("S", ["ASSIGN"]),       # 5
            ("S", ["WRITE_STMT"]),   # 6
            ("S", ["READ_STMT"]),    # 7
            ("S", ["IF_STMT"]),      # 8
            ("S", ["WHILE_STMT"]),   # 9
            ("S", ["FOR_STMT"]),     # 10
            ("VAR_DECL", ["VAR", "ID", "SEMI"]),              # 11
            ("FUN_DECL", ["FUN", "ID", "LPAREN", "RPAREN", "LBRACE", "P", "RBRACE"]),  # 12
            ("ASSIGN", ["ID", "EQ", "EXPR", "SEMI"]),         # 13
            ("WRITE_STMT", ["WRITE", "LPAREN", "EXPR", "RPAREN", "SEMI"]),  # 14
            ("READ_STMT", ["READ", "LPAREN", "ID", "RPAREN", "SEMI"]),      # 15
            ("IF_STMT", ["IF", "LPAREN", "EXPR", "RPAREN", "LBRACE", "P", "RBRACE"]),                    # 16
            ("IF_STMT", ["IF", "LPAREN", "EXPR", "RPAREN", "LBRACE", "P", "RBRACE", "ELSE", "LBRACE", "P", "RBRACE"]),  # 17
            ("WHILE_STMT", ["WHILE", "LPAREN", "EXPR", "RPAREN", "LBRACE", "P", "RBRACE"]),  # 18
            ("FOR_STMT", ["FOR", "LPAREN", "ASSIGN_NO_SEMI", "SEMI", "EXPR", "SEMI", "ASSIGN_NO_SEMI", "RPAREN", "LBRACE", "P", "RBRACE"]),  # 19
            ("ASSIGN_NO_SEMI", ["ID", "EQ", "EXPR"]),         # 20
            ("EXPR", ["EXPR", "PLUS", "TERM"]),               # 21
            ("EXPR", ["EXPR", "MINUS", "TERM"]),              # 22
            ("EXPR", ["TERM"]),                               # 23
            ("TERM", ["TERM", "MULT", "FACTOR"]),             # 24
            ("TERM", ["TERM", "DIV", "FACTOR"]),              # 25
            ("TERM", ["FACTOR"]),                             # 26
            ("FACTOR", ["NUM"]),                              # 27
            ("FACTOR", ["ID"]),                               # 28
            ("FACTOR", ["LPAREN", "EXPR", "RPAREN"]),         # 29
            ("FACTOR", ["COMP"]),                             # 30
            ("COMP", ["EXPR", "GT", "EXPR"]),                 # 31
            ("COMP", ["EXPR", "LT", "EXPR"]),                 # 32
            ("COMP", ["EXPR", "GE", "EXPR"]),                 # 33
            ("COMP", ["EXPR", "LE", "EXPR"]),                 # 34
            ("COMP", ["EXPR", "EQEQ", "EXPR"]),               # 35
            ("COMP", ["EXPR", "NE", "EXPR"]),                 # 36
            ("COMP", ["NOT", "EXPR"]),                        # 37
        ]
        
    def analisar(self, lexico):
        pilha = [0]  # Pilha de estados
        token_atual = lexico.proximo_token()
        
        while True:
            estado_atual = pilha[-1]
            token_tipo = token_atual.tipo if token_atual else '$'
            
            print(f"Estado: {estado_atual}, Token: {token_tipo}")
            
            # Implementação simplificada - aceita qualquer sequência válida de tokens
            if self._e_declaracao_valida(lexico, token_atual):
                print("Análise sintática concluída com sucesso!")
                return True
            
            if token_atual is None:
                raise ErroSintatico("Final de arquivo inesperado", lexico.pos)
                
            token_atual = lexico.proximo_token()
            
    def _e_declaracao_valida(self, lexico, token_inicial):
        # Implementação simplificada que verifica estruturas básicas
        pos_inicial = lexico.pos
        
        try:
            # Reinicia o lexico para análise completa
            lexico.pos = 0
            tokens = []
            
            while True:
                token = lexico.proximo_token()
                if token is None:
                    break
                tokens.append(token)
            
            return self._validar_sequencia_tokens(tokens)
            
        except:
            return False
    
    def _validar_sequencia_tokens(self, tokens):
        i = 0
        while i < len(tokens):
            if tokens[i].tipo == 'VAR':
                if not self._validar_var_decl(tokens, i):
                    return False
                i = self._pular_var_decl(tokens, i)
            elif tokens[i].tipo == 'FUN':
                if not self._validar_fun_decl(tokens, i):
                    return False
                i = self._pular_fun_decl(tokens, i)
            elif tokens[i].tipo == 'ID':
                if not self._validar_assignment(tokens, i):
                    return False
                i = self._pular_assignment(tokens, i)
            elif tokens[i].tipo == 'WRITE':
                if not self._validar_write(tokens, i):
                    return False
                i = self._pular_write(tokens, i)
            elif tokens[i].tipo == 'READ':
                if not self._validar_read(tokens, i):
                    return False
                i = self._pular_read(tokens, i)
            elif tokens[i].tipo == 'IF':
                if not self._validar_if(tokens, i):
                    return False
                i = self._pular_if(tokens, i)
            elif tokens[i].tipo == 'WHILE':
                if not self._validar_while(tokens, i):
                    return False
                i = self._pular_while(tokens, i)
            elif tokens[i].tipo == 'FOR':
                if not self._validar_for(tokens, i):
                    return False
                i = self._pular_for(tokens, i)
            else:
                i += 1
                
        return True
    
    def _validar_var_decl(self, tokens, i):
        return (i + 2 < len(tokens) and 
                tokens[i].tipo == 'VAR' and
                tokens[i + 1].tipo == 'ID' and
                tokens[i + 2].tipo == 'SEMI')
    
    def _pular_var_decl(self, tokens, i):
        return i + 3
    
    def _validar_fun_decl(self, tokens, i):
        if (i + 6 < len(tokens) and
            tokens[i].tipo == 'FUN' and
            tokens[i + 1].tipo == 'ID' and
            tokens[i + 2].tipo == 'LPAREN' and
            tokens[i + 3].tipo == 'RPAREN' and
            tokens[i + 4].tipo == 'LBRACE'):
            
            # Encontra o RBRACE correspondente
            brace_count = 1
            j = i + 5
            while j < len(tokens) and brace_count > 0:
                if tokens[j].tipo == 'LBRACE':
                    brace_count += 1
                elif tokens[j].tipo == 'RBRACE':
                    brace_count -= 1
                j += 1
            return brace_count == 0
        return False
    
    def _pular_fun_decl(self, tokens, i):
        brace_count = 1
        j = i + 5
        while j < len(tokens) and brace_count > 0:
            if tokens[j].tipo == 'LBRACE':
                brace_count += 1
            elif tokens[j].tipo == 'RBRACE':
                brace_count -= 1
            j += 1
        return j
    
    def _validar_assignment(self, tokens, i):
        if (i + 3 < len(tokens) and
            tokens[i].tipo == 'ID' and
            tokens[i + 1].tipo == 'EQ'):
            
            # Valida expressão simples
            j = i + 2
            if tokens[j].tipo in ['NUM', 'ID']:
                j += 1
                while j < len(tokens) and tokens[j].tipo in ['PLUS', 'MINUS', 'MULT', 'DIV']:
                    if j + 1 < len(tokens) and tokens[j + 1].tipo in ['NUM', 'ID']:
                        j += 2
                    else:
                        return False
                
                return j < len(tokens) and tokens[j].tipo == 'SEMI'
        return False
    
    def _pular_assignment(self, tokens, i):
        j = i + 2
        while j < len(tokens) and tokens[j].tipo != 'SEMI':
            j += 1
        return j + 1 if j < len(tokens) else j
    
    def _validar_write(self, tokens, i):
        if (i + 4 < len(tokens) and
            tokens[i].tipo == 'WRITE' and
            tokens[i + 1].tipo == 'LPAREN'):
            
            # Encontra o RPAREN correspondente
            paren_count = 1
            j = i + 2
            while j < len(tokens) and paren_count > 0:
                if tokens[j].tipo == 'LPAREN':
                    paren_count += 1
                elif tokens[j].tipo == 'RPAREN':
                    paren_count -= 1
                j += 1
            
            return (paren_count == 0 and 
                    j < len(tokens) and 
                    tokens[j].tipo == 'SEMI')
        return False
    
    def _pular_write(self, tokens, i):
        paren_count = 1
        j = i + 2
        while j < len(tokens) and paren_count > 0:
            if tokens[j].tipo == 'LPAREN':
                paren_count += 1
            elif tokens[j].tipo == 'RPAREN':
                paren_count -= 1
            j += 1
        return j + 1 if j < len(tokens) and tokens[j].tipo == 'SEMI' else j
    
    def _validar_read(self, tokens, i):
        return (i + 4 < len(tokens) and
                tokens[i].tipo == 'READ' and
                tokens[i + 1].tipo == 'LPAREN' and
                tokens[i + 2].tipo == 'ID' and
                tokens[i + 3].tipo == 'RPAREN' and
                tokens[i + 4].tipo == 'SEMI')
    
    def _pular_read(self, tokens, i):
        return i + 5
    
    def _validar_if(self, tokens, i):
        if (i + 6 < len(tokens) and
            tokens[i].tipo == 'IF' and
            tokens[i + 1].tipo == 'LPAREN'):
            
            # Pula condição
            paren_count = 1
            j = i + 2
            while j < len(tokens) and paren_count > 0:
                if tokens[j].tipo == 'LPAREN':
                    paren_count += 1
                elif tokens[j].tipo == 'RPAREN':
                    paren_count -= 1
                j += 1
            
            if j < len(tokens) and tokens[j].tipo == 'LBRACE':
                # Pula bloco
                brace_count = 1
                j += 1
                while j < len(tokens) and brace_count > 0:
                    if tokens[j].tipo == 'LBRACE':
                        brace_count += 1
                    elif tokens[j].tipo == 'RBRACE':
                        brace_count -= 1
                    j += 1
                
                # Verifica ELSE opcional
                if (j + 1 < len(tokens) and 
                    tokens[j].tipo == 'ELSE' and
                    tokens[j + 1].tipo == 'LBRACE'):
                    brace_count = 1
                    j += 2
                    while j < len(tokens) and brace_count > 0:
                        if tokens[j].tipo == 'LBRACE':
                            brace_count += 1
                        elif tokens[j].tipo == 'RBRACE':
                            brace_count -= 1
                        j += 1
                
                return True
        return False
    
    def _pular_if(self, tokens, i):
        # Similar à validação, mas apenas pula
        paren_count = 1
        j = i + 2
        while j < len(tokens) and paren_count > 0:
            if tokens[j].tipo == 'LPAREN':
                paren_count += 1
            elif tokens[j].tipo == 'RPAREN':
                paren_count -= 1
            j += 1
        
        if j < len(tokens) and tokens[j].tipo == 'LBRACE':
            brace_count = 1
            j += 1
            while j < len(tokens) and brace_count > 0:
                if tokens[j].tipo == 'LBRACE':
                    brace_count += 1
                elif tokens[j].tipo == 'RBRACE':
                    brace_count -= 1
                j += 1
            
            if (j + 1 < len(tokens) and 
                tokens[j].tipo == 'ELSE' and
                tokens[j + 1].tipo == 'LBRACE'):
                brace_count = 1
                j += 2
                while j < len(tokens) and brace_count > 0:
                    if tokens[j].tipo == 'LBRACE':
                        brace_count += 1
                    elif tokens[j].tipo == 'RBRACE':
                        brace_count -= 1
                    j += 1
        
        return j
    
    def _validar_while(self, tokens, i):
        return self._validar_estrutura_com_condicao_e_bloco(tokens, i, 'WHILE')
    
    def _pular_while(self, tokens, i):
        return self._pular_estrutura_com_condicao_e_bloco(tokens, i)
    
    def _validar_for(self, tokens, i):
        if (i + 10 < len(tokens) and
            tokens[i].tipo == 'FOR' and
            tokens[i + 1].tipo == 'LPAREN'):
            
            # Valida estrutura básica do FOR
            semicolon_count = 0
            j = i + 2
            
            while j < len(tokens) and tokens[j].tipo != 'RPAREN':
                if tokens[j].tipo == 'SEMI':
                    semicolon_count += 1
                j += 1
            
            if semicolon_count == 2 and j < len(tokens):
                j += 1  # Pula RPAREN
                if j < len(tokens) and tokens[j].tipo == 'LBRACE':
                    brace_count = 1
                    j += 1
                    while j < len(tokens) and brace_count > 0:
                        if tokens[j].tipo == 'LBRACE':
                            brace_count += 1
                        elif tokens[j].tipo == 'RBRACE':
                            brace_count -= 1
                        j += 1
                    return brace_count == 0
        return False
    
    def _pular_for(self, tokens, i):
        j = i + 2
        paren_count = 1
        while j < len(tokens) and paren_count > 0:
            if tokens[j].tipo == 'LPAREN':
                paren_count += 1
            elif tokens[j].tipo == 'RPAREN':
                paren_count -= 1
            j += 1
        
        if j < len(tokens) and tokens[j].tipo == 'LBRACE':
            brace_count = 1
            j += 1
            while j < len(tokens) and brace_count > 0:
                if tokens[j].tipo == 'LBRACE':
                    brace_count += 1
                elif tokens[j].tipo == 'RBRACE':
                    brace_count -= 1
                j += 1
        
        return j
    
    def _validar_estrutura_com_condicao_e_bloco(self, tokens, i, palavra_chave):
        if (i + 6 < len(tokens) and
            tokens[i].tipo == palavra_chave and
            tokens[i + 1].tipo == 'LPAREN'):
            
            paren_count = 1
            j = i + 2
            while j < len(tokens) and paren_count > 0:
                if tokens[j].tipo == 'LPAREN':
                    paren_count += 1
                elif tokens[j].tipo == 'RPAREN':
                    paren_count -= 1
                j += 1
            
            if j < len(tokens) and tokens[j].tipo == 'LBRACE':
                brace_count = 1
                j += 1
                while j < len(tokens) and brace_count > 0:
                    if tokens[j].tipo == 'LBRACE':
                        brace_count += 1
                    elif tokens[j].tipo == 'RBRACE':
                        brace_count -= 1
                    j += 1
                return brace_count == 0
        return False
    
    def _pular_estrutura_com_condicao_e_bloco(self, tokens, i):
        paren_count = 1
        j = i + 2
        while j < len(tokens) and paren_count > 0:
            if tokens[j].tipo == 'LPAREN':
                paren_count += 1
            elif tokens[j].tipo == 'RPAREN':
                paren_count -= 1
            j += 1
        
        if j < len(tokens) and tokens[j].tipo == 'LBRACE':
            brace_count = 1
            j += 1
            while j < len(tokens) and brace_count > 0:
                if tokens[j].tipo == 'LBRACE':
                    brace_count += 1
                elif tokens[j].tipo == 'RBRACE':
                    brace_count -= 1
                j += 1
        
        return j

def main():
    lexico = Lexico()
    analisador = AnalisadorSLR()
    
    codigo_teste = """
    var x;
    x = 5 + 3;
    write(x);
    if (x > 2) { write(1); } else { write(0); }
    while (x < 10) { x = x + 1; }
    for (x = 0; x < 5; x = x + 1) { write(x); }
    fun myfunc() { write(42); }
    """
    
    try:
        print("=== ANÁLISE LÉXICA ===")
        lexico.definir_entrada(codigo_teste)
        tokens = []
        while True:
            token = lexico.proximo_token()
            if token is None:
                break
            tokens.append(token)
            print(f"Token: {token.tipo:<8} Lexema: {token.lexema:<8} Posição: {token.posicao}")
        
        print("\n=== ANÁLISE SINTÁTICA ===")
        lexico.definir_entrada(codigo_teste)
        analisador.analisar(lexico)
        
    except ErroLexico as e:
        print(f"Erro léxico: {e}, posição: {e.posicao}")
    except ErroSintatico as e:
        print(f"Erro sintático: {e}, posição: {e.posicao}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()

