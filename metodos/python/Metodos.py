class MetodoIterativo:
    def calcular_iteracao(self, anterior):
        print ("Falta implementar")
        
    def deve_parar(self):
        return True
    
    def __iter__(self):
        self.iteracao = None
        return self
    
    def __next__(self):
        anterior = None
        if (self.iteracao):
            anterior = self.iteracao
        self.iteracao = self.calcular_iteracao(anterior)
        if (self.deve_parar()):
            raise StopIteration
        return self.iteracao
            
            
    
