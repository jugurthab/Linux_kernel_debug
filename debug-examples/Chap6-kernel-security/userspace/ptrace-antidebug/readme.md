# Chap6-kernel-security/userspace/ptrace-antidebug
Have fun reversing userspace debuggers and defeat security.

# Usage
Compile the program with debugging symbols : 
> gcc -o ptrace-anti-debug ptrace-anti-debug.c -g	

Run the code :
> ./ptrace-anti-debug

Finally,  try to attach gdb to it :
> gdb attach \`pidof ptrace-anti-debug\` -q



# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
