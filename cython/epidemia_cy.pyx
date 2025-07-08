# epidemia_cy.pyx
# cython: language_level=3
# cython: boundscheck=False, wraparound=False

from libc.stdlib cimport rand, RAND_MAX
cimport cython

@cython.cdivision(True)
cdef inline double crandom():
    return rand() / <double>RAND_MAX

cpdef paso_simulacion(set susceptibles, set infectados, int M, double infection_prob):
    cdef set nuevos_infectados = set()
    cdef int i, v

    for i in infectados:
        for v in [i - 1, i + 1]:
            if 0 <= v < M and v in susceptibles:
                if crandom() < infection_prob:
                    nuevos_infectados.add(v)

    infectados.update(nuevos_infectados)
    susceptibles.difference_update(nuevos_infectados)
    return susceptibles, infectados
