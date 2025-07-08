#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <vector>
#include <random>
#include <omp.h>

namespace py = pybind11;

py::tuple paso_simulacion_cpp_omp(py::array_t<bool> susceptibles_mask, py::array_t<int> infectados_indices, double infection_prob) {
    auto sus = susceptibles_mask.mutable_unchecked<1>();
    auto infectados = infectados_indices.unchecked<1>();
    ssize_t M = sus.shape(0);

    std::vector<int> nuevos_infectados_vec;
    nuevos_infectados_vec.reserve(2 * infectados.shape(0));  

    
    #pragma omp parallel
    {
        
        std::random_device rd;
        std::mt19937 gen(rd() + omp_get_thread_num());
        std::uniform_real_distribution<> dis(0.0, 1.0);

        std::vector<int> local_new_infected;
        local_new_infected.reserve(1000);

        //#pragma omp for schedule(guided)
        #pragma omp for nowait
        for (ssize_t i = 0; i < infectados.shape(0); ++i) {
            int idx = infectados[i];

            for (int vecino : {idx - 1, idx + 1}) {
                if (vecino >= 0 && vecino < M) {
                    
                    if (sus(vecino)) {
                        double rand_val = dis(gen);
                        if (infection_prob >= 1.0 || rand_val < infection_prob) {
                            local_new_infected.push_back(vecino);
                        }
                    }
                }
            }
        }

        // Actualizar susceptibles
        #pragma omp critical
        {
            for (int ni : local_new_infected) {
                if (sus(ni)) { 
                    sus(ni) = false;
                    nuevos_infectados_vec.push_back(ni);
                }
            }
        }
    }

    // Concatenar infectados anteriores con nuevos
    std::vector<int> infectados_actualizados(infectados.shape(0) + nuevos_infectados_vec.size());
    std::copy(infectados.data(0), infectados.data(0) + infectados.shape(0), infectados_actualizados.begin());
    std::copy(nuevos_infectados_vec.begin(), nuevos_infectados_vec.end(), infectados_actualizados.begin() + infectados.shape(0));

    py::array_t<int> infectados_np(infectados_actualizados.size());
    auto buf = infectados_np.mutable_unchecked<1>();
    for (size_t i = 0; i < infectados_actualizados.size(); ++i) {
        buf(i) = infectados_actualizados[i];
    }

    return py::make_tuple(susceptibles_mask, infectados_np);
}

PYBIND11_MODULE(simulacion, m) {
    m.doc() = "Simulación epidemiológica paralelizada con OpenMP y generadores aleatorios por hilo";
    m.def("paso_simulacion_cpp_omp", &paso_simulacion_cpp_omp,
          py::arg("susceptibles_mask"), py::arg("infectados_indices"), py::arg("infection_prob"));
}
