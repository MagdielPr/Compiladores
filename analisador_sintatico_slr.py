# Imports de bibliotecas que vamos usar. 're' é para expressões regulares (para reconhecer padrões no código), 'defaultdict' e 'deque' são estruturas de dados úteis, e 'namedtuple' para criar tipos simples de dados.
import re
from collections import defaultdict, deque, namedtuple

# LÉXICO

# Exceção personalizada para erros no analisador léxico (quando o código tem caracteres inválidos).
class ErroLexico(Exception):
    pass

# Classe para representar cada token 
class Token:
    def __init__(self, tipo, lexema, pos):
        self.tipo = tipo  # Tipo do token, como 'ID' para identificador.
        self.lexema = lexema  # O texto real do token, como 'x' para uma variável.
        self.pos = pos  # Posição no código onde o token começa.
    
    def __repr__(self):
        # Isso é só para imprimir o token de forma bonitinha
        return f"Token({self.tipo}, {self.lexema!r}, {self.pos})"

class Lexico:
    def __init__(self):
        # Definições de padrões para cada tipo de token usando expressões regulares.
        padroes = [
            ('FUN', r'\bfun\b'),
            ('VAR', r'\bvar\b'),
            ('WRITE', r'\bwrite\b'),
            ('READ', r'\bread\b'),
            ('IF', r'\bif\b'),
            ('ELSE', r'\belse\b'),
            ('WHILE', r'\bwhile\b'),
            ('FOR', r'\bfor\b'),
            ('GE', r'>='),
            ('LE', r'<='),
            ('EQEQ', r'=='),
            ('NE', r'!='),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('COMMA', r','),
            ('SEMI', r';'),
            ('EQ', r'='),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULT', r'\*'),
            ('DIV', r'/'),
            ('GT', r'>'),
            ('LT', r'<'),
            ('NOT', r'!'),
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Para nomes como variáveis ou funções.
            ('NUM', r'\d+'),  # Números.
            ('WS', r'[ \t\r]+'),  # Espaços em branco (ignorados).
            ('NEWLINE', r'\n'),  # Quebras de linha (para contar linhas).
        ]
        # Junta todos os padrões em uma grande regex para eficiente.
        regex = '|'.join(f'(?P<{n}>{r})' for n, r in padroes)
        self.pattern = re.compile(regex)  # Compila a regex.
        self.entrada = ''  # Código fonte que vai ser analisado.
        self.pos = 0  # Posição atual no código.
        self.linha = 1  # Número da linha atual.

    # Define o código fonte a ser analisado.
    def definir_entrada(self, s):
        self.entrada = s
        self.pos = 0
        self.linha = 1

    # Pega o próximo token do código.
    def proximo_token(self):
        while self.pos < len(self.entrada):  # Enquanto não chegamos ao fim do código.
            m = self.pattern.match(self.entrada, self.pos)  # Tenta um padrão.
            if not m:
                # Se não encontrar, é erro: caractere inválido.
                raise ErroLexico(f"Caractere inválido '{self.entrada[self.pos]}' na posição {self.pos}")
            tipo = m.lastgroup  # Tipo do token encontrado.
            lex = m.group()  # O texto do token.
            inicio = self.pos  # Posição de início.
            self.pos = m.end()  # Atualiza posição para o fim do token.
            if tipo == 'WS':  # Ignora espaços em branco.
                continue
            if tipo == 'NEWLINE':  # Conta nova linha.
                self.linha += 1
                continue
            # Retorna o token encontrado.
            return Token(tipo, lex, inicio)
        # Se acabou o código, retorna token de fim '$'.
        return Token('$', '', self.pos)

