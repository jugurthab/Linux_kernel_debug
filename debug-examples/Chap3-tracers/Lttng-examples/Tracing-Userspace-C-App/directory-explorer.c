#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/types.h>

#include "directory-explorer-tracepoint.h"

void displayErrorMsgExit(char msg[]);
int main(int argc, char *argv[]){
    
    DIR* directoryToExplore = NULL;
    int Filecounter = 0;
 
    struct dirent* exploreredEntity = NULL;

    if(argc!=2){
        displayErrorMsgExit("usage : ./directory-explorer PATH_TO_DIRECTORY\n"); 
    }
    
    getchar();

    directoryToExplore = opendir(argv[1]);
    if(directoryToExplore==NULL){
        displayErrorMsgExit("usage : ./directory-explorer PATH_TO_DIRECTORY\n");
    }

    
    while((exploreredEntity = readdir(directoryToExplore)) != NULL){
        Filecounter++;
        printf("+ File N°: %d =====>  '%s' \n", Filecounter, exploreredEntity->d_name);
        
        tracepoint(smile_directory_explorer_lttng_provider, smile_first_tracepoint, Filecounter, exploreredEntity->d_name);
    }


    if(closedir(directoryToExplore) == -1)
        perror("closedir Error ");
    
    
    return EXIT_SUCCESS;
}

void displayErrorMsgExit(char msg[]){
    printf("%s\n",msg);
    exit(EXIT_FAILURE);
}


