import subprocess
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, filedialog
from tkinter import Menu
from tkinter import messagebox as mbox
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import os

import numpy as np
from matplotlib.figure import Figure


class TraceCmdParserMainWindow():
    def __init__(self):
       # self.backgroundColor = backgroundColor
        self.mainWindow = tk.Tk()
        self.mainWindow.title("CMPTracers - GUI")
        self.mainWindow.resizable(False,False)
        #self.mainWindow.configure(background='#FFFFFF')
        self.normalizerNumber = 0

    def aboutDev(self):
        self.windowDev = tk.Toplevel(self.mainWindow)

        self.Label_Title_OESDebug = ttk.Label(master=self.windowDev,
                                              text="CMPTracers - GUI",
                                              font=(self.MAIN_TITLE_FONT, self.MAIN_TITLE_SIZE))
        self.pic = tk.PhotoImage(file='img/smile.png')

        self.devPic = tk.Label(master=self.windowDev, image=self.pic)
        self.devPic.photo = self.pic

        self.Label_Developpers = ttk.Label(master=self.windowDev,
                                           text="Developped by : SMILE"
                                           )

        self.Label_Title_OESDebug.grid(row=0, column=0)

        self.devPic.grid(row=5, column=0)
        self.Label_Developpers.grid(row=10, column=0)
        self.windowDev.mainloop()



    def _quitPorgram(self):
        """ Function called if user wants to exit the program """
        answer = mbox.askyesno('Exit program', 'Are you sure that you want to exit?')
        if (answer == True):
            self.mainWindow.quit()
            self.mainWindow.destroy()
            exit()

    def setMenuBar(self):
        self.menuBar = tk.Menu(self.mainWindow)
        self.mainWindow.config(menu=self.menuBar)

        # Define file menu
        fileMenu = tk.Menu(self.menuBar, tearoff=0)
        fileMenu.add_command(label="Exit", command=self._quitPorgram)
        self.menuBar.add_cascade(label="File", menu=fileMenu)

        # Define Help Section
        helpMenu = tk.Menu(self.menuBar, tearoff=0)
        helpMenu.add_command(label="Tutorial", command=self.showDoc)
        helpMenu.add_separator()
        helpMenu.add_command(label="About Devs", command=self.aboutDev)
        self.menuBar.add_cascade(label="Help", menu=helpMenu)

    def showDoc(self):
        import webbrowser, os
        webbrowser.open('file://' + os.path.realpath("doc/index.html"))
        print(os.path.realpath("doc/index.html"))

    def browseToDirectory(self):
        try:
            folder_selected = filedialog.askdirectory()
            #print(folder_selected)

            self.Entry_Path_To_Trace_Output_Dir.delete(0, tk.END)

            self.Entry_Path_To_Trace_Output_Dir.insert(0, folder_selected)
            # path = folder_selected + "/src/openocd"

            if (os.path.exists(folder_selected) and os.path.exists(folder_selected+"/ftraceQSort/")):
                self.Label_Directory_Path_Information.config(text="Great! this is a valid directory",
                                                               foreground="green")

                self.getTargePageSize()
                self.getNumberOftests()
                self.getTracers()
                self.getHostName()
                self.getTargetInformation()
            else:
                self.Label_Directory_Path_Information.config(text="Please select a valid output directory", foreground="red")

        except Exception as ex:
            print(ex)


    def getTargePageSize(self):
        path = self.Entry_Path_To_Trace_Output_Dir.get() + "/qsortbench/usr-bin-time/qsort0.txt"
        if (os.path.exists(path)):
            with open(path, "r") as file_read:
                for line in file_read:
                    if "Page size (bytes)" in line:
                        self.Label_Page_Size_Number.config(text=line.split(":")[1])


    def getNumberOftests(self):
        path = self.Entry_Path_To_Trace_Output_Dir.get() + "/qsortbench/usr-bin-time/"
        if (os.path.exists(path)):
            filesInDirectory = os.listdir(path)
            self.normalizerNumber = len(filesInDirectory)
            self.Label_Number_Of_Tests_Number.config(text=self.normalizerNumber)


    def getTracers(self):
        path = self.Entry_Path_To_Trace_Output_Dir.get()
        if (os.path.exists(path)):
            tracersInDirectory = os.listdir(path)
            tracersInDirectory.remove("sys-state")
            tracersInDirectory.remove("qsortbench")
            tracersInDirectory = str(tracersInDirectory)
            self.Label_Testes_Tracers_Number.config(text=tracersInDirectory)

    def getHostName(self):
        pathHost = self.Entry_Path_To_Trace_Output_Dir.get() + "/sys-state/sys-host.txt"
        if (os.path.exists(pathHost)):
            with open(pathHost, "r") as file_read:
                for line in file_read:
                    if "Hostname" in line:
                        self.Label_Target_Name_Number.config(text=line.split(":")[1])

    def getTargetInformation(self):
        pathSys = self.Entry_Path_To_Trace_Output_Dir.get() + "/sys-state/sys-stats.txt"
        if (os.path.exists(pathSys)):
            with open(pathSys, "r") as file_read:
                for line in file_read:
                    if "Uptime(Since system booting)" in line:
                        self.Label_Uptime_Number.config(text=line.split(":")[1])
                    elif "Total usable main memory size" in line:
                        self.Label_Available_Memory_Number.config(text=line.split(":")[1])
                    elif "Available memory size" in line:
                        self.Label_Free_Memory_Number.config(text=line.split(":")[1])
                    elif "Amount of shared memory" in line:
                        self.Label_Shared_Memory_Number.config(text=line.split(":")[1])
                    elif "Memory used by buffers" in line:
                        self.Label_Buffer_Memory_Number.config(text=line.split(":")[1])
                    elif "Total swap space size" in line:
                        self.Label_Swap_Memory_Number.config(text=line.split(":")[1])
                    elif "Swap space still available" in line:
                        self.Label_Free_Swap_Memory_Number.config(text=line.split(":")[1])
                    elif "Number of current processes" in line:
                        self.Label_Target_Processes_Number.config(text=line.split(":")[1])
                    elif "/proc/loadavg" in line:
                        load = line.split(":")[1].split(" ")
                        print(load)
                        self.Label_Load_Average_Value.config(text="1 minutes : " + load[1] + ", 5 minutes : "+load[2] + ", 15 minutes : " +load[3])


    def showFileSize(self):
        totalFileSize = 0
        x_values_tracer_name = []
        y_values_File_Size = []
        path = self.Entry_Path_To_Trace_Output_Dir.get()
        if (os.path.exists(path)):
            for file in os.listdir(path):
                if file != "sys-state":
                    totalFileSize = 0
                    x_values_tracer_name.append(file)
                    memoryFileSizePath = path + "/" + file + "/"
                    for fileSize in os.listdir(memoryFileSizePath):
                        print(fileSize)
                        if fileSize.endswith("perf") or fileSize.endswith("dat"):
                            totalFileSize+=os.path.getsize(memoryFileSizePath+fileSize)
                        elif fileSize.endswith("lttng"):
                            for path, dirs, files in os.walk(memoryFileSizePath+fileSize):
                                for f in files:
                                    fp = os.path.join(path, f)
                                    totalFileSize += os.path.getsize(fp)
                            print("lttng : " + str(totalFileSize) +"\n")
                            #print(os.path.getsize(memoryFileSizePath+fileSize))
                    y_values_File_Size.append(totalFileSize / (self.normalizerNumber * 1024))

        #print(y_values_elapsed_execution_time)
        colors = ['r', 'g', 'b', 'm', 'maroon']

        plt.bar(x_values_tracer_name, y_values_File_Size, color=colors)
        # plt.xticks(rotation=90)
        plt.xlabel("Tracer")
        plt.ylabel("File size (KB)")
        for i, v in enumerate(y_values_File_Size):
            plt.text(i, v/2 , str(int(v)), color='black', fontweight='bold',ha='center', va='bottom')
        plt.show()

    def showExecutedTime(self):
        totalExecutionTime = 0

        x_values_tracer_name = []
        y_values_elapsed_execution_time = []

        path = self.Entry_Path_To_Trace_Output_Dir.get()

        if (os.path.exists(path)):
            for file in os.listdir(path):
                if file != "sys-state":
                    totalExecutionTime = 0
                    x_values_tracer_name.append(file)
                    memoryTimePath = path + "/" + file + "/usr-bin-time/"
                    for fileTime in os.listdir(memoryTimePath):
                        print(memoryTimePath)
                        with open(memoryTimePath + fileTime, "r") as file_read:
                            for line in file_read:
                                if "Elapsed (wall clock) time" in line:
                                    #totalExecutionTime += int(line.split(":")[1])
                                    totalExecutionTime += float(line.split(":")[4]) * 60 + float(line.split(":")[5])
                    y_values_elapsed_execution_time.append(totalExecutionTime / self.normalizerNumber)

        print(y_values_elapsed_execution_time)
        colors = ['r', 'g', 'b', 'k', 'maroon']

        plt.bar(x_values_tracer_name, y_values_elapsed_execution_time, color=colors)
        # plt.xticks(rotation=90)
        plt.xlabel("Tracer")
        plt.ylabel("Execution time (s)")

        for i, v in enumerate(y_values_elapsed_execution_time):
            plt.text(i, v/2 , "{0:.2f}".format(v), color='black', fontweight='bold',ha='center', va='bottom')
        plt.show()

    def showContextSwitches(self):
        totalVoluntaryContextSwitches = 0
        x_values = []
        y_values = []

        path = self.Entry_Path_To_Trace_Output_Dir.get()
        if (os.path.exists(path)):
            for file in os.listdir(path):
                if file != "sys-state":
                    totalVoluntaryContextSwitches = 0
                    x_values.append(file)
                    memoryRssPath = path + "/" + file + "/usr-bin-time/"
                    for fileTime in os.listdir(memoryRssPath):
                        print(memoryRssPath)
                        with open(memoryRssPath + fileTime, "r") as file_read:
                            for line in file_read:
                                if "Voluntary context switches" in line:
                                    totalVoluntaryContextSwitches += int(line.split(":")[1])

                    y_values.append(totalVoluntaryContextSwitches / self.normalizerNumber)
        print(y_values)

        colors = ['#624ea7', 'g', 'yellow', 'm', 'maroon']

        #plt.bar(x_values[0], y_values[0], color=colors)
        plt.bar(x_values, y_values, color=colors)


        for i, v in enumerate(y_values):
            plt.text(i, v/2 , str(int(v)), color='black', fontweight='bold',ha='center', va='bottom')

        plt.xlabel("Tracers")
        plt.ylabel("nb voluntary context switches")

        #plt.xticks(rotation=90)
        plt.show()

    def showInvoluntaryContextSwitches(self):
        totalInvoluntaryContextSwitches = 0
        x_values = []
        y_values = []

        path = self.Entry_Path_To_Trace_Output_Dir.get()
        if (os.path.exists(path)):
            for file in os.listdir(path):
                if file != "sys-state":
                    totalInvoluntaryContextSwitches = 0
                    x_values.append(file)
                    memoryRssPath = path + "/" + file + "/usr-bin-time/"
                    for fileTime in os.listdir(memoryRssPath):
                        print(memoryRssPath)
                        with open(memoryRssPath + fileTime, "r") as file_read:
                            for line in file_read:
                               if "Involuntary context switches" in line:
                                    totalInvoluntaryContextSwitches += int(line.split(":")[1])

                    y_values.append(totalInvoluntaryContextSwitches / self.normalizerNumber)
        print(y_values)

        colors = ['#624ea7', 'g', 'yellow', 'm', 'maroon']

        #plt.bar(x_values[0], y_values[0], color=colors)
        plt.bar(x_values, y_values, color=colors)

        for i, v in enumerate(y_values):
            plt.text(i, v / 2, str(int(v)), color='black', fontweight='bold', ha='center', va='bottom')


        plt.xlabel("Tracers")
        plt.ylabel("nb of unvoluntary context switches")

        #plt.xticks(rotation=90)
        plt.show()

    def showPageFault(self):
        totalMinorPageFaults = 0
        x_values_tracer_name = []
        y_values_nb_page_faults = []

        pathPage = self.Entry_Path_To_Trace_Output_Dir.get()
        print(pathPage)
        if (os.path.exists(pathPage)):
            for filePageFault in os.listdir(pathPage):
                if filePageFault!="sys-state":
                    totalMinorPageFaults = 0
                    x_values_tracer_name.append(filePageFault)

                    memoryPageFaultsPath = pathPage + "/" + filePageFault + "/usr-bin-time/"
                    for filePageFaults in os.listdir(memoryPageFaultsPath):
                        #print(memoryRssPath)
                        with open(memoryPageFaultsPath+filePageFaults, "r") as file_read:
                            for line in file_read:
                                if "Minor (reclaiming a frame) page faults" in line:
                                    totalMinorPageFaults+=int(line.split(":")[1])
                    y_values_nb_page_faults.append(totalMinorPageFaults / self.normalizerNumber)

        colors = ['r', 'g', 'b', 'm', 'maroon']

        plt.bar(x_values_tracer_name, y_values_nb_page_faults, color=colors)
        # plt.xticks(rotation=90)
        plt.xlabel("Tracer")
        plt.ylabel("Minor Page faults")

        for i, v in enumerate(y_values_nb_page_faults):
            plt.text(i, v/2 , str(int(v)), color='black', fontweight='bold',ha='center', va='bottom')

        plt.show()


    def showExecRss(self):
        totalRss = 0
        x_values = []
        y_values = []

        pathRss = self.Entry_Path_To_Trace_Output_Dir.get()
        print(pathRss)
        if (os.path.exists(pathRss)):
            for file in os.listdir(pathRss):
                if file != "sys-state":
                    totalRss = 0
                    x_values.append(file)
                    #
                    #y_values.append(1)
                    memoryRssPath = pathRss + "/" + file + "/usr-bin-time/"
                    for fileTime in os.listdir(memoryRssPath):
                        print(memoryRssPath)

                        with open(memoryRssPath+fileTime, "r") as file_read:
                            for line in file_read:
                                if "Maximum resident set size (kbytes)" in line:
                                    totalRss+=int(line.split(":")[1])


                    y_values.append(totalRss/self.normalizerNumber)



        colors = ['r', 'g', 'b', 'm', 'maroon']
        plt.title("Max RSS")
        plt.text(10,10,"Hello")
        plt.bar(x_values, y_values, color=colors)
       # plt.xticks(rotation=90)
        plt.xlabel("Tracer")
        plt.ylabel("Max RSS size (KB)")

        for i, v in enumerate(y_values):
            plt.text(i, v/2 , str(int(v)), color='black', fontweight='bold',ha='center', va='bottom')

        plt.show()
    def mainWindowWidgetsDefinition(self):
        self.MAIN_TITLE_FONT = "Arial"
        self.MAIN_TITLE_SIZE = 26
        self.Label_Title_Main_Window = ttk.Label(master=self.mainWindow, text="CMPTracers - GUI",
                                                 font=(self.MAIN_TITLE_FONT, self.MAIN_TITLE_SIZE))

        self.Label_Frame_mainWindowWrapper = ttk.LabelFrame(master=self.mainWindow, text="Output directory settings")
