make
N=$1
echo "baseline:"
./build/baseline $N
echo "1d_array:"
./build/1d_array $N
echo "omp_naive:"
./build/omp_naive $N
echo "omp_1d_array:"
./build/omp_1d_array $N
echo "loop_interchange:"
./build/loop_interchange $N
echo "omp_loop_interchange:"
./build/omp_loop_interchange $N
