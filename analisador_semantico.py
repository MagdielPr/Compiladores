from analisador_lexico import Lexico, Token, ErroLexico
from analisador_sintatico_slr import SLR

class ErroSemantico(Exception):
    pass


class Simbolo:
    def __init__(self, nome, tipo, categoria, escopo, linha=0, params=None, inicializada=False):
        self.nome = nome
        self.tipo = tipo
        self.categoria = categoria
        self.escopo = escopo
        self.linha = linha
        self.inicializada = inicializada
        
        # params vem vazio? cria lista
        if params is None:
            self.params = []
        else:
            self.params = params


class TabelaSimbolos:
    def __init__(self):
        self.simbolos = {}  # chave: "escopo:nome"
        self.escopo_atual = 'global'

    # insere ou dá erro se já existir
    def inserir(self, simbolo):
        chave = self.escopo_atual + ":" + simbolo.nome
        if chave in self.simbolos:
            erro = "Linha " + str(simbolo.linha) + ": '" + simbolo.nome + "' já declarado"
            raise ErroSemantico(erro)
        self.simbolos[chave] = simbolo

    # busca no escopo atual, se não achar tenta no global
    def buscar(self, nome, escopo=None):
        if escopo is None:
            escopo = self.escopo_atual
        
        chave = escopo + ":" + nome
        if chave in self.simbolos:
            return self.simbolos[chave]
        
        if escopo != 'global':
            chave_global = "global:" + nome
            if chave_global in self.simbolos:
                return self.simbolos[chave_global]
        
        return None

    # imprime a tabela bonitinha
    def imprimir(self):
        print("\n" + "=" * 80)
        print("TABELA DE SÍMBOLOS")
        print("=" * 80)

        grupos_escopo = {}
        
        for chave in self.simbolos:
            simbolo = self.simbolos[chave]
            escopo_nome = simbolo.escopo
            
            if escopo_nome not in grupos_escopo:
                grupos_escopo[escopo_nome] = []
            
            grupos_escopo[escopo_nome].append(simbolo)
        
        for escopo in grupos_escopo:
            lista_simbolos = grupos_escopo[escopo]
            print("\nEscopo: " + escopo)
            print("Nome            Tipo       Cat.         Linha  Ini?   Params")
            print("-" * 80)
            
            for simbolo in lista_simbolos:
                # junta os params com vírgula
                if len(simbolo.params) > 0:
                    params_texto = ""
                    contador = 0
                    while contador < len(simbolo.params):
                        if contador > 0:
                            params_texto = params_texto + ", "
                        params_texto = params_texto + simbolo.params[contador]
                        contador = contador + 1
                else:
                    params_texto = "-"
                
                # sim ou não
                if simbolo.inicializada:
                    ini_texto = "Sim"
                else:
                    ini_texto = "Não"
                
                linha_str = str(simbolo.linha)
                
                print("%-15s %-10s %-12s %-6s %-5s %s" % 
                      (simbolo.nome, simbolo.tipo, simbolo.categoria, 
                       linha_str, ini_texto, params_texto))