#        self.Label_Frame_mainWindowWrapper.configure(background='#F28A30')

        self.Label_Directory_Path = ttk.Label(master=self.Label_Frame_mainWindowWrapper, text="Output directory path : ", font='Helvetica 11 bold')
        self.Entry_Path_To_Trace_Output_Dir = ttk.Entry(master=self.Label_Frame_mainWindowWrapper, width=52)

        self.Button_Browse_To_Trace_Cmd_File = ttk.Button(master=self.Label_Frame_mainWindowWrapper,
                                                          text="Browse output directory", command=self.browseToDirectory)

        self.Label_Directory_Path_Information = ttk.Label(master=self.Label_Frame_mainWindowWrapper,
                                              text="Navigate to output directory", foreground="green")



        self.Label_Frame_Button_Information_Block = ttk.LabelFrame(master=self.mainWindow, text="Tracing Information")
        self.Label_Number_Of_Tests = ttk.Label(master=self.Label_Frame_Button_Information_Block,
                                              text="Number of tests : ", font='Helvetica 11 bold')
        self.Label_Number_Of_Tests_Number = ttk.Label(master=self.Label_Frame_Button_Information_Block,
                                               text="0")

        self.Label_Testes_Tracers = ttk.Label(master=self.Label_Frame_Button_Information_Block,
                                               text="Tracers : ", font='Helvetica 11 bold')
        self.Label_Testes_Tracers_Number = ttk.Label(master=self.Label_Frame_Button_Information_Block,
                                              text="Not defined yet!")




        self.Label_Frame_Button_Information_Target_State = ttk.LabelFrame(master=self.mainWindow, text="Target Information")
        self.Label_Target_Name = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                text="Target Name : ", font='Helvetica 11 bold')
        self.Label_Target_Name_Number = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                       text="Not defined yet!")
        self.Label_Target_Processes = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                           text="Nb of running processes : ", font='Helvetica 11 bold')
        self.Label_Target_Processes_Number = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                  text="Not defined yet!")

        self.Label_Available_Memory = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                         text="Available Memory : ", font='Helvetica 11 bold')
        self.Label_Available_Memory_Number = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                text="Not defined yet!")

        self.Label_Free_Memory = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                text="Free Memory : ", font='Helvetica 11 bold')
        self.Label_Free_Memory_Number = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                       text="Not defined yet!")

        self.Label_Shared_Memory = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                           text="Shared Memory : ", font='Helvetica 11 bold')
        self.Label_Shared_Memory_Number = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                  text="Not defined yet!")

        self.Label_Buffer_Memory = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                             text="Buffer Memory : ", font='Helvetica 11 bold')
        self.Label_Buffer_Memory_Number = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                    text="Not defined yet!")

        self.Label_Swap_Memory = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                             text="Total Swap Size : ", font='Helvetica 11 bold')
        self.Label_Swap_Memory_Number = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                    text="Not defined yet!")

        self.Label_Free_Swap_Memory = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                           text="Free Swap Size : ", font='Helvetica 11 bold')
        self.Label_Free_Swap_Memory_Number = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                  text="Not defined yet!")

        self.Label_Page_Size = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                         text="Page size on the target (bytes) : ", font='Helvetica 11 bold')
        self.Label_Page_Size_Number = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                text="Not defined yet!")

        self.Label_Uptime = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                text="Uptime : ", font='Helvetica 11 bold')
        self.Label_Uptime_Number = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                                       text="Not defined yet!")

        self.Label_Load_Average = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                      text="Load Average : ", font='Helvetica 11 bold')
        self.Label_Load_Average_Value = ttk.Label(master=self.Label_Frame_Button_Information_Target_State,
                                             text="Not defined yet!")



        self.Label_Frame_Button_Control_Options = ttk.LabelFrame(master=self.mainWindow, text="Control Buttons")
        self.Button_Plot_Graph_Memory_RSS = ttk.Button(master=self.Label_Frame_Button_Control_Options,
                                                           text="Show RSS",
                                                           command=self.showExecRss)

        self.Button_Plot_Graph_Execution_Time = ttk.Button(master=self.Label_Frame_Button_Control_Options,
                                                          text="Show Execution Time",
                                                          command=self.showExecutedTime)

        self.Button_Plot_Graph_Context_Switches = ttk.Button(master=self.Label_Frame_Button_Control_Options,
                                                       text="Show Voluntary Context Switches",
                                                       command=self.showContextSwitches)

        self.Button_Plot_Graph_Involuntary_Context_Switches = ttk.Button(master=self.Label_Frame_Button_Control_Options,
                                                             text="Show Involuntary Context Switches",
                                                             command=self.showInvoluntaryContextSwitches)

        self.Button_Plot_Get_File_Sizes = ttk.Button(master=self.Label_Frame_Button_Control_Options,
                                                             text="File Size",
                                                             command=self.showFileSize)

        self.Button_Plot_Get_Minor_Page_Fault = ttk.Button(master=self.Label_Frame_Button_Control_Options,
                                                     text="Minor Page Faults",
                                                     command=self.showPageFault)


    def placeElementsMainWindow(self):
        self.Label_Title_Main_Window.grid(row=0, column=0, padx=10, pady=10)
        self.Label_Frame_mainWindowWrapper.grid(row=1, column=0, padx=10, pady=10)
        self.Label_Directory_Path.grid(row=1, column=0, padx=10, pady=10)
        self.Entry_Path_To_Trace_Output_Dir.grid(row=1, column=2, padx=10, pady=10)
        self.Button_Browse_To_Trace_Cmd_File.grid(row=1, column=4, padx=10, pady=5)
        self.Label_Directory_Path_Information.grid(row=2, column=2, padx=10, pady=5)

        self.Label_Frame_Button_Information_Block.grid(row=2, column=0, padx=10, pady=10)
        self.Label_Number_Of_Tests.grid(row=0, column=0, padx=10, pady=10)
        self.Label_Number_Of_Tests_Number.grid(row=0, column=1, padx=10, pady=10)
        self.Label_Testes_Tracers.grid(row=0, column=2, padx=10, pady=10)
        self.Label_Testes_Tracers_Number.grid(row=0, column=3, padx=10, pady=10)


        self.Label_Frame_Button_Information_Target_State.grid(row=3, column=0, padx=10, pady=10)
        self.Label_Target_Name.grid(row=0, column=0, padx=10, pady=10)
        self.Label_Target_Name_Number.grid(row=0, column=1, padx=10, pady=10)
        self.Label_Target_Processes.grid(row=0, column=2, padx=10, pady=10)
        self.Label_Target_Processes_Number.grid(row=0, column=3, padx=10, pady=10)
        self.Label_Available_Memory.grid(row=1, column=0, padx=10, pady=10)
        self.Label_Available_Memory_Number.grid(row=1, column=1, padx=10, pady=10)
        self.Label_Free_Memory.grid(row=1, column=2, padx=10, pady=10)
        self.Label_Free_Memory_Number.grid(row=1, column=3, padx=10, pady=10)
        self.Label_Shared_Memory.grid(row=2, column=0, padx=10, pady=10)
        self.Label_Shared_Memory_Number.grid(row=2, column=1, padx=10, pady=10)
        self.Label_Buffer_Memory.grid(row=2, column=2, padx=10, pady=10)
        self.Label_Buffer_Memory_Number.grid(row=2, column=3, padx=10, pady=10)
        self.Label_Swap_Memory.grid(row=3, column=0, padx=10, pady=10)
        self.Label_Swap_Memory_Number.grid(row=3, column=1, padx=10, pady=10)
        self.Label_Free_Swap_Memory.grid(row=3, column=2, padx=10, pady=10)
        self.Label_Free_Swap_Memory_Number.grid(row=3, column=3, padx=10, pady=10)
        self.Label_Uptime.grid(row=4, column=2, padx=10, pady=10)
        self.Label_Uptime_Number.grid(row=4, column=3, padx=10, pady=10)
        self.Label_Page_Size.grid(row=4, column=0, padx=10, pady=10)
        self.Label_Page_Size_Number.grid(row=4, column=1, padx=10, pady=10)

        self.Label_Load_Average.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
        self.Label_Load_Average_Value.grid(row=5, column=2, padx=10, pady=10, columnspan=2)


        self.Label_Frame_Button_Control_Options.grid(row=4, column=0, padx=10, pady=10)
        self.Button_Plot_Graph_Memory_RSS.grid(row=2, column=0, padx=10, pady=10)
        self.Button_Plot_Graph_Execution_Time.grid(row=2, column=1, padx=10, pady=10)
        self.Button_Plot_Graph_Context_Switches.grid(row=3, column=0, padx=10, pady=10)
        self.Button_Plot_Graph_Involuntary_Context_Switches.grid(row=3, column=1, padx=10, pady=10)
        self.Button_Plot_Get_File_Sizes.grid(row=2, column=2, padx=10, pady=10)

        self.Button_Plot_Get_Minor_Page_Fault.grid(row=3, column=2, padx=10, pady=10)

    def displayMainWindow(self):
        self.mainWindow.mainloop()

Launcher = TraceCmdParserMainWindow()
Launcher.setMenuBar()
Launcher.mainWindowWidgetsDefinition()
Launcher.placeElementsMainWindow()

Launcher.displayMainWindow()