# GRAMÁTICA
# Função que monta a lista de produções da gramática.
# Cada produção é uma regra, como "PROGRAM -> STMT_LIST" (o programa é uma lista de comandos).
def montar_gramatica():
    G = []  # Lista de produções.
    G.append(("S'", ["PROGRAM"]))  # 0 - Produção inicial, S' é o símbolo start.
    G.append(("PROGRAM", ["STMT_LIST"]))  # 1 - Programa é uma lista de statements.
    G.append(("STMT_LIST", ["STMT_LIST", "STMT"]))  # 2 - Lista de statements recursiva.
    G.append(("STMT_LIST", ["STMT"]))  # 3 - Ou só um statement.
    G.append(("STMT", ["VAR_DECL"]))  # 4 - Statement pode ser declaração de var.
    G.append(("STMT", ["FUN_DECL"]))  # 5 - Ou declaração de função.
    G.append(("STMT", ["ASSIGN"]))  # 6 - Ou atribuição.
    G.append(("STMT", ["WRITE_STMT"]))  # 7 - Ou write.
    G.append(("STMT", ["READ_STMT"]))  # 8 - Ou read.
    G.append(("STMT", ["IF_STMT"]))  # 9 - Ou if.
    G.append(("STMT", ["WHILE_STMT"]))  # 10 - Ou while.
    G.append(("STMT", ["FOR_STMT"]))  # 11 - Ou for.
    G.append(("STMT", ["EXPR_STMT"]))  # 12 - Ou expressão seguida de ;.
    G.append(("STMT", ["FUN_CALL_SEMI"]))  # 13 - Ou chamada de função com ;.
    G.append(("VAR_DECL", ["VAR", "ID", "SEMI"]))  # 14 - Declaração de var: var id;.
    G.append(("FUN_DECL", ["FUN", "ID", "LPAREN", "PARAMS_OPT", "RPAREN", "LBRACE", "STMT_LIST", "RBRACE"]))  # 15 - Declaração de função.
    G.append(("ASSIGN", ["ID", "EQ", "EXPR", "SEMI"]))  # 16 - Atribuição: id = expr;.
    G.append(("WRITE_STMT", ["WRITE", "LPAREN", "EXPR", "RPAREN", "SEMI"]))  # 17 - write(expr);.
    G.append(("READ_STMT", ["READ", "LPAREN", "ID", "RPAREN", "SEMI"]))  # 18 - read(id);.
    G.append(("IF_STMT", ["IF", "LPAREN", "EXPR", "RPAREN", "LBRACE", "STMT_LIST", "RBRACE", "ELSE_OPT"]))  # 19 - if (expr) { stmts } else_opt.
    G.append(("ELSE_OPT", ["ELSE", "LBRACE", "STMT_LIST", "RBRACE"]))  # 20 - Parte else.
    G.append(("ELSE_OPT", []))  # 21 - Ou vazio (sem else).
    G.append(("WHILE_STMT", ["WHILE", "LPAREN", "EXPR", "RPAREN", "LBRACE", "STMT_LIST", "RBRACE"]))  # 22 - while (expr) { stmts }.
    G.append(("FOR_STMT", ["FOR", "LPAREN", "ASSIGN_NS", "SEMI", "EXPR_OPT", "SEMI", "ASSIGN_NS", "RPAREN", "LBRACE", "STMT_LIST", "RBRACE"]))  # 23 - for (init; cond; incr) { stmts }.
    G.append(("ASSIGN_NS", ["ID", "EQ", "EXPR"]))  # 24 - Atribuição sem ; (para for).
    G.append(("EXPR_OPT", ["EXPR"]))  # 25 - Expressão opcional.
    G.append(("EXPR_OPT", []))  # 26 - Ou vazia.
    G.append(("EXPR_STMT", ["EXPR", "SEMI"]))  # 27 - Expr;.
    G.append(("FUN_CALL_SEMI", ["ID", "LPAREN", "ARG_LIST_OPT", "RPAREN", "SEMI"]))  # 28 - Chamada de função com ;.
    G.append(("ARG_LIST_OPT", ["ARG_LIST"]))  # 29 - Lista de args opcional.
    G.append(("ARG_LIST_OPT", []))  # 30 - Ou vazia.
    G.append(("ARG_LIST", ["ARG_LIST", "COMMA", "EXPR"]))  # 31 - Lista de args recursiva.
    G.append(("ARG_LIST", ["EXPR"]))  # 32 - Ou uma expr.
    G.append(("PARAMS_OPT", ["PARAMS"]))  # 33 - Parâmetros opcionais.
    G.append(("PARAMS_OPT", []))  # 34 - Ou vazios.
    G.append(("PARAMS", ["PARAMS", "COMMA", "ID"]))  # 35 - Parâmetros recursivos.
    G.append(("PARAMS", ["ID"]))  # 36 - Ou um id.
    G.append(("EXPR", ["REL"]))  # 37 - Expr é relacional.
    G.append(("REL", ["ADD", "REL_TAIL"]))  # 38 - Relacional: add + tail.
    G.append(("REL_TAIL", ["GT", "ADD"]))  # 39 - > add.
    G.append(("REL_TAIL", ["LT", "ADD"]))  # 40 - < add.
    G.append(("REL_TAIL", ["GE", "ADD"]))  # 41 - >= add.
    G.append(("REL_TAIL", ["LE", "ADD"]))  # 42 - <= add.
    G.append(("REL_TAIL", ["EQEQ", "ADD"]))  # 43 - == add.
    G.append(("REL_TAIL", ["NE", "ADD"]))  # 44 - != add.
    G.append(("REL_TAIL", []))  # 45 - Ou vazio.
    G.append(("ADD", ["ADD", "PLUS", "MUL"]))  # 46 - Add recursivo + mul.
    G.append(("ADD", ["ADD", "MINUS", "MUL"]))  # 47 - Add recursivo - mul.
    G.append(("ADD", ["MUL"]))  # 48 - Ou só mul.
    G.append(("MUL", ["MUL", "MULT", "UNARY"]))  # 49 - Mul recursivo * unary.
    G.append(("MUL", ["MUL", "DIV", "UNARY"]))  # 50 - Mul recursivo / unary.
    G.append(("MUL", ["UNARY"]))  # 51 - Ou só unary.
    G.append(("UNARY", ["NOT", "UNARY"]))  # 52 - ! unary (negação).
    G.append(("UNARY", ["MINUS", "UNARY"]))  # 53 - - unary (menos unário).
    G.append(("UNARY", ["PRIMARY"]))  # 54 - Ou primary.
    G.append(("PRIMARY", ["NUM"]))  # 55 - Número.
    G.append(("PRIMARY", ["ID"]))  # 56 - Id.
    G.append(("PRIMARY", ["LPAREN", "EXPR", "RPAREN"]))  # 57 - (expr).
    G.append(("PRIMARY", ["FUN_CALL"]))  # 58 - Chamada de função.
    G.append(("FUN_CALL", ["ID", "LPAREN", "ARG_LIST_OPT", "RPAREN"]))  # 59 - id(args).
    return G  # Retorna a lista de produções.

