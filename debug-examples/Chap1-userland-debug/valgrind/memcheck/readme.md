# Chap1-userland-debug/valgrind/memcheck
Examples illustrating how to troubleshoot common code's bottlenecks (*memory leaks*, *multiple deallocation of a resource*, ..., etc.) using the most known valgrind's utility : **memcheck**.   

# Usage
**memcheck** can point out several issues :

 - **Detecting memory leaks** : 
 
 > gcc memcheck-memory-leak.cpp -o memcheck-memory-leak -g

 > valgrind `--tool=memcheck` ./memcheck-memory-leak
 

 - **Reporting uninitialized variables** : 

> gcc memcheck-uninitialized-variable.cpp -o memcheck-uninitialized-variable -g

> valgrind `--tool=massif` ./memcheck-uninitialized-variable


- **Mismatch allocation and deallocation functions** : 

> gcc memcheck-mismatch-alloc-dealloc.cpp -o memcheck-mismatch-alloc-dealloc -g

> valgrind `--tool=massif` ./memcheck-mismatch-alloc-dealloc


- **Reading past-off  (after the end) a buffer** : 

> gcc memcheck-reading-past-buffer.cpp -o memcheck-reading-past-buffer -g

> valgrind `--tool=massif` ./memcheck-reading-past-buffer


- **Multiple deallocation of a resource** : 

> gcc memcheck-multiple-deallocation.cpp -o memcheck-multiple-deallocation -g

> valgrind `--tool=massif` ./memcheck-multiple-deallocation


# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
