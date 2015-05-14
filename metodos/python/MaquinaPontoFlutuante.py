from decimal import *
class NumeroMaquina:
    def numero_maquina(self):
        return (self.normalizar()).arredondar()
    
    def arredondar(self):
        novo_m = self.m.quantize(self.maquina.quantificador,
                                 rounding=self.maquina.contexto.rounding)
        novo_numero = NumeroMaquina(self.maquina, novo_m, self.e)
        return novo_numero

    def normalizar(self):
        m = self.m
        e = self.e
        if m == 0:
            return NumeroMaquina(self.maquina, 0, 0)
        while abs(m) > self.maquina.base:
            m /= self.maquina.base
            e += 1
        while abs(m) < 1:
            m *= self.maquina.base
            e -= 1
        return NumeroMaquina(self.maquina, m, e)
    
    def __eq__(self, other):
        n1 = self.numero_maquina()
        n2 = other.numero_maquina()
        return n1.m == n2.m and n1.e == n2.e

    def __add__(self, other):
        n1 = self.numero_maquina()
        n2 = other.numero_maquina()
        e = n1.e
        if n1.e < n2.e:
            m1 = n1.m * (self.maquina.base ** (n1.e - n2.e))
            m2 = n2.m
            e = n2.e
        if n1.e > n2.e:
            m1 = n1.m
            m2 = n2.m * (self.maquina.base ** (n2.e - n1.e))
            e = n1.e
            
        r = NumeroMaquina(self.maquina, m1 + m2, e)
        return r.numero_maquina()
    def __abs__(self):
        return NumeroMaquina(self.maquina, abs(self.m), self.e)

    def __mul__(self, other):    
        n1 = self.numero_maquina()
        n2 = other.numero_maquina()
        r = NumeroMaquina(self.maquina, n1.m * n2.m, n1.e + n2.e)
        return r.numero_maquina()

    def __sub__(self, other):
        n2 = NumeroMaquina(other.maquina, -other.m, other.e)
        return self + n2

    def __truediv__(self, other):
        n1 = self.numero_maquina()
        n2 = other.numero_maquina()
        if n2.m == 0:
            raise DivisionByZero
        r = NumeroMaquina(self.maquina, n1.m / n2.m, n1.e - n2.e)
        return r.numero_maquina();

    def __div__(self, other):
        return __truediv__(other)

    def __init__(self, maquina, m, e):
        self.m = Decimal(str(m))
        self.e = Decimal(str(e))
        self.maquina = maquina

    def mostrar_padrao(self):
        return "{} . {}^{}".format(self.m, self.maquina.base, self.e)
    
class MaquinaPontoFlutuante:
   
    def __init__(self, base, significando, exp_min, exp_max):
        self.base = base
        self.t = significando
        self.emin = exp_min
        self.emax = exp_max
        self.contexto = Context(rounding=ROUND_HALF_EVEN)
        self.quantificador = Decimal("1." + (significando-1)*"0")

m1 = MaquinaPontoFlutuante(10, 2, -3, 3)
n1 = NumeroMaquina(m1, 1.25, 0)
n2 = NumeroMaquina(m1, 0.38, 0)
n1.mostrar_padrao()
n2.mostrar_padrao()
n3 = NumeroMaquina(m1, 1.6, 0)
n4 = NumeroMaquina(m1, 1.4, 0)
um = NumeroMaquina(m1, 1, 0)
print ("{} = {}".format((n1 + n2).mostrar_padrao(), n3.mostrar_padrao()))
print ("{} = {}".format((n1 * n1).mostrar_padrao(), n4.mostrar_padrao()))
print ("{} = {}".format((n1 / n1).mostrar_padrao(), um.mostrar_padrao()))
testes = ((n1 + n2) == n3) and ((n1 * n1) == n4) and ((n1/n1) == um)
print ("Testes ok? {}".format( testes))
