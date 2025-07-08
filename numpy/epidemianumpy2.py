import numpy as np
import time
import sys

# Parámetros
M = int(sys.argv[1]) if len(sys.argv) > 1 else 80000
initial_infected = int(sys.argv[1]) if len(sys.argv) > 1 else 100
infection_prob = 1.0

def paso_simulacion_numpy(susceptibles_mask, infectados_indices):
    nuevos_infectados = []


    vecinos_izq = infectados_indices - 1
    vecinos_der = infectados_indices + 1


    vecinos_validos = np.concatenate([
        vecinos_izq[(vecinos_izq >= 0)],
        vecinos_der[(vecinos_der < M)]
    ])

    vecinos_susceptibles = vecinos_validos[susceptibles_mask[vecinos_validos]]

    if infection_prob == 1.0:
        nuevos_infectados = vecinos_susceptibles
    else:
        rand_vals = np.random.rand(len(vecinos_susceptibles))
        nuevos_infectados = vecinos_susceptibles[rand_vals < infection_prob]


    susceptibles_mask[nuevos_infectados] = False
    infectados_indices = np.unique(np.concatenate([infectados_indices, nuevos_infectados]))

    return susceptibles_mask, infectados_indices

def main():
    susceptibles_mask = np.ones(M, dtype=bool)

    infectados_indices = np.random.choice(M, size=initial_infected, replace=False)
    susceptibles_mask[infectados_indices] = False

    print(f"\nEstado inicial con M={M}, infectados iniciales={initial_infected}")
    start = time.time()
    paso = 0

    while True:
        susceptibles_mask, infectados_indices = paso_simulacion_numpy(susceptibles_mask, infectados_indices)
        S = np.count_nonzero(susceptibles_mask)
        I = len(infectados_indices)
        R = 0

        if paso % 500 == 0 or S == 0:
            tiempo_actual = time.time() - start
            print(f"Paso {paso}: S={S} I={I} R={R} | Tiempo: {tiempo_actual:.2f} s")

        paso += 1
        if S == 0:
            break

    end = time.time()
    print(f"\nToda la población fue infectada en {paso} pasos.")
    print(f"Tiempo total: {end - start:.2f} segundos.")

if __name__ == "__main__":
    main()
