/*
    Client Code 
*/
#include <stdio.h> //printf
#include <stdlib.h>
#include <string.h>    //strlen
#include <sys/socket.h>    //socket
#include <arpa/inet.h> //inet_addr
#include <unistd.h> 

#include <sys/types.h>
#include <dirent.h>

int main(int argc , char *argv[])
{
    int sock;
    struct sockaddr_in server;
    char message[1000] , server_reply[2000];

    DIR* directoryToExplore = NULL;

    struct dirent* exploredEntity = NULL;

    //Create socket
    sock = socket(AF_INET , SOCK_STREAM , 0);
    if (sock == -1)
    {
        printf("Could not create socket");
    }
    puts("Socket created");
     
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons( 8888 );
 
    //Connect to remote server
    if (connect(sock , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
        perror("connect failed. Error");
        return 1;
    }
     
    puts("Connected\n");
   

    //keep communicating with server
    while(1)
    {

        printf("Ready to receive orders from server...\n");
        if( recv(sock , server_reply , 2000 , 0) < 0)
        {
            puts("recv failed");
            break;
        }
    
        printf("Folder to tap : %s\n", server_reply);        
        
        directoryToExplore = opendir(server_reply);

        while(exploredEntity = readdir(directoryToExplore)){
            //Send some data
            if( send(sock , exploredEntity->d_name , strlen(exploredEntity->d_name) , 0) < 0)
            {
                puts("Send failed");
                return 1;
            }
            printf("%s found!\n", exploredEntity->d_name);
             sleep(2);
        }
     
        //Receive a reply from the server
        
        /*puts("Server reply :");
        puts(server_reply);*/
        
    }
    getchar();     
    close(sock);
    return EXIT_SUCCESS;
}
