#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <vector>
#include <algorithm>
#include <omp.h>
#include <random>

namespace py = pybind11;

py::tuple paso_simulacion_cpp_omp(py::array_t<bool> susceptibles_mask, py::array_t<int> infectados_indices, double infection_prob) {
    auto sus = susceptibles_mask.mutable_unchecked<1>();
    auto infectados = infectados_indices.unchecked<1>();
    int M = susceptibles_mask.shape(0);

    int num_threads = omp_get_max_threads();
    std::vector<std::vector<int>> infectados_por_hilo(num_threads);

    #pragma omp parallel
    {
        int tid = omp_get_thread_num();
        std::mt19937 rng(static_cast<unsigned int>(std::random_device{}()) + tid);
        std::uniform_real_distribution<double> dist(0.0, 1.0);

        std::vector<int> &local_infectados = infectados_por_hilo[tid];

        #pragma omp for
        for (ssize_t i = 0; i < infectados.shape(0); ++i) {
            int idx = infectados[i];

            if (idx > 0 && sus(idx - 1)) {
                double r = dist(rng);
                if (infection_prob >= 1.0 || r < infection_prob) {
                    local_infectados.push_back(idx - 1);
                }
            }

            if (idx < M - 1 && sus(idx + 1)) {
                double r = dist(rng);
                if (infection_prob >= 1.0 || r < infection_prob) {
                    local_infectados.push_back(idx + 1);
                }
            }
        }
    }

    // Combinar vectores locales fuera de la región paralela
    std::vector<int> nuevos_infectados_vec;
    for (const auto& vec : infectados_por_hilo) {
        nuevos_infectados_vec.insert(nuevos_infectados_vec.end(), vec.begin(), vec.end());
    }

    // Eliminar duplicados
    std::sort(nuevos_infectados_vec.begin(), nuevos_infectados_vec.end());
    nuevos_infectados_vec.erase(std::unique(nuevos_infectados_vec.begin(), nuevos_infectados_vec.end()), nuevos_infectados_vec.end());

    // Marcar como no susceptibles
    #pragma omp parallel for
    for (size_t i = 0; i < nuevos_infectados_vec.size(); ++i) {
        sus(nuevos_infectados_vec[i]) = false;
    }

    // Unir infectados antiguos y nuevos
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
    m.doc() = "Modulo para simulacion epidemiologica acelerada con pybind11 y OpenMP";
    m.def("paso_simulacion_cpp_omp", &paso_simulacion_cpp_omp, "Un paso de simulacion paralelizado",
          py::arg("susceptibles_mask"), py::arg("infectados_indices"), py::arg("infection_prob"));
}
