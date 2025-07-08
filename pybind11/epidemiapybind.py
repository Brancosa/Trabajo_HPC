import numpy as np
import simulacion
import time
import sys

#M = 100000000
M = int(sys.argv[1]) if len(sys.argv) > 1 else 80000
initial_infected = int(sys.argv[1]) if len(sys.argv) > 1 else 20000000
infection_prob = 1.0

susceptibles_mask = np.ones(M, dtype=bool)
infectados_indices = np.random.choice(M, initial_infected, replace=False)
susceptibles_mask[infectados_indices] = False

print(f"Estado inicial con M={M}, infectados iniciales={initial_infected}")
start = time.time()
paso = 0

while True:
    susceptibles_mask, infectados_indices = simulacion.paso_simulacion_cpp(susceptibles_mask, infectados_indices, infection_prob)
    S = np.count_nonzero(susceptibles_mask)
    I = len(infectados_indices)
    if paso % 500 == 0 or S == 0:
        print(f"Paso {paso}: S={S} I={I} | Tiempo: {time.time() - start:.2f} s")
    paso += 1
    if S == 0:
        break

print(f"\nToda la población fue infectada en {paso} pasos.")
print(f"Tiempo total: {time.time() - start:.2f} segundos.")
