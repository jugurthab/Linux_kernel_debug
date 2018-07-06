#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <unistd.h>
#include <math.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/param.h>
#include <sys/sysinfo.h>

#include "ftrace-perf-lttng-benchmarker.h"

#define FOLDER_NAME "output-trace-cmp"

#define MAX_ITTERATION 5
#define DIV 1024

int main(int argc, char *argv[]){
    int i=0, testNumber=0, selectTracer=0;

    // Number of arguments must be 2 or 3 (the third is optionnal)
    if(argc<2 || argc>3){
        printf("Usage : ./ftrace-perf-lttng-benchmarker tracer_number [test_Number]\n");
        printf("tracer_number : 1 - ftrace only, 2 - perf only, 3 - lttng only, 4 - all the tracers\n");
        printf("[test_Number] : number of times to repeat the test (default = 10)\n");
        printf("Example : ./ftrace-perf-lttng-benchmarker 3\n");
        
        exit(EXIT_SUCCESS);
    }   

    if(argc==3){
        /* Convert string to integer to select a tracer */
        testNumber = atoi(argv[2]);
        /* atoi returns 0 in case of invalid conversion */
        if(testNumber <=0 || testNumber > 40){ // check number of tests
            printf("Number of allowed tests is between [1 - 40]\n");
            exit(EXIT_FAILURE);
        }
    } else {
        testNumber = MAX_ITTERATION;
    }

    // Get tracer
    selectTracer = atoi(argv[1]);
    
    //Create folders bechmarking statistics 
    initializeFolders(selectTracer);
    
    // Get system's initial state 
    getMemoryCharacteristicsLinux();
         
    getDeviceHostName();


    for(i = 0; i < testNumber;i++){

            recordQSortExecutionTime(i);
            
            switch(selectTracer){
                case 1 : 
                        recordFtraceTracingProcess(i);
                        break;
                case 2 :
                        recordPerfTracingProcess(i);
                        break;
                case 3:
                        recordLttngTracingProcess(i);
                        break;
                case 4:
                        recordFtraceTracingProcess(i);
                        recordPerfTracingProcess(i);
                        recordLttngTracingProcess(i);
                        break;
                default:
                        printf("The tracer number option is not valid\n");
            }
        
    }
    
	return EXIT_SUCCESS;
}



void getDeviceHostName(){
    FILE *saveHostName = NULL;
    char tmp[60];
    sprintf(tmp, "%s%s", FOLDER_NAME,"/sys-state/sys-host.txt");
    saveHostName = fopen(tmp, "w+");
    if(saveHostName!=NULL){
        char name[100];
        gethostname(name, 100);
        printf("Hostname is : %s\n",name);
        fprintf(saveHostName, "Hostname : %s", name);
        fclose(saveHostName);
    } else{
        printf("Cannot get hostname!\n");
    }
    
}

