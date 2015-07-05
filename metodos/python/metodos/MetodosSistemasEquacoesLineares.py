class LU:
    def calcularLU(self):
        n = len(self.A)
        for i in range(n):
            self.L.append([])
            self.U.append([])
            for j in range(n):
                self.L[i].append(0)
                if i == j:
                    self.U[i].append(1)
                else:
                    self.U[i].append(0)
        
        for c in range(n):
            j = c
            for i in range(n):
                if i >= j:
                    self.L[i][j] = self.A[i][j]
                    for k in range(j):
                        self.L[i][j] -= self.L[i][k] * self.U[k][j]
            i = c
            for j in range(n):
                if i < j:
                    self.U[i][j] = self.A[i][j]
                    for k in range(i):
                        self.U[i][j] -= self.L[i][k] * self.U[k][j]
                    self.U[i][j] /= self.L[i][i]
            
    def calcular_y(self):
        n = len(self.A)
        self.y.append(self.b[0] / self.L[0][0])
        for i in range(1,n):
            self.y.append(self.b[i])
            for j in range(i):
                self.y[i] -= self.L[i][j] * self.y[j]
            self.y[i] /= self.L[i][i] 
    
    def calcular_x(self):
        n = len(self.A)
        for i in range(n):
            self.x.append(0)
        
        self.x[n-1] = self.y[n-1]
        for c in range(n-1):
            i = n-2-c
            self.x[i] = self.y[i]
            for j in range(i+1, n):
                self.x[i] -= self.U[i][j] * self.x[j]
                
        
    def __init__(self, A, b):
        self.A = A
        self.b = b
        self.L = []
        self.U = []
        self.y = []
        self.x = []
        self.calcularLU()
        self.calcular_y()
        self.calcular_x()
        
matrizA_3_4 = [
               [5,2,1],
               [3,6,-2],
               [2,-4,10]
               ] 

exemplo3_4 = LU(matrizA_3_4, [8,7,8])

#print("Matriz L")
#for linha in exemplo3_4.L:
#    print(linha)
    
#print("Matriz U")
#for linha in exemplo3_4.U:
#    print(linha)

#print("Matriz y")
#print(exemplo3_4.y)

#print("Matriz x")
#print(exemplo3_4.x)
