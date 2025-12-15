class PilhaEscopos:
    # Pilha manual pra gerenciar os escopos aninhados do programa
    # Funciona como um Autômato de Pilha da teoria de LFA
    def __init__(self):
        self.itens = []
        self.tamanho = 0
        self.empilhar({})  # escopo global
    
    def empilhar(self, escopo):
        # Adiciona um novo escopo no topo da pilha
        self.itens.append(escopo)
        self.tamanho += 1
    
    def desempilhar(self):
        # Remove o escopo do topo (mantém pelo menos o global)
        if self.tamanho > 1:
            self.tamanho -= 1
            return self.itens.pop()
        return None
    
    def topo(self):
        # Retorna o escopo que tá no topo (escopo atual)
        if self.tamanho > 0:
            return self.itens[self.tamanho - 1]
        return None
    
    def buscar(self, nome):
        # Procura uma variável em todos os escopos, de cima pra baixo
        i = self.tamanho - 1
        while i >= 0:
            escopo = self.itens[i]
            if nome in escopo:
                return escopo[nome]
            i -= 1
        return None
    
    def esta_no_escopo_atual(self, nome):
        # Checa se a variável existe especificadaamente no escopo atual
        escopo_atual = self.topo()
        if escopo_atual is None:
            return False
        return nome in escopo_atual
    
    def escopo_global(self):
        # Retorna o escopo global (sempre o primeiro da pilha)
        if self.tamanho > 0:
            return self.itens[0]
        return None
    
    def contar_variaveis_global(self):
        # Conta quantas variáveis tem no escopo global
        escopo = self.escopo_global()
        if escopo is None:
            return 0
        contador = 0
        for chave in escopo:
            contador += 1
        return contador


class TabelaSimbolos:
    def __init__(self):
        self.escopos = PilhaEscopos()
        self.tipos_validos = ['inteiro', 'flutuante', 'cadeia', 'lógico', 'função']

    def entrar_escopo(self):
        self.escopos.empilhar({})

    def sair_escopo(self):
        self.escopos.desempilhar()

    def declarar(self, nome, tipo='inteiro', linha=0):
        # Declara uma variável no escopo atual
        # Lança exceção se já existir no mesmo escopo
        if self.escopos.esta_no_escopo_atual(nome):
            raise Exception("Variavel '" + nome + "' ja declarada na linha " + str(linha))
        
        escopo_atual = self.escopos.topo()
        escopo_atual[nome] = {'tipo': tipo, 'linha': linha}

    def buscar(self, nome):
        # Busca a variável subindo pela pilha de escopos
        return self.escopos.buscar(nome)


def analisar_semantica(tokens):
    # Análise semântica em duas passadas:
    # Primeira passada: registra todas as declarações
    # Segunda passada: verifica se as variáveis usadas foram declaradas
    tabela = TabelaSimbolos()
    erros = []
    
    # PASSADA 1: Registrar declaracoes
    i = 0
    while i < len(tokens):
        tk = tokens[i]
    
        # Declaracao de variavel: var id ; OU inteiro id ; OU flutuante id ; etc
        if tk.tipo in ['var', 'inteiro', 'flutuante', 'cadeia', 'lógico']:  
            if i + 2 < len(tokens):
                if tokens[i + 1].tipo == 'id' and tokens[i + 2].tipo == 'pv':
                    tipo = 'inteiro' if tk.tipo == 'var' else tk.tipo  
                    nome = tokens[i + 1].lexema
                    try:
                        tabela.declarar(nome, tipo, tokens[i + 1].linha)  
                    except Exception as e:
                        erros.append(str(e))
                    i += 3
                    continue
            
        # Declaracao de funcao: fun id ( params )
        if tk.tipo == 'fun':
            if i + 1 < len(tokens):
                if tokens[i + 1].tipo == 'id':
                    nome = tokens[i + 1].lexema
                    try:
                        tabela.declarar(nome, 'função', tokens[i + 1].linha)
                    except Exception as e:
                        erros.append(str(e))
                    
                    # Registra parametros
                    j = i + 2
                    if j < len(tokens) and tokens[j].tipo == 'ap':
                        j += 1
                        while j < len(tokens) and tokens[j].tipo != 'fp':
                            if tokens[j].tipo == 'id':
                                try:
                                    tabela.declarar(tokens[j].lexema, 'inteiro', tokens[j].linha)
                                except Exception as e:
                                    erros.append(str(e))
                            j += 1
        
        i += 1
    
    # PASSADA 2: Verificar uso de variaveis
    i = 0
    while i < len(tokens):
        tk = tokens[i]
        
        # Pula declaracoes
        if tk.tipo in ['var', 'inteiro', 'flutuante', 'cadeia', 'lógico']:
            while i < len(tokens) and tokens[i].tipo != 'pv':
                i += 1
                i += 1
            continue
        
        if tk.tipo == 'fun':
            while i < len(tokens) and tokens[i].tipo != 'ab':
                i += 1
            continue
        
        # Verifica uso de ID
        if tk.tipo == 'id':
            # Checa se nao e declaracao
            eh_declaracao = False
            
            if i > 0:
                if tokens[i - 1].tipo in ['var', 'fun', 'v']:
                    eh_declaracao = True
            
            if i > 1:
                if tokens[i - 2].tipo == 'ap' and tokens[i - 3].tipo == 'fun':
                    eh_declaracao = True
            
            # Se nao e declaracao, verifica se foi declarada
            if not eh_declaracao:
                if tabela.buscar(tk.lexema) is None:
                    erros.append("Variavel '" + tk.lexema + "' nao declarada na linha " + str(tk.linha))
        
        i += 1
    
        return erros, tabela

