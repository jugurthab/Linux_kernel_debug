#include <stdio.h>
#include <stdlib.h>

void getErrorAndExit();

int main(){
	struct employeeInfo{
		char name[40];
		int age;
	};

	struct employeeInfo employeeInfoOutput = {"Jugurtha BELKALEM", 26}, employeeInfoInput={"nothing",0};
	
	FILE *writeEmployeeInfoOutputStream = NULL, *readEmployeeInfoInStream = NULL;	
	/* ------------------------------------------------------------------------ */
	/* -------------- Write structure to disk section ------------------------- */
	if((writeEmployeeInfoOutputStream=fopen("save-struct.txt","w+")) == NULL){ // get file stream
		getErrorAndExit();
	}
	/* save the structure into a binary file */	
	if(!fwrite(&employeeInfoOutput, sizeof(struct employeeInfo), 1,  writeEmployeeInfoOutputStream)){
		getErrorAndExit();
	}
	if(fclose(writeEmployeeInfoOutputStream)==-1) // close file stream
		perror("fclose() writeEmployeeInfoOutputStream ");

	/* ------------------------------------------------------------------------------ */
	/* -------------- Read back structure from disk section ------------------------- */
	if((readEmployeeInfoInStream=fopen("save-struct.txt","r+")) == NULL){ // get file stream
		getErrorAndExit();
	}
	
	/* save the structure into a binary file */	
	if(!fread(&employeeInfoInput, sizeof(struct employeeInfo), 1,  readEmployeeInfoInStream)){
		getErrorAndExit();
	}
	if(fclose(readEmployeeInfoInStream)==-1) // close file stream
		perror("fclose() readEmployeeInfoInputStream ");
	
	printf("----- The new content of structure employeeInfoInput ------\n");
	printf("\t\tName : %s\n", employeeInfoInput.name);
	printf("\t\tAge : %d\n", employeeInfoInput.age);

	return EXIT_SUCCESS;
}

void getErrorAndExit(){
		perror("Error ");
		exit(EXIT_FAILURE);
}

