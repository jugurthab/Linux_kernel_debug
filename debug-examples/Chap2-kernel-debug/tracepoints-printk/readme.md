# Chap2-kernel-debug/tracepoints-printk
Tracepoints are probes that can be attached statically (need to recompile the source) to kernel code. ***printk*** is the most basic tracepoint (*printk* has a lot of overhead, otherways to [tracepoint](https://www.kernel.org/doc/Documentation/trace/tracepoints.txt) do  exist ). 

# Usage
Compile module's sources:

> make

Insert module into the kernel :

> sudo insmod myKernelModule.ko

Read the printk messages from kernel's buffer :

> dmesg

 
# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
