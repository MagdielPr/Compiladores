
from analisador_lexico import AnalisadorLexico, TipoToken
from analisador_sintatico import AnalisadorSintatico
import os

def imprimir_separador(titulo="", largura=50):
    """Imprime um separador visual com título opcional"""
    print("=" * largura)
    if titulo:
        print(titulo.center(largura))
        print("=" * largura)

def imprimir_subsecao(titulo, largura=30):
    """Imprime um título de subseção"""
    print(f"\n{titulo}")
    print("-" * largura)

def main():
    """Função principal para testar o analisador léxico e sintático"""
    
    # Código-fonte de exemplo com vários casos de teste
    codigo_fonte = '''
    // Programa de exemplo para testar o analisador léxico
    
    inteiro x = 10;
    flutuante y = 3.14;
    cadeia msg = "Olá mundo";
    logico flag = verdadeiro;
    logico flag2 = falso;
    
    se (x > 5) {
        escreva(msg & " - x é maior que 5");
    } senao {
        escreva("x é menor ou igual a 5");
        x++;
    }
    
    // Teste de laços
    para (inteiro i = 0; i < 10; i++) {
        se (i % 2 == 0) {
            escreva("Par: " & i);
        }
    }
    
    enquanto (x > 0) {
        x--;
        leia(y);
    }
    
    // Teste de operadores
    inteiro a = 5;
    inteiro b = 10;
    logico resultado = (a >= b) && (a != b) || (a < 20);
    
    // Teste de arrays
    inteiro[100] numeros;
    numeros[0] = 42;
    numeros[1] = numeros[0] * 2;
    
    /* Comentário 
       multi-linha
       para teste */
    
    flutuante pi = 3.14159;
    cadeia nome = "Compilador";
    
    inicio
        escreva("Início do programa");
    fim
    '''
    
    # Cria o analisador
    analisador = AnalisadorLexico()
    
    # Analisa o código
    tokens, erros = analisador.analisar(codigo_fonte)
    
    # Exibe os resultados
    imprimir_separador("ANALISADOR LÉXICO - RESULTADOS")
    
    imprimir_subsecao("TOKENS ENCONTRADOS")
    if tokens:
        for i, token in enumerate(tokens, 1):
            print(f"{i:3d}. {token}")
    else:
        print("Nenhum token encontrado.")
    
    # Exibe erros léxicos se houver
    if erros:
        imprimir_subsecao(f"ERROS LÉXICOS ENCONTRADOS ({len(erros)})")
        for i, erro in enumerate(erros, 1):
            print(f"{i:3d}. {erro}")
    else:
        print("\n✓ NENHUM ERRO LÉXICO ENCONTRADO.")
    
    # Análise sintática
    if not erros:
        imprimir_subsecao("ANÁLISE SINTÁTICA")
        print("Iniciando análise sintática...")
        sintatico = AnalisadorSintatico(tokens)
        if sintatico.parse():
            print("✓ Linguagem aceita")
        else:
            print(f" {len(sintatico.erros)} erro(s) sintático(s) encontrado(s)")
            imprimir_subsecao("ERROS SINTÁTICOS")
            for i, erro in enumerate(sintatico.erros, 1):
                print(f"{i:3d}. {erro}")
    
    # Exibe estatísticas
    stats = analisador.obter_estatisticas()
    imprimir_subsecao("ESTATÍSTICAS")
    print(f"Total de tokens: {stats['total_tokens']}")
    print(f"Total de erros léxicos: {stats['total_erros']}")
    
    imprimir_subsecao("DISTRIBUIÇÃO POR TIPO")
    for tipo, quantidade in sorted(stats['tipos_tokens'].items()):
        print(f"{tipo:<25}: {quantidade}")

def testar_casos_erro():
    """Testa casos específicos que devem gerar erros"""
    imprimir_separador("TESTE DE CASOS DE ERRO")
    
    casos_teste = [
        {
            'nome': 'Cadeia não terminada',
            'codigo': 'cadeia teste = "hello world sem fechamento',
            'descricao': 'String que não foi fechada com aspas'
        },
        {
            'nome': 'Número com ponto final',
            'codigo': 'flutuante x = 123.;',
            'descricao': 'Número flutuante mal formado'
        },
        {
            'nome': 'Caractere inválido',
            'codigo': 'inteiro y = @123;',
            'descricao': 'Símbolo @ não reconhecido'
        },
        {
            'nome': 'Comentário não fechado',
            'codigo': 'inteiro z = 10; /* comentário sem fechamento',
            'descricao': 'Comentário multi-linha não terminado'
        },
        {
            'nome': 'Identificador inválido - número no início',
            'codigo': '123abc = 10;',
            'descricao': 'Identificador começando com número'
        },
        {
            'nome': 'Identificador inválido - após número',
            'codigo': 'inteiro 456def = 20;',
            'descricao': 'Número seguido de letras'
        },
        {
            'nome': 'Operador pipe simples',
            'codigo': 'inteiro x = 5 | 3;',
            'descricao': 'Uso de | em vez de ||'
        },
        {
            'nome': 'Cadeia com quebra de linha',
            'codigo': 'cadeia msg = "linha1\nlinha2";',
            'descricao': 'String com quebra de linha não escapada'
        },
        {
            'nome': 'Múltiplos erros',
            'codigo': 'inteiro @x = 123.; cadeia y = "sem fechamento',
            'descricao': 'Código com vários tipos de erro'
        }
    ]
    
    analisador = AnalisadorLexico()
    
    for i, caso in enumerate(casos_teste, 1):
        print(f"\n{i}. {caso['nome']}:")
        print(f"   Descrição: {caso['descricao']}")
        print(f"   Código: {caso['codigo']}")
        
        tokens, erros = analisador.analisar(caso['codigo'])
        
        if erros:
            print(f"   ✓ Erro(s) léxico(s) detectado(s):")
            for j, erro in enumerate(erros):
                print(f"     {j+1}. {erro}")
        else:
            print("   ✗ Nenhum erro léxico detectado (inesperado)")
        
        if tokens:
            print(f"   Tokens válidos encontrados: {len(tokens)}")
            sintatico = AnalisadorSintatico(tokens)
            print(f"   Iniciando análise sintática para caso {i}...")
            if sintatico.parse():
                print("   ✓ Análise sintática bem-sucedida")
            else:
                print(f"   {len(sintatico.erros)} erro(s) sintático(s) encontrado(s)")
                for j, erro in enumerate(sintatico.erros, 1):
                    print(f"     {j+1}. {erro}")

