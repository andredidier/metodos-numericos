from MaquinaPontoFlutuante import *
from Metodos import *
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

class Bissecao(MetodoIterativo):
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
    
    def __init__(self, maquina, a, b, l, f):
        self.maquina = maquina
        self.a = NumeroMaquina(maquina, a, 0).numero_maquina()
        self.b = NumeroMaquina(maquina, b, 0).numero_maquina()
        self.l = NumeroMaquina(maquina, l, 0).numero_maquina()
        self.f = f

class IterativoGerador(MetodoIterativo):
    def calcular_x_iteracao(self, x_anterior):
        None
        
    def calcular_iteracao(self, anterior):
        if anterior:
            x_anterior = anterior["x"]
            i = anterior["i"]
        else:
            x_anterior = self.x0
            i = 0
        x = self.calcular_x_iteracao(x_anterior)
        valor_f = self.f(x_anterior)
        erro_absoluto = abs(x - x_anterior)
        return {"i": i+1, "x": x, "valor_f": valor_f,
                "erro_absoluto": erro_absoluto}

    def deve_parar(self):
        i = self.iteracao["i"]
        err = self.iteracao["erro_absoluto"]
        valor_f = self.iteracao["valor_f"]
        return self.parada(i, err, valor_f)

    def __init__(self, maquina, x0, f, parada):
        self.maquina = maquina
        self.x0 = NumeroMaquina(maquina, x0, 0).numero_maquina()
        self.f = f
        self.parada = parada

class Halley(IterativoGerador):
    def calcular_x_iteracao(self, x_anterior):
        valor_f = self.f(x_anterior)
        valor_df = self.df(x_anterior)
        valor_ddf = self.ddf(x_anterior)
        numerador = self.dois * valor_f * valor_df
        denominador1 = self.dois * (valor_df ** self.dois)
        denominador2 = valor_f * valor_ddf
        denominador = denominador1 - denominador2
        return x_anterior - numerador / denominador
    
    
    def __init__(self, maquina, x0, f, df, ddf, parada):
        super().__init__(maquina, x0, f, parada)
        self.maquina = maquina
        self.df = df
        self.ddf = ddf
        self.dois = NumeroMaquina(maquina, 2, 0).numero_maquina()
    
 
class NewtonRaphson(IterativoGerador):
    def calcular_x_iteracao(self, x_anterior):
        valor_f = self.f(x_anterior)
        valor_df = self.df(x_anterior)
        return x_anterior - valor_f / valor_df

    def __init__(self, maquina, x0, f, df, parada):
        super().__init__(maquina, x0, f, parada)
        self.df = df

# Início dos testes
def parada_geral(i, erro_absoluto, valor_f):
    if i > 50:
        return True
    if erro_absoluto <= 0.000001 and valor_f <= 0.000001:
        return True
    
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

# Método de Newton-Raphson
def f24(x):
    return x * NumeroMaquina(m2, math.log(x), 0) - \
        NumeroMaquina(m2, 1, 0)
def df24(x):
    return NumeroMaquina(m2, math.log(x), 0) + NumeroMaquina(m2, 1, 0)

def ddf24(x):
    return NumeroMaquina(m2, 1, 0) / x

n1 = NewtonRaphson(m2, 1.75, f24, df24, parada_geral)
for t in n1:
    print ("{}".format(t))
    x0=t["x"]

print ("x0 = {}".format(x0))

n1 = Halley(m2, 1.75, f24, df24, ddf24, parada_geral)
for t in n1:
    print ("{}".format(t))
    x0=t["x"]

print ("x0 = {}".format(x0))
