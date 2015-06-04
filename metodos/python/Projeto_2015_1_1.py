from metodos.MetodosZeros import *
from metodos.MaquinaPontoFlutuante import *
from decimal import *

m = MaquinaPontoFlutuante(10, 6, -1000, 1000)
def num(x):
    #return NumeroMaquina(m, x, 0).numero_maquina()
    #return Decimal(str(x))
    return float(x)
def nm(f, x):
    return num(f(x))
def cos(x):
    return nm(math.cos, x)
def sin(x):
    return nm(math.sin, x)
def exp(x):
    return nm(math.exp, x)

def param_f(a0, a1, a2, a3, a4, a5):
    return lambda x: a0 * cos(a1 * x) + a2 * sin(a3 * x) + exp(a4 * x) + a5
def param_df(a0, a1, a2, a3, a4, a5):
    return lambda x: - a0 * a1 * sin(a1 * x) + a2 * a3 * cos(a3 * x) + a4 * exp(a4 * x)
def param_ddf(a0, a1, a2, a3, a4, a5):
    return lambda x: - a0 * (a1 ** num(2)) * cos(a1 * x) - a2 * (a3 ** num(2)) * sin(a3 * x) + (a4 ** num(2)) * exp(a4 * x)

def parada_param(N, e1, e2):
    return lambda iteracao: parada_geral(iteracao, N, e1, e2)

def parada_geral(iteracao, N, e1, e2):
    if "erro" in iteracao:
        return True
    i = iteracao["i"]
    if i >= N:
        return True
    if i > 0 and iteracao["erro_absoluto"] <= e1 and abs(iteracao["fx"]) <= e2:
        return True

def print_num(x):
    if x == None:
        return "-"
    print(x)
    try:
        return Decimal(str(x)).quantize(Decimal('.00001'), rounding=ROUND_HALF_EVEN)
    except:
        return x
    
def formato_geral():
    return ("Método: {0}\n"
        "\t{1}\n"
        "\tNúmero de iterações: {2}\n"
        "\tRaiz final: {3}\n"
        "\t|x_(i)-x_(i-1)|: {4}\n"
        "\t|f(x_i)|: {5}\n",
        "CONVERGIU",
        "NÃO CONVERGIU")
    
def formato_01():
    return ("\nMétodo: {0}\n\n"
        "\t{1}\n\n"
        "\tRAIZ ENCONTADA: {3}\n\n"
        "\tNUMERO DE ITERACOES: {2:02}\n\n"
        "\tERRO RELATIVO DE e1: {4}\n\n"
        "\tERRO RELATIVO DE e2: {5}\n\n",
        "Converge!!",
        "Nao Converge!!")

def formato_03():
    return ("\n\nMetodo: {0}\n"
        "\n{1}\n"
        "\nRaiz: {3}\n"
        "Erro em x: {4}\n"
        "Erro em y: {5}\n"
        "Numero de iterações: {2}\n",
        "CONVERGIU",
        "NÃO CONVERGIU"
        )
    
def formato_04():
    return ("Metodo: {0}\n"
        "{1}\n"
        "Numero de iteracoes: {2}\n"
        "Raiz final: {3}\n\n\n",
        "CONVERGIU",
        "NAO CONVERGIU")
    
def formato_05():
    return ("Método: {0}\n\n"
        "{1}\n"
        "Número de iterações: {2}\n"
        "Raiz final: {3}\n"
        "|x_({2})-x_({6})|: {4}\n"
        "|f(x_{2})|: {5}\n",
        "CONVERGIU",
        "NÃO CONVERGIU")
    
def formato_06():
    return ("Método: {0}\n"
        "\t{1}\n"
        "\tNumero de iteracoes: {2}\n"
        "\tRaiz final: {3}\n"
        "\t|x_({2})-x_({6})|: {4}\n"
        "\t|f(x_{2})|: {5}\n",
        "CONVERGIU",
        "NÃO CONVERGIU")
    
