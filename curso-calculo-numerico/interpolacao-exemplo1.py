# y = ax2 + bx + c
# p1 = (x1, y1) = (1,3)
# p2 = (x2, y2) = (2,4)

# 3 = a + b + c; c = 3 - a- b
# 4 = 4a + 2b + c
# 4 = 4a + 2b + 3 -a -b
# 1 = 3a + b
# b = 1 - 3a
# c = 3 -a -1 +3a
# c = 2 +2a
# y = ax2 + (1 -3a)x + 2 +2a
# y = ax2 + x -3ax + 2 + 2a
# y = a (x2 -2x + 2) + 2 + x


def exemplo1a(a):
    return lambda x: (a * ((x ** 2) - (3 * x) +2)) + x + 2

# y = ax3 + bx2 + cx + d
# 3 = a + b + c + d; d = 3 -a -b -c
# 4 = 8a + 4b + 2c + d
# 4 = 8a + 4b + 2c + 3 -a -b -c
# 1 = 7a + 3b + c
# c = 1 -7a -3b
# d = 3 -a -b -1 +7a +3b
# d = 2 +6a +2b
# y = ax3 + bx2 + (1 -7a -3b)x +2 +6a +2b
# y = ax3 + bx2 +x -7ax -3bx +2 +6a +2b
# y = ax3 + bx2 + (-7a -3b +1) x + 2 +6a +2b
# y = a (x3 -7x + 6) + b(x2 -3x + 2) +x +2

def exemplo1b(a,b):
    return lambda x: a * (x**3 -7*x + 6) + b*(x**2 -3*x + 2) +x +2

def dexemplo1b(a,b):
    return lambda x: 3*a*(x**2) + 2*b*(x) + (-7*a -3*b +1)

def print_function(min, max, calc, f):
    for xi in range(min, max, 1):
        x = calc(xi)
        print("{0:.2f}{1: 8.2f}".format(x, f(x)))

def busca_f():
    for bi in range(-11000, 10000, 1):
        b = bi / 10
        for ai in range(-11000, 10000, 1):
            a = ai / 10
            #print("Exemplo 1b - a=", a)
            f2exemplo1 = exemplo1b(a, b)
            df2exemplo1 = dexemplo1b(a,1)
            mudanca = 0
            df2a = df2exemplo1(0.4)
            for xi in range(5, 25, 1):
                x = xi/10
                df2 = df2exemplo1(x)
                if sign(df2a) != sign(df2):
                    mudanca+=1
                df2a = df2
                #print("{0:.2f}{1: 8.2f}".format(x,f2exemplo1(x)))
            if mudanca>2:
                print("Mudanças:", mudanca, " a=", a, "b=", b)
                print_function(5, 25, lambda x: x/10, f2exemplo1)
        
def sign(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1

print ("Exemplo 1a")
f1exemplo1 = exemplo1a(-1.5)
print_function(5, 25, lambda x: x/10, f1exemplo1)

print ("Exemplo 1b")
print ("Exemplo 1b-1")
print_function(5, 25, lambda x: x/10, exemplo1b(4,-17.333333333))

print ("Exemplo 1b-2")
print_function(5, 25, lambda x: x/10, exemplo1b(6.962963,-17.333333333))

print ("Exemplo 1b-3")
print_function(5, 25, lambda x: x/10, exemplo1b(2.888888889,1))


