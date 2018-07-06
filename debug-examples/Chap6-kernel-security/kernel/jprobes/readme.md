# Chap6-kernel-security/kernel/jprobes
Have fun with malicious Kernel code.

# Usage

Compile the module's sources : 
> make

Insert module into the Kernel :
> sudo insmod  kprobe-spy.ko

Read kernel messages :
> dmesg 

Shows every open file. Enjoy!

#### Remark
Location of *do_sys_open* (function to which jprobe is attached) must be replaced as explained in the internship report.

# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
