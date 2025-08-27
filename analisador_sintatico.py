
from typing import List, Optional
from analisador_lexico import Token, TipoToken

class AnalisadorSintatico:
    #Analisador sintático descendente recursivo para a gramática LL
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.erros = []  # Buffer de erros sintáticos
        self.max_recursion_depth = 100  # Limite de profundidade de recursão
    
    def current_token(self) -> Optional[Token]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def eat(self, expected_tipo: TipoToken, expected_lexema: Optional[str] = None) -> bool:
        if self.current_token():
            if self.current_token().tipo == expected_tipo and (expected_lexema is None or self.current_token().lexema == expected_lexema):
                self.pos += 1
                return True
            else:
                self.erros.append(f"Erro sintático na linha {self.current_token().linha}, coluna {self.current_token().coluna}: esperado {expected_tipo.value}" + (f" ('{expected_lexema}')" if expected_lexema else "") + f", encontrado {self.current_token().tipo.value} ('{self.current_token().lexema}')")
                return False
        else:
            self.erros.append("Erro sintático: fim inesperado do arquivo")
            return False
    
    def parse(self) -> bool:
        #Analisa o programa completo como uma sequência de comandos
        max_recovery_attempts = len(self.tokens)  # Limite de tentativas de recuperação
        attempts = 0
        
        while self.current_token() and attempts < max_recovery_attempts:
            print(f"DEBUG: Analisando token {self.pos}: {self.current_token()}")
            if self.comando():
                attempts = 0  # Resetar tentativas após sucesso
            else:
                attempts += 1
                if self.current_token():
                    # Pular até um ponto de sincronização
                    print(f"DEBUG: Falha em comando, pulando token {self.pos}: {self.current_token()}")
                    self.pos += 1  # Avança para evitar loop infinito
                    while self.current_token() and self.current_token().tipo not in [TipoToken.PONTO_VIRGULA, TipoToken.FIM_BLOCO, TipoToken.PALAVRA_RESERVADA]:
                        print(f"DEBUG: Pulando token {self.pos}: {self.current_token()} devido a erro")
                        self.pos += 1
                    if self.current_token() and self.current_token().tipo in [TipoToken.PONTO_VIRGULA, TipoToken.FIM_BLOCO]:
                        print(f"DEBUG: Consumindo ponto de sincronização {self.current_token()}")
                        self.pos += 1
                else:
                    break
            if self.current_token() and self.current_token().tipo == TipoToken.PALAVRA_RESERVADA and self.current_token().lexema == 'fim':
                self.eat(TipoToken.PALAVRA_RESERVADA, 'fim')
                break
        if attempts >= max_recovery_attempts:
            self.erros.append("Erro sintático: número máximo de tentativas de recuperação atingido")
        return len(self.erros) == 0
    
    def comando(self) -> bool:
        #COMANDO -> decl_var | decl_func | atribuicao | escreva | leia | if_comando | enquanto | para
        anterior = self.pos
        
        if self.decl_var():
            return True
        
        self.pos = anterior
        if self.decl_func():
            return True
        
        self.pos = anterior
        if self.atribuicao():
            return True
        
        self.pos = anterior
        if self.escreva():
            return True
        
        self.pos = anterior
        if self.leia():
            return True
        
        self.pos = anterior
        if self.if_comando():
            return True
        
        self.pos = anterior
        if self.enquanto():
            return True
        
        self.pos = anterior
        if self.para():
            return True
        
        print(f"DEBUG: Falha em comando, token {self.pos}: {self.current_token()}")
        return False
    
    def decl_var(self) -> bool:
        #DECL_VAR -> tipo [ '[' const_inteira ']' ] id [ '=' expressao ] ';'
        anterior = self.pos
        if self.tipo():
            if self.current_token() and self.current_token().tipo == TipoToken.COLCHETE_ABRE:
                self.eat(TipoToken.COLCHETE_ABRE)
                self.eat(TipoToken.CONSTANTE_INTEIRA)
                self.eat(TipoToken.COLCHETE_FECHA)
            if self.eat(TipoToken.IDENTIFICADOR):
                if self.current_token() and self.current_token().tipo == TipoToken.OP_ATRIBUICAO:
                    self.eat(TipoToken.OP_ATRIBUICAO)
                    self.expressao()
                return self.eat(TipoToken.PONTO_VIRGULA)
        self.pos = anterior
        return False
    
    def decl_func(self) -> bool:
        #DECL_FUNC -> tipo id '(' ')' bloco
        anterior = self.pos
        if self.tipo():
            if self.eat(TipoToken.IDENTIFICADOR):
                if self.eat(TipoToken.PARENTESE_ABRE):
                    if self.eat(TipoToken.PARENTESE_FECHA):
                        return self.bloco()
        self.pos = anterior
        return False
    
    def atribuicao(self) -> bool:
        #ATRIBUICAO -> variavel '=' expressao ';' | id '++' ';' | id '--' ';'
        anterior = self.pos
        if self.variavel():
            if self.eat(TipoToken.OP_ATRIBUICAO):
                if self.expressao():
                    return self.eat(TipoToken.PONTO_VIRGULA)
        self.pos = anterior
        
        if self.eat(TipoToken.IDENTIFICADOR):
            if self.current_token() and self.current_token().tipo in [TipoToken.OP_INCREMENTO, TipoToken.OP_DECREMENTO]:
                self.eat(self.current_token().tipo)
                return self.eat(TipoToken.PONTO_VIRGULA)
        self.pos = anterior
        return False
    
    def variavel(self) -> bool:
        #VARIAVEL -> id [ '[' expressao ']' ]
        anterior = self.pos
        if self.eat(TipoToken.IDENTIFICADOR):
            if self.current_token() and self.current_token().tipo == TipoToken.COLCHETE_ABRE:
                self.eat(TipoToken.COLCHETE_ABRE)
                self.expressao()
                self.eat(TipoToken.COLCHETE_FECHA)
            return True
        self.pos = anterior
        return False
    
    def expressao(self) -> bool:
        #EXPRESSAO -> exp_numerica | exp_logica | exp_cadeia
        anterior = self.pos
        if self.exp_numerica():
            return True
        self.pos = anterior
        if self.exp_logica():
            return True
        self.pos = anterior
        if self.exp_cadeia():
            return True
        print(f"DEBUG: Falha em expressao, token {self.pos}: {self.current_token()}")
        return False
    
    def exp_numerica(self) -> bool:
        #EXP_NUMERICA -> termo ( ('+' | '-' | '*' | '/' | '%') termo )*
        if not self.termo():
            return False
        while self.current_token() and self.current_token().tipo in [TipoToken.OP_ADICAO, TipoToken.OP_SUBTRACAO, TipoToken.OP_MULTIPLICACAO, TipoToken.OP_DIVISAO, TipoToken.OP_MODULO]:
            self.eat(self.current_token().tipo)
            if not self.termo():
                return False
        return True
    
    def termo(self) -> bool:
        #TERMO -> fator
        return self.fator()
    
    def fator(self) -> bool:
        #FATOR -> '(' exp_numerica ')' | variavel | const_inteira | const_flutuante
        anterior = self.pos
        if self.eat(TipoToken.PARENTESE_ABRE):
            if self.exp_numerica():
                return self.eat(TipoToken.PARENTESE_FECHA)
            return False
        self.pos = anterior
        if self.variavel():
            return True
        self.pos = anterior
        if self.current_token() and self.current_token().tipo in [TipoToken.CONSTANTE_INTEIRA, TipoToken.CONSTANTE_FLUTUANTE]:
            self.eat(self.current_token().tipo)
            return True
        return False
    
    def exp_logica(self, depth: int = 0) -> bool:
        #EXP_LOGICA -> exp_rel ( ('&&' | '||') exp_rel )*
        if depth > self.max_recursion_depth:
            self.erros.append(f"Erro sintático: profundidade máxima de recursão atingida em exp_logica na linha {self.current_token().linha}")
            return False
        print(f"DEBUG: Iniciando exp_logica, token {self.pos}: {self.current_token()}")
        if not self.exp_rel(depth + 1):
            print(f"DEBUG: Falha em exp_rel, token {self.pos}: {self.current_token()}")
            return False
        while self.current_token() and self.current_token().tipo in [TipoToken.OP_E_LOGICO, TipoToken.OP_OU_LOGICO]:
            print(f"DEBUG: Consumindo operador lógico {self.current_token()}, token {self.pos}")
            self.eat(self.current_token().tipo)
            if not self.exp_rel(depth + 1):
                print(f"DEBUG: Falha em exp_rel após operador lógico, token {self.pos}: {self.current_token()}")
                return False
        print(f"DEBUG: Finalizando exp_logica, token {self.pos}: {self.current_token()}")
        return True
    
    def exp_rel(self, depth: int = 0) -> bool:
        #EXP_REL -> '(' exp_logica ')' | const_logica | exp_numerica [ op_rel exp_numerica ]
        if depth > self.max_recursion_depth:
            self.erros.append(f"Erro sintático: profundidade máxima de recursão atingida em exp_rel na linha {self.current_token().linha}")
            return False
        anterior = self.pos
        print(f"DEBUG: Iniciando exp_rel, token {self.pos}: {self.current_token()}")
        
        if self.eat(TipoToken.PARENTESE_ABRE):
            if self.exp_logica(depth + 1):
                if self.eat(TipoToken.PARENTESE_FECHA):
                    print(f"DEBUG: Sucesso em exp_logica entre parênteses, token {self.pos}: {self.current_token()}")
                    return True
            print(f"DEBUG: Falha em exp_logica entre parênteses, token {self.pos}: {self.current_token()}")
            self.pos = anterior
            return False
        
        if self.current_token() and self.current_token().tipo == TipoToken.CONSTANTE_LOGICA:
            self.eat(TipoToken.CONSTANTE_LOGICA)
            print(f"DEBUG: Sucesso em const_logica, token {self.pos}: {self.current_token()}")
            return True
        
        if self.exp_numerica():
            if self.current_token() and self.current_token().tipo in [TipoToken.OP_MAIOR, TipoToken.OP_MENOR, TipoToken.OP_MAIOR_IGUAL, TipoToken.OP_MENOR_IGUAL, TipoToken.OP_IGUALDADE, TipoToken.OP_DIFERENTE]:
                print(f"DEBUG: Consumindo operador relacional {self.current_token()}, token {self.pos}")
                self.eat(self.current_token().tipo)
                if self.exp_numerica():
                    print(f"DEBUG: Sucesso em exp_numerica op_rel exp_numerica, token {self.pos}: {self.current_token()}")
                    return True
                print(f"DEBUG: Falha em segunda exp_numerica, token {self.pos}: {self.current_token()}")
                self.pos = anterior
                return False
            print(f"DEBUG: Sucesso em exp_numerica sem op_rel, token {self.pos}: {self.current_token()}")
            return True  # exp_numerica sozinha é válida (ex.: variável lógica)
        
        print(f"DEBUG: Falha em exp_rel, token {self.pos}: {self.current_token()}")
        self.pos = anterior
        return False
    
    def exp_cadeia(self) -> bool:
        #EXP_CADEIA -> termo_cadeia ( '&' exp_cadeia )*
        if not self.termo_cadeia():
            return False
        while self.current_token() and self.current_token().tipo == TipoToken.OP_CONCATENACAO:
            self.eat(TipoToken.OP_CONCATENACAO)
            if not self.termo_cadeia():
                return False
        return True
    
    def termo_cadeia(self) -> bool:
        #TERMO_CADEIA -> '(' exp_cadeia ')' | id | const_cadeia
        anterior = self.pos
        if self.eat(TipoToken.PARENTESE_ABRE):
            if self.exp_cadeia():
                return self.eat(TipoToken.PARENTESE_FECHA)
            return False
        self.pos = anterior
        if self.eat(TipoToken.IDENTIFICADOR):
            return True
        self.pos = anterior
        if self.eat(TipoToken.CONSTANTE_CADEIA):
            return True
        return False
    
    def escreva(self) -> bool:
        #ESCREVA -> 'escreva' '(' expressao ')' ';'
        anterior = self.pos
        print(f"DEBUG: Iniciando escreva, token {self.pos}: {self.current_token()}")
        if self.eat(TipoToken.PALAVRA_RESERVADA, 'escreva'):
            if self.eat(TipoToken.PARENTESE_ABRE):
                if self.expressao():
                    if self.eat(TipoToken.PARENTESE_FECHA):
                        if self.eat(TipoToken.PONTO_VIRGULA):
                            print(f"DEBUG: Sucesso em escreva, token {self.pos}: {self.current_token()}")
                            return True
                print(f"DEBUG: Falha em expressao ou parentese_fecha em escreva, token {self.pos}: {self.current_token()}")
        self.pos = anterior
        print(f"DEBUG: Falha em escreva, token {self.pos}: {self.current_token()}")
        return False
    
    def leia(self) -> bool:
        #LEIA -> 'leia' '(' id ')' ';'
        anterior = self.pos
        if self.eat(TipoToken.PALAVRA_RESERVADA, 'leia'):
            if self.eat(TipoToken.PARENTESE_ABRE):
                if self.eat(TipoToken.IDENTIFICADOR):
                    if self.eat(TipoToken.PARENTESE_FECHA):
                        return self.eat(TipoToken.PONTO_VIRGULA)
        self.pos = anterior
        return False
    
    def if_comando(self) -> bool:
        #IF -> 'se' '(' exp_logica ')' bloco [ 'senao' bloco ]
        anterior = self.pos
        print(f"DEBUG: Iniciando if_comando, token {self.pos}: {self.current_token()}")
        if self.eat(TipoToken.PALAVRA_RESERVADA, 'se'):
            if self.eat(TipoToken.PARENTESE_ABRE):
                if self.exp_logica():
                    if self.eat(TipoToken.PARENTESE_FECHA):
                        if self.bloco():
                            if self.current_token() and self.current_token().tipo == TipoToken.PALAVRA_RESERVADA and self.current_token().lexema == 'senao':
                                self.eat(TipoToken.PALAVRA_RESERVADA, 'senao')
                                return self.bloco()
                            print(f"DEBUG: Sucesso em if_comando sem senao, token {self.pos}: {self.current_token()}")
                            return True
                print(f"DEBUG: Falha em exp_logica ou parentese_fecha em if_comando, token {self.pos}: {self.current_token()}")
        self.pos = anterior
        print(f"DEBUG: Falha em if_comando, token {self.pos}: {self.current_token()}")
        return False
    
    def enquanto(self) -> bool:
        #ENQUANTO -> 'enquanto' '(' exp_logica ')' bloco
        anterior = self.pos
        if self.eat(TipoToken.PALAVRA_RESERVADA, 'enquanto'):
            if self.eat(TipoToken.PARENTESE_ABRE):
                if self.expressao():
                    if self.eat(TipoToken.PARENTESE_FECHA):
                        return self.bloco()
        self.pos = anterior
        return False
    
    def para(self) -> bool:
        #PARA -> 'para' '(' decl_var exp_logica ';' atribuicao_no_semicolon ')' bloco
        anterior = self.pos
        if self.eat(TipoToken.PALAVRA_RESERVADA, 'para'):
            if self.eat(TipoToken.PARENTESE_ABRE):
                if self.decl_var():
                    if self.exp_logica():
                        if self.eat(TipoToken.PONTO_VIRGULA):
                            if self.atribuicao_no_semicolon():
                                if self.eat(TipoToken.PARENTESE_FECHA):
                                    return self.bloco()
        self.pos = anterior
        return False
    
    def atribuicao_no_semicolon(self) -> bool:
        #ATRIBUICAO_NO_SEMICOLON -> variavel '=' expressao | id '++' | id '--'
        anterior = self.pos
        if self.variavel():
            if self.eat(TipoToken.OP_ATRIBUICAO):
                return self.expressao()
        self.pos = anterior
        
        if self.eat(TipoToken.IDENTIFICADOR):
            if self.current_token() and self.current_token().tipo in [TipoToken.OP_INCREMENTO, TipoToken.OP_DECREMENTO]:
                self.eat(self.current_token().tipo)
                return True
        self.pos = anterior
        return False
    
    def bloco(self) -> bool:
        #BLOCO -> '{' ( comando )* '}'
        anterior = self.pos
        print(f"DEBUG: Iniciando bloco, token {self.pos}: {self.current_token()}")
        if self.eat(TipoToken.INICIO_BLOCO):
            while self.current_token() and self.current_token().tipo != TipoToken.FIM_BLOCO:
                print(f"DEBUG: Processando comando dentro de bloco, token {self.pos}: {self.current_token()}")
                if not self.comando():
                    print(f"DEBUG: Falha em comando dentro de bloco, token {self.pos}: {self.current_token()}")
                    # Pular até o próximo ; ou } para recuperação de erros
                    while self.current_token() and self.current_token().tipo not in [TipoToken.PONTO_VIRGULA, TipoToken.FIM_BLOCO]:
                        print(f"DEBUG: Pulando token {self.pos}: {self.current_token()} dentro de bloco")
                        self.pos += 1
                    if self.current_token() and self.current_token().tipo == TipoToken.PONTO_VIRGULA:
                        self.eat(TipoToken.PONTO_VIRGULA)
            if self.eat(TipoToken.FIM_BLOCO):
                print(f"DEBUG: Sucesso em bloco, token {self.pos}: {self.current_token()}")
                return True
        self.pos = anterior
        print(f"DEBUG: Falha em bloco, token {self.pos}: {self.current_token()}")
        return False
    
    def tipo(self) -> bool:
        #TIPO -> 'inteiro' | 'flutuante' | 'logico' | 'cadeia'"""
        if self.current_token() and self.current_token().tipo == TipoToken.PALAVRA_RESERVADA and self.current_token().lexema in ['inteiro', 'flutuante', 'logico', 'cadeia']:
            self.pos += 1
            return True
        return False