// vector_add.cu - add two vectors on the GPU. Used in GPU Exercise 3.
//
// Build:  nvcc -O2 -o vector_add vector_add.cu
// Run:    ./vector_add [number_of_elements]     (default 16,777,216)
#include <cstdio>
#include <cstdlib>
#include <cuda_runtime.h>

#define CHECK(call)                                                        \
    do {                                                                   \
        cudaError_t err = (call);                                          \
        if (err != cudaSuccess) {                                          \
            fprintf(stderr, "CUDA error: %s (%s:%d)\n",                    \
                    cudaGetErrorString(err), __FILE__, __LINE__);          \
            exit(1);                                                       \
        }                                                                  \
    } while (0)

// Each GPU thread adds one pair of elements.
__global__ void vector_add(const float *a, const float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}

int main(int argc, char **argv) {
    int n = (argc > 1) ? atoi(argv[1]) : (1 << 24);
    size_t bytes = (size_t)n * sizeof(float);

    cudaDeviceProp prop;
    CHECK(cudaGetDeviceProperties(&prop, 0));
    printf("GPU: %s (compute capability %d.%d)\n", prop.name, prop.major, prop.minor);
    printf("Adding two vectors of %d elements\n", n);

    // Host (CPU) memory
    float *h_a = (float *)malloc(bytes);
    float *h_b = (float *)malloc(bytes);
    float *h_c = (float *)malloc(bytes);
    for (int i = 0; i < n; i++) { h_a[i] = 1.0f; h_b[i] = 2.0f; }

    // Device (GPU) memory
    float *d_a, *d_b, *d_c;
    CHECK(cudaMalloc(&d_a, bytes));
    CHECK(cudaMalloc(&d_b, bytes));
    CHECK(cudaMalloc(&d_c, bytes));

    cudaEvent_t start, stop;
    CHECK(cudaEventCreate(&start));
    CHECK(cudaEventCreate(&stop));

    CHECK(cudaMemcpy(d_a, h_a, bytes, cudaMemcpyHostToDevice));
    CHECK(cudaMemcpy(d_b, h_b, bytes, cudaMemcpyHostToDevice));

    int threads = 256;
    int blocks = (n + threads - 1) / threads;

    CHECK(cudaEventRecord(start));
    vector_add<<<blocks, threads>>>(d_a, d_b, d_c, n);
    CHECK(cudaGetLastError());
    CHECK(cudaEventRecord(stop));
    CHECK(cudaEventSynchronize(stop));

    float ms = 0.0f;
    CHECK(cudaEventElapsedTime(&ms, start, stop));
    CHECK(cudaMemcpy(h_c, d_c, bytes, cudaMemcpyDeviceToHost));

    // Check the answer: every element should be 3.0
    int errors = 0;
    for (int i = 0; i < n; i++) if (h_c[i] != 3.0f) errors++;

    // The kernel reads two vectors and writes one: 3 * bytes moved.
    printf("Kernel time: %.3f ms  (%.1f GB/s)\n", ms, 3.0 * bytes / (ms * 1e6));
    printf("%s (%d wrong elements)\n", errors == 0 ? "PASSED" : "FAILED", errors);

    cudaFree(d_a); cudaFree(d_b); cudaFree(d_c);
    free(h_a); free(h_b); free(h_c);
    return errors == 0 ? 0 : 1;
}
