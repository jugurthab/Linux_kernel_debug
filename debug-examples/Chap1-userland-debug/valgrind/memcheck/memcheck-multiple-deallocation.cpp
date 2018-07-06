#include <stdio.h>
#include <stdlib.h>

int main () {
   char *str;
   /* Allocate 20 memory cells of size of char */
   str = (char *) malloc(20);
	 
   free(str);
   free(str);
   return EXIT_SUCCESS;
}
