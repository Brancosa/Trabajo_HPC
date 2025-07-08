# sim_cython.pyx
import numpy as np
cimport numpy as np
from libc.stdlib cimport rand, srand
from libc.time cimport time

ctypedef np.int64_t np_int_t
ctypedef np.npy_bool np_bool_t

def paso_simulacion_cython(np.ndarray[np_bool_t, ndim=1] susceptibles_mask,
                           np.ndarray[np_int_t, ndim=1] infectados_indices,
                           int M,
                           double infection_prob):
    cdef np.ndarray[np_int_t, ndim=1] vecinos_izq
    cdef np.ndarray[np_int_t, ndim=1] vecinos_der
    cdef np.ndarray[np_int_t, ndim=1] vecinos_validos
    cdef np.ndarray[np_bool_t, ndim=1] suscep_mask
    cdef np.ndarray[np_int_t, ndim=1] vecinos_susceptibles
    cdef np.ndarray[np.float64_t, ndim=1] rand_vals
    
    cdef int i, j, k
    cdef int num_vecinos
    cdef int num_susceptibles
    cdef int infectados_len = infectados_indices.shape[0]
    
    # Vecinos a izquierda y derecha (con límites)
    vecinos_izq = infectados_indices - 1
    vecinos_der = infectados_indices + 1
    
    # Filtrar vecinos válidos (entre 0 y M-1)
    vecinos_validos = np.concatenate((vecinos_izq, vecinos_der))
    vecinos_validos = vecinos_validos[(vecinos_validos >= 0) & (vecinos_validos < M)]
    
    # Filtrar sólo los vecinos susceptibles
    suscep_mask = susceptibles_mask[vecinos_validos]
    vecinos_susceptibles = vecinos_validos[suscep_mask]
    
    num_susceptibles = vecinos_susceptibles.shape[0]
    
    # Generar valores aleatorios para infección
    rand_vals = np.random.rand(num_susceptibles)
    
    # Infectar con probabilidad infection_prob
    for i in range(num_susceptibles):
        if rand_vals[i] < infection_prob:
            susceptibles_mask[vecinos_susceptibles[i]] = False
    
    # Nuevos infectados son los que acaban de infectarse (los vecinos ahora no susceptibles)
    # Encontrar índices donde susceptibles_mask es False y no estaban infectados antes
    # Actualizar infectados_indices con los infectados anteriores + nuevos infectados
    
    # Una forma eficiente:
    new_infectados_mask = ~susceptibles_mask
    infectados_mask = np.zeros(M, dtype=bool)
    infectados_mask[infectados_indices] = True
    
    nuevos_infectados_mask = new_infectados_mask & (~infectados_mask)
    nuevos_indices = np.flatnonzero(nuevos_infectados_mask)
    
    # Concatenar infectados anteriores + nuevos
    infectados_indices = np.concatenate((infectados_indices, nuevos_indices))
    
    return susceptibles_mask, infectados_indices
