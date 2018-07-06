#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define NUMBER_MAX 100
#define NUMBER_MIN 1


#define CNRM  "\x1B[0m"
#define CRED  "\x1B[31m"
#define CGRN  "\x1B[32m"
#define CYEL  "\x1B[33m"
#define CCYN  "\x1B[36m"

int generateRandom();
void compareNumbers(int numberGenerated, int numberUser);

int main(){
	int numberGenerated=0, numberUser=0, number_of_tries=0;
	printf("\n---------------------------------------------------------\n");
	printf("--------------------Guess my number----------------------\n");
	printf("---------------------------------------------------------\n");
	srand(time(NULL));
	numberGenerated = generateRandom();
	
	do{

		printf("\n%sPlease choose a number between 0 and 100 : ",CYEL);	
		scanf("%d",&numberUser);
		number_of_tries+=1;
		compareNumbers(numberGenerated,numberUser);
		
	} while(numberGenerated!=numberUser);

	printf("\n%sNumber of tries : %d\n",CNRM, number_of_tries);	

	return EXIT_SUCCESS;
}

//Function to generate a pseudo-random number between NUMBER_MIN and NUMBER_MAX
int generateRandom(){
	return (rand() % (NUMBER_MAX - NUMBER_MIN)) + NUMBER_MIN;
}

void compareNumbers(int numberGenerated, int numberUser){
	
	if(numberGenerated>numberUser){
		printf("\n%sThe number is greater!\n",CRED);
	} else if(numberGenerated<numberUser){
		printf("\n%sThe number is smaller!\n",CCYN);
	} else {
		printf("\n%sCongratulations!!!!!!!!!!!You got it!\n",CGRN);
	}

}
