from decimal import *
class NumeroMaquina:
    def numero_maquina(self):
        return (self.normalizar()).arredondar()

    def proximo(self):
        n = self.numero_maquina()
        e =  n1.e - self.maquina.t + 1
        dif = NumeroMaquina(self.maquina, 1, e)
        return (self + dif).numero_maquina()

    def consecutivo(self, other):
        n1 = self.numero_maquina()
        n2 = other.numero_maquina()
        sub = n2 - n1
        e_dif = n1.e - self.maquina.t + 1
        dif = NumeroMaquina(self.maquina, 1, e_dif)
        return sub == dif
    
    def arredondar(self):
        novo_m = self.m.quantize(self.maquina.quantificador,
                                 rounding=self.maquina.contexto.rounding)
        novo_numero = NumeroMaquina(self.maquina, novo_m, self.e)
        return novo_numero

    def normalizar(self):
        m = self.m.normalize()
        e = self.e.normalize()
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
        m1 = n1.m
        m2 = n2.m
        if n1.e < n2.e:
            m1 = n1.m * (self.maquina.base ** (n1.e - n2.e))
            e = n2.e
        if n1.e > n2.e:
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
        return self + (-other)

    def __pow__(self, other):
        n1 = self.numero_maquina()
        n2 = other.numero_maquina()
        n2d = n2.__decimal__()
        m = n1.m ** n2d
        e = n1.e * n2d
        r = NumeroMaquina(self.maquina, m, e)
        return r.numero_maquina()

    def __truediv__(self, other):
        n1 = self.numero_maquina()
        n2 = other.numero_maquina()
        if n2.m == 0:
            raise DivisionByZero
        r = NumeroMaquina(self.maquina, n1.m / n2.m, n1.e - n2.e)
        return r.numero_maquina()

    def __div__(self, other):
        return __truediv__(other)

    def __lt__(self, other):
        return self.__decimal__() < other

    def __le__(self, other):
        return self.__decimal__() <= other

    def __gt__(self, other):
        return self.__decimal__() > other

    def __ge__(self, other):
        return self.__decimal__() >= other

    def __neg__(self):
        return NumeroMaquina(self.maquina, -self.m, self.e)

    def __init__(self, maquina, m, e):
        self.m = Decimal(str(m))
        self.e = Decimal(str(e))
        self.maquina = maquina

    def __decimal__(self):
        return self.m * (self.maquina.base ** self.e)

    def __float__(self):
        return float(self.__decimal__())
    
    def __int__(self):
        return int(self.__decimal__())

    def __format__(self, format_spec):
        return self.mostrar_padrao()

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
n1 = NumeroMaquina(m1, 1.25, 0).numero_maquina()
n2 = NumeroMaquina(m1, 0.38, 0).numero_maquina()
n1.mostrar_padrao()
n2.mostrar_padrao()
n3 = NumeroMaquina(m1, 1.6, 0).numero_maquina()
n4 = NumeroMaquina(m1, 1.4, 0).numero_maquina()
um = NumeroMaquina(m1, 1, 0).numero_maquina()
dois = NumeroMaquina(m1, 2, 0).numero_maquina()
print ("{} = {}".format((n1 + n2), n3))
print ("{} = {}".format((n1 * n1), n4))
print ("{} = {}".format((n1 / n1), um))
print ("{} = {}".format((n4.proximo().proximo()), n3))
print ("{} = {}".format(n4 ** dois, NumeroMaquina(m1, 1.96, 0).numero_maquina()))
testes = ((n1 + n2) == n3) and ((n1 * n1) == n4) and ((n1/n1) == um) and\
         ((n4.proximo().proximo()) == n3)
print ("Testes ok? {}".format( testes))
