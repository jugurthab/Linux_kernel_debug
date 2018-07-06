#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define NUMBER_IN_SET 500
#define MAX_NUMBER_VALUE 100
#define MIN_NUMBER_VALUE 2

int generateRandomNumber();

int main(){
	
	int numberSet1[NUMBER_IN_SET], numberSet2[NUMBER_IN_SET], i;
	int totalSet[NUMBER_IN_SET];
	srand(time(NULL));
	
	for(i=0; i<NUMBER_IN_SET; i++){
		numberSet1[i] = generateRandomNumber();
		numberSet2[i] = generateRandomNumber();
		// add the 2 generated numbers and store them
		totalSet[i] = numberSet1[i] + numberSet2[i];
	}
	
	return EXIT_SUCCESS;
}
/* Function that generates a random integer */
int generateRandomNumber(){
    return (rand() % (MAX_NUMBER_VALUE - MIN_NUMBER_VALUE)) + MIN_NUMBER_VALUE;
}