class AnalisadorSemantico:
    def __init__(self):
        self.tabela = TabelaSimbolos()
        self.tokens = []
        self.erros = []
        self.avisos = []

    # roda a análise toda
    def analisar(self, tokens):
        self.tokens = tokens
        self.erros = []
        self.avisos = []

        print("\n" + "=" * 80)
        print("ANÁLISE SEMÂNTICA")
        print("=" * 80)

        try:
            self.processar_tokens()
            self.tabela.imprimir()

            # mostra avisos
            if len(self.avisos) > 0:
                print("\n" + "=" * 80)
                print("AVISOS")
                print("=" * 80)
                for aviso in self.avisos:
                    print("  " + aviso)

            # mostra erros
            if len(self.erros) > 0:
                print("\n" + "=" * 80)
                print("ERROS")
                print("=" * 80)
                for erro in self.erros:
                    print("  " + erro)
                return False
            else:
                print("\n" + "=" * 80)
                print(" SEM ERROS")
                print("=" * 80)
                return True
        except ErroSemantico as e:
            self.erros.append(str(e))
            return False

    # passa por todos os tokens procurando var, fun, uso de id
    def processar_tokens(self):
        indice = 0
        while indice < len(self.tokens):
            token = self.tokens[indice]

            # var x;
            if token.tipo == 'var':
                if indice + 2 < len(self.tokens):
                    proximo = self.tokens[indice + 1]
                    depois = self.tokens[indice + 2]
                    if proximo.tipo == 'id' and depois.tipo == 'pv':
                        nome = proximo.lexema
                        linha = proximo.pos
                        try:
                            sim = Simbolo(nome, 'int', 'variavel', self.tabela.escopo_atual, linha)
                            self.tabela.inserir(sim)
                        except ErroSemantico as e:
                            self.erros.append(str(e))
                        indice = indice + 3
                        continue

            # fun soma(a, b)
            if token.tipo == 'fun':
                if indice + 1 < len(self.tokens):
                    proximo = self.tokens[indice + 1]
                    if proximo.tipo == 'id':
                        indice = self.processar_funcao(indice)
                        continue

            # uso de variável
            if token.tipo == 'id':
                self.validar_uso_id(indice)

            # + - * / → não pode usar função
            if token.tipo in ['mais', 'menos', 'mult', 'div']:
                self.validar_operacao(indice)

            indice = indice + 1

    # processa função inteira: params, escopo, corpo
    def processar_funcao(self, indice_inicio):
        nome_funcao = self.tokens[indice_inicio + 1].lexema
        linha = self.tokens[indice_inicio + 1].pos
        parametros = []

        # pega os params entre ( e )
        j = indice_inicio + 3
        while j < len(self.tokens):
            token_atual = self.tokens[j]
            if token_atual.tipo == 'fp':
                break
            if token_atual.tipo == 'id':
                parametros.append(token_atual.lexema)
            j = j + 1

        # função vai pro global
        self.tabela.escopo_atual = 'global'
        try:
            sim = Simbolo(nome_funcao, 'void', 'funcao', 'global', linha, parametros)
            self.tabela.inserir(sim)
        except ErroSemantico as e:
            self.erros.append(str(e))

        # entra no escopo da função
        self.tabela.escopo_atual = nome_funcao

        # params já vêm inicializados
        for param in parametros:
            try:
                sim = Simbolo(param, 'int', 'parametro', nome_funcao, linha, None, True)
                self.tabela.inserir(sim)
            except ErroSemantico as e:
                self.erros.append(str(e))

        # corpo: conta { e }
        k = j + 1
        nivel_bloco = 0
        entrou_no_bloco = False
        while k < len(self.tokens):
            token = self.tokens[k]

            if token.tipo == 'ab':
                nivel_bloco = nivel_bloco + 1
                entrou_no_bloco = True
            elif token.tipo == 'fb':
                nivel_bloco = nivel_bloco - 1
                if nivel_bloco == 0 and entrou_no_bloco:
                    self.tabela.escopo_atual = 'global'
                    return k

            # var dentro da função
            if token.tipo == 'var' and k + 2 < len(self.tokens):
                if self.tokens[k+1].tipo == 'id' and self.tokens[k+2].tipo == 'pv':
                    nome_var = self.tokens[k+1].lexema
                    linha_var = self.tokens[k+1].pos
                    try:
                        sim = Simbolo(nome_var, 'int', 'variavel', nome_funcao, linha_var)
                        self.tabela.inserir(sim)
                    except ErroSemantico as e:
                        self.erros.append(str(e))
            k = k + 1

        self.tabela.escopo_atual = 'global'
        if k < len(self.tokens):
            return k
        else:
            return len(self.tokens) - 1

    # verifica se variável foi declarada, inicializada, etc
    def validar_uso_id(self, indice):
        token = self.tokens[indice]
        nome = token.lexema
        linha = token.pos

        # ignora se for parte de declaração
        if indice > 0:
            anterior = self.tokens[indice - 1]
            if anterior.tipo in ['var', 'fun']:
                return
        if self.eh_parametro_declaracao(indice):
            return

        simbolo = self.tabela.buscar(nome)
        if simbolo is None:
            self.erros.append("Linha " + str(linha) + ": '" + nome + "' não declarado")
            return

        # x = 5 → marca como inicializada
        if indice < len(self.tokens) - 1:
            proximo = self.tokens[indice + 1]
            if proximo.tipo == 'igual':
                if simbolo.categoria in ['variavel', 'parametro']:
                    simbolo.inicializada = True

        # read(x) → também inicializa
        elif indice > 1:
            dois_atras = self.tokens[indice - 2]
            if dois_atras.tipo == 'read':
                if simbolo.categoria in ['variavel', 'parametro']:
                    simbolo.inicializada = True

        # uso normal: soma(x,y) ou só x
        else:
            if indice < len(self.tokens) - 1:
                proximo = self.tokens[indice + 1]
                if proximo.tipo == 'ap':
                    self.validar_chamada_funcao(indice)
            elif simbolo.categoria == 'variavel' and not simbolo.inicializada:
                self.avisos.append("Linha " + str(linha) + ": '" + nome + "' pode não estar inicializada")

    # vê se o id tá dentro de (a, b) na declaração
    def eh_parametro_declaracao(self, indice):
        if indice > 0 and indice < len(self.tokens) - 1:
            anterior = self.tokens[indice - 1]
            proximo = self.tokens[indice + 1]
            if anterior.tipo in ['ap', 'v'] and proximo.tipo in ['v', 'fp']:
                j = indice - 1
                while j >= 0:
                    if self.tokens[j].tipo == 'fun':
                        return True
                    if self.tokens[j].tipo in ['ab', 'fb', 'pv']:
                        break
                    j = j - 1
        return False

    # não pode fazer x + soma()
    def validar_operacao(self, indice):
        if indice > 0 and indice < len(self.tokens) - 1:
            esquerda = self.tokens[indice - 1]
            direita = self.tokens[indice + 1]
            operandos = [esquerda, direita]
            for op in operandos:
                if op.tipo == 'id':
                    simbolo = self.tabela.buscar(op.lexema)
                    if simbolo is not None and simbolo.categoria == 'funcao':
                        self.erros.append("Linha " + str(self.tokens[indice].pos) + ": função em operação")

    # conta argumentos em soma(x, y)
    def validar_chamada_funcao(self, indice):
        nome = self.tokens[indice].lexema
        linha = self.tokens[indice].pos
        simbolo = self.tabela.buscar(nome)
        if simbolo is None or simbolo.categoria != 'funcao':
            if simbolo is not None:
                self.erros.append("Linha " + str(linha) + ": '" + nome + "' não é função")
            return

        num_args = 0
        j = indice + 2
        nivel_parenteses = 0
        
        if j < len(self.tokens):
            token = self.tokens[j]
            if token.tipo != 'fp':
                num_args = 1
        
        while j < len(self.tokens):
            token = self.tokens[j]
            if token.tipo == 'ap':
                nivel_parenteses = nivel_parenteses + 1
            elif token.tipo == 'fp':
                if nivel_parenteses == 0:
                    break
                nivel_parenteses = nivel_parenteses - 1
            elif token.tipo == 'v' and nivel_parenteses == 0:
                num_args = num_args + 1
            j = j + 1

        if num_args != len(simbolo.params):
            self.erros.append("Linha " + str(linha) + ": '" + nome + 
                            "' espera " + str(len(simbolo.params)) + 
                            " arg(s), recebeu " + str(num_args))


# teste completo
def main():
    print("=" * 80)
    print("COMPILADOR")
    print("=" * 80)

    codigo_teste = """
    var x;
    var y;
    fun soma(a, b) {
        var resultado;
        resultado = a + b;
        write(resultado);
    }
    x = 5;
    y = x + 3;
    write(y);
    soma(x, y);
    """

    print("\nCódigo:")
    print(codigo_teste)

    try:
        print("\n" + "=" * 80)
        print("LÉXICA")
        print("=" * 80)
        lex = Lexico()
        lex.definir_entrada(codigo_teste)
        tokens = []
        while True:
            tk = lex.proximo_token()
            if tk.tipo == '$':
                break
            tokens.append(tk)
        print(" " + str(len(tokens)) + " tokens")

        print("\n" + "=" * 80)
        print("SINTÁTICA")
        print("=" * 80)
        slr = SLR()
        slr.analisar(tokens)

        sem = AnalisadorSemantico()
        if sem.analisar(tokens):
            print("\n" + "=" * 80)
            print(" OK")
            print("=" * 80)
    except Exception as e:
        print("\n ERRO: " + str(e))

if __name__ == "__main__":
    main()
