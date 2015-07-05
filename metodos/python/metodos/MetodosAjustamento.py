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
        self.A = []
        self.b = []
        for j in range(m):
            self.A.append([])
            self.b.append(0)
            self.montar_sistema_j(m, n, j)
        
        
    def __init__(self, tabela, lista_funcoes):
        self.tabela = tabela
        self.funcoes = lista_funcoes
        self.montar_sistema()
        print("Matriz A")
        for linha in self.A:
            print(linha)
        print("Matriz b = ", self.b)
        
tabela4_1 = [
             {'x': 1, 'f': 1.3},
             {'x': 2, 'f': 1.8},
             {'x': 3, 'f': 2.2},
             {'x': 4, 'f': 0.4},
             {'x': 5, 'f': 1.1},
             {'x': 6, 'f': 3.0},
             {'x': 7, 'f': 1.1},
             {'x': 8, 'f': 0.8},
             {'x': 9, 'f': 0.1}
             ]
funcoes4_1 = [ lambda x : 1, lambda x : x  ]

exemplo4_1 = MMQ(tabela4_1, funcoes4_1)
