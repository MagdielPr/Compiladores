from analisador_lexico import Token

class ParserDescendente:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.erros = []

    def atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token('$', '$', 0, 0)

    def avancar(self):
        self.pos += 1

    def esperar(self, tipo):
        if self.atual().tipo == tipo:
            self.avancar()
        else:
            self.erros.append(f"Erro sintático: Esperado '{tipo}', encontrado '{self.atual().tipo}' na linha {self.atual().linha}, coluna {self.atual().coluna}")

    def analisar(self):
        self.program()
        if self.erros:
            return self.erros
        return []

    def program(self):
        while self.atual().tipo != '$':
            self.stmt()

    def stmt(self):
        token = self.atual()
        if token.tipo == 'var':
            self.var_decl()
        elif token.tipo == 'fun':
            self.fun_decl()
        elif token.tipo == 'id':
            self.assign()
        elif token.tipo == 'escreva':
            self.escreva_stmt()
        elif token.tipo == 'leia':
            self.leia_stmt()
        elif token.tipo == 'se':
            self.if_stmt()
        else:
            # Token inesperado: adiciona erro e AVANÇA para evitar loop infinito
            self.erros.append(f"Erro sintático: Statement inesperado '{token.lexema}' na linha {token.linha}, coluna {token.coluna}")
            self.avancar() 
            
    def var_decl(self):
        self.esperar('var')
        self.esperar('id')
        self.esperar('pv')

    def fun_decl(self):
        self.esperar('fun')
        self.esperar('id')
        self.esperar('ap')
        if self.atual().tipo == 'id':
            self.params()
        self.esperar('fp')
        self.esperar('ab')
        while self.atual().tipo != 'fb':
            self.stmt()
        self.esperar('fb')

    def params(self):
        self.esperar('id')
        while self.atual().tipo == 'v':
            self.avancar()
            self.esperar('id')

    def assign(self):
        self.esperar('id')
        self.esperar('igual')
        self.expr()
        self.esperar('pv')

    def escreva_stmt(self):
        self.esperar('escreva')
        self.esperar('ap')
        self.expr()
        self.esperar('fp')
        self.esperar('pv')

    def leia_stmt(self):
        self.esperar('leia')
        self.esperar('ap')
        self.esperar('id')
        self.esperar('fp')
        self.esperar('pv')

    def if_stmt(self):
        self.esperar('se')
        self.esperar('ap')
        self.expr()
        self.esperar('fp')
        self.esperar('ab')
        while self.atual().tipo != 'fb':
            self.stmt()
        self.esperar('fb')
        if self.atual().tipo == 'senão':
            self.avancar()
            self.esperar('ab')
            while self.atual().tipo != 'fb':
                self.stmt()
            self.esperar('fb')

    def expr(self):
        self.term()
        while self.atual().tipo in ['mais', 'menos']:
            self.avancar()
            self.term()
        # Expressões lógicas
        if self.atual().tipo in ['maior', 'menor', 'ge', 'le', 'eqeq', 'ne']:
            self.avancar()
            self.term()

    def term(self):
        self.factor()
        while self.atual().tipo in ['mult', 'div']:
            self.avancar()
            self.factor()

    def factor(self):
        token = self.atual()
        if token.tipo == 'num' or token.tipo == 'id' or token.tipo == 'CADEIA':
            self.avancar()
        elif token.tipo == 'ap':
            self.avancar()
            self.expr()
            self.esperar('fp')
        else:
            self.erros.append(f"Erro sintático: Factor inesperado '{token.lexema}' na linha {token.linha}")

def analisar(tokens):
    parser = ParserDescendente(tokens)
    erros = parser.analisar()
    if erros:
        print("ERROS SINTÁTICOS NO DESCENDENTE RECURSIVO:")
        for erro in erros:
            print(f"  {erro}")
        return erros
    print("Análise sintática descendente recursiva bem-sucedida.")
    return []
