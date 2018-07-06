#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main(int argc, char *argv[]){
	int blinkTime=0;
	if(argc!=2){
		printf("Usage ./ledBlinkUser blinkTime\n");
		exit(EXIT_FAILURE);
	}
	blinkTime= atoi(argv[1]);
	while(1){
		system("echo 255 > /sys/class/leds/beaglebone:green:usr0/brightness");	
		usleep(blinkTime);
		system("echo 0 > /sys/class/leds/beaglebone:green:usr0/brightness");
		usleep(blinkTime);
	}
	return EXIT_SUCCESS;
}
