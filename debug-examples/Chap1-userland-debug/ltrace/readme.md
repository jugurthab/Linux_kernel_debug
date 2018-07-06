# Chap1-userland-debug/ltrace
Example code which helps learning how to record executable to library calls (and even amongst libraries).  

# Usage

Compile program's and library sources : 
> gcc -fPIC --shared -o  libsmile-hello-open-source.so smile-hello-open-source.cpp

> export LD_LIBRARY_PATH=.

> gcc -o ltrace-hello ltrace-hello.cpp -lsmile-hello-open-source -L.

Launch ltrace and look for the calls :
> ltrace ./ltrace-hello

# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
