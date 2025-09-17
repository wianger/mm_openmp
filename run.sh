make
echo "Benchmark:"
./build/benchmark 1000
echo "Main:"
./build/main 1000

if diff -q ./result/benchmark_res.txt ./result/main_res.txt >/dev/null; then
    echo "no difference"
else
    code=$?
    if [ $code -eq 1 ]; then
        echo "differences found"
    else
        echo "diff error (code=2)"
    fi
fi
