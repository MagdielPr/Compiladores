from typing import List, Dict, Set, Tuple
from analisador_lexico import Token, TipoToken

class SimboloGramatica:
    def __init__(self, nome: str, eh_terminal: bool = False):
        self.nome = nome
        self.eh_terminal = eh_terminal

    def __eq__(self, other):
        if not isinstance(other, SimboloGramatica):
            return False
        return self.nome == other.nome and self.eh_terminal == other.eh_terminal

    def __hash__(self):
        return hash((self.nome, self.eh_terminal))

    def __str__(self):
        return self.nome

# Símbolos terminais
TERMINAIS = {
    'EOF': SimboloGramatica('EOF', True),
    'ID': SimboloGramatica('ID', True),
    'CONST_INTEIRA': SimboloGramatica('CONST_INTEIRA', True),
    'CONST_FLUTUANTE': SimboloGramatica('CONST_FLUTUANTE', True),
    'CONST_CADEIA': SimboloGramatica('CONST_CADEIA', True),
    'CONST_LOGICA': SimboloGramatica('CONST_LOGICA', True),
    'SE': SimboloGramatica('SE', True),
    'SENAO': SimboloGramatica('SENAO', True),
    'PARA': SimboloGramatica('PARA', True),
    'ENQUANTO': SimboloGramatica('ENQUANTO', True),
    'ESCREVA': SimboloGramatica('ESCREVA', True),
    'LEIA': SimboloGramatica('LEIA', True),
    'INTEIRO': SimboloGramatica('INTEIRO', True),
    'FLUTUANTE': SimboloGramatica('FLUTUANTE', True),
    'LOGICO': SimboloGramatica('LOGICO', True),
    'CADEIA': SimboloGramatica('CADEIA', True),
    'INICIO': SimboloGramatica('INICIO', True),
    'FIM': SimboloGramatica('FIM', True),
    'RETURN': SimboloGramatica('RETURN', True),
    'INICIO_BLOCO': SimboloGramatica('INICIO_BLOCO', True),
    'FIM_BLOCO': SimboloGramatica('FIM_BLOCO', True),
    'PAREN_ABRE': SimboloGramatica('PAREN_ABRE', True),
    'PAREN_FECHA': SimboloGramatica('PAREN_FECHA', True),
    'COL_ABRE': SimboloGramatica('COL_ABRE', True),
    'COL_FECHA': SimboloGramatica('COL_FECHA', True),
    'ADICAO': SimboloGramatica('ADICAO', True),
    'SUBTRACAO': SimboloGramatica('SUBTRACAO', True),
    'MULTIPLICACAO': SimboloGramatica('MULTIPLICACAO', True),
    'DIVISAO': SimboloGramatica('DIVISAO', True),
    'MODULO': SimboloGramatica('MODULO', True),
    'MAIOR': SimboloGramatica('MAIOR', True),
    'MENOR': SimboloGramatica('MENOR', True),
    'MAIOR_IGUAL': SimboloGramatica('MAIOR_IGUAL', True),
    'MENOR_IGUAL': SimboloGramatica('MENOR_IGUAL', True),
    'IGUAL': SimboloGramatica('IGUAL', True),
    'DIFERENTE': SimboloGramatica('DIFERENTE', True),
    'NEGACAO': SimboloGramatica('NEGACAO', True),
    'ATRIBUICAO': SimboloGramatica('ATRIBUICAO', True),
    'ATRIBUICAO_COMP': SimboloGramatica('ATRIBUICAO_COMP', True),
    'CONCATENACAO': SimboloGramatica('CONCATENACAO', True),
    'INCREMENTO': SimboloGramatica('INCREMENTO', True),
    'DECREMENTO': SimboloGramatica('DECREMENTO', True),
    'PONTO_VIRGULA': SimboloGramatica('PONTO_VIRGULA', True),
    'VIRGULA': SimboloGramatica('VIRGULA', True),
    'E_LOGICO': SimboloGramatica('E_LOGICO', True),
    'OU_LOGICO': SimboloGramatica('OU_LOGICO', True)
}

