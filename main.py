from analisador_lexico import Lexico, Token
from analisador_sintatico_slr import SLR
from analisador_semantico import Semantico

def ler_codigo():
    # Lê o código de entrada
    print("=" * 80)
    print("COMPILADOR - ENTRADA")
    print("=" * 80)
    
    codigo = """
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
    
    print("CÓDIGO:")
    print(codigo.strip())
    print("=" * 80)
    return codigo


def fazer_lexica(codigo):
    # Fase 1 - Análise Léxica
    print("\n1. ANÁLISE LÉXICA")
    print("=" * 80)
    
    lex = Lexico()
    lex.definir_entrada(codigo)
    tokens = []
    
    # Extrai todos os tokens
    while True:
        tk = lex.proximo_token()
        if tk.tipo == '$':
            break
        print(f"{tk.tipo:10} | {tk.lexema:15} | Linha: {tk.linha:2} | Col: {tk.coluna:2}")
        tokens.append(tk)
    
    print(f"\nTotal: {len(tokens)} tokens")
    print("=" * 80)
    return tokens



def main():
    # Função principal que executa todas as fases
    print("\nINICIANDO COMPILADOR\n")
    
    # Lê o código
    codigo = ler_codigo()
    
    # Fase 1 - Léxica
    tokens = fazer_lexica(codigo)
    if not tokens:
        print("Erro na análise léxica")
        return
    
if __name__ == "__main__":
    main()
