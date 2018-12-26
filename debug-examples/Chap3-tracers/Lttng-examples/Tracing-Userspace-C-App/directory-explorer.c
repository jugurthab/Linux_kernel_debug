#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/types.h>

#include "directory-explorer-tracepoint.h"

void displayErrorMsgExit(char msg[]);
int main(int argc, char *argv[]){
    // used to point to a directory to discover
    DIR* directoryToExplore = NULL;
    // count nb of entities (files and folders) in a directory
    int Filecounter = 0;
    // used to point to an entity (file and folder)
    struct dirent* exploreredEntity = NULL;

    if(argc!=2){ // check nb of arguments
        displayErrorMsgExit("usage : ./directory-explorer PATH_TO_DIRECTORY\n"); 
    }
    
    // Waits, because user must start LTTng before going further
    getchar(); 

    directoryToExplore = opendir(argv[1]); // Open directory
    if(directoryToExplore==NULL){
        displayErrorMsgExit("usage : ./directory-explorer PATH_TO_DIRECTORY\n");
    }

    // Traverse directory content
    while((exploreredEntity = readdir(directoryToExplore)) != NULL){
        Filecounter++;
        // Print directory entity (file and folder)
        printf("+ File N°: %d =====>  '%s' \n", Filecounter, exploreredEntity->d_name);
        /* 
        -------------------------------------------
        ------- Generate an LTTng event -----------
        ---- WARNING: LTTNG MUST BE STARTED -------
        ---------- BEFORE THIS STEP, --------------
        --- OTHERWISE EVENTS WILL NOT BE CAUGHT ---
        -------------------------------------------
         */
        tracepoint(smile_directory_explorer_lttng_provider, smile_first_tracepoint, Filecounter, exploreredEntity->d_name);
    }


    // Always close directory to free ressources
    if(closedir(directoryToExplore) == -1)
        perror("closedir Error ");
    
    
    return EXIT_SUCCESS;
}

// Display error messages
void displayErrorMsgExit(char msg[]){
    printf("%s\n",msg);
    exit(EXIT_FAILURE);
}