# Símbolos não-terminais
NAO_TERMINAIS = {
    'PROGRAMA': SimboloGramatica('PROGRAMA'),
    'LISTA_DECL_FUNCAO': SimboloGramatica('LISTA_DECL_FUNCAO'),
    'BLOCO_PRINCIPAL': SimboloGramatica('BLOCO_PRINCIPAL'),
    'LISTA_COMANDOS': SimboloGramatica('LISTA_COMANDOS'),
    'COMANDO': SimboloGramatica('COMANDO'),
    'DECL_FUNCAO': SimboloGramatica('DECL_FUNCAO'),
    'PARAMS': SimboloGramatica('PARAMS'),
    'LISTA_PARAM': SimboloGramatica('LISTA_PARAM'),
    'CHAMADA_FUNCAO': SimboloGramatica('CHAMADA_FUNCAO'),
    'LISTA_ARGS': SimboloGramatica('LISTA_ARGS'),
    'DECL_VAR': SimboloGramatica('DECL_VAR'),
    'COMANDO_ATRIBUICAO': SimboloGramatica('COMANDO_ATRIBUICAO'),
    'EXP_NUM': SimboloGramatica('EXP_NUM'),
    'TERMO_NUM': SimboloGramatica('TERMO_NUM'),
    'FATOR_NUM': SimboloGramatica('FATOR_NUM'),
    'EXP_LOG': SimboloGramatica('EXP_LOG'),
    'TERMO_LOG': SimboloGramatica('TERMO_LOG'),
    'FATOR_LOG': SimboloGramatica('FATOR_LOG'),
    'EXP_CADEIA': SimboloGramatica('EXP_CADEIA'),
    'ESCRITA': SimboloGramatica('ESCRITA'),
    'LEITURA': SimboloGramatica('LEITURA'),
    'IF': SimboloGramatica('IF'),
    'ELSE': SimboloGramatica('ELSE'),
    'FOR': SimboloGramatica('FOR'),
    'WHILE': SimboloGramatica('WHILE'),
    'RETURN_STMT': SimboloGramatica('RETURN_STMT'),
    'TIPO': SimboloGramatica('TIPO'),
    'VARIAVEL': SimboloGramatica('VARIAVEL'),
    'INIC_FOR': SimboloGramatica('INIC_FOR'),
    'DECL_VAR_SEM_PV': SimboloGramatica('DECL_VAR_SEM_PV'),
    'ATRIBUICAO_SEM_PV': SimboloGramatica('ATRIBUICAO_SEM_PV'),
    'INCR_FOR': SimboloGramatica('INCR_FOR')
}

