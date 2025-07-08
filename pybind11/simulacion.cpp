#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <vector>
#include <algorithm>

namespace py = pybind11;

//constexpr int M = 10000000;

py::tuple paso_simulacion_cpp(py::array_t<bool> susceptibles_mask, py::array_t<int> infectados_indices, double infection_prob) {
    // Obtener buffers (sin copiar memoria)
    auto sus = susceptibles_mask.mutable_unchecked<1>();  // 1D array bool
    auto infectados = infectados_indices.unchecked<1>(); // 1D array int
    ssize_t M = sus.shape(0);

    std::vector<int> nuevos_infectados_vec;

    // Para cada infectado, revisar vecinos
    for (ssize_t i = 0; i < infectados.shape(0); ++i) {
        int idx = infectados[i];
        // Vecinos posibles
        if (idx > 0 && sus(idx-1)) {
            // infectar con probabilidad
            if (infection_prob >= 1.0 || (double)rand() / RAND_MAX < infection_prob) {
                nuevos_infectados_vec.push_back(idx - 1);
            }
        }
        if (idx < M - 1 && sus(idx+1)) {
            if (infection_prob >= 1.0 || (double)rand() / RAND_MAX < infection_prob) {
                nuevos_infectados_vec.push_back(idx + 1);
            }
        }
    }

    // Eliminar duplicados y mantener únicos
    std::sort(nuevos_infectados_vec.begin(), nuevos_infectados_vec.end());
    nuevos_infectados_vec.erase(std::unique(nuevos_infectados_vec.begin(), nuevos_infectados_vec.end()), nuevos_infectados_vec.end());

    // Actualizar máscara de susceptibles e infectados
    for (int ni : nuevos_infectados_vec) {
        sus(ni) = false;
    }

    // Concatenar infectados antiguos con nuevos infectados
    std::vector<int> infectados_actualizados(infectados.shape(0) + nuevos_infectados_vec.size());
    std::copy(infectados.data(0), infectados.data(0) + infectados.shape(0), infectados_actualizados.begin());
    std::copy(nuevos_infectados_vec.begin(), nuevos_infectados_vec.end(), infectados_actualizados.begin() + infectados.shape(0));

    // Crear numpy array para infectados actualizados
    //py::array_t<int> infectados_np(infectados_actualizados.size(), infectados_actualizados.data()); aqui lo cambie por lo de abajo


    // Crear numpy array vacío del tamaño necesario
    py::array_t<int> infectados_np(infectados_actualizados.size());

    // Obtener acceso mutable al buffer
    auto buf = infectados_np.mutable_unchecked<1>();

    // Copiar los valores del vector al array numpy
    for (size_t i = 0; i < infectados_actualizados.size(); ++i) {
        buf(i) = infectados_actualizados[i];
}

    return py::make_tuple(susceptibles_mask, infectados_np);
}

PYBIND11_MODULE(simulacion, m) {
    m.doc() = "Modulo para simulacion epidemiologica acelerada con pybind11";
    m.def("paso_simulacion_cpp", &paso_simulacion_cpp, "Un paso de simulacion",
          py::arg("susceptibles_mask"), py::arg("infectados_indices"), py::arg("infection_prob"));
}
