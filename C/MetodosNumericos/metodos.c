#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <metodos.h>

void formatarMaquina(MaquinaPontoFlutuante m, char* formatada)
{
	sprintf(formatada, "F(%d, %d, %d, %d)", m.base, m.digitos, m.e1, m.e2);
}

/**
erro: 1: Overflow, -1: Underflow
*/
int converterNumeroMaquina(MaquinaPontoFlutuante m, double numeroUsuario, NumeroMaquina* n)
{
	double s = numeroUsuario;
	int c = 0;
	
	if (s == 0) {
		n->significando = 0;
		n->expoente = m.e1;
		return 0;
	}
	while (fabs(s) >= m.base)
	{
		s /= (double)m.base;
		c++;
		if (c > m.e2)
		{
			// overflow
			return 1;
		}
	}

	while (fabs(s) < 1)
	{
		s *= (double)m.base;
		c--;
		if (c < m.e1)
		{
			return -1;
		}
	}
	n->significando = s;
	n->expoente = c;

	arredondarNumeroMaquina(m, n);
	return 0;
}

double valorNumeroMaquina(MaquinaPontoFlutuante m, NumeroMaquina numero)
{
	double valor = numero.significando * pow(m.base, numero.expoente);
	return valor;
}

void formatarNumeroMaquina(MaquinaPontoFlutuante m, NumeroMaquina numero, char* res)
{
	char *formatador = malloc(100);
	sprintf(formatador, "%%.%df * 10 ^ %%d", m.digitos-1);
	sprintf(res, formatador, numero.significando, numero.expoente);
}

void arredondarNumeroMaquina(MaquinaPontoFlutuante m, NumeroMaquina* n) 
{
#ifdef DEBUG	
	printf("\tsignificando: %lf\n", n->significando);
#endif
	double desnorm = n->significando * pow(m.base, m.digitos);
#ifdef DEBUG	
	printf("\tdesnorm: %lf\n", desnorm);
#endif
	long digitos = desnorm;
	int digitoArred = digitos % m.base;
	digitos /= 10;
#ifdef DEBUG	
	printf("\tdigitos: %ld\n", digitos);
	printf("\tdigitoArred: %d\n", digitoArred);
#endif
	if (digitoArred > 5 || ((digitoArred == 5) && (digitos % 2 == 1)))
	{
		digitos++;
	}
	n->significando = digitos * pow(m.base, -m.digitos+1);
	//TODO arredondamento no overflow 9.9999999
}

int somar(MaquinaPontoFlutuante m, NumeroMaquina n1, NumeroMaquina n2, NumeroMaquina* res)
{
	int c = n1.expoente;
	if (n1.expoente < n2.expoente)
	{
		n1.significando *= pow(m.base, n1.expoente - n2.expoente);
		c = n2.expoente;
	} else if (n2.expoente < n1.expoente)
	{
		n2.significando *= pow(m.base, n2.expoente - n1.expoente);
		c = n1.expoente;
	}
	res->significando = n1.significando + n2.significando;
	res->expoente = c;
#ifdef DEBUG
	printf("\tResultado: %lf * %d ^ %d\n", res->significando, m.base, res->expoente);
#endif
	return converterNumeroMaquina(m, valorNumeroMaquina(m, *res), res);
}

int multiplicar(MaquinaPontoFlutuante m, NumeroMaquina n1, NumeroMaquina n2, NumeroMaquina* res)
{
	double valor = n1.significando * n2.significando * pow(m.base, n1.expoente + n2.expoente);
	return converterNumeroMaquina(m, valor, res);
}

int dividir(MaquinaPontoFlutuante m, NumeroMaquina n1, NumeroMaquina n2, NumeroMaquina* res)
{
	if (n2.significando == 0)
	{
		return 100;
	}
	double valor = n1.significando / n2.significando * pow(m.base, n1.expoente - n2.expoente);
	return converterNumeroMaquina(m, valor, res);
}

int jacobi(MaquinaPontoFlutuante m, int tamanhoMatriz, NumeroMaquina **A, NumeroMaquina *b, NumeroMaquina *x)
{
	int i, j;
	NumeroMaquina *xk = malloc(tamanhoMatriz * sizeof(NumeroMaquina));
	for (i = 0; i < tamanhoMatriz; i++)
	{
		xk[i] = x[i];
	}

	for (i = 0; i < tamanhoMatriz; i++)
	{
		x[i] = b[i];
#ifdef DEBUG
		printf("b[%d] = %lf\n", (i+1), valorNumeroMaquina(m, b[i]));
		printf("x[%d] = %lf\n", (i+1), valorNumeroMaquina(m, x[i]));
#endif
		for (j = 0; j < tamanhoMatriz; j++)
		{
			if (j == i)
			{
				continue;
			}
			NumeroMaquina res;
			multiplicar(m, A[i][j], xk[j], &res);
#ifdef DEBUG
			printf("\tA[%d][%d](%lf) * x[%d](%lf) = %lf * %d ^ %d\n", i, j, 
				valorNumeroMaquina(m, A[i][j]), j, valorNumeroMaquina(m, x[j]),
				res.significando, m.base, res.expoente);
#endif
			res.significando = -res.significando;
			somar(m, x[i], res, &x[i]);
#ifdef DEBUG
			printf("x[%d] = %lf [%d]\n", (i+1), valorNumeroMaquina(m, x[i]), j);
#endif
		}
		dividir(m, x[i], A[i][i], &x[i]);
#ifdef DEBUG
		printf("x[%d] = %lf\n", (i+1), valorNumeroMaquina(m, x[i]));
#endif
	}

}