# Gramática SLR revisada
GRAMATICA = {
    NAO_TERMINAIS['PROGRAMA']: [
        [NAO_TERMINAIS['LISTA_DECL_FUNCAO'], NAO_TERMINAIS['BLOCO_PRINCIPAL']]
    ],
    NAO_TERMINAIS['LISTA_DECL_FUNCAO']: [
        [NAO_TERMINAIS['DECL_FUNCAO'], NAO_TERMINAIS['LISTA_DECL_FUNCAO']],
        []
    ],
    NAO_TERMINAIS['BLOCO_PRINCIPAL']: [
        [TERMINAIS['INICIO'], NAO_TERMINAIS['LISTA_COMANDOS'], TERMINAIS['FIM']]
    ],
    NAO_TERMINAIS['LISTA_COMANDOS']: [
        [NAO_TERMINAIS['COMANDO'], NAO_TERMINAIS['LISTA_COMANDOS']],
        []
    ],
    NAO_TERMINAIS['COMANDO']: [
        [NAO_TERMINAIS['CHAMADA_FUNCAO'], TERMINAIS['PONTO_VIRGULA']],
        [NAO_TERMINAIS['DECL_VAR']],
        [NAO_TERMINAIS['COMANDO_ATRIBUICAO']],
        [NAO_TERMINAIS['ESCRITA']],
        [NAO_TERMINAIS['LEITURA']],
        [NAO_TERMINAIS['IF']],
        [NAO_TERMINAIS['WHILE']],
        [NAO_TERMINAIS['FOR']],
        [NAO_TERMINAIS['RETURN_STMT']]
    ],
    NAO_TERMINAIS['DECL_FUNCAO']: [
        [NAO_TERMINAIS['TIPO'], TERMINAIS['ID'], TERMINAIS['PAREN_ABRE'], NAO_TERMINAIS['PARAMS'], TERMINAIS['PAREN_FECHA'], TERMINAIS['INICIO_BLOCO'], NAO_TERMINAIS['LISTA_COMANDOS'], TERMINAIS['FIM_BLOCO']]
    ],
    NAO_TERMINAIS['PARAMS']: [
        [NAO_TERMINAIS['LISTA_PARAM']],
        []
    ],
    NAO_TERMINAIS['LISTA_PARAM']: [
        [NAO_TERMINAIS['TIPO'], TERMINAIS['ID']],
        [NAO_TERMINAIS['TIPO'], TERMINAIS['ID'], TERMINAIS['VIRGULA'], NAO_TERMINAIS['LISTA_PARAM']]
    ],
    NAO_TERMINAIS['CHAMADA_FUNCAO']: [
        [TERMINAIS['ID'], TERMINAIS['PAREN_ABRE'], NAO_TERMINAIS['LISTA_ARGS'], TERMINAIS['PAREN_FECHA']]
    ],
    NAO_TERMINAIS['LISTA_ARGS']: [
        [NAO_TERMINAIS['EXP_NUM']],
        [NAO_TERMINAIS['EXP_NUM'], TERMINAIS['VIRGULA'], NAO_TERMINAIS['LISTA_ARGS']],
        []
    ],
    NAO_TERMINAIS['DECL_VAR']: [
        [NAO_TERMINAIS['TIPO'], TERMINAIS['ID'], TERMINAIS['PONTO_VIRGULA']],
        [NAO_TERMINAIS['TIPO'], TERMINAIS['ID'], TERMINAIS['ATRIBUICAO'], NAO_TERMINAIS['EXP_NUM'], TERMINAIS['PONTO_VIRGULA']]
    ],
    NAO_TERMINAIS['COMANDO_ATRIBUICAO']: [
        [NAO_TERMINAIS['VARIAVEL'], TERMINAIS['ATRIBUICAO'], NAO_TERMINAIS['EXP_NUM'], TERMINAIS['PONTO_VIRGULA']],
        [NAO_TERMINAIS['VARIAVEL'], TERMINAIS['ATRIBUICAO_COMP'], NAO_TERMINAIS['EXP_NUM'], TERMINAIS['PONTO_VIRGULA']],
        [TERMINAIS['ID'], TERMINAIS['INCREMENTO'], TERMINAIS['PONTO_VIRGULA']],
        [TERMINAIS['ID'], TERMINAIS['DECREMENTO'], TERMINAIS['PONTO_VIRGULA']]
    ],
    NAO_TERMINAIS['VARIAVEL']: [
        [TERMINAIS['ID']],
        [TERMINAIS['ID'], TERMINAIS['COL_ABRE'], NAO_TERMINAIS['EXP_NUM'], TERMINAIS['COL_FECHA']]
    ],
    NAO_TERMINAIS['EXP_NUM']: [
        [NAO_TERMINAIS['TERMO_NUM']],
        [NAO_TERMINAIS['EXP_NUM'], TERMINAIS['ADICAO'], NAO_TERMINAIS['TERMO_NUM']],
        [NAO_TERMINAIS['EXP_NUM'], TERMINAIS['SUBTRACAO'], NAO_TERMINAIS['TERMO_NUM']]
    ],
    NAO_TERMINAIS['TERMO_NUM']: [
        [NAO_TERMINAIS['FATOR_NUM']],
        [NAO_TERMINAIS['TERMO_NUM'], TERMINAIS['MULTIPLICACAO'], NAO_TERMINAIS['FATOR_NUM']],
        [NAO_TERMINAIS['TERMO_NUM'], TERMINAIS['DIVISAO'], NAO_TERMINAIS['FATOR_NUM']],
        [NAO_TERMINAIS['TERMO_NUM'], TERMINAIS['MODULO'], NAO_TERMINAIS['FATOR_NUM']]
    ],
    NAO_TERMINAIS['FATOR_NUM']: [
        [TERMINAIS['CONST_INTEIRA']],
        [TERMINAIS['CONST_FLUTUANTE']],
        [NAO_TERMINAIS['VARIAVEL']],
        [TERMINAIS['PAREN_ABRE'], NAO_TERMINAIS['EXP_NUM'], TERMINAIS['PAREN_FECHA']],
        [NAO_TERMINAIS['CHAMADA_FUNCAO']]
    ],
    NAO_TERMINAIS['EXP_LOG']: [
        [NAO_TERMINAIS['TERMO_LOG']],
        [NAO_TERMINAIS['EXP_LOG'], TERMINAIS['E_LOGICO'], NAO_TERMINAIS['TERMO_LOG']],
        [NAO_TERMINAIS['EXP_LOG'], TERMINAIS['OU_LOGICO'], NAO_TERMINAIS['TERMO_LOG']]
    ],
    NAO_TERMINAIS['TERMO_LOG']: [
        [NAO_TERMINAIS['FATOR_LOG']],
        [TERMINAIS['NEGACAO'], NAO_TERMINAIS['FATOR_LOG']]
    ],
    NAO_TERMINAIS['FATOR_LOG']: [
        [TERMINAIS['CONST_LOGICA']],
        [TERMINAIS['PAREN_ABRE'], NAO_TERMINAIS['EXP_LOG'], TERMINAIS['PAREN_FECHA']],
        [NAO_TERMINAIS['EXP_NUM'], TERMINAIS['MAIOR'], NAO_TERMINAIS['EXP_NUM']],
        [NAO_TERMINAIS['EXP_NUM'], TERMINAIS['MENOR'], NAO_TERMINAIS['EXP_NUM']],
        [NAO_TERMINAIS['EXP_NUM'], TERMINAIS['MAIOR_IGUAL'], NAO_TERMINAIS['EXP_NUM']],
        [NAO_TERMINAIS['EXP_NUM'], TERMINAIS['MENOR_IGUAL'], NAO_TERMINAIS['EXP_NUM']],
        [NAO_TERMINAIS['EXP_NUM'], TERMINAIS['IGUAL'], NAO_TERMINAIS['EXP_NUM']],
        [NAO_TERMINAIS['EXP_NUM'], TERMINAIS['DIFERENTE'], NAO_TERMINAIS['EXP_NUM']]
    ],
    NAO_TERMINAIS['ESCRITA']: [
        [TERMINAIS['ESCREVA'], TERMINAIS['PAREN_ABRE'], NAO_TERMINAIS['EXP_NUM'], TERMINAIS['PAREN_FECHA'], TERMINAIS['PONTO_VIRGULA']],
        [TERMINAIS['ESCREVA'], TERMINAIS['PAREN_ABRE'], NAO_TERMINAIS['EXP_CADEIA'], TERMINAIS['PAREN_FECHA'], TERMINAIS['PONTO_VIRGULA']]
    ],
    NAO_TERMINAIS['LEITURA']: [
        [TERMINAIS['LEIA'], TERMINAIS['PAREN_ABRE'], NAO_TERMINAIS['VARIAVEL'], TERMINAIS['PAREN_FECHA'], TERMINAIS['PONTO_VIRGULA']]
    ],
    NAO_TERMINAIS['IF']: [
        [TERMINAIS['SE'], TERMINAIS['PAREN_ABRE'], NAO_TERMINAIS['EXP_LOG'], TERMINAIS['PAREN_FECHA'], TERMINAIS['INICIO_BLOCO'], NAO_TERMINAIS['LISTA_COMANDOS'], TERMINAIS['FIM_BLOCO'], NAO_TERMINAIS['ELSE']]
    ],
    NAO_TERMINAIS['ELSE']: [
        [TERMINAIS['SENAO'], TERMINAIS['INICIO_BLOCO'], NAO_TERMINAIS['LISTA_COMANDOS'], TERMINAIS['FIM_BLOCO']],
        []
    ],
    NAO_TERMINAIS['FOR']: [
        [TERMINAIS['PARA'], TERMINAIS['PAREN_ABRE'], NAO_TERMINAIS['INIC_FOR'], TERMINAIS['PONTO_VIRGULA'], NAO_TERMINAIS['EXP_LOG'], TERMINAIS['PONTO_VIRGULA'], NAO_TERMINAIS['INCR_FOR'], TERMINAIS['PAREN_FECHA'], TERMINAIS['INICIO_BLOCO'], NAO_TERMINAIS['LISTA_COMANDOS'], TERMINAIS['FIM_BLOCO']]
    ],
    NAO_TERMINAIS['INIC_FOR']: [
        [NAO_TERMINAIS['DECL_VAR_SEM_PV']],
        [NAO_TERMINAIS['ATRIBUICAO_SEM_PV']]
    ],
    NAO_TERMINAIS['DECL_VAR_SEM_PV']: [
        [NAO_TERMINAIS['TIPO'], TERMINAIS['ID'], TERMINAIS['ATRIBUICAO'], NAO_TERMINAIS['EXP_NUM']]
    ],
    NAO_TERMINAIS['ATRIBUICAO_SEM_PV']: [
        [NAO_TERMINAIS['VARIAVEL'], TERMINAIS['ATRIBUICAO'], NAO_TERMINAIS['EXP_NUM']]
    ],
    NAO_TERMINAIS['INCR_FOR']: [
        [NAO_TERMINAIS['VARIAVEL'], TERMINAIS['INCREMENTO']],
        [NAO_TERMINAIS['VARIAVEL'], TERMINAIS['DECREMENTO']],
        [NAO_TERMINAIS['ATRIBUICAO_SEM_PV']]
    ],
    NAO_TERMINAIS['WHILE']: [
        [TERMINAIS['ENQUANTO'], TERMINAIS['PAREN_ABRE'], NAO_TERMINAIS['EXP_LOG'], TERMINAIS['PAREN_FECHA'], TERMINAIS['INICIO_BLOCO'], NAO_TERMINAIS['LISTA_COMANDOS'], TERMINAIS['FIM_BLOCO']]
    ],
    NAO_TERMINAIS['RETURN_STMT']: [
        [TERMINAIS['RETURN'], NAO_TERMINAIS['EXP_NUM'], TERMINAIS['PONTO_VIRGULA']],
        [TERMINAIS['RETURN'], TERMINAIS['PONTO_VIRGULA']]
    ],
    NAO_TERMINAIS['TIPO']: [
        [TERMINAIS['INTEIRO']],
        [TERMINAIS['FLUTUANTE']],
        [TERMINAIS['LOGICO']],
        [TERMINAIS['CADEIA']]
    ]
}

