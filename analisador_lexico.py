
import re
from enum import Enum
from typing import List, Tuple, Optional

class TipoToken(Enum):
    #Enumeração dos tipos de tokens suportados
    
    # Identificadores e constantes
    IDENTIFICADOR = "identificador"
    CONSTANTE_INTEIRA = "constante_inteira"
    CONSTANTE_FLUTUANTE = "constante_flutuante"
    CONSTANTE_CADEIA = "constante_cadeia"
    CONSTANTE_LOGICA = "constante_logica"
    
    # Palavras reservadas
    PALAVRA_RESERVADA = "palavra_reservada"
    
    # Operadores aritméticos
    OP_ADICAO = "operador_adicao"
    OP_SUBTRACAO = "operador_subtracao"
    OP_MULTIPLICACAO = "operador_multiplicacao"
    OP_DIVISAO = "operador_divisao"
    OP_MODULO = "operador_modulo"
    
    # Operadores relacionais
    OP_MAIOR = "operador_maior"
    OP_MENOR = "operador_menor"
    OP_MAIOR_IGUAL = "operador_maior_igual"
    OP_MENOR_IGUAL = "operador_menor_igual"
    OP_IGUALDADE = "operador_igualdade"
    OP_DIFERENTE = "operador_diferente"
    
    # Operadores lógicos
    OP_E_LOGICO = "operador_e_logico"
    OP_OU_LOGICO = "operador_ou_logico"
    OP_NEGACAO = "operador_negacao"
    
    # Outros operadores
    OP_ATRIBUICAO = "operador_atribuicao"
    OP_CONCATENACAO = "operador_concatenacao"
    OP_INCREMENTO = "operador_incremento"
    OP_DECREMENTO = "operador_decremento"
    
    # Delimitadores
    PARENTESE_ABRE = "parentese_abre"
    PARENTESE_FECHA = "parentese_fecha"
    COLCHETE_ABRE = "colchete_abre"
    COLCHETE_FECHA = "colchete_fecha"
    INICIO_BLOCO = "inicio_bloco"
    FIM_BLOCO = "fim_bloco"
    PONTO_VIRGULA = "ponto_virgula"
    VIRGULA = "virgula"

class Token:
    #Representa um token identificado no código fonte
    
    def __init__(self, tipo: TipoToken, lexema: str, linha: int, coluna: int):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna
    
    def __str__(self) -> str:
        return f"Token(tipo='{self.tipo.value}', lexema='{self.lexema}', linha={self.linha}, coluna={self.coluna})"
    
    def __repr__(self) -> str:
        return self.__str__()

class ErroLexico:
    #Representa um erro léxico encontrado durante a análise
    
    def __init__(self, mensagem: str, linha: int, coluna: int):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
    
    def __str__(self) -> str:
        return f"Erro na linha {self.linha}, coluna {self.coluna}: {self.mensagem}"
    
    def __repr__(self) -> str:
        return self.__str__()