# GRAMÁTICA (FIRST, FOLLOW)
# Classe que representa a gramática, calcula FIRST e FOLLOW (para resolver conflitos).
class Gramatica:
    def __init__(self, producoes):
        self.producoes = producoes  # Lista de produções.
        # Identifica não-terminais (símbolos como 'EXPR') e terminais (como 'ID', '+').
        self.nao_terminais = set(lhs for lhs, _ in producoes)
        todos_simbolos = {s for _, rhs in producoes for s in rhs}
        self.terminais = todos_simbolos - self.nao_terminais
        self.terminais.add('$')  # Adiciona $ como terminal de fim.
        self.por_lhs = defaultdict(list)  # Agrupa produções por lado esquerdo.
        for i, (lhs, rhs) in enumerate(producoes):
            self.por_lhs[lhs].append((i, rhs))
        # Dicionários para FIRST e FOLLOW.
        self.first = {s: set() for s in self.nao_terminais | self.terminais}
        for t in self.terminais:
            self.first[t].add(t)  # FIRST de terminal é ele mesmo.
        self.follow = {nt: set() for nt in self.nao_terminais}
        self.simbolo_inicial = producoes[0][0]  # Símbolo start.
        self._calcular_first()  # Calcula FIRST.
        self._calcular_follow()  # Calcula FOLLOW.

    # Calcula o conjunto FIRST (primeiros terminais que podem vir de um símbolo).
    def _calcular_first(self):
        alterado = True
        while alterado:  # Loop até não mudar mais.
            alterado = False
            for lhs, rhs in self.producoes:
                antes = self.first[lhs].copy()  # Copia atual para comparar.
                if not rhs:  # Produção vazia: FIRST inclui ε.
                    self.first[lhs].add('ε')
                else:
                    epsilon_para_lhs = True
                    for s in rhs:  # Para cada símbolo na direita.
                        self.first[lhs] |= (self.first[s] - {'ε'})  # Adiciona FIRST sem ε.
                        if 'ε' not in self.first[s]:  # Se não produz ε, para.
                            epsilon_para_lhs = False
                            break
                    if epsilon_para_lhs:  # Se todos produzem ε, adiciona ε.
                        self.first[lhs].add('ε')
                if antes != self.first[lhs]:  # Se mudou, continua o loop.
                    alterado = True

    # Calcula FIRST de uma sequência de símbolos (usado no FOLLOW).
    def _first_de_sequencia(self, seq):
        res = set()
        if not seq:  # Sequência vazia: ε.
            res.add('ε')
            return res
        for s in seq:
            res |= (self.first[s] - {'ε'})
            if 'ε' not in self.first[s]:  # Para se não tem ε.
                return res
        res.add('ε')  # Se todos tem ε.
        return res

    # Calcula FOLLOW (o que pode vir depois de um não-terminal).
    def _calcular_follow(self):
        self.follow[self.simbolo_inicial].add('$')  # FOLLOW do start inclui $.
        alterado = True
        while alterado:
            alterado = False
            for lhs, rhs in self.producoes:
                for i, B in enumerate(rhs):  # Para cada posição na direita.
                    if B in self.nao_terminais:  # Se é não-terminal.
                        beta = rhs[i+1:]  # O que vem depois.
                        first_beta = self._first_de_sequencia(beta)
                        antes = self.follow[B].copy()
                        self.follow[B] |= (first_beta - {'ε'})  # Adiciona FIRST de beta sem ε.
                        if 'ε' in first_beta or not beta:  # Se beta pode ser vazio, adiciona FOLLOW de lhs.
                            self.follow[B] |= self.follow[lhs]
                        if antes != self.follow[B]:
                            alterado = True