class Item:
    def __init__(self, nt: SimboloGramatica, producao: List[SimboloGramatica], ponto: int = 0):
        self.nt = nt
        self.producao = producao
        self.ponto = ponto

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.nt == other.nt and self.producao == other.producao and self.ponto == other.ponto

    def __hash__(self):
        return hash((self.nt, tuple(self.producao), self.ponto))

    def __str__(self):
        prod_antes = ' '.join(str(s) for s in self.producao[:self.ponto])
        prod_depois = ' '.join(str(s) for s in self.producao[self.ponto:])
        return f"{self.nt} -> {prod_antes} • {prod_depois}"

def calcular_first(simbolo: SimboloGramatica, first: Dict[SimboloGramatica, Set[SimboloGramatica]] = None, visitados: Set[SimboloGramatica] = None) -> Set[SimboloGramatica]:
    if first is None:
        first = {}
    if visitados is None:
        visitados = set()
    if simbolo in first:
        return first[simbolo]
    if simbolo in visitados:
        return set()
    visitados.add(simbolo)
    first[simbolo] = set()
    if simbolo.eh_terminal:
        first[simbolo].add(simbolo)
    else:
        for producao in GRAMATICA.get(simbolo, []):
            if not producao:
                first[simbolo].add(None)
            else:
                i = 0
                while i < len(producao):
                    subs_first = calcular_first(producao[i], first, visitados)
                    first[simbolo] |= subs_first - {None}
                    if None not in subs_first:
                        break
                    i += 1
                if i == len(producao):
                    first[simbolo].add(None)
    visitados.remove(simbolo)
    return first[simbolo]

