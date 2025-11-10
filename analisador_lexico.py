class Token:
    # Representa um token com tipo, lexema, linha e coluna
    def __init__(self, tipo, lexema, linha, coluna):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

    #to string do java só q do python
    def __repr__(self):
        return f"[{self.tipo}: '{self.lexema}' @ {self.linha},{self.coluna}]"
class Lexico:
    def __init__(self):
        # Palavras reservadas da linguagem, só com as chaves pra eu verificar se é reservada
        self.reservadas = {
            'se', 'senao', 'para', 'faca', 'enquanto', 'escreva', 'leia',
            'inteiro', 'flutuante', 'logico', 'cadeia', 'inicio', 'fim',
            'fun', 'var', 'if', 'else', 'while', 'for', 'write', 'read'
        }
        
        # Operadores e símbolos com as chaves já inclusass
        self.operadores = {
            '+': 'mais', '-': 'menos', '*': 'mult', '/': 'div',
            '(': 'ap', ')': 'fp', '{': 'ab', '}': 'fb',
            ',': 'v', ';': 'pv', '=': 'igual',
            '>': 'maior', '<': 'menor', '>=': 'ge', '<=': 'le',
            '==': 'eqeq', '!=': 'ne', '!': 'neg'
        }
    
    #aqui to inicializando as varáveis de estado
        
        self.codigo = "" # guardando código inteiro
        self.pos = 0 # guardando minha posição atual
        self.linha = 1 
        self.coluna = 1

    def definir_entrada(self, codigo):
        # Define o código fonte a ser analisado
        self.codigo = codigo
        self.pos = 0
        self.linha = 1
        self.coluna = 1

    def proximo_token(self):
        # Retorna o próximo token do código
        while self.pos < len(self.codigo): #enquanto posição for menor q o tamanho continua
            c = self.codigo[self.pos]

            # Ignora espaços e tabulações
            if c in ' \t\r':
                self.coluna += 1
                self.pos += 1
                continue
                
            # Trata quebra de linha
            if c == '\n':
                self.linha += 1 #adiciona nova linha
                self.coluna = 1 # volta pra coluna 1 pra fazer o procesos de novo
                self.pos += 1
                continue

            # Verifica operadores de 2 caracteres
            if self.pos + 1 < len(self.codigo):
                dois = self.codigo[self.pos:self.pos+2]
                if dois in self.operadores:
                    token = Token(self.operadores[dois], dois, self.linha, self.coluna)
                    self.pos += 2
                    self.coluna += 2
                    return token
                
                #aqui em cima eu to verificando se é >= por exemplo não apenas > ou =
                #se forem operadores registrados la no dicionario de operadores, crio token e pulo 2 ali

            # Verifica operadores de 1 caractere
            if c in self.operadores:
                token = Token(self.operadores[c], c, self.linha, self.coluna)
                self.pos += 1
                self.coluna += 1
                return token

            # Reconhece números
            if c.isdigit():
                inicio = self.pos
                while self.pos < len(self.codigo) and (self.codigo[self.pos].isdigit() or self.codigo[self.pos] == '.'):
                    self.pos += 1
                num = self.codigo[inicio:self.pos]
                self.coluna += len(num)
                return Token('num', num, self.linha, self.coluna - len(num))
            
            #se começa com digitos, pega todos até parar, tipo pega todos os numeros independente da quantidade até vir espaço ou outro caracte

            # Reconhece identificadores e palavras reservadas
            if c.isalpha() or c == '_':
                inicio = self.pos
                while self.pos < len(self.codigo) and (self.codigo[self.pos].isalnum() or self.codigo[self.pos] == '_'):
                    self.pos += 1
                palavra = self.codigo[inicio:self.pos]
                #nesse loop aqui em cima ó, ele vai pegar a primeira posição e percorrer até achar algo diferente de string
                #se comea com letra junta até parar
                #se tiver lá no dicionário como palavra reservada vira var
                #se não tiver vira id identificador
                
                # Verifica se é palavra reservada
                if palavra in self.reservadas:
                    tipo = palavra
                else:
                    tipo = 'id'
                    
                self.coluna += len(palavra)
                return Token(tipo, palavra, self.linha, self.coluna - len(palavra))

            # Caractere inválido
            raise Exception(f"Caractere inválido: '{c}' na linha {self.linha}, coluna {self.coluna}")

        # Fim do arquivo
        return Token('$', '', self.linha, self.coluna)
