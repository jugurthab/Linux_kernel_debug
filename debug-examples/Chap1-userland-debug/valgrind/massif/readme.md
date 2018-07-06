# Chap1-userland-debug/valgrind/massif
Monitor application's memory usage during it's lifecycle using *valgrind-massif*.  

# Usage

Compile program's sources with `debugging symbols` : 
> gcc heap-usage-massif.c -o heap-usage-massif -g

Launch dhat :
> valgrind `--tool=massif` ./heap-usage-massif

# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
