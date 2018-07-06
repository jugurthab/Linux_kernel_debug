#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(){
    int ret = 0;
    
    ret = execl("/usr/bin/vi", "vi" ,NULL);
    if(ret < 0){
        perror("Cannot execute execl");
        exit(EXIT_FAILURE);
    }
              
    return EXIT_SUCCESS;
}


