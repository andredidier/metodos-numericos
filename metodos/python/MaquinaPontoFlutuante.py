from decimal import *
class NumeroMaquina:
    def arredondar(self, quantificador, contexto):
        novo_m = self.m.quantize(quantificador,
                                rounding=contexto.rounding)
        novo_numero = NumeroMaquina(novo_m, self.base, self.exp)
        return novo_numero

    def mudar_exp(self, novo_exp):
        m = self.m
        e = self.exp
        while e > novo_exp:
            e -= 1
            m *= self.base
        while e < novo_exp:
            e += 1
            m /= self.base
        return NumeroMaquina(m, self.base, e)
    
    def normalizar(self):
        m = self.m
        exp = self.exp
        if m == 0:
            exp = 0
            return
        while abs(m) > self.base:
            m /= self.base
            exp += 1
        while abs(m) < 1:
            m *= self.base
            exp -= 1
        return NumeroMaquina(m, self.base, exp)
            
    def __init__(self, m, base, exp):
        self.m = Decimal(str(m))
        self.base = Decimal(str(base))
        self.exp = Decimal(str(exp))

    def mostrar_padrao(self):
        return "{} . {}^{}".format(self.m, self.base, self.exp)
    
class MaquinaPontoFlutuante:
    def arredondar(self, nm):
        return nm.arredondar(self.quantificador, self.context)
    
    def normalizar(self, n):
        return n.normalizar();

    def numero_maquina(self, n):
        return self.arredondar(self.normalizar(n))

    def somar(self, n1, n2):
        n1n = self.numero_maquina(n1)
        n2n = self.numero_maquina(n2)
        maior_exp = max(n1.exp, n2.exp)
        n1s = n1n.mudar_exp(maior_exp)
        n2s = n2n.mudar_exp(maior_exp)
        r = NumeroMaquina(n1s.m + n2s.m, n1s.base, maior_exp)
        return self.numero_maquina(r)

    def multiplicar(self, n1, n2):
        n1n = self.numero_maquina(n1)
        n2n = self.numero_maquina(n2)
        r = NumeroMaquina(n1n.m * n2n.m, n1n.base, n1n.exp + n2n.exp)
        return self.numero_maquina(r)
    
    def __init__(self, base, significando, exp_min, exp_max):
        self.base = base
        self.t = significando
        self.emin = exp_min
        self.emax = exp_max
        self.context = Context(rounding=ROUND_HALF_EVEN)
        self.quantificador = Decimal("1." + (significando-1)*"0")
