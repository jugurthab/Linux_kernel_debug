#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define KEY "4FG512"

int testKeyAuthentification(const char *userKey, const char *realKey){
    if(strcmp(userKey,realKey)==0){
        return 1;
    }
    else
        return 0;
}

int main(int argc, char *argv[]){

    
    char secretKeyUSER[10];

    printf("Secret Key : ");
    scanf("%s", secretKeyUSER);

    if(testKeyAuthentification(secretKeyUSER, KEY))
        printf("Hello SMILE admin\n");
    else 
        printf("You are not admin\n");

    return EXIT_SUCCESS;
}

