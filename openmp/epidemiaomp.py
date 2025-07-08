import numpy as np
import simulacion
import time
import sys

def main():

    #M = 100000000
    M = 100000000
    
    initial_infected = int(sys.argv[1]) if len(sys.argv) > 1 else 10000000
    infection_prob = 1.0  # puedes cambiar este valor entre 0 y 1

    # Inicializar población
    susceptibles_mask = np.ones(M, dtype=bool)
    infectados_indices = np.random.choice(M, initial_infected, replace=False)
    susceptibles_mask[infectados_indices] = False

    print(f"Estado inicial con M={M}, infectados iniciales={initial_infected}")
    start = time.time()
    paso = 0

    while True:
        susceptibles_mask, infectados_indices = simulacion.paso_simulacion_cpp_omp(
            susceptibles_mask, infectados_indices, infection_prob
        )

        S = np.count_nonzero(susceptibles_mask)
        I = len(infectados_indices)
        R = 0  # no hay recuperados en este modelo

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
