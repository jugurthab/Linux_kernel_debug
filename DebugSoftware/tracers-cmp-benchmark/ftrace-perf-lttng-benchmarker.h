int createFolder(char folderName[]);
void getErrorAndExit(char msg[]);
void getDeviceHostName();
void getMemoryCharacteristicsLinux();
void recordFtraceTracingProcess(int tableIndex);
void recordPerfTracingProcess(int tableIndex);
void recordQSortExecutionTime(int tableIndex);
void recordLttngTracingProcess(int tableIndex);
void initializeFolders(int selectTracer);
