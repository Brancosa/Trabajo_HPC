import random
import time
from epidemia_cy import paso_simulacion
import sys

# Parámetros
M = 240000
initial_infected = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
infection_prob = 1.0

def main():
    todos = set(range(M))
    infectados = set(random.sample(range(M), initial_infected))
    susceptibles = todos - infectados

    print(f"\nEstado inicial con M={M}, infectados iniciales={initial_infected}")
    start = time.time()
    paso = 0

    while True:
        susceptibles, infectados = paso_simulacion(susceptibles, infectados, M, infection_prob)
        S = len(susceptibles)
        I = len(infectados)
        R = 0
        if paso % 500 == 0 or S == 0:
            print(f"Paso {paso}: S={S} I={I} R={R} | Tiempo: {time.time() - start:.2f} s")
        paso += 1
        if S == 0:
            break

    end = time.time()
    print(f"\nToda la población fue infectada en {paso} pasos.")
    print(f"Tiempo total: {end - start:.2f} segundos.")

if __name__ == "__main__":
    main()
