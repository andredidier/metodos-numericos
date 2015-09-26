#include <stdio.h>
#include <stdlib.h>
#include <metodos.h>

MaquinaPontoFlutuante lerMaquina(void)
{
	MaquinaPontoFlutuante m;

	FILE* f = fopen("MaquinaPontoFlutuante.bin", "r");
	if (f) 
	{
		fread(&m, sizeof(MaquinaPontoFlutuante), 1, f);
		fclose(f);
		char usarExistente;
		char* formatacaoMaquina = malloc(1024);
		formatarMaquina(m, formatacaoMaquina);
		int done = 0;
		while (!done)
		{
			printf("Deseja usar a maquina existente? (%s)\n", formatacaoMaquina);
			scanf(" %c", &usarExistente);
			switch(usarExistente)
			{
				case 's':
				case 'S':
					return m;
				break;
				case 'n':
				case 'N':
					done = 1;
				break;
			}
		}
		free(formatacaoMaquina);
	}

	printf("Informe os dados da maquina de ponto flutuante:\n");
	printf("Base: ");
	scanf("%d", &m.base);
	printf("Digitos: ");
	scanf("%d", &m.digitos);
	printf("Menor expoente: ");
	scanf("%d", &m.e1);
	printf("Maior expoente: ");
	scanf("%d", &m.e2);
	
	f = fopen("MaquinaPontoFlutuante.bin", "w");
	fwrite(&m, sizeof(MaquinaPontoFlutuante), 1, f);
	fclose(f);

	return m;
}

void representarNumero(void)
{
	double numeroUsuario;
	char* formatacaoMaquina;
	MaquinaPontoFlutuante m = lerMaquina();
	printf("Informe o numero: ");
	scanf("%lf", &numeroUsuario);

	formatacaoMaquina = malloc(1024);
	formatarMaquina(m, formatacaoMaquina);

	NumeroMaquina numeroMaquina;
	int err = converterNumeroMaquina(m, numeroUsuario, &numeroMaquina);
	switch(err)
	{
		case 0:
			printf("Numero na maquina %s: %lf ==> %lf\n", 
				formatacaoMaquina, numeroUsuario, 
				valorNumeroMaquina(m, numeroMaquina));
			break;
		case 1:
			printf("Overflow");
			break;
		case -1:
			printf("Underflow");
			break;
	}

	free(formatacaoMaquina);
}

void operacoes(void)
{
	MaquinaPontoFlutuante m = lerMaquina();
	printf("Informe a operacao: ");
	double v1, v2;
	char op;
	int err;
	scanf("%lf %c %lf", &v1, &op, &v2);
	NumeroMaquina n1, n2, res;
	converterNumeroMaquina(m, v1, &n1);
	converterNumeroMaquina(m, v2, &n2);
	switch(op)
	{
		case '+':
			err = somar(m, n1, n2, &res);
			break;
		case '-':
			n2.significando = -n2.significando;
			err = somar(m, n1, n2, &res);
			break;
		case '*':
			err = multiplicar(m, n1, n2, &res);
			break;
		case '/':
			err = dividir(m, n1, n2, &res);
			break;
	}

	char* formatacaoMaquina = malloc(1024);
	char *f1 = malloc(200);
	char *f2 = malloc(200);
	char *f3 = malloc(200);
	formatarMaquina(m, formatacaoMaquina);

	switch(err)
	{
		case 0:
			formatarNumeroMaquina(m, n1, f1);
			formatarNumeroMaquina(m, n2, f2);
			formatarNumeroMaquina(m, res, f3);
			printf("Resultado de %s %c %s na maquina %s:  %s\n",
				f1, op, f2, formatacaoMaquina, f3);
			break;
		case 1:
			printf("Overflow");
			break;
		case -1:
			printf("Underflow");
			break;
		case 100:
			printf("Divisao por zero");
			break;
	}
	free(formatacaoMaquina);
	free(f1);
	free(f2);
	free(f3);
}

