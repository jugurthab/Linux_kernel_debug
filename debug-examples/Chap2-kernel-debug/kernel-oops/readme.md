# Chap2-kernel-debug/kernel-oops
**kernel-oops** are issued by the kernel when errors (but not necessarily crucial) are detected. Oops may lead to Kernel PANIC and inconsistencies.  

The example shows dereferencing a NULL pointer in the kernel. 

# Usage
Compile module's sources:

> make

Insert module into the kernel :

> sudo insmod kernel-oops-mod.ko

Read the oops messages from kernel's buffer :

> dmesg

 ### Important
 The most useful field in an oops is the : RIP (Instruction pointer).
 
# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
