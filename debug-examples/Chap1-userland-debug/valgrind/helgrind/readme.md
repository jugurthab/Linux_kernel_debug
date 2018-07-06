# Chap1-userland-debug/valgrind/helgrind
Work out example to analyse multithreaded applications using *valgrind-helgrind*.  

# Usage

Compile program's sources with `debugging symbols` : 
> gcc hellgrind-thread-posix.c -o hellgrind-thread-posix -g

Launch dhat :
> valgrind `--tool=helgrind` ./hellgrind-thread-posix

# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
