#include <stdio.h>
#include <stdlib.h>

int main(int argc,char *argv[]){    
    FILE *fileDescriptorSmile=NULL;
    char c;    
    fileDescriptorSmile = fopen("smile-stats.txt","r");
    if(fileDescriptorSmile != NULL){
        while (c != EOF){
            printf ("%c", c);
            c = fgetc(fileDescriptorSmile);
        }
        printf("\n");
        fclose(fileDescriptorSmile);
    }
    else {
        printf("Cannot open the file !\n");
    }     
    return EXIT_SUCCESS;
}
