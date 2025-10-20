from analisador_lexico import Lexico, Token, ErroLexico
from analisador_sintatico_slr import SLR

class ErroSemantico(Exception):
    """Exceção para erros semânticos"""
    pass

class Simbolo:
    """Representa um símbolo na tabela de símbolos"""
    def __init__(self, nome, tipo, categoria, escopo, linha=0, params=None, inicializada=False):
        self.nome = nome
        self.tipo = tipo  # 'int', 'void'
        self.categoria = categoria  # 'variavel', 'funcao', 'parametro'
        self.escopo = escopo
        self.linha = linha
        self.params = params if params else []
        self.inicializada = inicializada

class TabelaSimbolos:
    """Gerencia escopos e símbolos"""
    def __init__(self):
        self.simbolos = {}  # {nome: Simbolo}
        self.escopo_atual = 'global'
    
    def inserir(self, simbolo):
        """Insere símbolo"""
        chave = f"{simbolo.escopo}:{simbolo.nome}"
        if chave in self.simbolos:
            raise ErroSemantico(
                f"Linha {simbolo.linha}: '{simbolo.nome}' já declarado no escopo '{simbolo.escopo}'"
            )
        self.simbolos[chave] = simbolo
    
    def buscar(self, nome, escopo=None):
        """Busca símbolo no escopo atual ou global"""
        if escopo is None:
            escopo = self.escopo_atual
        
        # Busca no escopo atual
        chave = f"{escopo}:{nome}"
        if chave in self.simbolos:
            return self.simbolos[chave]
        
        # Busca no global
        if escopo != 'global':
            chave = f"global:{nome}"
            if chave in self.simbolos:
                return self.simbolos[chave]
        
        return None
    
    def imprimir(self):
        """Imprime a tabela de símbolos"""
        print("\n" + "=" * 80)
        print("TABELA DE SÍMBOLOS")
        print("=" * 80)
        
        # Agrupa por escopo
        escopos = {}
        for chave, sim in self.simbolos.items():
            if sim.escopo not in escopos:
                escopos[sim.escopo] = []
            escopos[sim.escopo].append(sim)
        
        for escopo, simbolos in escopos.items():
            print(f"\nEscopo: {escopo}")
            print(f"{'Nome':<15} {'Tipo':<10} {'Categoria':<12} {'Linha':<6} {'Inic.':<6} {'Params'}")
            print("-" * 80)
            for sim in simbolos:
                params_str = ', '.join(sim.params) if sim.params else '-'
                inic = 'Sim' if sim.inicializada else 'Não'
                print(f"{sim.nome:<15} {sim.tipo:<10} {sim.categoria:<12} {sim.linha:<6} {inic:<6} {params_str}")

