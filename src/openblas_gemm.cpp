#include <cblas.h>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

unsigned long long N;
unsigned long long ITERATIONS;
using namespace std;

double timestamp() {
  struct timeval tv;
  gettimeofday(&tv, 0);
  return tv.tv_sec + 1e-6 * tv.tv_usec;
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

  float a = 1.0, b = 0.0;
  for (int i = 0; i < N * N; i++) {
    A[i] = (float)rand() / (float)(RAND_MAX / a);
    B[i] = (float)rand() / (float)(RAND_MAX / a);
    C[i] = 0;
  }

  double time1 = timestamp();
  for (int numOfTimes = 0; numOfTimes < ITERATIONS; numOfTimes++) {
    cblas_sgemm(CblasRowMajor, // Storage order (row-major)
                CblasNoTrans,  // Don't transpose A
                CblasNoTrans,  // Don't transpose B
                N,             // Rows in A and C
                N,             // Columns in B and C
                N,             // Columns in A and Rows in B
                a,             // alpha (scalar for A*B)
                A,             // Matrix A
                N,             // Leading dimension of A (columns for row-major)
                B,             // Matrix B
                N,             // Leading dimension of B
                b,             // beta (scalar for C)
                C,             // Matrix C
                N              // Leading dimension of C
    );
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
  result_file << "openblas," << N << "," << gflopsPerSecond << ","
              << flops / (1000000000) << "," << time << "\n";
  result_file.close();

  delete[] A;
  delete[] B;
  delete[] C;

  return 0;
}