# ITENS LR(0), AUTÔMATO E TABELAS

# Item representa uma produção com um ponto indicando onde estamos na análise.
Item = namedtuple('Item', ['prod_idx', 'dot'])

# Classe que constrói o autômato LR(0) e as tabelas ACTION e GOTO do SLR.
class ConstrutorSLR:
    def __init__(self, gramatica: Gramatica):
        self.G = gramatica  # A gramática.
        self.producoes = gramatica.producoes
        self.C = []  # Lista de estados (conjuntos de itens).
        self._construir_automato()  # Constrói os estados.
        self.action = {}  # Tabela ACTION (shift/reduce).
        self.goto = {}  # Tabela GOTO (para não-terminais).
        self._construir_tabelas()  # Preenche as tabelas.

    # Calcula o closure: adiciona itens derivados de um conjunto.
    def closure(self, itens):
        fecho = set(itens)  # Começa com os itens iniciais.
        alterado = True
        while alterado:
            alterado = False
            novos = set()  # Novos itens a adicionar.
            for it in list(fecho):  # Para cada item.
                lhs, rhs = self.producoes[it.prod_idx]
                if it.dot < len(rhs):  # Se o ponto não está no fim.
                    B = rhs[it.dot]  # Símbolo depois do ponto.
                    if B in self.G.nao_terminais:  # Se é não-terminal.
                        for idx, gamma in self.G.por_lhs[B]:  # Adiciona produções de B com dot=0.
                            novo = Item(idx, 0)
                            if novo not in fecho:
                                novos.add(novo)
            if novos:  # Se tem novos, adiciona e continua.
                fecho |= novos
                alterado = True
        return frozenset(fecho)  # Retorna como conjunto congelado.

    # Calcula o goto: move o ponto para um símbolo X.
    def goto_set(self, itens, X):
        movidos = set()  # Itens onde o ponto avança sobre X.
        for it in itens:
            lhs, rhs = self.producoes[it.prod_idx]
            if it.dot < len(rhs) and rhs[it.dot] == X:
                movidos.add(Item(it.prod_idx, it.dot + 1))
        if not movidos:
            return frozenset()
        return self.closure(movidos)  # Fecha o conjunto.

    # Constrói todos os estados do autômato usando fila.
    def _construir_automato(self):
        inicial = Item(0, 0)  # Item inicial: S' -> .PROGRAM
        I0 = self.closure([inicial])  # Closure do inicial.
        self.C = [I0]  # Lista de estados.
        fila = deque([I0])  # Fila para processar.
        self.estado_id = {I0: 0}  # ID dos estados.
        while fila:
            I = fila.popleft()  # Pega estado atual.
            # Para cada símbolo possível depois do ponto.
            for X in {rhs[it.dot] for it in I for _, rhs in [self.producoes[it.prod_idx]] if it.dot < len(rhs)}:
                J = self.goto_set(I, X)  # Calcula goto.
                if J and J not in self.estado_id:  # Se novo, adiciona.
                    self.estado_id[J] = len(self.C)
                    self.C.append(J)
                    fila.append(J)

    # Preenche as tabelas ACTION e GOTO baseadas nos estados.
    def _construir_tabelas(self):
        for I in self.C:  # Para cada estado.
            i = self.estado_id[I]
            for it in I:  # Para cada item no estado.
                lhs, rhs = self.producoes[it.prod_idx]
                if it.dot < len(rhs):  # Se não acabou a produção.
                    a = rhs[it.dot]  # Símbolo depois do ponto.
                    J = self.goto_set(I, a)
                    if J:
                        j = self.estado_id[J]
                        if a in self.G.terminais:  # Se terminal, shift.
                            self.action[(i, a)] = ('shift', j)
                        else:  # Se não-terminal, goto.
                            self.goto[(i, a)] = j
                else:  # Se dot no fim, reduce.
                    if it.prod_idx == 0:  # Produção inicial: accept.
                        self.action[(i, '$')] = ('accept',)
                    else:
                        # Usa FOLLOW para decidir quando reduzir.
                        for a in self.G.follow[lhs]:
                            self.action[(i, a)] = ('reduce', it.prod_idx)

