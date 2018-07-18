#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUMBER_OF_RANDOM 5
#define DOUBLE_TRIPLE_CHOICE_NUMBER 50
#define NUMBER_MAX 100
#define NUMBER_MIN 1

int generateRandom();
int doubleGeneratedRandomNumber(int x);
int tripleGeneratedRandomNumber(int y);
void printFinalGeneratedNumbers(int myNumbers[]);

int main(int argc,char *argv[]){
	// RandomNumbers holds the generated random numbers
	int RandomNumbers[NUMBER_OF_RANDOM] = {0}; 

	// Initialize the pseudo-random generator	
	srand(time(NULL));
	
	//Generate and save 10 random numbers
	for(int i=0; i< NUMBER_OF_RANDOM; i++){
		RandomNumbers[i] = generateRandom();
		if(RandomNumbers[i] < DOUBLE_TRIPLE_CHOICE_NUMBER)
			RandomNumbers[i] = doubleGeneratedRandomNumber(RandomNumbers[i]);
		else
			RandomNumbers[i] = tripleGeneratedRandomNumber(RandomNumbers[i]);		
		
	}	
		
	printFinalGeneratedNumbers(RandomNumbers);
	

	return EXIT_SUCCESS;

}

//Function to generate a pseudo-random number between NUMBER_MIN and NUMBER_MAX
int generateRandom(){
	return (rand() % (NUMBER_MAX - NUMBER_MIN)) + NUMBER_MIN;
}

int doubleGeneratedRandomNumber(int x){
	return 2 * x;
}

int tripleGeneratedRandomNumber(int y){
	return 2 * y;
}

void printFinalGeneratedNumbers(int myNumbers[]){
	printf("The program generated the following numbers : ");
	for(int i=0; i< NUMBER_OF_RANDOM; i++){
		printf("%d ",myNumbers[i]);
	}
	printf("\n");
}
