# Chap1-userland-debug/valgrind/dhat
Work out example to profile program's heap using *valgrind-dhat*.  

# Usage

Compile program's sources with `debugging symbols` : 
> gcc multiple-block-allocation-DHAT.c -o multiple-block-allocation-DHAT -g

Launch dhat :
> valgrind --tool=exp-dhat ./multiple-block-allocation-DHAT

# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
