/*
 * metodos.h
 *
 *  Created on: 26/09/2015
 *      Author: andre
 */

#ifndef METODOS_H_
#define METODOS_H_

typedef struct
{
	int base;
	int digitos;
	int e1;//menor expoente
	int e2;//maior expoente
} MaquinaPontoFlutuante;

typedef struct
{
	double significando;
	int expoente;
} NumeroMaquina;

void formatarMaquina(MaquinaPontoFlutuante m, char* formatada);
/**
erro: 1: Overflow, -1: Underflow
*/
int converterNumeroMaquina(MaquinaPontoFlutuante m, double numeroUsuario, NumeroMaquina* n);
double valorNumeroMaquina(MaquinaPontoFlutuante m, NumeroMaquina numero);
void formatarNumeroMaquina(MaquinaPontoFlutuante m, NumeroMaquina numero, char* res);
void arredondarNumeroMaquina(MaquinaPontoFlutuante m, NumeroMaquina* n);
/**
erro: 1: Overflow, -1: Underflow
*/
int somar(MaquinaPontoFlutuante m, NumeroMaquina n1, NumeroMaquina n2, NumeroMaquina* res);
/**
erro: 1: Overflow, -1: Underflow
*/
int multiplicar(MaquinaPontoFlutuante m, NumeroMaquina n1, NumeroMaquina n2, NumeroMaquina* res);
/**
erro: 1: Overflow, -1: Underflow, 100: div by zero
*/
int dividir(MaquinaPontoFlutuante m, NumeroMaquina n1, NumeroMaquina n2, NumeroMaquina* res);

int jacobi(MaquinaPontoFlutuante m, int tamanhoMatriz, NumeroMaquina** A, NumeroMaquina* b, NumeroMaquina* x);

#endif /* METODOS_H_ */