class AnalisadorLexico:
    #Analisador léxico para a linguagem de programação especificada
    
    def __init__(self):
        # Palavras reservadas da linguagem
        self.palavras_reservadas = {
            'se', 'senao', 'para', 'faca', 'enquanto', 'escreva', 'leia',
            'inteiro', 'flutuante', 'logico', 'cadeia', 'inicio', 'fim'
        }
        
        # Constantes lógicas
        self.constantes_logicas = {'verdadeiro', 'falso'}
        
        # Estado do analisador
        self.reset()
    
    def reset(self):
        #Reinicia o estado do analisador
        self.codigo_fonte = ""
        self.posicao = 0
        self.linha_atual = 1
        self.coluna_atual = 1
        self.tokens = []
        self.erros = []
    
    def analisar(self, codigo_fonte: str) -> Tuple[List[Token], List[ErroLexico]]:
        
        ##Analisa o código fonte e retorna os tokens e erros encontrados
        
        ##Args:
            ##codigo_fonte: String contendo o código fonte a ser analisado
            
        ##Returns:
            ##Tupla contendo (lista de tokens, lista de erros)
        
        self.reset()
        self.codigo_fonte = codigo_fonte
        
        while self.posicao < len(self.codigo_fonte):
            char = self.char_atual()
            
            # Pula espaços em branco
            if char.isspace():
                self._avancar()
                continue
            
            # Identifica o tipo de token
            if char.isalpha() or char == '_':
                self._processar_identificador()
            elif char.isdigit():
                self._processar_numero()
            elif char == '"':
                self._processar_cadeia()
            elif char == '/':
                if self._olhar_proximo() in '/*':
                    self._processar_comentario()
                else:
                    self._processar_operador()
            elif char in '+-*=><()[]{};&!|%,':
                self._processar_operador()
            else:
                self._adicionar_erro(f"Caractere inválido: '{char}'")
                self._avancar()
        
        return self.tokens, self.erros
    
    def char_atual(self) -> str:
        #Retorna o caractere atual ou string vazia se fim do arquivo
        if self.posicao < len(self.codigo_fonte):
            return self.codigo_fonte[self.posicao]
        return ''
    
    def _olhar_proximo(self, offset: int = 1) -> str:
        #Olha o próximo caractere sem avançar a posição
        pos = self.posicao + offset
        if pos < len(self.codigo_fonte):
            return self.codigo_fonte[pos]
        return ''
    
    def _avancar(self):
        #Avança para o próximo caractere, atualizando linha e coluna
        if self.posicao < len(self.codigo_fonte):
            if self.codigo_fonte[self.posicao] == '\n':
                self.linha_atual += 1
                self.coluna_atual = 1
            else:
                self.coluna_atual += 1
            self.posicao += 1
    
    def _adicionar_token(self, tipo: TipoToken, lexema: str, coluna: int):
        #Adiciona um novo token a lista
        token = Token(tipo, lexema, self.linha_atual, coluna)
        self.tokens.append(token)
    
    def _adicionar_erro(self, mensagem: str):
        #Adiciona um novo erro a lista
        erro = ErroLexico(mensagem, self.linha_atual, self.coluna_atual)
        self.erros.append(erro)
    
    def _processar_identificador(self):
        #Processa identificadores e palavras reservadas
        coluna_inicial = self.coluna_atual
        inicio = self.posicao
        
        # Primeiro caractere deve ser letra ou underscore
        if not (self.char_atual().isalpha() or self.char_atual() == '_'):
            self._adicionar_erro("Identificador deve começar com letra ou underscore")
            self._avancar()
            return
        
        # Consome caracteres válidos do identificador
        while (self.posicao < len(self.codigo_fonte) and 
               (self.char_atual().isalnum() or self.char_atual() == '_')):
            self._avancar()
        
        lexema = self.codigo_fonte[inicio:self.posicao]
        
        # Classifica o token
        if lexema in self.palavras_reservadas:
            self._adicionar_token(TipoToken.PALAVRA_RESERVADA, lexema, coluna_inicial)
        elif lexema in self.constantes_logicas:
            self._adicionar_token(TipoToken.CONSTANTE_LOGICA, lexema, coluna_inicial)
        else:
            self._adicionar_token(TipoToken.IDENTIFICADOR, lexema, coluna_inicial)
    
    def _processar_numero(self):
        #Processa números inteiros e flutuantes
        coluna_inicial = self.coluna_atual
        inicio = self.posicao
        eh_flutuante = False
        
        # Consome dígitos da parte inteira
        while self.posicao < len(self.codigo_fonte) and self.char_atual().isdigit():
            self._avancar()
        
        # Verifica se há parte decimal
        if (self.char_atual() == '.' and 
            self._olhar_proximo().isdigit()):
            eh_flutuante = True
            self._avancar()  # consome o ponto
            
            # Consome dígitos da parte decimal
            while self.posicao < len(self.codigo_fonte) and self.char_atual().isdigit():
                self._avancar()
        
        lexema = self.codigo_fonte[inicio:self.posicao]
        
        # Verifica erro: número seguido de ponto sem dígitos
        if self.char_atual() == '.' and not eh_flutuante:
            lexema_erro = lexema + '.'
            self._avancar()
            self._adicionar_erro(f"Número inválido: '{lexema_erro}' - ponto decimal deve ser seguido por dígitos")
            return
        
        # Verifica erro: identificador começando com número
        if (self.posicao < len(self.codigo_fonte) and 
            (self.char_atual().isalpha() or self.char_atual() == '_')):
            inicio_erro = self.posicao
            while (self.posicao < len(self.codigo_fonte) and 
                   (self.char_atual().isalnum() or self.char_atual() == '_')):
                self._avancar()
            lexema_invalido = self.codigo_fonte[inicio_erro:self.posicao]
            self._adicionar_erro(f"Identificador inválido: números não podem preceder identificadores (encontrado após número: '{lexema_invalido}')")
            return
        
        # Adiciona token apropriado
        if eh_flutuante:
            self._adicionar_token(TipoToken.CONSTANTE_FLUTUANTE, lexema, coluna_inicial)
        else:
            self._adicionar_token(TipoToken.CONSTANTE_INTEIRA, lexema, coluna_inicial)
    
    def _processar_cadeia(self):
        #Processa cadeias de caracteres
        coluna_inicial = self.coluna_atual
        self._avancar()  # pula a aspa inicial
        inicio = self.posicao
        
        while self.posicao < len(self.codigo_fonte) and self.char_atual() != '"':
            if self.char_atual() == '\n':
                self._adicionar_erro("Cadeia não pode conter quebra de linha")
                return
            self._avancar()
        
        if self.posicao >= len(self.codigo_fonte):
            self._adicionar_erro("Cadeia não terminada (fim do arquivo alcançado)")
            return
        
        lexema_interno = self.codigo_fonte[inicio:self.posicao]
        self._avancar()  # pula a aspa final
        
        lexema_completo = '"' + lexema_interno + '"'
        self._adicionar_token(TipoToken.CONSTANTE_CADEIA, lexema_completo, coluna_inicial)
    
    def _processar_comentario(self):
        #Processa comentários de linha (//) e multi-linha (/* */)
        if self._olhar_proximo() == '/':
            # Comentário de linha
            self._avancar()  # consome primeiro '/'
            self._avancar()  # consome segundo '/'
            while self.posicao < len(self.codigo_fonte) and self.char_atual() != '\n':
                self._avancar()
        elif self._olhar_proximo() == '*':
            # Comentário multi-linha
            self._avancar()  # consome '/'
            self._avancar()  # consome '*'
            
            while self.posicao < len(self.codigo_fonte) - 1:
                if self.char_atual() == '*' and self._olhar_proximo() == '/':
                    self._avancar()  # consome '*'
                    self._avancar()  # consome '/'
                    return
                self._avancar()
            
            # Comentário não foi fechado
            self._adicionar_erro("Comentário multi-linha não terminado")
    
    def _processar_operador(self):
        #Processa operadores e delimitadores
        coluna_inicial = self.coluna_atual
        char = self.char_atual()
        proximo = self._olhar_proximo()
        
        # Operadores de dois caracteres
        operadores_duplos = {
            '++': TipoToken.OP_INCREMENTO,
            '--': TipoToken.OP_DECREMENTO,
            '>=': TipoToken.OP_MAIOR_IGUAL,
            '<=': TipoToken.OP_MENOR_IGUAL,
            '==': TipoToken.OP_IGUALDADE,
            '!=': TipoToken.OP_DIFERENTE,
            '||': TipoToken.OP_OU_LOGICO,
            '&&': TipoToken.OP_E_LOGICO,
        }
        
        lexema_duplo = char + proximo
        if lexema_duplo in operadores_duplos:
            self._adicionar_token(operadores_duplos[lexema_duplo], lexema_duplo, coluna_inicial)
            self._avancar()
            self._avancar()
            return
        
        # Operadores de um caractere
        operadores_simples = {
            '=': TipoToken.OP_ATRIBUICAO,
            '+': TipoToken.OP_ADICAO,
            '-': TipoToken.OP_SUBTRACAO,
            '*': TipoToken.OP_MULTIPLICACAO,
            '/': TipoToken.OP_DIVISAO,
            '>': TipoToken.OP_MAIOR,
            '<': TipoToken.OP_MENOR,
            '!': TipoToken.OP_NEGACAO,
            '&': TipoToken.OP_CONCATENACAO,
            '(': TipoToken.PARENTESE_ABRE,
            ')': TipoToken.PARENTESE_FECHA,
            '[': TipoToken.COLCHETE_ABRE,
            ']': TipoToken.COLCHETE_FECHA,
            '{': TipoToken.INICIO_BLOCO,
            '}': TipoToken.FIM_BLOCO,
            ';': TipoToken.PONTO_VIRGULA,
            '%': TipoToken.OP_MODULO,
            ',': TipoToken.VIRGULA,
        }
        
        if char in operadores_simples:
            self._adicionar_token(operadores_simples[char], char, coluna_inicial)
            self._avancar()
        elif char == '|':
            self._adicionar_erro(f"Operador inválido: '{char}' (talvez você quis dizer '||'?)")
            self._avancar()
        else:
            self._adicionar_erro(f"Operador desconhecido: '{char}'")
            self._avancar()
    
    def obter_estatisticas(self) -> dict:
        #Retorna estatísticas sobre os tokens analisados
        contagem_tipos = {}
        for token in self.tokens:
            tipo = token.tipo.value
            contagem_tipos[tipo] = contagem_tipos.get(tipo, 0) + 1
        
        return {
            'total_tokens': len(self.tokens),
            'total_erros': len(self.erros),
            'tipos_tokens': contagem_tipos
        }