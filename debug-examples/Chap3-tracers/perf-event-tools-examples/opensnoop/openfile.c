#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
int main(int argc ,char *argv[]){
    

    FILE* fileDecriptor = NULL;    
    int ret = 0;
    char c;
    struct stat st;

    if(argc!=2){
        printf("Usage : ./opensnoop-file-open fileName\n");
        exit(EXIT_FAILURE);
    }

    fileDecriptor = fopen(argv[1],"r+");        
    if(fileDecriptor != NULL){
        printf("File content : ");
        while((c = getc(fileDecriptor)) !=EOF)
            putchar(c);
        fclose(fileDecriptor);
        printf("\n");
    }   
    else {
        printf("Cannot open the file\n"); 
        exit(EXIT_FAILURE); 
    }

    ret = stat(argv[1], &st);
    
    printf("---------- File statistics ------------\n");
    printf("File Name : %s\n",argv[1]);
    printf("File size : %ld bytes\n",st.st_size); 
    printf("File inode : %ld\n",st.st_ino); 
    return EXIT_SUCCESS;
}

