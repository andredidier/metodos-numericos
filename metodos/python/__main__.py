from metodos.MetodosZeros import *

Maquina1 = MaquinaPontoFlutuante(10, 7, -99, 99)

def num_maq1(x):
    return NumeroMaquina(Maquina1, x, 0).numero_maquina()
    
# Exemplo 2.2 do livro (edição 3)
def f22(init_num, x):
    a1 = init_num(2)
    a2 = init_num(-2)
    n1 = a1 ** (-x)
    n2 = a2 * init_num(math.sin(x))
    return n1 + n2

# Método de Newton-Raphson
def f24(init_num, x):
    return x * init_num(math.log(x)) - init_num(1)
        
def df24(init_num, x):
    return init_num(math.log(x)) + init_num(1)

def ddf24(init_num, x):
    return init_num(1) / x

def f24b(init_num, x):
    dois = init_num(2)
    return (x ** dois) - dois

def df24b(init_num, x):
    dois = init_num(2)
    return dois * (x ** (dois - init_num(1)))

def f26(init_num, x):
    return x * init_num(math.log(x)) - init_num(1)

# Início dos testes
def parada_geral(iteracao):
    i = iteracao["i"]
    if i > 50:
        return True
    if "erro_absoluto" in iteracao and "fx" in iteracao:
        if i > 0 and iteracao["erro_absoluto"] <= 0.000001 and \
            abs(iteracao["fx"]) <= 0.000001:
            return True



b1 = Bissecao(num_maq1, 0, 1, lambda x: f22(num_maq1, x))
n1 = NewtonRaphson(num_maq1, 1.75, lambda x: f24(num_maq1, x), lambda x: df24(num_maq1, x))
n2 = NewtonRaphson(num_maq1, 1.0, lambda x: f24b(num_maq1, x), lambda x: df24b(num_maq1, x))
s1 = Secantes(num_maq1, 1.7, 1.8, lambda x: f26(num_maq1, x))

print (b1)
for t in b1:
    x = t["x"]
    i = t["i"]
    a = t["a"]
    b = t["b"]
    fa = t["fa"]
    fb = t["fb"]
    fx = t["fx"]
    c = t["l"]
    print ("{:>3} |{:>20} |{:>20} |{:>20} |{:>20} |{:>20} |{:>20} |{:>20}"
           .format(i, a, b, fa, fb, x, fx, c))
    if "l" in t:
        if t["l"] <= 0.05:
            break

print (n1)
for t in n1:
    x = t["x"]
    i = t["i"] 
    print ("{:>3} | {:>15}".format(i, x))
    if "erro_absoluto" in t:
        if t["erro_absoluto"] <= 0.0001:
            break

print (n2)        
for t in n2:
    x = t["x"]
    i = t["i"] 
    print ("{:>3} | {:>15}".format(i, x))
    if "erro_absoluto" in t:
        if t["erro_absoluto"] <= 0.0001:
            break

print (s1)
for t in s1:
    x = t["x"]
    i = t["i"]
    print ("{:>3} | {:>15}".format(i, x))
    if "erro_absoluto" in t:
        if t["erro_absoluto"] <= 0.0001:
            break
