# Chap1-userland-debug/valgrind/callgrind
Work out example to check program's cache interaction using *valgrind-callgrind*.  

# Usage

Compile program's sources with `debugging symbols` : 
> gcc callgrind-test.c -o callgrind-test -g

Launch callgrind :
> valgrind --tool=callgrind ./callgrind-test

# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
