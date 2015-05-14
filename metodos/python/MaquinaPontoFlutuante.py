from decimal import *
class NumeroMaquina:
    def arredondar(self, significando, context):
        quantificador = "1." + (significando-1)*"0"
        self.m = self.m.quantize(Decimal(quantificador),
                                 rounding=context.rounding)
    def normalizar(self):
        if self.m == 0:
            self.exp = 0
            return
        while abs(self.m) > self.base:
            self.m /= self.base
            self.exp += 1
        while abs(self.m) < 1:
            self.m *= self.base
            self.exp -= 1
            
    def __init__(self, m, base, exp):
        self.m = Decimal(str(m))
        self.base = Decimal(str(base))
        self.exp = Decimal(str(exp))
        self.normalizar()

    def mostrar_padrao(self):
        return "{} . {}^{}".format(self.m, self.base, self.exp)
class MaquinaPontoFlutuante:
    def arredondar(self, nm):
        nm.arredondar(self.t, self.context);
    def __init__(self, base, significando, exp_min, exp_max):
        self.base = base
        self.t = significando
        self.emin = exp_min
        self.emax = exp_max
        self.context = Context(rounding=ROUND_HALF_EVEN)
