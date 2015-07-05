from metodos.MetodosAjustamento import *
from metodos.MetodosSistemasEquacoesLineares import *

#tabela4_1 = [
#             {'x': 1, 'f': 1.3},
#             {'x': 2, 'f': 1.8},
#             {'x': 3, 'f': 2.2},
#             {'x': 4, 'f': 0.4},
#             {'x': 5, 'f': 1.1},
#             {'x': 6, 'f': 3.0},
#             {'x': 7, 'f': 1.1},
#             {'x': 8, 'f': 0.8},
#             {'x': 9, 'f': 0.1}
#             ]
#funcoes4_1 = [ lambda x : 1, lambda x : x  ]

#exemplo4_1 = MMQ(tabela4_1, funcoes4_1)

#exemplo4_1_SEL = LU(exemplo4_1.A, exemplo4_1.b)

#print("Exemplo 4.1")
#print(exemplo4_1_SEL.x)

funcoes = {
           'a': math.sin,
           'b': math.cos,
           'c': math.log,
           'd': math.exp,
           'e': lambda x : x ** 5,
           'f': lambda x : x ** 4,
           'g': lambda x : x ** 3,
           'h': lambda x : x ** 2,
           'i': lambda x : x,
           'j': lambda _ : 1,
           }

try:
    arquivo = open("entrada-projeto2.txt", "r")
    quantidade_casos = int(arquivo.readline())
    
    for caso in range(quantidade_casos):
        quantidade_pontos = int(arquivo.readline())
        linha_tabelamento = arquivo.readline()
        pares = linha_tabelamento.split(";")
        tabelamento = []
        for par in pares:
            par_split = list(map(lambda x : x.strip(), par.split(",")))
            x = eval(par_split[0])
            f = eval(par_split[1])
            tabelamento.append({"x": x, "f": f})
        quantidade_funcoes = int(arquivo.readline())
        linha_funcoes = arquivo.readline() 
        letras_funcoes = map(lambda x : x.strip(), linha_funcoes.split("+"))
        ajustamento = MMQ(tabelamento, list(map(lambda f: funcoes[f], letras_funcoes)))
        sistema = LU(ajustamento.A, ajustamento.b)
        x = sistema.x
        for i,xi in enumerate(sistema.x):
            x[i] = "{:f}".format(round(xi, 8))
        print("Caso {}:".format(caso+1))
        print("\t", end="")
        print(*x, sep=", ")
finally:
    if arquivo:
        arquivo.close()
        
        
        