# Chap3-tracers/Lttng-examples/Tracing-Userspace-C-App

Example demonstrating the use of LTTng USDT to trace a C/C++ application.

# Usage

Compile the tracepoint provider :

> gcc -c -I. directory-explorer-tracepoint.c

Generate program's object code :

> gcc −c directory-explorer.c

Link program's object code to tracepoint provider :

> gcc -o directory-explorer directory-explorer.o directory-explorer-tracepoint.o -llttng-ust -ldl

We 're done! enjoy tracing with LTTng.

 
# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