def calcular_follow(simbolo: SimboloGramatica, first: Dict[SimboloGramatica, Set[SimboloGramatica]], follow: Dict[SimboloGramatica, Set[SimboloGramatica]] = None, visitados: Set[SimboloGramatica] = None) -> Set[SimboloGramatica]:
    if follow is None:
        follow = {}
    if visitados is None:
        visitados = set()
    if simbolo in follow:
        return follow[simbolo]
    if simbolo in visitados:
        return set()
    visitados.add(simbolo)
    follow[simbolo] = set()
    if simbolo == NAO_TERMINAIS['PROGRAMA']:
        follow[simbolo].add(TERMINAIS['EOF'])
    for nt, producoes in GRAMATICA.items():
        for producao in producoes:
            for i in range(len(producao)):
                if producao[i] == simbolo:
                    if i + 1 < len(producao):
                        subs_first = calcular_first(producao[i + 1], first)
                        follow[simbolo] |= subs_first - {None}
                        if None in subs_first:
                            follow[simbolo] |= calcular_follow(nt, first, follow, visitados)
                    else:
                        if nt != simbolo:
                            follow[simbolo] |= calcular_follow(nt, first, follow, visitados)
    visitados.remove(simbolo)
    return follow[simbolo]

def closure(itens: Set[Item], first: Dict[SimboloGramatica, Set[SimboloGramatica]]) -> Set[Item]:
    fechamento = set(itens)
    mudanca = True
    while mudanca:
        mudanca = False
        novo = set()
        for item in fechamento:
            if item.ponto < len(item.producao):
                simbolo = item.producao[item.ponto]
                if not simbolo.eh_terminal:
                    for prod in GRAMATICA.get(simbolo, []):
                        novo_item = Item(simbolo, prod, 0)
                        if novo_item not in fechamento:
                            novo.add(novo_item)
                            mudanca = True
        fechamento |= novo
    return fechamento

