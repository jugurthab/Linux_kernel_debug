# Chap1-userland-debug/valgrind/cachegrind
Work out example to check program's cache interaction using *valgrind-cachegrind*.  

# Usage

Compile program's sources with `debugging symbols` : 
> gcc cachegrind-test.c -o cachegrind-test -g

Launch cachegrind :
> valgrind --tool=cachegrind ./cachegrind-test

# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
