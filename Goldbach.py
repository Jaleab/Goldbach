#!/usr/bin/python3

from mpi4py import MPI
import random
import math
import numpy as np
import matplotlib.pyplot as plt

def goldbach(primos, numero):
	expression = [];
	n = numero;
	size = len(primos)
	for i in reversed(range(len(primos))):
		if primos[i] <= n and n - primos[i] >= 2:
			expression.append(primos[i])
			n = n - primos[i]
			break #i = -1
	for i in reversed(range(len(primos))):
		if primos[i] <= n and n - primos[i] >= 2 or n - primos[i] == 0 :
			expression.append(primos[i])
			n = n - primos[i]
			break #i = -1
	for i in reversed(range(len(primos))):
		if primos[i] <= n and n - primos[i] >= 0 or n - primos[i] == 0:
			expression.append(primos[i])
			n = n - primos[i]
			break #i = -1	
	return expression
	
def setPrimos(v):
	primos = [2,3]
	for i in range(len(v)):
		esPrimo = 1
		for j in range(len(primos)):
			if v[i] % primos[j] == 0:
				esPrimo = 0
		if esPrimo == 1:
			primos.append(v[i])
	return primos

def fillVector(v, n):
	for i in range(5,n+1):
		v.append(i)

def main():
	comm = MPI.COMM_WORLD
	pid = comm.rank
	size = comm.size
	v = []
	expression = []
	n = 0
	goldbachs = []
	if pid == 0:
		n = int(input("Digite el n: "))
		fillVector(v, n)
		v = setPrimos(v)
	v = comm.bcast(v,0)
	n = comm.bcast((n),0)
	comm.Barrier()	
	t_start = MPI.Wtime()
	chunkSize = n//size
	offset = ((chunkSize) * pid) + 5
	if pid == size-1:
		chunkSize = (n+1) - (offset)
	for i in range(offset, offset+chunkSize, 1):
		expression.append(goldbach(v,i))
	comm.Barrier()
	expression = comm.reduce(expression, op=MPI.SUM)
	comm.Barrier()	
	diff_time = MPI.Wtime() - t_start
	if pid == 0:
		for i in range(len(expression)):
			if len(expression[i]) == 2:
				print(expression[i][0]+expression[i][1], " = ", expression[i][0], " + ", expression[i][1])
			else:
				print(expression[i][0]+expression[i][1]+expression[i][2], " = ", expression[i][0], " + ", expression[i][1], " + ", expression[i][2])
		print(diff_time)
main()