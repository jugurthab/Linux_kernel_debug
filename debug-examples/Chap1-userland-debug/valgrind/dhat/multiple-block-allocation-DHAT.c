#include <stdio.h>
#include <stdlib.h>

void allocateMoreBlocks();

int main(int argc, char *argv[])
{
    int* nbBlocksAllocated = NULL;

    nbBlocksAllocated = (int*) malloc(10 * sizeof(int));


    allocateMoreBlocks();

    free(nbBlocksAllocated);

    return EXIT_SUCCESS;
}

void allocateMoreBlocks(){
    int* nbExtraBlocks = NULL;
    nbExtraBlocks = (int*) malloc(30 * sizeof(int));

    free(nbExtraBlocks);
}

