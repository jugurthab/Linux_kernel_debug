#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
int main(){

    if(ptrace(PTRACE_TRACEME , 0) < 0 ){
        printf("You cannot debug me!\n");
        exit(EXIT_FAILURE);
    }

        
    getchar();
    printf("No debugger detected\n");
    return EXIT_SUCCESS;
}

