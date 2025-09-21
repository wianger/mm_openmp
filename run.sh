make
N=$1
ITERATIONS=$2
for file in build/*; do
    echo "$file:"
    ./$file $N $ITERATIONS
    echo ""
done
