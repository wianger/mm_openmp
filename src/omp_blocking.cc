#include <algorithm>
#include <fstream>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

unsigned long long N;
unsigned long long ITERATIONS;
constexpr unsigned long long block_size = 32;
using namespace std;

double timestamp() {
  struct timeval tv;
  gettimeofday(&tv, 0);
  return tv.tv_sec + 1e-6 * tv.tv_usec;
}

void mm(float a, float b, float *A, float *B, float *C) {
#pragma omp parallel for schedule(static)
  for (int i0 = 0; i0 < N; i0 += block_size) {
    for (int j0 = 0; j0 < N; j0 += block_size) {
      for (int k0 = 0; k0 < N; k0 += block_size) {
        for (int i = i0; i < std::min(i0 + block_size, N); i++) {
          for (int k = k0; k < std::min(k0 + block_size, N); k++) {
            const float r = a * A[i * N + k];
            for (int j = j0; j < std::min(j0 + block_size, N); j++) {
              C[i * N + j] += r * B[k * N + j];
            }
          }
        }
      }
    }
  }
}

int main(int argc, char *argv[]) {
  if (argc != 3) {
    fprintf(stderr, "Usage: %s <matrix_size> <iterations>\n", argv[0]);
    return 1;
  }
  N = strtoull(argv[1], NULL, 10);
  ITERATIONS = strtoull(argv[2], NULL, 10);
  float *A = new float[N * N];
  float *B = new float[N * N];
  float *C = new float[N * N];

  float a = 0.5, b = 0.3;
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      A[i * N + j] = (float)rand() / (float)(RAND_MAX / a);
      B[i * N + j] = (float)rand() / (float)(RAND_MAX / a);
      C[i * N + j] = 0;
    }
  }

  for (int j = 0; j < N; j++) {
    for (int i = 0; i < N; i++) {
      C[i * N + j] += b * C[i * N + j];
      float tmp = 0;
      for (int k = 0; k < N; k++) {
        // C[i][j] += a*A[i][k]*B[k][j];
        tmp += A[i * N + k] * B[k * N + j];
      }
      C[i * N + j] += tmp * a;
    }
  }

  for (int i = 0; i < N * N; i++) {
    C[i] = 0;
  }

  double time1 = timestamp();
  for (int numOfTimes = 0; numOfTimes < ITERATIONS; numOfTimes++) {
    mm(a, b, A, B, C);
  }
  double time2 = timestamp();

  double time = (time2 - time1) / ITERATIONS;
  double flops = 2 * N * N + 2 * N * N * N + 2 * N * N;
  // double flops = 2*N*N + 2*N*N*N + N*N*N;
  double gflopsPerSecond = flops / (1000000000) / time;
  printf("GFLOPS/s=%lf\n", gflopsPerSecond);
  printf("GFLOPS=%lf\n", flops / (1000000000));
  printf("time(s)=%lf\n", time);

  fstream result_file("./result/result.csv", ios::app);
  result_file << "omp_blocking," << N << "," << gflopsPerSecond << ","
              << flops / (1000000000) << "," << time << "\n";
  result_file.close();

  delete[] A;
  delete[] B;
  delete[] C;

  return 0;
}
