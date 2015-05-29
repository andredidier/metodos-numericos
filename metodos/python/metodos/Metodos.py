class MetodoIterativo:
    def calcular_iteracao(self, anterior):
        print ("Falta implementar")
    def inicializar(self):
        print ("Falta implementar")
        
    def deve_parar(self):
        return self.parada(self.iteracao)

    def __iter__(self):
        self.iteracao = None
        return self
    
    def __next__(self):
        if (self.iteracao):
            anterior = self.iteracao
            self.iteracao = self.calcular_iteracao(anterior)
        else:
            self.iteracao = self.inicializar()
            
        if (self.deve_parar()):
            raise StopIteration
        return self.iteracao

    def __init__(self, init_num):
        self.init_num = init_num
            
            
    
