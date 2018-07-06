# Chap2-kernel-debug/debug-module
Example used to demonstrate debugging a module (only the compilation is shown, more can be found in the internship report).  

# Usage
Compile module's sources:

> make

Insert module into the kernel :

> sudo insmod kernel-oops-mod.ko

We should see a message `Module is running major 245 !` (245 being device's major number).

Add an entry in `/dev/` :

> mknod /dev/basictest c 245 0

Interact with the character driver :

> cat /dev/basictest

Take a look at kernel's log message:

> dmesg


 
# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
