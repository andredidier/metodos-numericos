from metodos.MaquinaPontoFlutuante import *
from metodos.Metodos import *
import math

class Bissecao(MetodoIterativo):

    def __iter__(self):
        self.iteracao = None
        return self
    
    def __next__(self):
        anterior = self.iteracao
        atual = {}
        if anterior == None:
            a = self.a
            b = self.b
            i = 0
        else:
            i = anterior["i"]
            a = anterior["a"]
            b = anterior["b"]
            x = anterior["x"]
            fa = anterior["fa"]
            fx = anterior["fx"]
            if fa * fx < 0:
                b = x
            else:
                a = x
            i+=1
        x = (a + b) / self.init_num(2)
        fa = self.f(a)
        fb = self.f(b)
        fx = self.f(x)
        l = b - a
        atual["i"] = i
        atual["a"] = a
        atual["b"] = b
        atual["l"] = l
        atual["x"] = x
        atual["fa"] = fa
        atual["fb"] = fb
        atual["fx"] = fx
        if i > 0:
            atual["erro_absoluto"] = abs(x - anterior["x"])
            
        if self.N > -1 and atual["i"] == self.N:
            raise StopIteration
        
        self.iteracao = atual
        return self.iteracao
        
    def __str__(self):
        return "Bissecao(a={0}, b={1}, f={2})".format(self.a, self.b, self.f)

    def __init__(self, init_num, a, b, f, N=-1):
        super().__init__(init_num)
        self.f = f
        self.a = init_num(a)
        self.b = init_num(b)
        self.N = N

class IterativoGerador():
    def calcular_x_iteracao(self, x_anterior):
        None

    def __next__(self):
        anterior = self.iteracao
        atual = {}
        if anterior == None:
            atual["i"] = 0
            atual["x"] = self.x0
        else:
            atual["i"] = anterior["i"] + 1
            try:
                atual["x"] = self.calcular_x_iteracao(anterior["x"])
                atual["fx"] = self.f(anterior["x"])
                atual["erro_absoluto"] = abs(atual["x"] - anterior["x"])
            except:
                #atual["x"] = None
                #atual["fx"] = None
                atual["erro"] = "Erro no cálculo da iteração"
            
        if self.N > -1 and atual["i"] == self.N:
            raise StopIteration
        
        self.iteracao = atual
        return atual
        
    def __iter__(self):
        self.iteracao = None
        return self

    def __init__(self, init_num, f, N=-1):
        self.init_num = init_num
        self.f = f
        self.N = N

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
    
    def __str__(self):
        return "Halley(x0={0}, f={1}, df={2}, ddf={3})".format(self.x0, self.f, self.df, self.ddf)
    
    def __init__(self, init_num, x0, f, df, ddf, N=-1):
        super().__init__(init_num, f, N)
        self.df = df
        self.ddf = ddf
        self.dois = self.init_num(2)
        self.x0 = self.init_num(x0)
    
 
class NewtonRaphson(IterativoGerador):
    def calcular_x_iteracao(self, x_anterior):
        valor_f = self.f(x_anterior)
        valor_df = self.df(x_anterior)
        return x_anterior - valor_f / valor_df

    def __str__(self):
        return "NewtonRaphson(x0={0}, f={1}, df={2})".format(self.x0, self.f, self.df)

    def __init__(self, init_num, x0, f, df, N=-1):
        super().__init__(init_num, f, N)
        self.df = df
        self.x0 = self.init_num(x0)

class Secantes():
        
    def __iter__(self):
        self.iteracao = {}
        self.iteracao["i"] = 0
        self.iteracao["x"] = self.a
        self.iteracao["x(i-1)"] = self.b
        return self

    def __next__(self):
        anterior = self.iteracao
        atual = {}
        atual["i"] = anterior["i"] + 1
        try:
            x = anterior["x"]
            fx = self.f(x)
            xi1 = anterior["x(i-1)"]
            fxi1 = self.f(xi1)
            numerador = (xi1 * fx) - (x * fxi1)
            denominador = fx - fxi1
            xi1,x = x,numerador / denominador
            atual["x"] = x
            atual["x(i-1)"] = xi1
            atual["fx"] = self.f(x)
            atual["erro_absoluto"] = abs(atual["x"] - anterior["x"])
        except Exception as err:
            #atual["x"] = None
            #atual["fx"] = None
            atual["erro"] = "Erro no cálculo da iteração"
            
        if self.N > -1 and atual["i"] == self.N:
            raise StopIteration
        
        self.iteracao = atual
        return atual

    def __str__(self):
        return "Secantes(a={0}, b={1}, f={2})".format(self.a, self.b, self.f)
    
    def __init__(self, init_num, a, b, f, N=-1):
        self.init_num = init_num
        self.f = f
        self.N = N
        self.a = init_num(a)
        self.b = init_num(b)
        
        