def goto(fechamento: Set[Item], simbolo: SimboloGramatica, first: Dict[SimboloGramatica, Set[SimboloGramatica]]) -> Set[Item]:
    novo = set()
    for item in fechamento:
        if item.ponto < len(item.producao) and item.producao[item.ponto] == simbolo:
            novo.add(Item(item.nt, item.producao, item.ponto + 1))
    return closure(novo, first)

def construir_estados(first: Dict[SimboloGramatica, Set[SimboloGramatica]]) -> List[Set[Item]]:
    estados = []
    inicial = closure({Item(NAO_TERMINAIS['PROGRAMA'], GRAMATICA[NAO_TERMINAIS['PROGRAMA']][0])}, first)
    estados.append(inicial)
    i = 0
    while i < len(estados):
        estado = estados[i]
        simbolos = set()
        for item in estado:
            if item.ponto < len(item.producao):
                simbolos.add(item.producao[item.ponto])
        for simbolo in simbolos:
            novo_estado = goto(estado, simbolo, first)
            if novo_estado and novo_estado not in estados:
                estados.append(novo_estado)
        i += 1
    return estados

def construir_tabelas(estados: List[Set[Item]], first: Dict, follow: Dict) -> Tuple[Dict, Dict]:
    tabela_acao = {i: {} for i in range(len(estados))}
    tabela_goto = {i: {} for i in range(len(estados))}
    for i, estado in enumerate(estados):
        for item in estado:
            if item.ponto < len(item.producao):
                simbolo = item.producao[item.ponto]
                novo_estado = goto(estado, simbolo, first)
                if novo_estado in estados:
                    j = estados.index(novo_estado)
                    if simbolo.eh_terminal:
                        if simbolo.nome in tabela_acao[i]:
                            print(f"Conflito shift/reduce no estado {i} para símbolo {simbolo.nome}")
                        tabela_acao[i][simbolo.nome] = ('shift', j)
                    else:
                        tabela_goto[i][simbolo.nome] = j
            elif item.nt == NAO_TERMINAIS['PROGRAMA'] and item.ponto == len(item.producao):
                tabela_acao[i]['EOF'] = ('accept', None)
            else:
                for terminal in [t.nome for t in follow[item.nt] if t is not None]:
                    if terminal in tabela_acao[i]:
                        print(f"Conflito reduce/reduce no estado {i} para terminal {terminal}")
                    tabela_acao[i][terminal] = ('reduce', item.nt, item.producao)
    return tabela_acao, tabela_goto

