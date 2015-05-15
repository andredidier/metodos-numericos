from MaquinaPontoFlutuante import *
import math

class TabelaBissecao:
    def __format__(self, format_spec):
        return "{}|{}|{}|{}|{}|{}|{}|{}".format(
            self.i, self.a, self.b,
            self.fa, self.fb, self.xi,
            self.fxi, self.c)
    def __init__(self, i, a, b, fa, fb, xi, fxi, c):
        self.i = i
        self.a = a
        self.b = b
        self.fa = fa
        self.fb = fb
        self.xi = xi
        self.fxi = fxi
        self.c = c

class Bissecao:
    def executar(self, a, b, l, f):
        c = b - a
        x0 = (a + b) / 2
        while c > l or f(x0) != 0:
            if f(a) * f(x0) < 0:
                b = x0
            if f(a) * f(x0) > 0:
                a = x0
            c = b - a
            x0 = (a + b) / 2

    def criar_tabela(self, i, a, b):
        fa = self.f(self.maquina, a)
        fb = self.f(self.maquina, b)
        xi = (a + b) / NumeroMaquina(self.maquina, 2, 0)
        fxi = self.f(self.maquina, xi)
        c = b - a
        return TabelaBissecao(i, a, b, fa, fb, xi, fxi, c)
        
    def __iter__(self):
        ad = self.a.__decimal__()
        bd = self.b.__decimal__()
        ld = self.l.__decimal__()
        td = (math.log(bd - ad) - math.log(ld)) / math.log(2)
        self.k = math.ceil(td)
        self.tabela = self.criar_tabela(0, self.a, self.b)
        return self

    def __next__(self):
        if self.tabela.i > self.k:
            raise StopIteration
        else:
            tabela = self.tabela
            i = tabela.i + 1
            a = tabela.a
            b = tabela.b
            if tabela.fa * tabela.fxi < 0:
                b = tabela.xi
            if tabela.fa * tabela.fxi > 0:
                a = self.tabela.xi
            self.tabela = self.criar_tabela(i, a, b)
            return tabela
    
    def __call__(self, *args, **kwargs):
        return self.executar(args[0], args[1], args[2], args[3])
    
    def __init__(self, maquina, a, b, l, f):
        self.maquina = maquina
        self.a = NumeroMaquina(maquina, a, 0).numero_maquina()
        self.b = NumeroMaquina(maquina, b, 0).numero_maquina()
        self.l = NumeroMaquina(maquina, l, 0).numero_maquina()
        self.f = f


# Início dos testes
# Exemplo 2.2 do livro (edição 3)
def f22(m, x):
    a1 = NumeroMaquina(m, 2, 0)
    a2 = NumeroMaquina(m, -2, 0)
    n1 = a1 ** (-x)
    n2 = a2 * NumeroMaquina(m, math.sin(x), 0)
    return n1 + n2

m1 = MaquinaPontoFlutuante(10, 2, -3, 3)
m2 = MaquinaPontoFlutuante(10, 7, -99, 99)
b1 = Bissecao(m2, 0, 1, 0.05, f22)

for t in b1:
    print ("{}".format(t))
    x0 = t.xi
print ("x_0 = {}".format(x0))
