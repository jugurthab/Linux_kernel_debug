#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]){
    
    int numberOfTimeToSaySmile = 0, i=0;    
    
    if(argc != 2){
        printf("Usage : ./gdb-basi-usage Number_Of_Time_To_Say_Smile \n");
        exit(EXIT_FAILURE);    
    }
    
    numberOfTimeToSaySmile = atoi(argv[1]);
    
    for(i=0;i<numberOfTimeToSaySmile;i++)
        printf("Hello World, Smile and enjoy life!!!\n");
    
    
    return EXIT_SUCCESS;
}

