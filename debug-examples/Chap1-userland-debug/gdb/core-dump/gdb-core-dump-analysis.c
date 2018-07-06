#include <stdio.h>
#include <stdlib.h>

int main(){

    *(int *)NULL = 0;

    printf("SMILE, This is a dereferenced NULL pointer!!\n");
           
    return EXIT_SUCCESS;
}

