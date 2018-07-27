
# tracers-cmp-benchmark

**tracers-cmp-benchmark** measures the overhead associated with Linux tracers : **[Trace-cmd](https://github.com/rostedt/trace-cmd)**, **[Perf](https://github.com/torvalds/linux/tree/master/tools/perf)**  and  **[LTTng](https://github.com/lttng)**.

# Dependencies
 tracers-cmp-benchmark is written in C which requires build-essential package :
 > sudo apt-get install build-essential

## Compile QSort sources
Qsort is the reference program used with the different tracers
> $ gcc -o qsort qsort.cpp
## Compile benchmarker sources

**ftrace-perf-lttng-benchmarker** launches QSort and attaches the tracers to collect their overhead.

> $ gcc -o ftrace-perf-lttng-benchmarker ftrace-perf-lttng-benchmarker.c

# Usage : Collect tracers overhead
ftrace-perf-lttng-benchmarkercan be started (make sure to install the tracers before) :
> $ ./ftrace-perf-lttng-benchmarker [select-tracer] [number_of_tests_to perform]

Where :

 - select-tracer : 1 - ftrace, 2 - Perf, 3 - LTTng, 4 - All Tracers
 - number_of_tests_to_perform : number of times to repeat collecting the data. It is always better to take the average of multiple tests 
 
 As an example, to measure the overhead of all tracers and repeat the test for 10 times : 
 
> $ sudo ./ftrace-perf-lttng-benchmarker 4 10


# Feedbacks
please feel free to contact me : <jugurthabelkalem@gmail.com>
