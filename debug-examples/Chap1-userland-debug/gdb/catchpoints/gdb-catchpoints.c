#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(){
    
    pid_t pid;
    pid = fork ();
    
    if (pid > 0)
        printf ("I am process %d and my child's pid=%d!\n",getpid(), pid);
    else if (!pid)
        printf ("Hello, I'm the child process!\n");
    else
        perror ("fork cannot be made");

    return EXIT_SUCCESS;
}

