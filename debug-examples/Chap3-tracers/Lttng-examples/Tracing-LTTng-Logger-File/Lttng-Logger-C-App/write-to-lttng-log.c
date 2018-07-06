#include <stdio.h>
#include <stdlib.h>

int main(){
    FILE* fd_writer_to_log = NULL;
    
    fd_writer_to_log = fopen("/proc/lttng-logger","r+");    
    if (fd_writer_to_log != NULL) {
        fprintf(fd_writer_to_log,"""Hello SMILE from C Code!\n");
        fclose(fd_writer_to_log);
    } 
    else {
        printf("Cannot open /proc/lttng_logger\n");
        exit(EXIT_FAILURE);
    }
    return EXIT_SUCCESS;
}

