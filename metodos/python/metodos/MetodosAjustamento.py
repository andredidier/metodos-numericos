import math

class MMQ:
    def montar_sistema_j(self, m, n, j):
        G = self.funcoes
        for i in range(n):
            xi = self.tabela[i]["x"]
            fxi = self.tabela[i]["f"]
            self.b[j] += fxi * G[j](xi) 
            
        for k in range(m):
            self.A[j].append(0)
            for i in range(n):
                xi = self.tabela[i]["x"]
                self.A[j][k] += G[k](xi) * G[j](xi)
                
        
    def montar_sistema(self):
        m = len(self.funcoes)
        n = len(self.tabela)
        for j in range(m):
            self.A.append([])
            self.b.append(0)
            self.montar_sistema_j(m, n, j)
        
        
    def __init__(self, tabela, lista_funcoes):
        self.tabela = tabela
        self.funcoes = lista_funcoes
        self.A = []
        self.b = []
        self.montar_sistema()
        
