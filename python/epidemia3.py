import random
import time
import sys

# Parámetros
#M = 80000
M = int(sys.argv[1]) if len(sys.argv) > 1 else 80000
initial_infected = int(sys.argv[2]) if len(sys.argv) > 2 else 100
infection_prob = 1



def paso_simulacion(susceptibles, infectados):
    nuevos_infectados = set()

    for i in infectados:
        vecinos = [i - 1, i + 1]
        for v in vecinos:
            if 0 <= v < M and v in susceptibles:
                if random.random() < infection_prob:
                    nuevos_infectados.add(v)

    
    infectados |= nuevos_infectados
    susceptibles -= nuevos_infectados
    return susceptibles, infectados

def main():
    todos = set(range(M))
    infectados = set(random.sample(range(M), initial_infected))
    susceptibles = todos - infectados

    print(f"\nEstado inicial con M={M}, infectados iniciales={initial_infected}")
    start = time.time()
    paso = 0

    while True:
        susceptibles, infectados = paso_simulacion(susceptibles, infectados)
        S = len(susceptibles)
        I = len(infectados)
        if paso % 500 == 0 or S == 0:
            tiempo_actual = time.time() - start
            print(f"Paso {paso}: S={S} I={I}| Tiempo: {tiempo_actual:.2f} s")
        paso += 1
        if S == 0:
            break

    end = time.time()
    print(f"\nToda la población fue infectada en {paso} pasos.")
    print(f"Tiempo total: {end - start:.2f} segundos.")

if __name__ == "__main__":
    main()