def testar_casos_complexos():
    """Testa casos mais complexos de análise léxica e sintática"""
    imprimir_separador("TESTE DE CASOS COMPLEXOS")
    
    casos_complexos = [
        {
            'nome': 'Expressão matemática complexa',
            'codigo': 'resultado = (a + b) * (c - d) / (e >= f && g != h);'
        },
        {
            'nome': 'Múltiplas cadeias e concatenações',
            'codigo': 'cadeia frase = "Olá" & " " & "mundo" & "!";'
        },
        {
            'nome': 'Array multidimensional',
            'codigo': 'inteiro[10][20] matriz; matriz[i][j] = valores[k++];'
        },
        {
            'nome': 'Estrutura condicional aninhada',
            'codigo': '''
            se (x > 0) {
                se (y < 10) {
                    escreva("Ambas condições verdadeiras");
                } senao {
                    escreva("Apenas primeira condição");
                }
            }
            '''
        },
        {
            'nome': 'Laço com múltiplos operadores',
            'codigo': 'para (inteiro i = 0; i <= 100; i += 2) { soma += numeros[i]; }'
        }
    ]
    
    analisador = AnalisadorLexico()
    
    for i, caso in enumerate(casos_complexos, 1):
        print(f"\n{i}. {caso['nome']}:")
        print(f"   Código: {caso['codigo'].strip()}")
        
        tokens, erros = analisador.analisar(caso['codigo'])
        
        print(f"   Tokens encontrados: {len(tokens)}")
        if erros:
            print(f"   Erros léxicos encontrados: {len(erros)}")
            for erro in erros:
                print(f"     - {erro}")
        else:
            print("   ✓ Análise léxica bem-sucedida")
            sintatico = AnalisadorSintatico(tokens)
            print(f"   Iniciando análise sintática para caso {i}...")
            if sintatico.parse():
                print("   ✓ Análise sintática bem-sucedida")
            else:
                print(f"   {len(sintatico.erros)} erro(s) sintático(s) encontrado(s)")
                for j, erro in enumerate(sintatico.erros, 1):
                    print(f"     {j+1}. {erro}")

def menu_interativo():
    """Permite ao usuário testar o analisador interativamente"""
    analisador = AnalisadorLexico()
    
    while True:
        imprimir_separador("MODO INTERATIVO")
        print("Digite o código para analisar (ou 'sair' para terminar):")
        print("Para código multi-linha, termine com '###' em uma linha separada")
        
        linhas = []
        while True:
            linha = input("> ")
            if linha.lower() == 'sair':
                return
            if linha == '###':
                break
            linhas.append(linha)
        
        if not linhas:
            continue
            
        codigo = '\n'.join(linhas)
        
        # Analisa o código
        tokens, erros = analisador.analisar(codigo)
        
        # Mostra resultados
        print(f"\n Resultado da análise léxica:")
        print(f"   Tokens: {len(tokens)}")
        print(f"   Erros léxicos: {len(erros)}")
        
        if tokens:
            print("\n Tokens encontrados:")
            for i, token in enumerate(tokens, 1):
                print(f"   {i:2d}. {token}")
        
        if erros:
            print("\n Erros léxicos encontrados:")
            for i, erro in enumerate(erros, 1):
                print(f"   {i:2d}. {erro}")
        
        if not erros:
            print(f"\n Resultado da análise sintática:")
            sintatico = AnalisadorSintatico(tokens)
            print("   Iniciando análise sintática...")
            if sintatico.parse():
                print("   ✓ Linguagem aceita")
            else:
                print(f"   {len(sintatico.erros)} erro(s) sintático(s) encontrado(s)")
                for i, erro in enumerate(sintatico.erros, 1):
                    print(f"   {i:2d}. {erro}")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    try:
        # Executa todos os testes
        main()
        testar_casos_erro()
        testar_casos_complexos()
        
        # Pergunta se o usuário quer usar o modo interativo
        print("\n" + "="*50)
        resposta = input("Deseja testar o analisador interativamente? (s/n): ").lower()
        if resposta in ['s', 'sim', 'y', 'yes']:
            menu_interativo()
        
        print("\n Testes concluídos com sucesso!")
        
    except KeyboardInterrupt:
        print("\n\n Execução interrompida pelo usuário.")
    except Exception as e:
        print(f"\n Erro inesperado: {e}")