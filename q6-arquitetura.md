De modo abstrato, o compilador é um programa que converte código de uma
linguagem para outra. Como se fosse uma função do tipo `compilador(str) -> str`.
No caso de compiladores que emitem código de máquina ou bytecode, seria mais
preciso dizer `compilador(str) -> bytes`, mas a idéia básica é a mesma.

De forma geral o processo é dividido em etapas como abaixo

```python
def compilador(x1: str) -> str | bytes:
    x2 = lex(x1)        # análise léxica
    x3 = parse(x2)      # análise sintática
    x4 = analysis(x3)   # análise semântica
    x5 = optimize(x4)   # otimização
    x6 = codegen(x5)    # geração de código
    return x6
```

Defina brevemente o que cada uma dessas etapas realizam e marque quais seriam os
tipos de entrada e saída de cada uma dessas funções. Explique de forma clara o
que eles representam. Você pode usar exemplos de linguagens e/ou compiladores
conhecidos para ilustrar sua resposta. Salve sua resposta nesse arquivo.

# lex(?) -> ?
Complete as ? e responda aqui!

Nessa etapa ele recebe o código fonte como uma string e transforma-o em uma lista de tokens.
Um token é uma unidade léxica, como palavras-chave (if, while), identificadores (x, contador), operadores (+, -, ==), literais (42, "texto"), etc.
Exemplo em python: A string x = 2 + y pode ser transformada na lista de tokens:
  [Token(ID, "x"), Token(OP, "="), Token(NUM, "2"), Token(OP, "+"), Token(ID, "y")]

# parse(?) -> ?
 Aqui ele transforma a lista de tokens em uma árvore sintática abstrata (AST - Abstract Syntax Tree), que representa a estrutura gramatical do programa.
A AST organiza os tokens conforme as regras da gramática da linguagem.
Exemplo: A expressão x = 2 + y vira algo como em python: 
Assign(
    target=Variable("x"),
    value=Add(
        left=Number(2),
        right=Variable("y")
    )
)



# analysis(?) -> ?
A análise semântica pega a AST gerada pelo parser e verifica se o código faz sentido de acordo com as regras da linguagem. Ela checa coisas como tipos de dados compatíveis, se variáveis foram declaradas antes do uso, e se os escopos estão corretos. Por exemplo, se você tentar somar um número com um texto ou usar uma variável que não existe, o compilador aponta esses erros aqui. A saída é uma AST anotada com informações de tipos e escopos, ou mensagens de erro se encontrar problemas.

Exemplo com erro:

c
int main() {
    int x = 10;
    x = "oi";  // Erro semântico! Não pode colocar texto em um int.
    return x;
}
Saída: O compilador grita: "Error: cannot convert ‘const char’ to ‘int’"* e para a compilação.

# optimize(?) -> ?
Já a otimização pega esse código verificado e tenta deixá-lo mais eficiente sem mudar o que ele faz. Ela simplifica cálculos que podem ser resolvidos durante a compilação, remove trechos de código que nunca serão executados e faz outras melhorias. Por exemplo, se você escrever "int x = 2 + 3 * 5;", o compilador pode calcular isso direto e transformar em "int x = 17;". Ou se tiver um "if(false)" com código dentro, ele remove tudo porque sabe que nunca vai executar. A saída é uma versão mais enxuta do código, ainda em formato intermediário, pronta para virar código de máquina ou bytecode na próxima etapa.


# codegen(?) -> ?

Converte o código intermediário (IR ou AST otimizada) em código de máquina, bytecode ou outra linguagem.
Exemplo (C → x86-64):

c
int soma(int a, int b) {
    return a + b;
}

Saída (Assembly x86-64):

asm
soma:
    add edi, esi   ; Soma os registradores a e b.
    mov eax, edi   ; Armazena o resultado em eax (retorno).
    ret



    Com isso fica assim : 
    Código Fonte ("int x = 2;")
    -> lex -> Tokens ["int", "x", "=", "2", ";"]
    -> parse -> AST (Declaração de variável)
    -> analysis -> AST anotada (tipo int verificado)
    -> optimize -> AST/IR simplificada (x = 2)
    -> codegen -> mov [rbp-4], 2 (x86-64)