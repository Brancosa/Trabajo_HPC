#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <unordered_set>
#include <vector>
#include <cstdlib>
#include <ctime>

namespace py = pybind11;

py::tuple paso_simulacion_cpp(py::array_t<bool> susceptibles_mask, py::array_t<int> infectados_indices, double infection_prob) {
    auto sus = susceptibles_mask.mutable_unchecked<1>();
    auto infectados = infectados_indices.unchecked<1>();
    ssize_t M = sus.shape(0);

    std::unordered_set<int> nuevos_infectados;

    for (ssize_t i = 0; i < infectados.shape(0); ++i) {
        int idx = infectados[i];
        for (int vecino : {idx - 1, idx + 1}) {
            if (0 <= vecino && vecino < M && sus(vecino)) {
                if (infection_prob >= 1.0 || static_cast<double>(rand()) / RAND_MAX < infection_prob) {
                    nuevos_infectados.insert(vecino);
                    sus(vecino) = false;
                }
            }
        }
    }

    std::vector<int> infectados_actualizados;
    infectados_actualizados.reserve(infectados.shape(0) + nuevos_infectados.size());

    for (ssize_t i = 0; i < infectados.shape(0); ++i)
        infectados_actualizados.push_back(infectados[i]);

    for (int ni : nuevos_infectados)
        infectados_actualizados.push_back(ni);

    py::array_t<int> infectados_np(infectados_actualizados.size());
    auto buf = infectados_np.mutable_unchecked<1>();
    for (size_t i = 0; i < infectados_actualizados.size(); ++i)
        buf(i) = infectados_actualizados[i];

    return py::make_tuple(susceptibles_mask, infectados_np);
}

PYBIND11_MODULE(simulacion, m) {
    m.doc() = "Modulo para simulacion epidemiologica acelerada con pybind11";
    m.def("paso_simulacion_cpp", &paso_simulacion_cpp,
          py::arg("susceptibles_mask"), py::arg("infectados_indices"), py::arg("infection_prob"));
}
