import re

class ErroLexico(Exception):
    """Exceção para erros no analisador léxico"""
    pass

class Token:
    """Representa um token"""
    def __init__(self, tipo, lexema, posicao):
        self.tipo = tipo
        self.lexema = lexema
        self.pos = posicao
    
    def __repr__(self):
        return f"Token({self.tipo}, {self.lexema!r}, {self.pos})"

class Lexico:
    """Analisador léxico"""
    
    def __init__(self):
        padroes = [
            ('fun', r'\bfun\b'),
            ('var', r'\bvar\b'),
            ('write', r'\bwrite\b'),
            ('read', r'\bread\b'),
            ('if', r'\bif\b'),
            ('else', r'\belse\b'),
            ('while', r'\bwhile\b'),
            ('for', r'\bfor\b'),
            ('ge', r'>='),
            ('le', r'<='),
            ('eqeq', r'=='),
            ('ne', r'!='),
            ('ap', r'\('),
            ('fp', r'\)'),
            ('ab', r'\{'),
            ('fb', r'\}'),
            ('v', r','),
            ('pv', r';'),
            ('igual', r'='),
            ('mais', r'\+'),
            ('menos', r'-'),
            ('mult', r'\*'),
            ('div', r'/'),
            ('maior', r'>'),
            ('menor', r'<'),
            ('neg', r'!'),
            ('id', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('num', r'\d+'),
            ('ws', r'[ \t\r]+'),
            ('nl', r'\n'),
        ]
        
        regex = '|'.join(f'(?P<{n}>{r})' for n, r in padroes)
        self.padrao = re.compile(regex)
        self.entrada = ''
        self.pos = 0
        self.linha = 1

    def definir_entrada(self, codigo):
        self.entrada = codigo
        self.pos = 0
        self.linha = 1

    def proximo_token(self):
        while self.pos < len(self.entrada):
            m = self.padrao.match(self.entrada, self.pos)
            
            if not m:
                raise ErroLexico(f"Caractere inválido '{self.entrada[self.pos]}' na posição {self.pos}")
            
            tipo = m.lastgroup
            lex = m.group()
            inicio = self.pos
            self.pos = m.end()
            
            if tipo == 'ws':
                continue
            if tipo == 'nl':
                self.linha += 1
                continue
            
            return Token(tipo, lex, inicio)
        
        return Token('$', '', self.pos)

