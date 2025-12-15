from analisador_lexico import Lexico
from analisador_sintatico_slr import SLR
from analisador_sintatico import analisar as analisar_descendente
from analisador_semantico import analisar_semantica
from gerador_codigo_mips import GeradorMIPS

def ler_codigo():
    print("=" * 70)
    print("COMPILADOR - Entrada de Codigo")
    print("=" * 70)
    
    # Código de teste com várias estruturas da linguagem
    codigo = """
inteiro x;
flutuante y;
cadeia mensagem;
logico condicao;

fun soma(a, b) {
    inteiro resultado;
    resultado = a + b;
}

x = 10;
y = 3.14;
mensagem = "Ola mundo!";
condicao = verdadeiro;

// REMOVIDO: x++;
// REMOVIDO: y--;

if (x > 3) {
    write("x é maior que 3");
} else {
    write("x não é maior que 3");
}

if (x >= 10) {
    write("x maior ou igual a 10");
}

if (y <= 5.0) {
    write("y menor ou igual a 5");
}

if (x != 5) {
    write("x diferente de 5");
}

for (inteiro i = 0; i < 5; i = i + 1) {
    write("Valor de i: ");
    write(i);
}

while (condicao) {
    write("Dentro do while");
    condicao = falso;
}

read(x);
soma(x, 10);

resultado = x + y;
resultado = x - y;
resultado = x * 2;
resultado = x / 2;
"""
    
    print("Codigo:")
    print(codigo.strip())
    print("=" * 70)
    return codigo

def contar_manual(lista):
    # Conta elementos da lista
    cont = 0
    for item in lista:
        cont += 1
    return cont

def fazer_lexica(codigo):
    print("\n[1] Analise Lexica")
    print("-" * 70)

    lex = Lexico()
    tokens, erros = lex.analisar(codigo)

    if erros:
        print("ERROS encontrados:")
        for e in erros:
            print("  - " + e)
        return None, erros

    # Mostra os primeiros 25 tokens gerados
    print("Tokens gerados (primeiros 25):")
    cont = 0
    for tk in tokens:
        if cont >= 25:
            break
        print("  " + tk.tipo.ljust(10) + " | " + tk.lexema.ljust(12) + " | L:" + str(tk.linha).rjust(2))
        cont += 1
    
    total = contar_manual(tokens)
    if total > 25:
        print("  ... (+" + str(total - 25) + " tokens)")

    print("Total: " + str(total) + " tokens")
    print("-" * 70)
    return tokens, []


def fazer_sintatica(tokens):
    print("\n[2] Analise Sintatica (SLR)")
    print("-" * 70)

    slr = SLR()
    # Faz uma cópia dos tokens pra não afetar as outras fases
    erros = slr.analisar(tokens[:])

    if erros:
        print("ERROS encontrados:")
        cont = 0
        for e in erros:
            if cont >= 5:
                break
            print("  - " + e)
            cont += 1
        
        total = contar_manual(erros)
        if total > 5:
            print("  ... (+" + str(total - 5) + " erros)")
        return False, erros

    print("OK - Analise sintatica passou!")
    print("  Variaveis, funcoes, if/else, for, while: OK")
    print("-" * 70)
    return True, []


def fazer_semantica(tokens):
    print("\n[3] Analise Semantica")
    print("-" * 70)

    erros, tabela = analisar_semantica(tokens)

    if erros:
        print("ERROS encontrados:")
        cont = 0
        for e in erros:
            if cont >= 5:
                break
            print("  - " + e)
            cont += 1
        
        total = contar_manual(erros)
        if total > 5:
            print("  ... (+" + str(total - 5) + " erros)")
        return False, erros

    print("OK - Analise semantica passou!")
    print("  Variaveis declaradas: " + str(tabela.escopos.contar_variaveis_global()))
    print("  Todas as variaveis foram declaradas antes do uso")
    print("-" * 70)
    return True, []


def fazer_geracao_codigo(tokens):
    print("\n[4] Geracao de Codigo MIPS")
    print("-" * 70)

    gerador = GeradorMIPS()
    codigo_mips = gerador.gerar_codigo(tokens)

    # Mostra as primeiras 15 linhas do código gerado
    print("Codigo MIPS gerado (primeiras 15 linhas):")
    linhas = codigo_mips.split('\n')
    
    cont = 0
    for linha in linhas:
        if cont >= 15:
            break
        print(linha)
        cont += 1
    
    total = contar_manual(linhas)
    if total > 15:
        print("... (+" + str(total - 15) + " linhas)")
    
    print("-" * 70)

    # Salva o código MIPS num arquivo
    with open("saida.asm", "w", encoding="utf-8") as f:
        f.write(codigo_mips)

    print("Arquivo gerado: saida.asm")
    return codigo_mips

def main():
    print("\n" + "=" * 70)
    print("COMPILADOR - Trabalho de Compiladores")
    print("Lexico + Sintatico (SLR) + Semantico + Geracao MIPS")
    print("=" * 70)

    # Lê o código de entrada
    codigo = ler_codigo()

    # Fase 1: Análise Léxica
    tokens, erros = fazer_lexica(codigo)
    if erros:
        print("\nERRO: Falha na analise lexica")
        return

    # Fase 2: Análise Sintática (SLR)
    ok, erros = fazer_sintatica(tokens)
    if not ok:
        print("\nERRO: Falha na analise sintatica")
        return

    # Fase 2a: Análise Sintática Descendente Recursiva 
    print("\n[2a] Analise Sintatica Descendente Recursivo")
    print("-" * 70)
    erros_desc = analisar_descendente(tokens[:])
    
    total = contar_manual(erros_desc)
    if erros_desc:
        print("Erros encontrados: " + str(total))
        print("(Normal - descendente nao suporta todas as estruturas)")
    else:
        print("Sem erros no descendente!")
    print("-" * 70)

    # Fase 3: Análise Semântica
    ok, erros = fazer_semantica(tokens)
    if not ok:
        print("\nERRO: Falha na analise semantica")
        return

    # Fase 4: Geração de Código MIPS
    codigo_mips = fazer_geracao_codigo(tokens)

    
    print("\n" + "=" * 70)
    print("SUCESSO! Compilacao concluida")
    print("=" * 70)
    print("Arquivo gerado: saida.asm")
    print("Execute no MARS MIPS Simulator")
    print("=" * 70)


if __name__ == "__main__":
    main()
