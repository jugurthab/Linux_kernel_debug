# Chap1-userland-debug/valgrind/drd
Work out example to analyse multithreaded applications using *valgrind-drd*.  

# Usage

Compile program's sources with `debugging symbols` : 
> gcc unlock-unlocked-mutex-DRD.c -o unlock-unlocked-mutex-DRD -g

Launch dhat :
> valgrind --tool=drd ./unlock-unlocked-mutex-DRD

# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