// get device's memory and load average status before starting benchmark
void getMemoryCharacteristicsLinux(){
    FILE *saveInitialReportMachineState = NULL;
    char tmp[60];
    sprintf(tmp, "%s%s", FOLDER_NAME,"/sys-state/sys-stats.txt");

	struct sysinfo info;
	sysinfo(&info);
	printf("\033[31m Uptime(Since system booting) : %ld \n",info.uptime);
	//printf("\033[32m Load average : 1 minutes = %ld, 5 minutes = %ld, 15 minutes = %ld\n",info.loads[0],info.loads[1],info.loads[2]);
	printf("\033[33m Total usable main memory size : %ld kB\n",info.totalram/DIV);
	printf("\033[34m Available memory size : %ld kB\n",info.freeram/DIV);	
	printf("\033[35m Amount of shared memory  : %ld kB\n",info.sharedram/DIV);
	printf("\033[36m Memory used by buffers : %ld kB\n",info.bufferram/DIV);
	printf("\033[31m Total swap space size : %ld kB\n",info.totalswap/DIV);	
	printf("\033[33m swap space still available : %ld kB\n",info.freeswap/DIV);	
	printf("\033[32m Number of current processes : %d\n",info.procs);	
	printf("\033[34m Total high memory size : %ld kB\n",info.totalhigh/DIV);	

	printf("\033[35m Available high memory size : %ld kB\n",info.freehigh/DIV);	
	printf("\033[36m Memory unit size in bytes : %d\n",info.mem_unit);

    saveInitialReportMachineState = fopen(tmp, "w+");
    if(saveInitialReportMachineState != NULL){
        fprintf(saveInitialReportMachineState,"Uptime(Since system booting) : %ld \n",info.uptime);
	    //fprintf(saveInitialReportMachineState,"Load average : 1 minutes = %ld, 5 minutes = %ld, 15 minutes = %ld\n",info.loads[0],info.loads[1],info.loads[2]);
	    fprintf(saveInitialReportMachineState,"Total usable main memory size : %ld kB\n",info.totalram/DIV);
	    fprintf(saveInitialReportMachineState,"Available memory size : %ld kB\n",info.freeram/DIV);	
	    fprintf(saveInitialReportMachineState,"Amount of shared memory  : %ld kB\n",info.sharedram/DIV);
	    fprintf(saveInitialReportMachineState,"Memory used by buffers : %ld kB\n",info.bufferram/DIV);
	    fprintf(saveInitialReportMachineState,"Total swap space size : %ld kB\n",info.totalswap/DIV);	
	    fprintf(saveInitialReportMachineState,"Swap space still available : %ld kB\n",info.freeswap/DIV);	
	    fprintf(saveInitialReportMachineState,"Number of current processes : %d\n",info.procs);	
	    fprintf(saveInitialReportMachineState,"Total high memory size : %ld kB\n",info.totalhigh/DIV);	

	    fprintf(saveInitialReportMachineState,"Available high memory size : %ld kB\n",info.freehigh/DIV);	
	    fprintf(saveInitialReportMachineState,"Memory unit size in bytes : %d\n",info.mem_unit);


        /* Parsing /proc/loadavg to get CPUs load average */ 
        FILE *procLoadAvg = NULL;
        procLoadAvg = fopen("/proc/loadavg","r+");
        
        
        if(procLoadAvg == NULL) {
               getErrorAndExit("/proc/loadavg not found ");
        }

        else {
                 if(!fgets(tmp, 60, procLoadAvg)){ // Read load average
                    getErrorAndExit("cannot read /proc/loadavg ");
                 }
                 printf("Load average : %s\n", tmp);
                 fprintf(saveInitialReportMachineState,"/proc/loadavg : %s", tmp);  // Stores the load average
                 fclose(procLoadAvg);
        }

        


        fclose(saveInitialReportMachineState); // close filestream to free resources
    }   else {
        printf("Cannot save state report\n");
    }

}

/* Ftrace (trace-cmd) benchmarker function */
void recordFtraceTracingProcess(int tableIndex){
    char tmp[250];
    sprintf(tmp, "/usr/bin/time -v -o %s/ftraceQSort/usr-bin-time/qsort%d.txt trace-cmd record -p function_graph -e all -o %s/ftraceQSort/ftrace%d.dat ./qsort", FOLDER_NAME, tableIndex, FOLDER_NAME, tableIndex);
    system(tmp);
    system("trace-cmd reset"); // trace-cmd must be stopped 

}


/* Perf benchmarker function */
void recordPerfTracingProcess(int tableIndex){   
    char tmp[250];
    sprintf(tmp, "/usr/bin/time -v -o %s/perfQSort/usr-bin-time/qsort%d.txt perf record -o %s/perfQSort/perf%d.perf ./qsort", FOLDER_NAME, tableIndex, FOLDER_NAME, tableIndex);
    system(tmp);
}

/* LTTng benchmarker function */
void recordLttngTracingProcess(int tableIndex){   
    char tmp[250];
    sprintf(tmp, "lttng create my-session-%d --output=%s%s%dlttng; lttng enable-event --kernel --all; lttng start; /usr/bin/time -v -o %s/lttngQSort/usr-bin-time/qsort%d.txt ./qsort; lttng stop; lttng destroy", 
tableIndex, FOLDER_NAME, "/lttngQSort/", tableIndex, FOLDER_NAME, tableIndex);
     system(tmp);  

}