def formato_07():
    return ("\nMetodo: {}\n"
        "{}\n"
        "Numero de iteracoes: {}\n"
        "Raiz final: {}\n"
        "|x_(i)-x_(i-1)|: {}\n"
        "|f(x_i)|: {}\n\n",
        "CONVERGIU",
        "NAO CONVERGIU")
    
def formato_08():
    return ("Método: {0}\n\n"
        "\t{1}\n"
        "\tNúmero de iterações: {2}\n"
        "\tRaíz final: {3}\n"
        "\t|x_({2})-x_({6})|: {4}\n"
        "\t|f(x_{2})|: {5}\n",
        "CONVERGIU",
        "NÃO CONVERGIU")
    
def formato_11():
    return ("\nMetodo: {0}\n"
        "     {1}\n"
        "     Numero de Iteracoes: {2}\n"
        "     Raiz Final: {3}\n"
        "     |x_({2})-x_({6})|: {4}\n"
        "     |f(x_{2})|: {5}\n",
        "CONVERGIU",
        "NAO CONVERGIU")
    
def formato_13():
    return ("\nMETODO DE {0}\n\n"
        "{1}\n\n"
        "Numero de Interacoes:{2}\n"
        "Raiz final:{3}\n"
        "|x_i-x_i-1|:{4}\n"
        "|f(x_i)|:{5}\n",
        "CONVERGIU",
        "NÃO CONVERGIU")

    
def padrao_saida(saida, metodo, t):
    x = t.get("x", None)
    erro_absoluto = None
    abs_fx = None
    if not "erro" in t:
        erro_absoluto = t["erro_absoluto"]
        abs_fx = abs(t["fx"])
    
    ap = formato_13()
    
    conv = not "erro" in t and (t["erro_absoluto"] <= e1 or abs(t["fx"]) <= e2)
    
    if conv:
        conv_str = ap[1]
    else:
        conv_str = ap[2]

    texto = ap[0].format(metodo, conv_str, t["i"], print_num(x), 
                         print_num(erro_absoluto), print_num(abs_fx),
                         t["i"]-1)
    print(texto)
    saida.write(texto)
    

      

def rodar_parada(metodo, nome, parada):
    print("Método: {}".format(nome))
    c=0
    erro = False
    t = None
    for t in metodo:
        x=t.get("x", 0)
        erro = "erro" in t
        i = t["i"]
        print("{:>10} | {:>20} | {:>20} | {:>20}"
              .format(i, x, t.get("erro_absoluto", 0), abs(t.get("fx", 0))))
        if parada(t):
            break;
        c+=1
    conv = not erro and (t["erro_absoluto"] <= e1 or abs(t["fx"]) <= e2)
    padrao_saida(saida, nome, t)
    
entrada = open("entrada.txt", "r")
saida = open("saida.txt", "w")

ent=0
while True:
    conf = entrada.readline()
    if conf:
        init = num
        ent+=1
        a0,a1,a2,a3,a4,a5,N,e1,e2,a,b=map(eval, conf.split())
        a0=init(a0)
        a1=init(a1)
        a2=init(a2)
        a3=init(a3)
        a4=init(a4)
        a5=init(a5)
        f   = param_f(a0,a1,a2,a3,a4,a5)
        df  = param_df(a0,a1,a2,a3,a4,a5)
        ddf = param_ddf(a0,a1,a2,a3,a4,a5)
        parada = parada_param(N,e1,e2)
        x0 = (a + b) / 2
        
        mh = Halley(init, x0, f, df, ddf)
        mn = NewtonRaphson(init, x0, f, df)
        mb = Bissecao(init, a, b, f)

        saida.write("Entrada: {}\n".format(ent))
        print("Entrada: {}".format(ent))
        rodar_parada(mh, "Halley", parada)
        rodar_parada(mn, "Newton-Raphson", parada)
        rodar_parada(mb, "Bisseção", parada)
        
    else:
        break;

entrada.close()
saida.close()

