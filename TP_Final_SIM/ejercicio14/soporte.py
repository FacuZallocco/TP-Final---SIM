import math
import random


def generarDemanda(contador):
    # normal
    global random1, random2
    if contador == 0:
        random1 = random.random()
        random2 = random.random()
        n1 = ((math.sqrt(-2 * math.log(random1)) * math.cos(2 * math.pi * random2)) * 50) + 300
        #n2 = ((math.sqrt(-2 * math.log(random1)) * math.sin(2 * math.pi * random2)) * 50) + 300
        #print(n1, n2)
        return n1

    elif contador == 1:
        n2 = ((math.sqrt(-2 * math.log(random1)) * math.sin(2 * math.pi * random2)) * 50) + 300
        #print("Otro camino", n2)
        return n2


def generarDemora():
    # exponencial
    u = 8
    v = [0]
    for i in range(len(v)):
        if i == 0:
            v[i] = (-u) * math.log(1 - random.random())
    if int(v[0]) == 0:
        return 1
    return int(v[0])
