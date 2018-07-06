# Chap6-kernel-security/userspace/ptrace-antidebug
Have fun reversing userspace debuggers and defeat security.

# Usage
Compile the program's sources : 
> gcc -o secure-program secure-program.c

Compile the library :
> gcc -fPIC --shared -o libhijack-strcmp.so library-code-strcmp.c

Finally,  start the program :
> LD_PRELOAD=./libhijack-strcmp.so secure-program

Try any password, it's gonna work!


# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