def map_token_to_simbolo(token: Token) -> str:
    if token.tipo == TipoToken.PALAVRA_RESERVADA:
        return token.lexema.upper()
    else:
        tipo_token_map = {
            TipoToken.IDENTIFICADOR: 'ID',
            TipoToken.CONSTANTE_INTEIRA: 'CONST_INTEIRA',
            TipoToken.CONSTANTE_FLUTUANTE: 'CONST_FLUTUANTE',
            TipoToken.CONSTANTE_CADEIA: 'CONST_CADEIA',
            TipoToken.CONSTANTE_LOGICA: 'CONST_LOGICA',
            TipoToken.OP_ADICAO: 'ADICAO',
            TipoToken.OP_SUBTRACAO: 'SUBTRACAO',
            TipoToken.OP_MULTIPLICACAO: 'MULTIPLICACAO',
            TipoToken.OP_DIVISAO: 'DIVISAO',
            TipoToken.OP_MODULO: 'MODULO',
            TipoToken.OP_MAIOR: 'MAIOR',
            TipoToken.OP_MENOR: 'MENOR',
            TipoToken.OP_MAIOR_IGUAL: 'MAIOR_IGUAL',
            TipoToken.OP_MENOR_IGUAL: 'MENOR_IGUAL',
            TipoToken.OP_IGUALDADE: 'IGUAL',
            TipoToken.OP_DIFERENTE: 'DIFERENTE',
            TipoToken.OP_NEGACAO: 'NEGACAO',
            TipoToken.OP_ATRIBUICAO: 'ATRIBUICAO',
            TipoToken.OP_ATRIBUICAO_SOMA: 'ATRIBUICAO_COMP',
            TipoToken.OP_ATRIBUICAO_SUB: 'ATRIBUICAO_COMP',
            TipoToken.OP_CONCATENACAO: 'CONCATENACAO',
            TipoToken.OP_INCREMENTO: 'INCREMENTO',
            TipoToken.OP_DECREMENTO: 'DECREMENTO',
            TipoToken.PARENTESE_ABRE: 'PAREN_ABRE',
            TipoToken.PARENTESE_FECHA: 'PAREN_FECHA',
            TipoToken.COLCHETE_ABRE: 'COL_ABRE',
            TipoToken.COLCHETE_FECHA: 'COL_FECHA',
            TipoToken.INICIO_BLOCO: 'INICIO_BLOCO',
            TipoToken.FIM_BLOCO: 'FIM_BLOCO',
            TipoToken.PONTO_VIRGULA: 'PONTO_VIRGULA',
            TipoToken.VIRGULA: 'VIRGULA',
            TipoToken.OP_E_LOGICO: 'E_LOGICO',
            TipoToken.OP_OU_LOGICO: 'OU_LOGICO'
        }
        if token.tipo in tipo_token_map:
            return tipo_token_map[token.tipo]
        else:
            raise ValueError(f"Token desconhecido: {token.tipo} {token.lexema}")
        
