from metodos.MetodosAjustamento import *
from metodos.MetodosSistemasEquacoesLineares import *
A = [[3,7,3], [2,1,4], [3,1,1]]
b = [1,1,1]
sistema = LU(A, b)
x = sistema.x
for i,xi in enumerate(sistema.x):
     x[i] = "{:f}".format(round(xi, 8))
     print(*x, sep=", ")