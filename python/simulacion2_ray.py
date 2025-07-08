import random
import time
import sys
import ray

# Inicializa Ray
ray.init()

# Parámetros
M = 80000
NUM_ZONAS = 8
ZONE_SIZE = M // NUM_ZONAS
initial_infected = int(sys.argv[1]) if len(sys.argv) > 1 else 100
infection_prob = 1

@ray.remote
def paso_simulacion_zona(zona_idx, susceptibles_zona, infectados_global, M, infection_prob, zona_inicio, zona_fin):
    nuevos_infectados = set()

    for i in infectados_global:
        vecinos = [i - 1, i + 1]
        for v in vecinos:
            if zona_inicio <= v < zona_fin and v in susceptibles_zona:
                if random.random() < infection_prob:
                    nuevos_infectados.add(v)

    infectados_zona = set(infectados_global) & set(range(zona_inicio, zona_fin))
    infectados_zona |= nuevos_infectados
    susceptibles_zona -= nuevos_infectados

    return susceptibles_zona, infectados_zona

def main():
    todos = set(range(M))
    infectados = set(random.sample(range(M), initial_infected))
    susceptibles = todos - infectados

    # Dividir susceptibles e infectados por zonas
    susceptibles_zonas = []
    infectados_zonas = []

    for i in range(NUM_ZONAS):
        zona_inicio = i * ZONE_SIZE
        zona_fin = (i + 1) * ZONE_SIZE if i < NUM_ZONAS - 1 else M

        susceptibles_zona = {x for x in susceptibles if zona_inicio <= x < zona_fin}
        infectados_zona = {x for x in infectados if zona_inicio <= x < zona_fin}

        susceptibles_zonas.append(susceptibles_zona)
        infectados_zonas.append(infectados_zona)

    print(f"\nEstado inicial con M={M}, infectados iniciales={initial_infected}")
    start = time.time()
    paso = 0

    while True:
        futures = []
        for i in range(NUM_ZONAS):
            zona_inicio = i * ZONE_SIZE
            zona_fin = (i + 1) * ZONE_SIZE if i < NUM_ZONAS - 1 else M

            futures.append(paso_simulacion_zona.remote(
                i,
                susceptibles_zonas[i],
                infectados,  # global
                M,
                infection_prob,
                zona_inicio,
                zona_fin
            ))

        resultados = ray.get(futures)

        # Actualizar zonas
        susceptibles_zonas = []
        infectados_zonas = []
        for sus_zona, inf_zona in resultados:
            susceptibles_zonas.append(sus_zona)
            infectados_zonas.append(inf_zona)

        # Unir resultados globales
        susceptibles = set().union(*susceptibles_zonas)
        infectados = set().union(*infectados_zonas)

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