class AnalisadorSintaticoSLR:
    def __init__(self):
        self.first = {}
        for simbolo in list(TERMINAIS.values()) + list(NAO_TERMINAIS.values()):
            calcular_first(simbolo, self.first)
        self.follow = {}
        for simbolo in NAO_TERMINAIS.values():
            calcular_follow(simbolo, self.first, self.follow)
        self.estados = construir_estados(self.first)
        self.tabela_acao, self.tabela_goto = construir_tabelas(self.estados, self.first, self.follow)
        self.erros = []

    def parse(self, tokens: List[Token]) -> bool:
        self.erros = []
        pilha = [0]
        tokens = tokens + [Token(TipoToken.PALAVRA_RESERVADA, 'EOF', tokens[-1].linha if tokens else 1, tokens[-1].coluna if tokens else 1)]
        i = 0
        sincronizacao = ['PONTO_VIRGULA', 'FIM_BLOCO', 'FIM', 'SENAO', 'PAREN_FECHA']

        while i < len(tokens):
            estado = pilha[-1]
            token = tokens[i]
            try:
                simbolo = map_token_to_simbolo(token)
            except ValueError as e:
                self.erros.append(f"Erro na linha {token.linha}, coluna {token.coluna}: {str(e)}")
                i += 1
                continue

            acao = self.tabela_acao.get(estado, {}).get(simbolo)
            if not acao:
                self.erros.append(f"Erro sintático na linha {token.linha}, coluna {token.coluna}: token inesperado '{token.lexema}' (estado {estado})")
                while i < len(tokens) and map_token_to_simbolo(tokens[i]) not in sincronizacao:
                    self.erros.append(f"Pulando token: {tokens[i].lexema} (linha {tokens[i].linha}, coluna {tokens[i].coluna})")
                    i += 1
                if i < len(tokens):
                    self.erros.append(f"Consumindo ponto de sincronização: {tokens[i].lexema} (linha {tokens[i].linha}, coluna {tokens[i].coluna})")
                continue

            if acao[0] == 'accept':
                return len(self.erros) == 0
            elif acao[0] == 'shift':
                pilha.append(simbolo)
                pilha.append(acao[1])
                i += 1
            elif acao[0] == 'reduce':
                nt, producao = acao[1], acao[2]
                for _ in range(len(producao) * 2):
                    if pilha:
                        pilha.pop()
                if not pilha:
                    self.erros.append(f"Erro sintático: pilha vazia ao reduzir para {nt.nome} (linha {token.linha}, coluna {token.coluna})")
                    return False
                estado = pilha[-1]
                goto_estado = self.tabela_goto.get(estado, {}).get(nt.nome)
                if goto_estado is None:
                    self.erros.append(f"Erro sintático: goto inválido para {nt.nome} no estado {estado} (linha {token.linha}, coluna {token.coluna})")
                    while i < len(tokens) and map_token_to_simbolo(tokens[i]) not in sincronizacao:
                        self.erros.append(f"Pulando token: {tokens[i].lexema} (linha {tokens[i].linha}, coluna {tokens[i].coluna})")
                        i += 1
                    if i < len(tokens):
                        self.erros.append(f"Consumindo ponto de sincronização: {tokens[i].lexema} (linha {tokens[i].linha}, coluna {tokens[i].coluna})")
                    continue
                pilha.append(nt.nome)
                pilha.append(goto_estado)
            else:
                self.erros.append(f"Erro sintático na linha {token.linha}, coluna {token.coluna}: ação inválida para '{token.lexema}' (estado {estado})")
                i += 1

        return len(self.erros) == 0