/*
    Server Code
*/

#include<stdio.h>
#include<string.h>    
#include<stdlib.h>    
#include<sys/socket.h>
#include<arpa/inet.h> 
#include<unistd.h>    
#include<pthread.h> 
 

#define LOG_PATH "log.txt"

void getErrorAndExit(char msg[]);
void *connection_handler(void *);
void initializeLogFile();
void closeLogStream();

typedef struct getConnectedUser{
    int socket_desc;
    struct sockaddr_in clientIdentity;
} getConnectedUser;
 

FILE *logConnectedClientsStream = NULL;


int main(int argc , char *argv[])
{
    int socket_desc , client_sock , c , *new_sock;
    struct sockaddr_in server , client;
     
    initializeLogFile();
    atexit(closeLogStream);
    printf("Log file created!\n");
    //Create socket
    socket_desc = socket(AF_INET , SOCK_STREAM , 0);
    if (socket_desc == -1)
    {
        getErrorAndExit("Socket error ");
    }
    printf("Socket created\n");
     
    //Prepare the sockaddr_in structure
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons( 8888 );
     
    //Bind
    if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
    {
        //print the error message
        perror("bind failed. Error");
        return 1;
    }
    printf("bind done\n");
     
    //Listen
    listen(socket_desc , 3);
     
    //Accept and incoming connection
    printf("Waiting for incoming connections...\n");
    c = sizeof(struct sockaddr_in);
     
    
    while( (client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c)) )
    {
        printf("Connection accepted\n");
         
        pthread_t sniffer_thread;
        //new_sock = malloc(1);
        //*new_sock = client_sock;
        getConnectedUser *c = malloc(sizeof(getConnectedUser));
        c->socket_desc = client_sock;
        c->clientIdentity = client;
       
        //if( pthread_create( &sniffer_thread , NULL ,  connection_handler , (void*) new_sock) < 0)
        if( pthread_create( &sniffer_thread , NULL ,  connection_handler , (void*) c) < 0)
        {
            getErrorAndExit("could not create thread");
        }
         
        //Now join the thread , so that we dont terminate before the thread
        //pthread_join(sniffer_thread , NULL);
        puts("Handler assigned");
    }
     
    if (client_sock < 0)
    {
        getErrorAndExit("accept failed");
    }
     
    return EXIT_SUCCESS;
}
 
/*
 * This will handle connection for each client
 * */
void *connection_handler(void *socket_desc)
{
    //Get the socket descriptor
   /* int sock = *(int*)socket_desc;*/

    getConnectedUser c = *(getConnectedUser*)socket_desc;
     
    int read_size;
    char message[20] , client_message[2000];
   
    flockfile(logConnectedClientsStream);
        fprintf(logConnectedClientsStream, "Client %s connected on port : %d\n", inet_ntoa(c.clientIdentity.sin_addr), ntohs(c.clientIdentity.sin_port));
        fflush(logConnectedClientsStream);
    funlockfile(logConnectedClientsStream);


    printf("\nDirectory to explore : ");
    scanf("%s", message);
    printf("\n");


    write(c.socket_desc , message , strlen(message));
    
    while( (read_size = recv(c.socket_desc , client_message , 2000 , 0)) > 0 )
    {
        //Send the message back to client
        
        printf("% *d Client %s on port %d reported : %s\n", (c.socket_desc-4) * 8, c.socket_desc, inet_ntoa(c.clientIdentity.sin_addr), ntohs(c.clientIdentity.sin_port), client_message); 
        memset(client_message, 0,strlen(client_message));           
        //write(sock , client_message , strlen(client_message));
    }
     
    if(read_size == 0)
    {
        puts("Client disconnected");
        fflush(stdout);
    }
    else if(read_size == -1)
    {
        perror("recv failed");
    }
         
    //Free the socket pointer
    free(socket_desc);
     
    return EXIT_SUCCESS;
}


void initializeLogFile(){ 
    
    logConnectedClientsStream = fopen(LOG_PATH, "w+");
    
    if(logConnectedClientsStream == NULL){
        getErrorAndExit("Error Log File ");
    }

}

void closeLogStream(){
    fclose(logConnectedClientsStream);
}

/* Debug function in case of error */
void getErrorAndExit(char msg[]){
    char tmp[20];
    sprintf(tmp, "%s", msg);
    perror(tmp); // Get the error
    exit(EXIT_FAILURE);   // Exit from program
}