/* qsort algorithm (reference program) */
void recordQSortExecutionTime(int tableIndex){   
    char tmp[150];
    sprintf(tmp, "/usr/bin/time -v -o %s/qsortbench/usr-bin-time/qsort%d.txt ./qsort", FOLDER_NAME, tableIndex);
    system(tmp);
}

/* Create folders to save benchmarking statistics */
void initializeFolders(int selectTracer){
    char tmp[250];
    sprintf(tmp, "rm -rf %s", FOLDER_NAME);
    system(tmp); 

    // Creating root output folder to save the traces    
    if(createFolder(FOLDER_NAME) < 0){
        getErrorAndExit("output2 ");
    }

    /* Machine status Folder */
    // create the sys-state folder
    sprintf(tmp, "%s%s", FOLDER_NAME, "/sys-state");
    if(createFolder(tmp) < 0){
        getErrorAndExit("sys-state creation ");
    }

    /* QSORT BENCH FOLDER */
    // create the qsortbench folder
    sprintf(tmp, "%s%s", FOLDER_NAME, "/qsortbench");
    if(createFolder(tmp) < 0){
        getErrorAndExit("qsortbench creation ");
    }

    
    // create the qsortbench folder
    sprintf(tmp, "%s%s%s", FOLDER_NAME, "/qsortbench","/usr-bin-time");
    if(createFolder(tmp) < 0){
        getErrorAndExit("qsortbench/usr-bin-time creation ");
    }


    if(selectTracer==1 || selectTracer==4){

            /* FTRACE TRACER FOLDER */
            // create the ftraceQSort folder
            sprintf(tmp, "%s%s", FOLDER_NAME, "/ftraceQSort");
            if(createFolder(tmp) < 0){
                getErrorAndExit("ftraceQSort creation ");
            }
            
            // create the ftraceQSort/usr-bin-time folder
            sprintf(tmp, "%s%s%s", FOLDER_NAME, "/ftraceQSort","/usr-bin-time");
            if(createFolder(tmp) < 0){
                getErrorAndExit("ftraceQSort/usr-bin-time creation ");
            }
    }

    if(selectTracer==2 || selectTracer==4){
            /* PERF PROFILER-TRACER FOLDER */

            // create the perfQSort folder
            sprintf(tmp, "%s%s", FOLDER_NAME, "/perfQSort");
            if(createFolder(tmp) < 0){
                getErrorAndExit("perfQSort creation ");
            }
             // create the perfQSort/usr-bin-time folder
            sprintf(tmp, "%s%s%s", FOLDER_NAME, "/perfQSort","/usr-bin-time");
            if(createFolder(tmp) < 0){
                getErrorAndExit("perfQSort/usr-bin-time creation ");
            }
    }

    if(selectTracer==3 || selectTracer==4){
        /* LTTNG TRACER FOLDER */
        
        // create the perfQSort folder
        sprintf(tmp, "%s%s", FOLDER_NAME, "/lttngQSort");
        if(createFolder(tmp) < 0){
            getErrorAndExit("lttngQSort creation ");
        }
         // create the perfQSort/usr-bin-time folder
        sprintf(tmp, "%s%s%s", FOLDER_NAME, "/lttngQSort","/usr-bin-time");
        if(createFolder(tmp) < 0){
            getErrorAndExit("lttngQSort/usr-bin-time creation ");
        }

        system("lttng-sessiond --daemonize"); // start LTTng deamon (must be started once)
    }

}


int createFolder(char folderName[]){
    /* Create a folder */
    return mkdir(folderName, S_IRWXU|S_IRWXG|S_IRWXO);
}

/* Debug function in case of error */
void getErrorAndExit(char msg[]){
    char tmp[20];
    sprintf(tmp, "%s", msg);
    perror(tmp); // Get the error
    exit(EXIT_FAILURE);   // Exit from program
}

