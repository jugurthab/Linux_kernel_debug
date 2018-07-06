#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    int* userSmileNB = NULL;

    userSmileNB = (int*) malloc(sizeof(int));
    if (userSmileNB == NULL)
    {
        printf("Cannot allocate memory!\n");
        exit(EXIT_FAILURE);
    }

    printf("How many times do you SMILE per day ? ");
    scanf("%d", userSmileNB);
    
    printf("You have said that you SMILE %d times per Day\n", *userSmileNB);

    free(userSmileNB);

    return EXIT_SUCCESS;
}

