# sim_cython.pyx
from libc.stdlib cimport rand, srand
from libc.time cimport time as ctime
cimport cython

cdef int M = 100000
cdef double infection_prob = 1.0

@cython.boundscheck(False)
@cython.wraparound(False)
def paso_simulacion(int[:] estado):
    cdef int i
    cdef int nuevos_infectados = 0
    cdef int infectado_actual
    cdef int vecino
    
    # Copia del estado para actualizar simultáneamente
    cdef int[:] nuevo_estado = estado.copy()
    
    for i in range(M):
        if estado[i] == 1:  # infectado
            # Vecinos
            for vecino in (i-1, i+1):
                if 0 <= vecino < M and estado[vecino] == 0:
                    # Probabilidad de infección
                    if (rand() / <double> RAND_MAX) < infection_prob:
                        nuevo_estado[vecino] = 1
                        nuevos_infectados += 1
    
    for i in range(M):
        estado[i] = nuevo_estado[i]
    
    return nuevos_infectados
