import numpy as np
import time
from sim_cython import paso_simulacion_cython

# Parámetros
M = 1000000
initial_infected = 100
infection_prob = 1.0  # Puedes modificar si quieres menos que 1.0

def main():
    susceptibles_mask = np.ones(M, dtype=bool)
    infectados_indices = np.random.choice(M, size=initial_infected, replace=False)
    susceptibles_mask[infectados_indices] = False

    print(f"\nEstado inicial con M={M}, infectados iniciales={initial_infected}")
    start = time.time()
    paso = 0

    while True:
        susceptibles_mask, infectados_indices = paso_simulacion_cython(
            susceptibles_mask,
            infectados_indices,
            M,
            infection_prob
        )
        S = np.count_nonzero(susceptibles_mask)
        I = len(infectados_indices)
        R = 0  # No implementado

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
