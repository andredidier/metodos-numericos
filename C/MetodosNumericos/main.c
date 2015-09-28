#include <stdio.h>
#include <stdlib.h>
#include <metodos.h>
#include <math.h>

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

void sistemaEqLineares(int *tamanhoSistemaUsu, NumeroMaquina **AUsu, NumeroMaquina *bUsu, NumeroMaquina *xUsu)
{
	char metodo;
	int tamanhoSistema;

	NumeroMaquina **A;
	NumeroMaquina *b;
	NumeroMaquina *x;
	int i,j, rep;

	MaquinaPontoFlutuante m = lerMaquina();

	if (tamanhoSistemaUsu)
	{
		A = AUsu;
		b = bUsu;
		x = xUsu;
		tamanhoSistema = *tamanhoSistemaUsu;
	}
	else 
	{
		printf("Qual o tamanho do sistema? ");
		scanf("%d", &tamanhoSistema);

		A = malloc(tamanhoSistema * sizeof(NumeroMaquina*));
		b = malloc(tamanhoSistema * sizeof(NumeroMaquina));
		x = malloc(tamanhoSistema * sizeof(NumeroMaquina));
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
	}


	int done = 0;
	char *formatador;
	do
	{
		printf("Escolha um metodo:\n");
		printf("j: Jacobi\n");
		printf("v: Voltar\n");
		scanf(" %c", &metodo);

		switch(metodo)
		{
			case 'j':
				printf("Quantas repeticoes? ");
				scanf("%d", &rep);
				formatador = malloc(100);
				for (j = 1; j <= rep; j++)
				{
					printf("x_%03d =", j);
					jacobi(m, tamanhoSistema, A, b, x);
					for (i = 0; i < tamanhoSistema; i++)
					{
						formatarNumeroMaquina(m, x[i], formatador);
						printf(" %s", formatador);
					}
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

	if (!tamanhoSistemaUsu)
	{
		for (i = 0; i < tamanhoSistema; i++) free(A[i]);
		free(A);
		free(x);
		free(b);
	}
}

int ident(MaquinaPontoFlutuante m, NumeroMaquina x, NumeroMaquina *res)
{
	*res = x;
	return 0;
}

int const1(MaquinaPontoFlutuante m, NumeroMaquina x, NumeroMaquina *res)
{
	return converterNumeroMaquina(m, 1, res);
}

int power2(MaquinaPontoFlutuante m, NumeroMaquina x, NumeroMaquina *res)
{
	return multiplicar(m, x, x, res);
}

int power3(MaquinaPontoFlutuante m, NumeroMaquina x, NumeroMaquina *res)
{
	int erro = power2(m, x, res);
	if (erro) return erro;
	return multiplicar(m, x, *res, res);
}

int power4(MaquinaPontoFlutuante m, NumeroMaquina x, NumeroMaquina *res)
{
	int erro = power3(m, x, res);
	if (erro) return erro;
	return multiplicar(m, x, *res, res);
}

int sinNumeroMaquina(MaquinaPontoFlutuante m, NumeroMaquina x, NumeroMaquina *res)
{
	double xd = valorNumeroMaquina(m, x);
	xd = sin(xd);
	return converterNumeroMaquina(m, xd, res);
}

int cosNumeroMaquina(MaquinaPontoFlutuante m, NumeroMaquina x, NumeroMaquina *res)
{
	double xd = valorNumeroMaquina(m, x);
	xd = cos(xd);
	return converterNumeroMaquina(m, xd, res);
}

int tanNumeroMaquina(MaquinaPontoFlutuante m, NumeroMaquina x, NumeroMaquina *res)
{
	double xd = valorNumeroMaquina(m, x);
	xd = tan(xd);
	return converterNumeroMaquina(m, xd, res);
}

void ajustamento(void)
{
	int quantidadePontosTabelados;
	int quantidadeFuncoes;
	NumeroMaquina **A;
	NumeroMaquina *b;
	NumeroMaquina **tabelamento;
	Funcao *G;
	MaquinaPontoFlutuante m;
	int i, j;
	char funcaoEscolhida;

	m = lerMaquina();

	int quantidadeFuncoesCadastradas = 8;
	char **descricaoFuncao = malloc(sizeof(char *) * quantidadeFuncoesCadastradas);
	Funcao *funcao = malloc(sizeof(Funcao *) * quantidadeFuncoesCadastradas);
	funcao[0] = &const1;
	funcao[1] = &ident;
	funcao[2] = &power2;
	funcao[3] = &power3;
	funcao[4] = &power4;
	funcao[5] = &sinNumeroMaquina;
	funcao[6] = &cosNumeroMaquina;
	funcao[7] = &tanNumeroMaquina;
	for (i = 0; i < quantidadeFuncoesCadastradas; i++)
	{
		descricaoFuncao[i] = malloc(100);
	}
	descricaoFuncao[0] = "Constante 1";
	descricaoFuncao[1] = "Identidade";
	descricaoFuncao[2] = "Potencia 2";
	descricaoFuncao[3] = "Potencia 3";
	descricaoFuncao[4] = "Potencia 4";
	descricaoFuncao[5] = "Seno";
	descricaoFuncao[6] = "Cosseno";
	descricaoFuncao[7] = "Tangente";

	printf("Quantos sao os pontos tabelados? ");
	scanf("%d", &quantidadePontosTabelados);
	printf("Quantas sao as funcoes? ");
	scanf("%d", &quantidadeFuncoes);

	G = malloc(sizeof(Funcao *) * quantidadeFuncoes);
	for (i = 0; i < quantidadeFuncoes; i++)
	{
		printf("Escolha uma funcao para G[%d]:\n", i);
		for (j = 0; j < quantidadeFuncoesCadastradas; j++)
		{
			printf("\t(%c) %s\n", 'a'+j, descricaoFuncao[j]);
		}
		scanf(" %c", &funcaoEscolhida);
		G[i] = funcao[funcaoEscolhida-'a'];
		printf("\tG[%d]: %s\n", i, descricaoFuncao[funcaoEscolhida-'a']);
	}

	tabelamento = malloc(sizeof(NumeroMaquina *) * 2);
	tabelamento[0] = malloc(sizeof(NumeroMaquina) * quantidadePontosTabelados);
	tabelamento[1] = malloc(sizeof(NumeroMaquina) * quantidadePontosTabelados);

	double x, fx;
	for (i = 0; i < quantidadePontosTabelados; i++)
	{
		printf("Informe x_%d e f(x_%d): ", i, i);
		scanf("%lf %lf", &x, &fx);

		converterNumeroMaquina(m, x, &tabelamento[0][i]);
		converterNumeroMaquina(m, fx, &tabelamento[1][i]);
	}

	A = malloc(sizeof(NumeroMaquina *) * quantidadeFuncoes);
	b = malloc(sizeof(NumeroMaquina) * quantidadeFuncoes);
	for (i = 0; i < quantidadeFuncoes; i++) {
		A[i] = malloc(sizeof(NumeroMaquina) * quantidadeFuncoes);
	}

	mmq(m, quantidadeFuncoes, G, quantidadePontosTabelados, tabelamento, A, b);

	char *formatado, *n2;
	formatado = malloc(100);
	for (i = 0; i < quantidadeFuncoes; i++)
	{
		for (j = 0; j < quantidadeFuncoes; j++)
		{
			formatarNumeroMaquina(m, A[i][j], formatado);
			printf("\t(%s a_%d)", formatado, j);
		}
		formatarNumeroMaquina(m, b[i], formatado);
		printf(" = %s\n", formatado);
	}

	NumeroMaquina *a;
	a = malloc(sizeof(NumeroMaquina) * quantidadeFuncoes);
	sistemaEqLineares(&quantidadeFuncoes, A, b, a);

	for (i = 0 ; i < quantidadeFuncoes; i++)
	{
		formatarNumeroMaquina(m, a[i], formatado);
		printf("a_%d = %s\n", i, formatado);
	}

	int done = 0;
	char opcao;
	double numeroUsuario;
	NumeroMaquina res, numero, soma;
	n2 = malloc(100);
	do
	{
		printf("Deseja calcular um numero (s/n)? ");
		scanf(" %c", &opcao);
		switch(opcao)
		{
			case 's':
			case 'S':
			case 'y':
			case 'Y':
				printf("Valor de x: ");
				scanf("%lf", &numeroUsuario);
				converterNumeroMaquina(m, numeroUsuario, &numero);
				converterNumeroMaquina(m, 0, &soma);
				for (i = 0; i < quantidadeFuncoes; i++)
				{
					G[i](m, numero, &res);
					multiplicar(m, res, a[i], &res);
					somar(m, res, soma, &soma);
				}
				formatarNumeroMaquina(m, numero, formatado);
				formatarNumeroMaquina(m, soma, n2);
				printf("Valor de f(%s): %s\n", formatado, n2);
				break;
			case 'n':
			case 'N':
				done = 1;
				break;
		}
	} while(!done);

	free(formatado);
	free(n2);
	for (i = 0; i < quantidadeFuncoesCadastradas; i++) free(funcao[i]);
	for (i = 0; i < quantidadeFuncoesCadastradas; i++) free(descricaoFuncao[i]);
	for (i = 0; i < quantidadeFuncoes; i++) free(A[i]);
	
	free(funcao);
	free(descricaoFuncao);
	free(tabelamento[0]);
	free(tabelamento[1]);
	free(tabelamento);
	free(G);
	free(A);
	free(b);
	free(a);
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

	for (i = 0; i < 3; i++) free(A[i]);
	free(A);
	free(x);
	free(b);
#endif

#ifdef DEBUG
	MaquinaPontoFlutuante m2 = lerMaquina();
	Funcao *G = (Funcao *)malloc(sizeof(Funcao *) * 2);
	G[0] = &const1;
	G[1] = &ident;
	NumeroMaquina **tabelamento = malloc(sizeof(NumeroMaquina *) * 2);
	tabelamento[0] = malloc(sizeof(NumeroMaquina) * 9);
	tabelamento[1] = malloc(sizeof(NumeroMaquina) * 9);
	A = malloc(2 * sizeof(NumeroMaquina*));
	b = malloc(2 * sizeof(NumeroMaquina));
	A[0] = malloc(2 * sizeof(NumeroMaquina));
	A[1] = malloc(2 * sizeof(NumeroMaquina));

	converterNumeroMaquina(m, 1, &tabelamento[0][0]);
	converterNumeroMaquina(m, 2, &tabelamento[0][1]);
	converterNumeroMaquina(m, 3, &tabelamento[0][2]);
	converterNumeroMaquina(m, 4, &tabelamento[0][3]);
	converterNumeroMaquina(m, 5, &tabelamento[0][4]);
	converterNumeroMaquina(m, 6, &tabelamento[0][5]);
	converterNumeroMaquina(m, 7, &tabelamento[0][6]);
	converterNumeroMaquina(m, 8, &tabelamento[0][7]);
	converterNumeroMaquina(m, 9, &tabelamento[0][8]);
	converterNumeroMaquina(m, 1.3, &tabelamento[1][0]);
	converterNumeroMaquina(m, 1.8, &tabelamento[1][1]);
	converterNumeroMaquina(m, 2.2, &tabelamento[1][2]);
	converterNumeroMaquina(m, 0.4, &tabelamento[1][3]);
	converterNumeroMaquina(m, 1.1, &tabelamento[1][4]);
	converterNumeroMaquina(m, 3.0, &tabelamento[1][5]);
	converterNumeroMaquina(m, 1.1, &tabelamento[1][6]);
	converterNumeroMaquina(m, 0.8, &tabelamento[1][7]);
	converterNumeroMaquina(m, 0.1, &tabelamento[1][8]);

	mmq(m2, 2, G, 9, tabelamento, A, b);
	char *formatado = malloc(100);
	for (i = 0; i < 2; i++)
	{
		for (j = 0; j < 2; j++)
		{
			formatarNumeroMaquina(m, A[i][j], formatado);
			printf("\t(%s a_%d)", formatado, j);
		}
		formatarNumeroMaquina(m, b[i], formatado);
		printf(" = %s\n", formatado);
	}
	
	for (i = 0; i < 2; i++) free(G[i]);
	for (i = 0; i < 2; i++) free(A[i]);
	for (i = 0; i < 2; i++) free(tabelamento[i]);

	free(formatado);
	free(G);
	free(A);
	free(b);
	free(tabelamento);
#endif


	do
	{
		printf("\n-----------------------\n");
		printf("Opcoes:\n");
		printf("n: Representar numero\n");
		printf("1: Operacoes matematicas basicas\n");
		printf("2: Sistemas de Equacoes Lineares\n");
		printf("4: Ajustamento\n");
		printf("x: Sair\n");
		scanf(" %c", &opcao);
		printf("Opcao escolhida: \"%c\"\n", opcao);
		switch(opcao)
		{
		case 'n':
			representarNumero();
			break;
		case '1':
			operacoes();
			break;
		case '2':
			sistemaEqLineares(NULL, NULL, NULL, NULL);
			break;
		case '4':
			ajustamento();
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

