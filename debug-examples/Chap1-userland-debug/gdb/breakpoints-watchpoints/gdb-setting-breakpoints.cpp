#include <stdio.h>
#include <stdlib.h>

int getNumberFromUser(const char *msg);
int computeSum(int num1, int num2);

int main(){
    
    int firstNumber=0, secondNumber=0, result=0;
    
    firstNumber = getNumberFromUser("First number : ");
    secondNumber = getNumberFromUser("Second number : ");
    
    result = computeSum(firstNumber,secondNumber);

    printf("The result : %d + %d = %d \n",firstNumber,secondNumber,result);

    return EXIT_SUCCESS;
}

int getNumberFromUser(const char *msg){
    int numberFromUser = 0;
    printf("%s",msg);
    scanf("%d",&numberFromUser);
    return numberFromUser;
}

int computeSum(int num1, int num2){
    return num1+num2;
}

