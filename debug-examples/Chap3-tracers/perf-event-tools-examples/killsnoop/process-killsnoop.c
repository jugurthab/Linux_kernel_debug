#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <signal.h>

int main(){

    pid_t myPid = getpid();

    kill(myPid,SIGKILL);
    
    return EXIT_SUCCESS;
}