# PARSER SLR
# Classe que faz a análise sintática usando as tabelas.
class AnalisadorSLR:
    def __init__(self, producoes_gramatica):
        self.gramatica = Gramatica(producoes_gramatica)  # Cria gramática.
        self.builder = ConstrutorSLR(self.gramatica)  # Constrói tabelas.
        self.action = self.builder.action
        self.goto = self.builder.goto
        self.producoes = self.gramatica.producoes

    # Função principal de parsing: analisa a lista de tokens.
    def parse(self, tokens, verbose=True):
        stream = [t.tipo for t in tokens] + ['$']  # Stream de tipos de tokens + $.
        pilha = [0]  # Pilha de estados, começa no 0.
        ip = 0  # Índice no stream.
        passos = 0  # Contador de passos.
        if verbose:  # Se verbose, imprime tabela de passos.
            print(f"{'passo':<5} {'pilha':<30} {'entrada':<30} {'ação'}")
            print("-"*90)
        while True:
            estado = pilha[-1]  # Estado no topo da pilha.
            a = stream[ip]  # Próximo token.
            act = self.action.get((estado, a))  # Ação da tabela.
            if verbose:  # Imprime o passo.
                pilha_str = ",".join(map(str, pilha))
                entrada_str = " ".join(stream[ip:ip+6])
                print(f"{passos:<5} {pilha_str:<30} {entrada_str:<30} {act}")
            if act is None:  # Se não tem ação, erro sintático.
                raise SyntaxError(f"Erro sintático no estado {estado} com token {a}")
            if act[0] == 'shift':  # Shift: adiciona estado novo na pilha, avança.
                pilha.append(act[1])
                ip += 1
            elif act[0] == 'reduce':  # Reduce: aplica produção.
                prod_idx = act[1]
                lhs, rhs = self.producoes[prod_idx]  # Lado esquerdo e direito.
                for _ in rhs:  # Remove da pilha o tamanho da direita.
                    pilha.pop()
                topo = pilha[-1]  # Novo topo.
                goto_estado = self.goto.get((topo, lhs))  # Goto para lhs.
                if goto_estado is None:  # Se não tem, erro.
                    raise SyntaxError(f"GOTO indefinido para estado {topo} e não-terminal {lhs}")
                pilha.append(goto_estado)  # Adiciona novo estado.
            elif act[0] == 'accept':  # Accept: análise ok.
                if verbose:
                    print("\nACEITO: entrada aceita pelo analisador SLR.")
                return True
            passos += 1
            if passos > 10000:  # Previne loop infinito.
                raise RuntimeError("Loop infinito detectado na análise")

# EXECUÇÃO
# Função que pega tokens de um código fonte.
def tokens_da_fonte(codigo):
    lex = Lexico()  # Cria léxico.
    lex.definir_entrada(codigo)  # Define o código.
    lista = []  # Lista de tokens.
    while True:
        tk = lex.proximo_token()  # Pega próximo.
        if tk.tipo == '$':  # Para no fim.
            break
        lista.append(tk)
    return lista

# Função principal: testa o parser com código de exemplo.
def main():
    G = montar_gramatica()  # Monta gramática.
    parser = AnalisadorSLR(G)  # Cria parser.

    # Código de teste com exemplos de todos os elementos.
    codigo_teste = r"""
    var x;
    x = 5 + 3 * (2 + 1);
    write(x);
    read(x);
    if (x > 2) { write(1); } else { write(0); }
    while (x < 10) { x = x + 1; }
    for (x = 0; x < 5; x = x + 1) { write(x); }
    fun minhaFunc(a, b) { write(a); write(b); }
    minhaFunc(10, 20);
    """

    print("=== LÉXICO ===")  # Mostra tokens.
    toks = tokens_da_fonte(codigo_teste)
    for t in toks:
        print(t)
    print(f"Total de tokens: {len(toks)}\n")

    print("=== PARSER SLR ===")  # Faz parsing e mostra passos.
    try:
        ok = parser.parse(toks, verbose=True)
        print("Resultado da análise:", ok)
    except Exception as e:  # Se erro, imprime.
        print("Erro durante parsing:", e)

if __name__ == "__main__":
    main()
