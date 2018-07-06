# Chap1-userland-debug/strace
Example code which helps learning how to record system calls (Syscalls) using strace.  

# Usage

Compile program's sources : 
> gcc fileNotFound.cpp -o fileNotFound

Launch strace and tap system calls :
> strace ./fileNotFound

### Remark
Try removing `smile-stats.txt` file and look at what's happening to SysCalls.

# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
