#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define NB_THREADS 4
#define VECTOR_LENGTH 400
#define RANDOM_MAX_USER 20

pthread_mutex_t myMutex; // creates a mutex


double vector1[VECTOR_LENGTH];
double vector2[VECTOR_LENGTH];


// indices des tableaux pour les threads
int arrayOffsetIndex[NB_THREADS]={0,100,200,300};

//Stocker le produit scalaire
double totalDotProduct = 0.0;

// function to compute the dot product
void *computeDotProduct(void *arg)
{
	int i=0, itterationRange = 0;
	//Récupérer l'indice du tableau (offset)
	int valeToAdd = *(int *) arg; 
	
	//calcule l'intervalle du tableau déstiné pour ce thread
	itterationRange = valeToAdd + 100;
	
	double resultTmp = 0.0;	// stocker la valeur partiel calculé par le thread

	for(i=valeToAdd; i < itterationRange; i++){
		//Produit scalaire
		resultTmp+= vector1[i] * vector2[i];
	}
	//Afficher le résultat obtenu par le thread
	printf("Result from worker thread[%d] is : %lf\n",valeToAdd/100,resultTmp);

	//Acquisition du mutex - Section critique
	//pthread_mutex_lock(&myMutex); 
		totalDotProduct += resultTmp;// actualisation de la valeur globale.
	//Libération du mutex
	//pthread_mutex_unlock(&myMutex);

	pthread_exit((void *) 0);
}


int main (int argc, char *argv[])
{
	pthread_t thread[NB_THREADS];
	pthread_attr_t attr;
	int rc = 0, t = 0;
	void *status = NULL;
	srand(time(NULL)); //Initialisation du générateur Pseudo-Aléatoire

	for(t=0;t<VECTOR_LENGTH;t++){
		vector1[t] = rand() % RANDOM_MAX_USER;
		vector2[t] = rand() % RANDOM_MAX_USER;
	}
		
	pthread_mutex_init(&myMutex,NULL);

	 /* Initialisation et activation d'attributs */
	 pthread_attr_init(&attr); //valeur par défaut

	 pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE); //attente du thread possible
	

	printf("------------- Synchronization of threads using Mutex ----------------\n");

	// creates working threads
	 for(t=0; t<NB_THREADS; t++)
	 {
		 printf("Creation of worker thread : %d\n", t);
		
		
		//create a thread with myValue as a parameter		
		 rc = pthread_create(&thread[t], &attr, computeDotProduct, &arrayOffsetIndex[t]);
		 if (rc)
		 {
			 printf("ERROR; pthread_create() returned code :  %d\n", rc);
			 exit(-1);
		 }
	 }
	
	 /* liberation des attributs et attente de la terminaison des threads */
	 pthread_attr_destroy(&attr);

	 for(t=0; t<NB_THREADS; t++)
	 {
		 rc = pthread_join(thread[t], &status);
		 if (rc)
		 {
			 printf("ERROR; pthread_join() returned a status code : %d\n", rc);
			 exit(-1);
		 }
		 printf("Join has been done with thread %d which returned a result = %ld\n",t, (long)status);
	 }
	
	// Display the result of dot product
	printf("\n--------------*** Main Thread display****-------------------------\n");
	printf("Main thread displays total Dot-Product is : %lf\n",totalDotProduct);
	printf("------------------------------------------------------------------\n");
	pthread_mutex_destroy(&myMutex);
	
	pthread_exit(NULL);
}
