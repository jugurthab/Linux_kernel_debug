#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_NUMBER 36000
#define ARRAY_SIZE 1000000

int cmpfunc (const void * a, const void * b)
{
    return ( *(int*)a - *(int*)b );
}

int main ()
{
    int n=0;
    srand(time(NULL));   // should only be called once

    int i, a[ARRAY_SIZE] = {0};
    for(i = 0; i < ARRAY_SIZE; ++i)
        a[i] = rand() % MAX_NUMBER;

    /*printf("Before sorting the list is: \n");
    for( n = 0 ; n < ARRAY_SIZE; n++ )
    {
        printf("%d ", a[n]);
    }
    printf("\n");*/
    qsort(a, ARRAY_SIZE, sizeof(int), cmpfunc);
/*
    printf("\nAfter sorting the list is: \n");
    for( n = 0 ; n < ARRAY_SIZE; n++ )
    {
        printf("%d ", a[n]);
    }*/
    printf("\n");
    return(0);
}
