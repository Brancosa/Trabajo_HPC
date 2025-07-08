#include <iostream>
#include <vector>
#include <random>
#include <cuda.h>
#include <curand_kernel.h>

const int M = 1000;             // Tamaño población
const int initial_infected = 10; // Infectados iniciales
const float infection_prob = 1.0f; // Probabilidad infección (1.0 para que siempre infecte)

// Kernel CUDA para intentar infectar vecinos de cada infectado
__global__ void infectar_vecinos(
    bool* susceptibles_mask,
    bool* nuevos_infectados_mask,
    const int* infectados_indices,
    int num_infectados,
    int M,
    float infection_prob,
    unsigned long long seed)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= num_infectados) return;

    int idx = infectados_indices[i];

    // Inicializar estado aleatorio per hilo
    curandState state;
    curand_init(seed, i, 0, &state);

    // Vecinos a infectar: idx-1 e idx+1
    int vecinos[2] = { idx - 1, idx + 1 };

    for (int j = 0; j < 2; ++j) {
        int vecino = vecinos[j];
        if (vecino >= 0 && vecino < M) {
            if (susceptibles_mask[vecino]) {
                float p = curand_uniform(&state);
                if (p < infection_prob) {
                    nuevos_infectados_mask[vecino] = true;
                }
            }
        }
    }
}

int main() {
    // Inicializar población en host
    std::vector<bool> susceptibles_mask(M, true);
    std::vector<int> infectados_indices;

    // Infectar inicialmente aleatoriamente
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, M - 1);
    while ((int)infectados_indices.size() < initial_infected) {
        int x = dis(gen);
        if (susceptibles_mask[x]) {
            susceptibles_mask[x] = false;
            infectados_indices.push_back(x);
        }
    }

    // Buffers device
    bool *d_susceptibles_mask, *d_nuevos_infectados_mask;
    int *d_infectados_indices;

    cudaMalloc(&d_susceptibles_mask, M * sizeof(bool));
    cudaMalloc(&d_nuevos_infectados_mask, M * sizeof(bool));

    int max_infectados = M; // máximo posible infectados

    cudaMalloc(&d_infectados_indices, max_infectados * sizeof(int));

    int paso = 0;
    while (true) {
        // Copiar datos a device
        cudaMemcpy(d_susceptibles_mask, susceptibles_mask.data(), M * sizeof(bool), cudaMemcpyHostToDevice);
        cudaMemcpy(d_infectados_indices, infectados_indices.data(), infectados_indices.size() * sizeof(int), cudaMemcpyHostToDevice);
        cudaMemset(d_nuevos_infectados_mask, 0, M * sizeof(bool));

        // Lanzar kernel
        int blockSize = 256;
        int numBlocks = (int)((infectados_indices.size() + blockSize - 1) / blockSize);
        infectar_vecinos<<<numBlocks, blockSize>>>(
            d_susceptibles_mask,
            d_nuevos_infectados_mask,
            d_infectados_indices,
            (int)infectados_indices.size(),
            M,
            infection_prob,
            1234ULL + paso);

        cudaDeviceSynchronize();

        // Copiar nuevos infectados a host
        std::vector<bool> nuevos_infectados_mask(M);
        cudaMemcpy(nuevos_infectados_mask.data(), d_nuevos_infectados_mask, M * sizeof(bool), cudaMemcpyDeviceToHost);

        // Actualizar máscaras y lista de infectados en host
        int nuevos = 0;
        for (int i = 0; i < M; ++i) {
            if (nuevos_infectados_mask[i] && susceptibles_mask[i]) {
                susceptibles_mask[i] = false;
                infectados_indices.push_back(i);
                nuevos++;
            }
        }

        int susceptibles = 0;
        for (bool b : susceptibles_mask) if (b) susceptibles++;

        std::cout << "Paso " << paso << ": Infectados = " << infectados_indices.size() << " Susceptibles = " << susceptibles << std::endl;

        paso++;

        if (nuevos == 0 || susceptibles == 0) {
            std::cout << "No hay nuevos infectados o se infectó toda la población.\n";
            break;
        }
    }

    cudaFree(d_susceptibles_mask);
    cudaFree(d_nuevos_infectados_mask);
    cudaFree(d_infectados_indices);

    return 0;
}