void sistemaEqLineares(void)
{
	char metodo;
	int tamanhoSistema;

	NumeroMaquina **A;
	NumeroMaquina *b;
	NumeroMaquina *x;
	int i,j, rep;

	printf("Qual o tamanho do sistema? ");
	scanf("%d", &tamanhoSistema);

	A = malloc(tamanhoSistema * sizeof(NumeroMaquina*));
	b = malloc(tamanhoSistema * sizeof(NumeroMaquina));
	x = malloc(tamanhoSistema * sizeof(NumeroMaquina));

	MaquinaPontoFlutuante m = lerMaquina();
	for (i = 0; i < 3; i++)
	{
		A[i] = malloc(tamanhoSistema * sizeof(NumeroMaquina));
		converterNumeroMaquina(m, 0, &x[i]);
	}

	double valor;
	for (i = 0; i < tamanhoSistema; i++)
	{
		for (j = 0; j < tamanhoSistema; j++)
		{
			printf("a[%d][%d] = ", i+1, j+1);
			scanf("%lf", &valor);
			converterNumeroMaquina(m, valor, &A[i][j]);
		}
		printf("b[%d] = ", i+1);
		scanf("%lf", &valor);
		converterNumeroMaquina(m, valor, &b[i]);
	}

	int done = 0;
	do
	{
		printf("Escolha um metodo:\n");
		printf("j: Jacobi:\n");
		printf("v: Voltar:\n");
		scanf(" %c", &metodo);

		switch(metodo)
		{
			case 'j':
				printf("Quantas repeticoes? ");
				scanf("%d", &rep);
				char *formatador = malloc(100);
				for (j = 0; j <= rep; j++)
				{
					printf("x_%3d =", j);
					for (i = 0; i < tamanhoSistema; i++)
					{
						formatarNumeroMaquina(m, x[i], formatador);
						printf(" %s", formatador);
					}
					jacobi(m, tamanhoSistema, A, b, x);
					printf("\n");
				}
				free(formatador);
			break;
			case 'v':
				done = 1;
			break;
			default:
				printf("Opcao invalida\n");
		}
	} while(!done);

	free(A);
	free(x);
	free(b);
}

int main(void)
{
	int done = 0;
	char opcao;

#ifdef DEBUG
	printf("DEBUG\n");

	NumeroMaquina **A;
	NumeroMaquina *b;
	NumeroMaquina *x;
	int i,j;

	A = malloc(3 * sizeof(NumeroMaquina*));
	b = malloc(3 * sizeof(NumeroMaquina));
	x = malloc(3 * sizeof(NumeroMaquina));

	MaquinaPontoFlutuante m = lerMaquina();
	for (i = 0; i < 3; i++)
	{
		A[i] = malloc(3 * sizeof(NumeroMaquina));
		converterNumeroMaquina(m, 0, &x[i]);
	}

	converterNumeroMaquina(m,  5, &A[0][0]);
	converterNumeroMaquina(m,  2, &A[0][1]);
	converterNumeroMaquina(m,  1, &A[0][2]);
	converterNumeroMaquina(m,  3, &A[1][0]);
	converterNumeroMaquina(m,  6, &A[1][1]);
	converterNumeroMaquina(m, -2, &A[1][2]);
	converterNumeroMaquina(m,  2, &A[2][0]);
	converterNumeroMaquina(m, -4, &A[2][1]);
	converterNumeroMaquina(m, 10, &A[2][2]);
	converterNumeroMaquina(m, 8, &b[0]);
	converterNumeroMaquina(m, 7, &b[1]);
	converterNumeroMaquina(m, 8, &b[2]);

	jacobi(m, 3, A, b, x);
	for (i = 0; i < 3; i++)
	{
		printf("\t%lf", valorNumeroMaquina(m, x[i]));
	}

	free(A);
	free(x);
	free(b);
#endif

	do
	{
		printf("\n-----------------------\n");
		printf("Opcoes:\n");
		printf("1: Representar numero\n");
		printf("2: Operacoes matematicas basicas\n");
		printf("3: Sistemas de Equacoes Lineares\n");
		printf("x: Sair\n");
		scanf(" %c", &opcao);
		printf("Opcao escolhida: \"%c\"\n", opcao);
		switch(opcao)
		{
		case '1':
			representarNumero();
			break;
		case '2':
			operacoes();
			break;
		case '3':
			sistemaEqLineares();
			break;
		case 'x':
			done = 1;
			break;
		default:
			printf("Opcao invalida\n");
		}
	} while(!done);
	return 0;
}
