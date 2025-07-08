import numpy as np
import time

S = 0
I = 1
R = 2

M = 100000
initial_infected = 100
infection_prob = 1.0
recovery_prob = 0.0  # no recovery in this model

def paso_simulacion(poblacion):                                                                         
    infectados = np.where(poblacion == I)[0]
    nuevos_infectados = []

    for i in infectados:
        vecinos = [i - 1, i + 1]
        for v in vecinos:
            if 0 <= v < M and poblacion[v] == S:
                if np.random.random() < infection_prob:
                    nuevos_infectados.append(v)

    poblacion[nuevos_infectados] = I
    return poblacion

def contar_estados(poblacion):
    unique, counts = np.unique(poblacion, return_counts=True)
    cuenta = dict(zip(unique, counts))
    return (
        cuenta.get(S, 0),
        cuenta.get(I, 0),
        cuenta.get(R, 0),
    )

def main():
    poblacion = np.full(M, S, dtype=np.uint8)
    poblacion[:initial_infected] = I
    np.random.shuffle(poblacion)

    print(f"\nEstado inicial con M={M}, infectados iniciales={initial_infected}")
    start = time.time()
    paso = 0
    while True:
        poblacion = paso_simulacion(poblacion)
        s, i, r = contar_estados(poblacion)

        if paso % 500 == 0 or s == 0:
            print(f"Paso {paso}: S={s} I={i} R={r} | Tiempo: {time.time() - start:.2f} s")

        if s == 0:
            break
        paso += 1

    print(f"\nToda la población fue infectada en {paso} pasos.")
    print(f"Tiempo total: {time.time() - start:.2f} segundos.")

if __name__ == "__main__":
    main()
