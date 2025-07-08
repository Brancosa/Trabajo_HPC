import random
import time
import sys
SUSCEPTIBLE = "S"
INFECTED = "I"

M = int(sys.argv[1]) if len(sys.argv) > 1 else 80000          
initial_infected = 100

def paso_simulacion(poblacion):
    nueva_poblacion = poblacion.copy()
    for i, estado in enumerate(poblacion):
        if estado == INFECTED:
            vecinos = [i - 1, i + 1]
            for v in vecinos:
                if 0 <= v < len(poblacion) and poblacion[v] == SUSCEPTIBLE:
                    nueva_poblacion[v] = INFECTED
    return nueva_poblacion

def contar_estados(poblacion):
    return (
        poblacion.count(SUSCEPTIBLE),
        poblacion.count(INFECTED)
    )

def main():
    poblacion = [SUSCEPTIBLE] * M
    for i in range(initial_infected):
        poblacion[i] = INFECTED
    random.shuffle(poblacion)

    print(f"\nEstado inicial con M={M}, infectados iniciales={initial_infected}")
    start = time.time()
    paso = 0
    while True:
        poblacion = paso_simulacion(poblacion)
        S, I = contar_estados(poblacion)
        if paso % 500 == 0 or S == 0:
            tiempo_actual = time.time() - start
            print(f"Paso {paso}: S={S} I={I} | Tiempo: {tiempo_actual:.2f} s")
        paso += 1
        if S == 0:
            break
    end = time.time()

    print(f"\nToda la población fue infectada en {paso} pasos.")
    print(f"Tiempo total: {end - start:.2f} segundos.")

if __name__ == "__main__":
    main()