class AnalisadorSemantico:
    """Analisador semântico simplificado"""
    
    def __init__(self):
        self.tabela = TabelaSimbolos()
        self.tokens = []
        self.erros = []
        self.avisos = []
        self.escopo_atual = 'global'
    
    def analisar(self, tokens):
        """Executa análise semântica"""
        self.tokens = tokens
        self.erros = []
        self.avisos = []
        
        print("\n" + "=" * 80)
        print("ANÁLISE SEMÂNTICA")
        print("=" * 80)
        
        try:
            # Processa tokens sequencialmente
            self.processar_tokens()
            
            # Imprime tabela
            self.tabela.imprimir()
            
            # Mostra avisos
            if self.avisos:
                print("\n" + "=" * 80)
                print("AVISOS")
                print("=" * 80)
                for aviso in self.avisos:
                    print(f"  {aviso}")
            
            # Mostra erros
            if self.erros:
                print("\n" + "=" * 80)
                print("ERROS SEMÂNTICOS")
                print("=" * 80)
                for erro in self.erros:
                    print(f" {erro}")
                return False
            else:
                print("\n" + "=" * 80)
                print(" ANÁLISE SEMÂNTICA CONCLUÍDA SEM ERROS")
                print("=" * 80)
                return True
                
        except ErroSemantico as e:
            self.erros.append(str(e))
            return False
    
    def processar_tokens(self):
        """Processa todos os tokens"""
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            
            # Declaração de variável: var id;
            if token.tipo == 'var' and i + 2 < len(self.tokens):
                if self.tokens[i + 1].tipo == 'id' and self.tokens[i + 2].tipo == 'pv':
                    nome = self.tokens[i + 1].lexema
                    linha = self.tokens[i + 1].pos
                    try:
                        sim = Simbolo(nome, 'int', 'variavel', self.escopo_atual, linha)
                        self.tabela.inserir(sim)
                    except ErroSemantico as e:
                        self.erros.append(str(e))
                    i += 3
                    continue
            
            # Declaração de função: fun id (params) { ... }
            if token.tipo == 'fun' and i + 1 < len(self.tokens):
                if self.tokens[i + 1].tipo == 'id':
                    i = self.processar_funcao(i)
                    continue
            
            # Uso de identificador
            if token.tipo == 'id':
                self.validar_uso_id(i)
            
            # Validações de operações
            if token.tipo in ['mais', 'menos', 'mult', 'div']:
                self.validar_operacao(i)
            
            i += 1
    
    def processar_funcao(self, i):
        """Processa declaração de função e seu corpo"""
        nome_func = self.tokens[i + 1].lexema
        linha = self.tokens[i + 1].pos
        
        # Coleta parâmetros
        params = []
        j = i + 3  # Pula 'fun', 'id', '('
        while j < len(self.tokens) and self.tokens[j].tipo != 'fp':
            if self.tokens[j].tipo == 'id':
                params.append(self.tokens[j].lexema)
            j += 1
        
        # Insere função no global
        self.escopo_atual = 'global'
        self.tabela.escopo_atual = 'global'
        try:
            sim = Simbolo(nome_func, 'void', 'funcao', 'global', linha, params)
            self.tabela.inserir(sim)
        except ErroSemantico as e:
            self.erros.append(str(e))
        
        # Entra no escopo da função
        self.escopo_atual = nome_func
        self.tabela.escopo_atual = nome_func
        
        # Insere parâmetros
        for param in params:
            try:
                param_sim = Simbolo(param, 'int', 'parametro', nome_func, linha, inicializada=True)
                self.tabela.inserir(param_sim)
            except ErroSemantico as e:
                self.erros.append(str(e))
        
        # Procura o abre bloco e processa até o fecha bloco
        k = j + 1  # Depois do ')'
        nivel = 0
        encontrou_ab = False
        
        while k < len(self.tokens):
            if self.tokens[k].tipo == 'ab':
                nivel += 1
                encontrou_ab = True
            elif self.tokens[k].tipo == 'fb':
                nivel -= 1
                if nivel == 0 and encontrou_ab:
                    # Saiu da função
                    self.escopo_atual = 'global'
                    self.tabela.escopo_atual = 'global'
                    return k
            
            # Processa tokens dentro da função (MANTÉM O ESCOPO)
            # Declaração de variável dentro da função
            if self.tokens[k].tipo == 'var' and k + 2 < len(self.tokens):
                if self.tokens[k + 1].tipo == 'id' and self.tokens[k + 2].tipo == 'pv':
                    nome_var = self.tokens[k + 1].lexema
                    linha_var = self.tokens[k + 1].pos
                    try:
                        var_sim = Simbolo(nome_var, 'int', 'variavel', nome_func, linha_var)
                        self.tabela.inserir(var_sim)
                    except ErroSemantico as e:
                        self.erros.append(str(e))
            
            k += 1
        
        # Se chegou aqui, volta ao global
        self.escopo_atual = 'global'
        self.tabela.escopo_atual = 'global'
        return k if k < len(self.tokens) else len(self.tokens) - 1
    
    def validar_uso_id(self, i):
        """Valida uso de identificador"""
        token = self.tokens[i]
        nome = token.lexema
        linha = token.pos
        
        # Ignora declarações
        if i > 0 and self.tokens[i - 1].tipo in ['var', 'fun']:
            return
        
        # Ignora parâmetros em declaração
        if self.eh_parametro_declaracao(i):
            return
        
        # Verifica se existe
        sim = self.tabela.buscar(nome)
        if not sim:
            self.erros.append(f"Linha {linha}: '{nome}' não declarado")
            return
        
        # Atribuição: marca como inicializada
        if i < len(self.tokens) - 1 and self.tokens[i + 1].tipo == 'igual':
            if sim.categoria in ['variavel', 'parametro']:
                sim.inicializada = True
        
        # Read: marca como inicializada
        elif i > 1 and self.tokens[i - 2].tipo == 'read':
            if sim.categoria in ['variavel', 'parametro']:
                sim.inicializada = True
        
        # Uso: verifica inicialização
        else:
            # Chamada de função: valida argumentos
            if i < len(self.tokens) - 1 and self.tokens[i + 1].tipo == 'ap':
                self.validar_chamada_funcao(i)
            # Uso comum: verifica inicialização
            elif sim.categoria == 'variavel' and not sim.inicializada:
                self.avisos.append(f"Linha {linha}: '{nome}' pode não estar inicializada")
    
    def eh_parametro_declaracao(self, i):
        """Verifica se é parâmetro em declaração de função"""
        if i > 0 and i < len(self.tokens) - 1:
            if self.tokens[i - 1].tipo in ['ap', 'v'] and self.tokens[i + 1].tipo in ['v', 'fp']:
                # Procura 'fun' antes
                j = i - 1
                while j >= 0:
                    if self.tokens[j].tipo == 'fun':
                        return True
                    if self.tokens[j].tipo in ['ab', 'fb', 'pv']:
                        break
                    j -= 1
        return False
    
    def validar_operacao(self, i):
        """Valida operação aritmética"""
        if i > 0 and i < len(self.tokens) - 1:
            esq = self.tokens[i - 1]
            dir = self.tokens[i + 1]
            
            # Verifica operandos
            for operando in [esq, dir]:
                if operando.tipo == 'id':
                    sim = self.tabela.buscar(operando.lexema)
                    if sim and sim.categoria == 'funcao':
                        self.erros.append(
                            f"Linha {self.tokens[i].pos}: Não pode usar função '{sim.nome}' em operação aritmética"
                        )
    
    def validar_chamada_funcao(self, i):
        """Valida chamada de função"""
        nome = self.tokens[i].lexema
        linha = self.tokens[i].pos
        sim = self.tabela.buscar(nome)
        
        if not sim:
            return  # Erro já reportado em validar_uso_id
        
        if sim.categoria != 'funcao':
            self.erros.append(f"Linha {linha}: '{nome}' não é uma função")
            return
        
        # Conta argumentos
        num_args = 0
        j = i + 2  # Pula 'id' e '('
        nivel = 0
        if j < len(self.tokens) and self.tokens[j].tipo != 'fp':
            num_args = 1
            while j < len(self.tokens):
                if self.tokens[j].tipo == 'ap':
                    nivel += 1
                elif self.tokens[j].tipo == 'fp':
                    if nivel == 0:
                        break
                    nivel -= 1
                elif self.tokens[j].tipo == 'v' and nivel == 0:
                    num_args += 1
                j += 1
        
        if num_args != len(sim.params):
            self.erros.append(
                f"Linha {linha}: '{nome}' espera {len(sim.params)} argumento(s), mas recebeu {num_args}"
            )

def main():
    print("=" * 80)
    print("COMPILADOR COMPLETO")
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
        # Léxico
        print("\n" + "=" * 80)
        print("ANÁLISE LÉXICA")
        print("=" * 80)
        
        lex = Lexico()
        lex.definir_entrada(codigo_teste)
        tokens = []
        while True:
            tk = lex.proximo_token()
            if tk.tipo == '$':
                break
            tokens.append(tk)
        
        print(f" {len(tokens)} tokens identificados")
        
        # Sintático
        print("\n" + "=" * 80)
        print("ANÁLISE SINTÁTICA SLR")
        print("=" * 80)
        slr = SLR()
        slr.analisar(tokens)
        
        # Semântico
        semantico = AnalisadorSemantico()
        resultado = semantico.analisar(tokens)
        
        if resultado:
            print("\n" + "=" * 80)
            print(" COMPILAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 80)
        
    except Exception as e:
        print(f"\n Erro: {e}")

if __name__ == "__main__":
    main()