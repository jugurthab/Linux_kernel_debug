#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import os

from subprocess import Popen, PIPE

from windowProperties import mainWindowProperties



class programLauncher():
    def __init__(self):
        self.mainWindowProp = mainWindowProperties(600,350,(255,255,255))
        self.SmileMainWindow = tk.Tk()
        self.SmileMainWindow.title("OESdebug")
        self.SmileMainWindow.resizable(False,False)

        self.SmileMainWindow.config(bg='white')
        self.MAIN_TITLE_FONT = "Arial"
        self.MAIN_TITLE_SIZE = 26
        self.SECONDARY_TITLE_SIZE = 18
        self.PATH_TO_OPENOCD = "/usr/share/openocd/"
        self.LABEL_FRAME_FONT = "Century Gothic"
        self.LABEL_FRAME_SIZE = 14

        self.LABEL_FONTS = "Times New Roman"
        self.LABEL_SIZE = 12

    def readKnownMicrocontrollers(self, path):
        listOfMicrocontrollers = []
        if (os.path.exists(path)):
            for file in os.listdir(path):
                listOfMicrocontrollers.append(file.split(".")[0])
            listOfMicrocontrollers.sort()
            # print(listOfMicrocontrollers)
            return listOfMicrocontrollers
        else:
            return []

    def readKnownInterfaces(self, path):
        listOfInterfaces = []
        if (os.path.exists(path)):
            for file in os.listdir(path):
                if file.endswith(".cfg"):
                    listOfInterfaces.append(file.split(".")[0])
            for file in os.listdir(path+"/ftdi"):
                if file.endswith(".cfg"):
                    listOfInterfaces.append("ftdi/"+file.split(".")[0])
            listOfInterfaces.sort()
            # print(listOfInterfaces)
            return listOfInterfaces
        else:
            return []


    def parseFolderToGetKnownMCA(self,path):

        if self.Checkbox_Manual_Installation_OpenOCD.get() == 0:
            path = "/usr/share/openocd/scripts/"
        else:
            path = self.Entry_Manual_Path_OpenOCD.get() + "/tcl/"
            print(path)



        self.ComboBox_Microcontroller_ID.set("")
        if self.User_Choice_Card_MCA.get()==2 :
            path += "target/"
            print("target : " + path)
            self.listOfKnownMicrocontrollers = self.readKnownMicrocontrollers(path)

            self.Label_Microcontroller.config(text="Microcontroller(MCU) : ")

            self.Label_Supported_Microcontrollers.config(text="Nb of supported microcontrollers(MCU) by your OPENOCD : ")
            self.Label_Supported_Microcontrollers_User_Input.config(text="Is your MCU supported : ")
            self.ComboBox_Microcontroller_ID['values'] = self.listOfKnownMicrocontrollers

            self.Label_Number_Supported_Microcontrollers_User_Input.config(text="<Choose Your MCU>")

        else:
            path += "board/"
            print("board : " + path)
            self.listOfKnownMicrocontrollers = self.readKnownMicrocontrollers(path)

            self.Label_Microcontroller.config(text="Board : ")
            self.Label_Supported_Microcontrollers_User_Input.config(text="Is your Board supported : ")
            self.Label_Supported_Microcontrollers.config(text="Nb of supported Boards by your OPENOCD : ")
            self.ComboBox_Microcontroller_ID['values'] = self.listOfKnownMicrocontrollers

            self.Label_Number_Supported_Microcontrollers_User_Input.config(text="<Choose Your Board>")

        self.Label_Number_Supported_Microcontrollers.config(text=len(self.listOfKnownMicrocontrollers))

    def _quitPorgram(self):
        """ Function called if user wants to exit the program """
        answer = mbox.askyesno('Exit program', 'Are you sure that you want to exit?')
        if (answer == True):
            self.SmileMainWindow.quit()
            self.SmileMainWindow.destroy()
            exit()

    def detectOpenOCD(self, path):

        if (os.path.exists(path+"/scripts/target/") and os.path.exists(path+"/scripts/board/")):
            return True
        else:
            return False

    def getOPENOCDVersion(self):
        print("version")

    def createTabsForNavigation(self):
        """ Define the tabs for easier navigation """
        self.tabControl = ttk.Notebook(self.SmileMainWindow)
        # OpenOCD Check Support
        self.SMILE_Tab_OPENOCDSUPPORT = ttk.Frame(self.tabControl)
        self.tabControl.add(self.SMILE_Tab_OPENOCDSUPPORT, text='OPENOCD Support')

        # Adapter Check Support
        self.SMILE_Tab_AdapterSUPPORT = ttk.Frame(self.tabControl)
        self.tabControl.add(self.SMILE_Tab_AdapterSUPPORT, text='Adapter Support')

        # MCA(Microcontroller) Check Support
        self.SMILE_Tab_MicroControllerSUPPORT = ttk.Frame(self.tabControl)
        self.tabControl.add(self.SMILE_Tab_MicroControllerSUPPORT, text='MCU Support')

        # Generation of config files
        self.SMILE_Tab_ConfigFileGeneration = ttk.Frame(self.tabControl)
        self.tabControl.add(self.SMILE_Tab_ConfigFileGeneration, text='Config File')

        self.tabControl.pack(expand=1, fill="both")

    def locateOpenOCD(self):
        try:
            folder_selected = filedialog.askdirectory()
            print(folder_selected)

            self.Entry_Manual_Path_OpenOCD.delete(0, tk.END)

            self.Entry_Manual_Path_OpenOCD.insert(0, folder_selected)
            path = folder_selected + "/src/openocd"
            if (os.path.exists(path)):
                self.Label_Manual_Path_OpenOCD_Error.config(text="OpenOCD was found!", foreground="green")
            else:
                myErrortext = "Cannot find " + path
                self.Label_Manual_Path_OpenOCD_Error.config(text=myErrortext, foreground="red")
            self.getNumberOfKnownAdapters()
            self.parseFolderToGetKnownMCA("/usr/share/openocd/scripts/board/")
        except Exception as ex:
            print(ex)


    def locateSaveConfigFolder(self):
        try:
            folder_selected = filedialog.askdirectory()
            print(folder_selected)

            self.Entry_Manual_Path_OpenOCD_Config.delete(0, tk.END)

            self.Entry_Manual_Path_OpenOCD_Config.insert(0, folder_selected)
            #path = folder_selected + "/src/openocd"
            path = folder_selected
            if (os.path.exists(path)):
                self.Label_Manual_Path_Save_Config_Info.config(text="Config files will be saved to "+path, foreground="green")
            else:
                myErrortext = "Cannot save to " + path
                self.Label_Manual_Path_Save_Config_Info.config(text=myErrortext, foreground="red")

        except Exception as ex:
            print(ex)

    def loadPreviousConfig(self):
        try:
            file_selected = filedialog.askopenfilename()
            print(file_selected)

            # Load cfg configuration file
            fd = open(file_selected, "r")
            content = fd.read()

            self.ScrolledText_Adapter_Config.delete('1.0', tk.END)
            self.ScrolledText_Adapter_Config.insert(tk.INSERT, content)

            fd.close()

            # Load oes configuration file
            file_selected = str(file_selected).replace(".cfg",".oes")
            with open(file_selected, "r") as file_read:
                for line in file_read:
                    if line.split(",")[0] == "#Adapter_Found":
                        self.User_Choice_Adapter_Existance.set(1)
                        self.selectedInterface_Adapter_Dongle.set(line.split(",")[1].strip())
                        self.hideOrShowAdapter()
                    elif line.split(",")[0] == "#Adapter_New":
                        self.User_Choice_Adapter_Existance.set(2)

                        self.ComboBox_Variable_Protocol_Dongle_Interface.set(line.split(",")[1].strip())

                        self.Entry_Manufacturer_ID_Dongle.delete(0, tk.END)
                        self.Entry_Manufacturer_ID_Dongle.insert(0, line.split(",")[2].strip())

                        self.Entry_Vendor_ID_Dongle.delete(0, tk.END)
                        self.Entry_Vendor_ID_Dongle.insert(0, line.split(",")[3].strip())

                        self.Entry_Product_ID_Dongle.delete(0, tk.END)
                        self.Entry_Product_ID_Dongle.insert(0, line.split(",")[4].strip())

                        self.ComboBox_Variable_Protocol_Dongle_Interface_speed.set(line.split(",")[5].strip())
                        self.hideOrShowAdapter()


                    if line.split(",")[0] == "#BOARD_Found":
                        self.User_Choice_MCU_Existance.set(1)
                        self.hideOrShowMCU()
                        self.User_Choice_Card_MCA.set(1)
                        self.parseFolderToGetKnownMCA("/usr/share/openocd/scripts/board/")
                        self.selectedMicrocontroller.set(line.split(",")[1].strip())


                    elif line.split(",")[0] == "#MCU_Found":
                        self.User_Choice_MCU_Existance.set(1)
                        self.hideOrShowMCU()
                        self.User_Choice_Card_MCA.set(2)
                        self.parseFolderToGetKnownMCA("/usr/share/openocd/scripts/target/")
                        self.selectedMicrocontroller.set(line.split(",")[1].strip())

                    if line.split(",")[0] == "#CHIP_Not_Found":
                        self.User_Choice_MCU_Existance.set(2)
                        self.hideOrShowMCU()
                        self.Entry_Chip_Name.delete(0, tk.END)
                        self.Entry_Chip_Name.insert(0, line.split(",")[1].strip())

                        self.ComboBox_Chip_Type.set(line.split(",")[2].strip())
                        self.ComboBox_Chip_Family.set(line.split(",")[3].strip())

                        self.ComboBox_Chip_IR_Length.set(line.split(",")[4].strip())

                        self.ComboBox_Chip_Endianness.set(line.split(",")[5].strip())


                        self.Entry_Chip_Tap_ID.delete(0, tk.END)
                        self.Entry_Chip_Tap_ID.insert(0, line.split(",")[6].strip())

                    if line.split(",")[0] == "#Memory_Config":
                        print("helo")
                        self.Configure_Memory.set(1)
                        self.Configure_Memory_SDRAM.set(1)

                        self.Entry_Chip_SDRAM_Start_Address.delete(0, tk.END)
                        self.Entry_Chip_SDRAM_Start_Address.insert(0, line.split(",")[1])

                        self.Entry_Chip_SDRAM_Size_Address.delete(0, tk.END)
                        self.Entry_Chip_SDRAM_Size_Address.insert(0, line.split(",")[2])

                        if line.split(",")[3]=="physical":
                            self.Type_SDRam_variable.set(1)
                        else:
                            self.Type_SDRam_variable.set(2)

                        if line.split(",")[4].strip()=="0":
                            self.Backup_SDRam_variable.set(1)
                        else:
                            self.Backup_SDRam_variable.set(2)
                    # else:
                    #     print("oui")
                    #     self.Configure_Memory.set(0)
                    #     self.Configure_Memory_SDRAM.set(0)
                    #     self.Entry_Chip_SDRAM_Start_Address.delete(0, tk.END)
                    #     self.Entry_Chip_SDRAM_Size_Address.delete(0, tk.END)




                    if line.split(",")[0] == "#Flash_Memory_Config":
                        self.Configure_Memory.set(1)
                        #self.Configure_Memory_SDRAM.set(1)

                        self.Configure_Memory_FLASH.set(1)

                        if line.split(",")[1]=="Nor":
                            self.ComboBox_Chip_Flash_Type_Variable.set("Nor")

                            position = self.listOfNorDriversList.index(line.split(",")[2])
                            self.ComboBox_Chip_Flash_Type.current(position)

                            self.ScrolledText_Nor_Flash_Command_Field.delete('1.0', tk.END)
                            self.ScrolledText_Nor_Flash_Command_Field.insert(tk.INSERT, line.split(",")[3])

                            self.Nor_Flash_variable.set(int(line.split(",")[4].strip()))

                        elif line.split(",")[1]=="Nand":
                            self.ComboBox_Chip_Flash_Type_Variable.set("Nand")

                            position = self.ComboBox_Nand_Flash_values.index(line.split(",")[2])

                            self.ComboBox_Nand_Flash_Driver.current(position)

                            self.ScrolledText_Nand_Flash_Command_Field.delete('1.0', tk.END)
                            self.ScrolledText_Nand_Flash_Command_Field.insert(tk.INSERT, line.split(",")[3])


                        elif line.split(",")[1]=="mFlash":
                            self.ComboBox_Chip_Flash_Type_Variable.set("mFlash")

                            position = self.listOfMFlashDrivers.index(line.split(",")[2])
                            self.ComboBox_mFlash_Driver.current(position)

                            self.ScrolledText_mFlash_Command_Field.delete('1.0', tk.END)
                            self.ScrolledText_mFlash_Command_Field.insert(tk.INSERT, line.split(",")[3])

                    else:
                        self.Configure_Memory_FLASH.set(0)

            self.showOrHideMemorySettings()
            self.showOrHideMemoryType()
            file_read.close()

            self.GoToFileCOnfigTab()
        except Exception as ex:
            print(ex)

    def setMenuBar(self):
        self.menuBar = tk.Menu(self.SmileMainWindow)
        self.SmileMainWindow.config(menu=self.menuBar)

        # Define file menu
        fileMenu = tk.Menu(self.menuBar, tearoff=0)
        fileMenu.add_command(label="Load config", command=self.loadPreviousConfig)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self._quitPorgram)
        self.menuBar.add_cascade(label="File", menu=fileMenu)

        # Define Help Section
        toolMenu = tk.Menu(self.menuBar, tearoff=0)
        #toolMenu.add_command(label="Tools")
        #toolMenu.add_separator()
        toolMenu.add_command(label="Discover TAP ID", command=self.discoverTapID)
        self.menuBar.add_cascade(label="Tools", menu=toolMenu)

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


    def SmileDefineWidgetsOpenOCDSupport(self):
        self.Label_Frame_mainWindowWrapper = ttk.LabelFrame(master=self.SMILE_Tab_OPENOCDSUPPORT, text="OPENOCD Auto-Detection")

        self.TitleWindowLabel = ttk.Label(master=self.Label_Frame_mainWindowWrapper, text="OESdebug",
                                          font=(self.MAIN_TITLE_FONT, self.MAIN_TITLE_SIZE))
        self.SecondaryTitleWindowLabel = ttk.Label(master=self.Label_Frame_mainWindowWrapper,
                                                   text="Open Easy Debug - Reduce Target debugging time",
                                                   font=(self.MAIN_TITLE_FONT, self.SECONDARY_TITLE_SIZE))
        self.Label_Frame_mainWindowWrapper.pack(fill="both", expand=True)
        if (self.detectOpenOCD(self.PATH_TO_OPENOCD)):
            textToDiaplay = self.getOpenOCDVersion() + " detected"
            self.detectingOpenOCD = ttk.Label(master=self.Label_Frame_mainWindowWrapper, text=textToDiaplay,
                                              font=(self.LABEL_FONTS, self.LABEL_SIZE), foreground="green")
            self.pic = tk.PhotoImage(file='img/validate_icon.gif')
        else:
            textToDiaplay = "OPENOCD was not detected"
            self.detectingOpenOCD = ttk.Label(master=self.Label_Frame_mainWindowWrapper,
                                              text=textToDiaplay,
                                              font=(self.LABEL_FONTS, self.LABEL_SIZE), foreground="red")
            self.pic = tk.PhotoImage(file='img/no-x.gif')



        self.can = tk.Label(master=self.Label_Frame_mainWindowWrapper,image=self.pic)
        self.can.photo = self.pic



        self.Checkbox_Manual_Installation_OpenOCD = tk.IntVar()
        self.SMILE_CheckBox_Install_Open_OCD = ttk.Checkbutton(master=self.Label_Frame_mainWindowWrapper,
                                                               text="I have compiled OpenOCD from sources",onvalue = 1, offvalue = 0,
                                                               variable=self.Checkbox_Manual_Installation_OpenOCD,
                                                               command=self.showOrHideOpenOCDManualInstall)
        self.Checkbox_Manual_Installation_OpenOCD.set(0)


        self.LabelFrame_Manual_Installation_OpenOCD = ttk.LabelFrame(master=self.Label_Frame_mainWindowWrapper,
                                                            text="Installation directory OpenOCD")
        self.Label_Manual_Path_OpenOCD = ttk.Label(master=self.LabelFrame_Manual_Installation_OpenOCD,
                                                      text="OpenOCD install directory : ")
        self.Entry_Manual_Path_OpenOCD = ttk.Entry(master=self.LabelFrame_Manual_Installation_OpenOCD)
        self.Button_Manual_Path_OpenOCD = tk.Button(master=self.LabelFrame_Manual_Installation_OpenOCD,
                                                   text="Browse", command=self.locateOpenOCD)
        self.Label_Manual_Path_OpenOCD_Error = ttk.Label(master=self.LabelFrame_Manual_Installation_OpenOCD,
                                                   text="Please browse to OpenOCD install directory",foreground="green")



        self.Label_Frame_mainWindowWrapper_Buttons = ttk.LabelFrame(master=self.SMILE_Tab_OPENOCDSUPPORT, text="Control Operation")
        self.SMILE_OPENOCD_Install_Button = tk.Button(master=self.Label_Frame_mainWindowWrapper_Buttons,text="Install OPENOCD",
                                                      command=self.installOpenOCD)
        self.SMILE_OPENOCD_Check_Support_Button = tk.Button(master=self.Label_Frame_mainWindowWrapper_Buttons,
                                                      text="Check again OpenOCD support",
                                                            command=self.checkAgainOPENOCDSupport)

        self.SMILE_OPENOCD_Next_Button = tk.Button(master=self.Label_Frame_mainWindowWrapper_Buttons,
                                                      text="Next",command=self.GoToAdapterSupport)
    def SmilePlaceWidgetsOpenOCDSupport(self):
        self.Label_Frame_mainWindowWrapper.grid(row=0, column=0)

        self.TitleWindowLabel.grid(row=0, column=0, columnspan=2)
        self.SecondaryTitleWindowLabel.grid(row=1, column=0, padx=5, pady=5,columnspan=2)

        self.detectingOpenOCD.grid(row=2, column=0, padx=5, pady=5,columnspan=2)
        self.can.grid(row=3, column=0, padx=5, pady=5,columnspan=2)

        self.SMILE_CheckBox_Install_Open_OCD.grid(row=4, column=0, padx=5, pady=5,columnspan=2)
        self.LabelFrame_Manual_Installation_OpenOCD.grid(row=5, column=0, padx=5, pady=5,columnspan=2)
        self.Label_Manual_Path_OpenOCD.grid(row=6, column=0, padx=5, pady=5)
        self.Entry_Manual_Path_OpenOCD.grid(row=6, column=1, padx=5, pady=5)
        self.Button_Manual_Path_OpenOCD.grid(row=6, column=2, padx=5, pady=5)
        self.Label_Manual_Path_OpenOCD_Error.grid(row=7, column=0, padx=5, pady=5,columnspan=3)


        self.Label_Frame_mainWindowWrapper_Buttons.grid(row=1,column=0, padx=5, pady=5)
        self.SMILE_OPENOCD_Install_Button.grid(row=0, column=0, padx=8, pady=5)
        self.SMILE_OPENOCD_Check_Support_Button.grid(row=0, column=1, padx=8, pady=5)
        self.SMILE_OPENOCD_Next_Button.grid(row=0, column=2, padx=8, pady=5)


    def installOpenOCD(self):
        self.SMILE_WINDOW_Install_Open_OCD = tk.Toplevel(self.SmileMainWindow)
        self.SMILE_LABEL_FRAME_Install_Open_OCD = ttk.LabelFrame(master=self.SMILE_WINDOW_Install_Open_OCD,text="")

        self.SMILE_LABEL_Install_Open_OCD = ttk.Label(master=self.SMILE_WINDOW_Install_Open_OCD,
                                                      text="Installation of OpenOCD")
        self.SMILE_LABEL_Install_Open_OCD_Follow = ttk.Label(master=self.SMILE_WINDOW_Install_Open_OCD,
                                                      text="Updates are important to find the latest version of the software")

        self.valueOfUpdateCheckBox = tk.IntVar()
        self.SMILE_CheckBox_Install_Open_OCD = ttk.Checkbutton(master=self.SMILE_WINDOW_Install_Open_OCD,
                                                               text="With cache Update",variable=self.valueOfUpdateCheckBox)

        self.SMILE_Button_Install_Open_OCD_Real = ttk.Button(master=self.SMILE_WINDOW_Install_Open_OCD,text="Install Now",
                                                             command=self.downloadOpenOCD)

        self.SMILE_LABEL_FRAME_Install_Open_OCD.grid(row=0,column=0)

        self.SMILE_LABEL_Install_Open_OCD.grid(row=1,column=0)
        self.SMILE_LABEL_Install_Open_OCD_Follow.grid(row=2, column=0)
        self.SMILE_CheckBox_Install_Open_OCD.grid(row=3, column=0)
        self.SMILE_Button_Install_Open_OCD_Real.grid(row=5, column=0)

    def SmileDefineWidgetsMCASupport(self):


        self.TitleWindowLabelMCASupport = ttk.Label(master=self.SMILE_Tab_MicroControllerSUPPORT, text="OESdebug",
                                          font=(self.MAIN_TITLE_FONT, self.MAIN_TITLE_SIZE))

        self.User_Choice_MCU_Existance = tk.IntVar()
        self.RadioButton_MCU_Exists = tk.Radiobutton(master=self.SMILE_Tab_MicroControllerSUPPORT,
                                                         text="Existing MCU or Board", value=1,
                                                         variable=self.User_Choice_MCU_Existance,
                                                         command=self.hideOrShowMCU)

        self.RadioButton_MCU_Does_Not_Exists = tk.Radiobutton(master=self.SMILE_Tab_MicroControllerSUPPORT,
                                                                  text="Create a custom chip",
                                                                  value=2,
                                                                  variable=self.User_Choice_MCU_Existance,
                                                                  command=self.hideOrShowMCU)
        self.User_Choice_MCU_Existance.set(1)



        self.Label_Frame_mainWindowWrapper_MCA = ttk.LabelFrame(master=self.SMILE_Tab_MicroControllerSUPPORT,
                                                                text="Check MCU (Microcontroller) or board support")
        self.Label_Micro_Board = ttk.Label(master=self.Label_Frame_mainWindowWrapper_MCA,
                                               text="Target : ")

        self.User_Choice_Card_MCA = tk.IntVar()
        self.RadioButton_Board = tk.Radiobutton(master=self.Label_Frame_mainWindowWrapper_MCA,
                                                              text="Board", value=1,
                                                              variable=self.User_Choice_Card_MCA,command=lambda: self.parseFolderToGetKnownMCA("/usr/share/openocd/scripts/board/"))

        self.RadioButton_MCA = tk.Radiobutton(master=self.Label_Frame_mainWindowWrapper_MCA, text="MCU",
                                                     value=2,
                                                     variable=self.User_Choice_Card_MCA,command=lambda: self.parseFolderToGetKnownMCA("/usr/share/openocd/scripts/target/"))
        self.User_Choice_Card_MCA.set(1)

        self.Label_Microcontroller = ttk.Label(master=self.Label_Frame_mainWindowWrapper_MCA,
                                               text="Microcontroller(MCU) : ", font=(self.LABEL_FONTS, self.LABEL_SIZE))
        self.listOfKnownMicrocontrollers = self.readKnownMicrocontrollers("/usr/share/openocd/scripts/board/")


        self.Label_Supported_Microcontrollers = ttk.Label(master=self.Label_Frame_mainWindowWrapper_MCA,
                                                          text="Nb of supported microcontrollers(MCU) by your OPENOCD : ",
                                                          font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.Label_Number_Supported_Microcontrollers = ttk.Label(master=self.Label_Frame_mainWindowWrapper_MCA,
                                                                 text=len(self.listOfKnownMicrocontrollers),
                                                                 font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.selectedMicrocontroller = tk.StringVar()

        self.selectedMicrocontroller.trace("w", self._listOfMatchesWithYourMicrocontrollers)
        # print(self.listOfKnownMicrocontrollers)
        self.ComboBox_Microcontroller_ID = ttk.Combobox(master=self.Label_Frame_mainWindowWrapper_MCA,
                                                        values=self.listOfKnownMicrocontrollers,
                                                        textvariable=self.selectedMicrocontroller)

        self.Label_Supported_Microcontrollers_User_Input = ttk.Label(master=self.Label_Frame_mainWindowWrapper_MCA,
                                                                     text="Is your MCU supported : ",
                                                                     font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.Label_Number_Supported_Microcontrollers_User_Input = ttk.Label(master=self.Label_Frame_mainWindowWrapper_MCA,
                                                                            text="<Choose Your MCU>",
                                                                            font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.Label_TRUE_Number_Supported_Microcontrollers_User_Input = ttk.Label(master=self.Label_Frame_mainWindowWrapper_MCA,
                                                                                 text="",
                                                                                 font=(
                                                                                 self.LABEL_FONTS, self.LABEL_SIZE))



        # Define a new SOC
        self.Label_Frame_mainWindowWrapper_NEW_SOC = ttk.LabelFrame(master=self.SMILE_Tab_MicroControllerSUPPORT,
                                                                text="Define new SOC")

        self.Label_Chip_Name = ttk.Label(master=self.Label_Frame_mainWindowWrapper_NEW_SOC,
                                           text="CHIP Name : ")
        self.Entry_Chip_Name = ttk.Entry(master=self.Label_Frame_mainWindowWrapper_NEW_SOC)

        self.Label_Chip_Type = ttk.Label(master=self.Label_Frame_mainWindowWrapper_NEW_SOC,
                                         text="CHIP Type : ")
        self.ComboBox_Chip_Type_variable = tk.StringVar()
        self.ComboBox_Chip_Type = ttk.Combobox(master=self.Label_Frame_mainWindowWrapper_NEW_SOC,
                                                     values=['cpu', 'dsp'],
                                                     textvariable=self.ComboBox_Chip_Type_variable)
        self.ComboBox_Chip_Type.current(0)

        self.Label_Chip_Family = ttk.Label(master=self.Label_Frame_mainWindowWrapper_NEW_SOC,
                                         text="CHIP Family : ")
        self.ComboBox_Chip_Family_variable = tk.StringVar()
        self.ComboBox_Chip_Family_values = self.listSupportedOpenOCDMCUFamily()
        self.ComboBox_Chip_Family = ttk.Combobox(master=self.Label_Frame_mainWindowWrapper_NEW_SOC,
                                                     values=self.ComboBox_Chip_Family_values,
                                                     textvariable=self.ComboBox_Chip_Family_variable)

        self.Label_Chip_IR_Length = ttk.Label(master=self.Label_Frame_mainWindowWrapper_NEW_SOC,
                                         text="Length of instruction register (IR) : ")
        self.ComboBox_Chip_IR_Length_variable = tk.StringVar()
        self.ComboBox_Chip_IR_Length = ttk.Combobox(master=self.Label_Frame_mainWindowWrapper_NEW_SOC,
                                                     values=['2', '4','5','6','10','15'],
                                                     textvariable=self.ComboBox_Chip_IR_Length_variable)
        self.ComboBox_Chip_IR_Length.current(1)

        self.Label_Chip_Endianness = ttk.Label(master=self.Label_Frame_mainWindowWrapper_NEW_SOC,
                                         text="Endianness of Chip : ")

        self.ComboBox_Chip_Endianness_variable = tk.StringVar()
        self.ComboBox_Chip_Endianness = ttk.Combobox(master=self.Label_Frame_mainWindowWrapper_NEW_SOC,
                                                     values=['little','big'],
                                                     textvariable=self.ComboBox_Chip_Endianness_variable)

        self.ComboBox_Chip_Endianness.current(0)



        self.Label_Chip_Tap_ID = ttk.Label(master=self.Label_Frame_mainWindowWrapper_NEW_SOC,
                                               text="CPU Tap ID : ")
        self.Entry_Chip_Tap_ID = ttk.Entry(master=self.Label_Frame_mainWindowWrapper_NEW_SOC)

        self.Configure_Memory = tk.IntVar()

        self.CheckButton_Enable_Memory_Config = ttk.Checkbutton(master=self.Label_Frame_mainWindowWrapper_NEW_SOC,
                                                                text="Enable Memory Config",
                                                                variable=self.Configure_Memory,
                                                                onvalue=1, offvalue=0,command=self.showOrHideMemorySettings)
        self.Configure_Memory.set(0)

        #Memory SDRAM and Flash Settings

        self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings = ttk.LabelFrame(master=self.SMILE_Tab_MicroControllerSUPPORT,
                                                                text="Memory settings")

        self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM = ttk.LabelFrame(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings,
            text="Memory on chip (SDRAM)")

        self.Configure_Memory_SDRAM = tk.IntVar()
        self.CheckButton_Enable_Memory_Config_SDRAM = ttk.Checkbutton(master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM,
                                                                text="Enable SDRAM settings",
                                                                variable=self.Configure_Memory_SDRAM,
                                                                onvalue=1, offvalue=0)
        self.Configure_Memory_SDRAM.set(0)

        self.Label_Chip_SDRAM_Start_Address = ttk.Label(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM,
            text="Starting work area : ")
        self.Entry_Chip_SDRAM_Start_Address = ttk.Entry(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM)

        self.Label_Chip_SDRAM_Size_Address = ttk.Label(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM,
            text="Size of work area : ")
        self.Entry_Chip_SDRAM_Size_Address = ttk.Entry(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM)

        self.Label_Chip_SDRAM_Type_Address = ttk.Label(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM,
            text="Type of Adresses : ")

        self.Type_SDRam_variable = tk.IntVar()
        self.RadioButton_SDRam_Type_Physical = tk.Radiobutton(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM,
            text="Physical", value=1,
            variable=self.Type_SDRam_variable)

        self.RadioButton_SDRam_Type_Virtual = tk.Radiobutton(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM, text="Virtual",
            value=2,
            variable=self.Type_SDRam_variable)
        self.Type_SDRam_variable.set(1)





        self.Label_Chip_SDRAM_Backup_Address = ttk.Label(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM,
            text="Back-up work area : ")

        self.Backup_SDRam_variable = tk.IntVar()
        self.RadioButton_SDRam_Backup_yes = tk.Radiobutton(master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM,
                                                text="yes", value=1,
                                                variable=self.Backup_SDRam_variable)

        self.RadioButton_SDRam_Backup_no = tk.Radiobutton(master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM, text="no",
                                              value=2,
                                              variable=self.Backup_SDRam_variable)
        self.Backup_SDRam_variable.set(2)



        self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_Flash = ttk.LabelFrame(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings,
            text="Flash memory")

        self.Configure_Memory_FLASH = tk.IntVar()
        self.CheckButton_Enable_Memory_Config_FLASH = ttk.Checkbutton(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_Flash,
            text="Enable Flash settings",
            variable=self.Configure_Memory_FLASH,
            onvalue=1, offvalue=0)

        self.Label_Chip_Flash_Type = ttk.Label(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_Flash,
            text="Flash technology : ")

        self.ComboBox_Chip_Flash_Type_Variable = tk.StringVar()
        self.ComboBox_Chip_Flash_Type = ttk.Combobox(master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_Flash,
                                                     values=['Nor','Nand','mFlash'],
                                                     textvariable=self.ComboBox_Chip_Flash_Type_Variable)
        self.ComboBox_Chip_Flash_Type_Variable.set("Nor")
        self.ComboBox_Chip_Flash_Type_Variable.trace('w', self.showOrHideMemoryType)


        self.Label_Chip_Flash_Driver = ttk.Label(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_Flash,
            text="Flash technology Driver : ")

        self.ComboBox_Chip_Flash_Driver_Variable = tk.StringVar()
        self.ComboBox_Chip_Flash_Driver = ttk.Combobox(
            master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_Flash,
            values=['1', '2'],
            textvariable=self.ComboBox_Chip_Flash_Driver_Variable)
        self.ComboBox_Chip_Flash_Driver.current(0)

        # Control buttons MCU
        self.Label_Frame_ControlButtonsMCA = ttk.LabelFrame(master=self.SMILE_Tab_MicroControllerSUPPORT,
                                                            text="Control Buttons")

        self.Button_Previous_MCA = ttk.Button(master=self.Label_Frame_ControlButtonsMCA,
                                                text="Previous",command=self.GoToAdapterSupport)

        self.Button_Look_In_GitHub = ttk.Button(master=self.Label_Frame_ControlButtonsMCA,
                                                text="Look external support in GitHub")

        self.Button_Next_MCA = ttk.Button(master=self.Label_Frame_ControlButtonsMCA,
                                              text="Next",command=self.GoToFileCOnfigTab)

    def SmilePlaceWidgetsMCASupport(self):


        self.TitleWindowLabelMCASupport.grid(row=0,column=0,columnspan=3,pady=10)
        self.RadioButton_MCU_Exists.grid(row=1,column=0)

        self.RadioButton_MCU_Does_Not_Exists.grid(row=1,column=1)


        self.Label_Frame_mainWindowWrapper_MCA.grid(row=2, column=0,columnspan=3,pady=10)
        self.Label_Micro_Board.grid(row=2,column=0,pady=10)
        self.RadioButton_Board.grid(row=2,column=1,pady=10)

        self.RadioButton_MCA.grid(row=2,column=2,pady=10)

        self.Label_Supported_Microcontrollers.grid(row=3, column=0,pady=10)
        self.Label_Number_Supported_Microcontrollers.grid(row=3, column=1,columnspan=2, pady=10)

        self.Label_Microcontroller.grid(row=4,column=0,pady=10)

        self.ComboBox_Microcontroller_ID.grid(row=4,column=1,columnspan=2,pady=10)
        self.Label_Supported_Microcontrollers_User_Input.grid(row=5,column=0,pady=10)
        self.Label_Number_Supported_Microcontrollers_User_Input.grid(row=5,column=1,columnspan=2,pady=10)
        self.Label_TRUE_Number_Supported_Microcontrollers_User_Input.grid(row=6, column=0,columnspan=3,pady=10)


        # define new CHIP
        self.Label_Frame_mainWindowWrapper_NEW_SOC.grid(row=3, column=0,columnspan=2,pady=10)

        self.Label_Chip_Name.grid(row=0,column=0,pady=10)
        self.Entry_Chip_Name.grid(row=0,column=1,pady=10)

        self.Label_Chip_Type.grid(row=1,column=0,pady=10)
        self.ComboBox_Chip_Type.grid(row=1,column=1,pady=10)

        self.Label_Chip_Family.grid(row=2,column=0,pady=10)
        self.ComboBox_Chip_Family.grid(row=2, column=1, pady=10)

        self.Label_Chip_IR_Length.grid(row=3,column=0,pady=10)
        self.ComboBox_Chip_IR_Length.grid(row=3, column=1, pady=10)

        self.Label_Chip_Endianness.grid(row=4, column=0)
        self.ComboBox_Chip_Endianness.grid(row=4, column=1)
        self.Label_Chip_Tap_ID.grid(row=5,column=0,pady=10)
        self.Entry_Chip_Tap_ID.grid(row=5,column=1,pady=10)

        self.CheckButton_Enable_Memory_Config.grid(row=6, column=0,columnspan=2)



        #Memory settings

        self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings.grid(row=3, column=5,columnspan=2,pady=10)

        self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_SDRAM.grid(row=0,column=0,pady=10)
        self.CheckButton_Enable_Memory_Config_SDRAM.grid(row=0,column=0,columnspan=3,pady=10)
        self.Label_Chip_SDRAM_Start_Address.grid(row=1, column=0,pady=10)
        self.Entry_Chip_SDRAM_Start_Address.grid(row=1, column=1,pady=10,columnspan=2)


        self.Label_Chip_SDRAM_Size_Address.grid(row=2, column=0,pady=10)
        self.Entry_Chip_SDRAM_Size_Address.grid(row=2, column=1,pady=10,columnspan=2)

        self.Label_Chip_SDRAM_Type_Address.grid(row=3, column=0,pady=10)
        self.RadioButton_SDRam_Type_Physical.grid(row=3, column=1,pady=10)
        self.RadioButton_SDRam_Type_Virtual.grid(row=3, column=2,pady=10)





        self.Label_Chip_SDRAM_Backup_Address.grid(row=4, column=0, pady=10)
        self.RadioButton_SDRam_Backup_yes.grid(row=4, column=1,pady=10)
        self.RadioButton_SDRam_Backup_no.grid(row=4, column=2,pady=10)


        self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_Flash.grid(row=1,column=0,pady=10)

        self.CheckButton_Enable_Memory_Config_FLASH.grid(row=0,column=0,columnspan=2,pady=10)

        self.Label_Chip_Flash_Type.grid(row=1,column=0,pady=10)
        self.ComboBox_Chip_Flash_Type.grid(row=1,column=1,pady=10)

        #self.Label_Chip_Flash_Driver.grid(row=2,column=0,pady=10)
        #self.ComboBox_Chip_Flash_Driver.grid(row=2,column=1,pady=10)



        #Memory Driver Configuration
        self.mFlashGraphicalComponents()
        self.nandFlashGraphicalComponents()
        self.norFlashGraphicalComponents()
        #Control buttons
        self.Label_Frame_ControlButtonsMCA.grid(row=4,column=0,padx=10,columnspan=3,pady=10)

        self.Button_Previous_MCA.grid(row=0,column=0,padx=10,pady=5)
        self.Button_Look_In_GitHub.grid(row=0,column=1,padx=10,pady=5)
        self.Button_Next_MCA.grid(row=0, column=2,padx=10,pady=5)

        self.hideOrShowMCU()
        #self.showOrHideMemorySettings()

        self.showOrHideMemoryType()
    def _listOfMatchesWithYourMicrocontrollers(self, name='', index='', mode=''):
        userMicro = self.selectedMicrocontroller.get()
        if not userMicro:
            self.Label_TRUE_Number_Supported_Microcontrollers_User_Input.config(text="")
            if self.User_Choice_Card_MCA.get() == 2:
                self.Label_Number_Supported_Microcontrollers_User_Input.config(text="<Choose Your MCU>", foreground="black")
            else:
                self.Label_Number_Supported_Microcontrollers_User_Input.config(text="<Choose Your Board>", foreground="black")
            return
        nbMatchesMicrocontrollers = 0
        matchFound = ""
        for subMicrocontrollers in self.listOfKnownMicrocontrollers:
            if userMicro in subMicrocontrollers:
                nbMatchesMicrocontrollers += 1
                matchFound = subMicrocontrollers
        if (matchFound == userMicro and nbMatchesMicrocontrollers == 1):
            self.Label_Number_Supported_Microcontrollers_User_Input.config(text="Perfect support!", foreground="green")
            if self.User_Choice_Card_MCA.get() == 2:
                self.Label_TRUE_Number_Supported_Microcontrollers_User_Input.config(
                    text="Your Microcontroller was found, congratulation!", foreground="green")
            else:
                self.Label_TRUE_Number_Supported_Microcontrollers_User_Input.config(
                    text="Your Board was found, congratulation!", foreground="green")
        elif (nbMatchesMicrocontrollers >= 1):
            self.Label_Number_Supported_Microcontrollers_User_Input.config(text="Exact match is not found yet!",
                                                                           foreground="orange")
            if self.User_Choice_Card_MCA.get() == 2:
                textToDisplay = "Number of Microcontrollers close to your search : " + str(nbMatchesMicrocontrollers)
            else:
                textToDisplay = "Number of Board close to your search : " + str(nbMatchesMicrocontrollers)
            self.Label_TRUE_Number_Supported_Microcontrollers_User_Input.config(text=textToDisplay, foreground="orange")
        else:
            self.Label_Number_Supported_Microcontrollers_User_Input.config(text="Not supported!", foreground="red")
            if self.User_Choice_Card_MCA.get() == 2:
                self.Label_TRUE_Number_Supported_Microcontrollers_User_Input.config(
                    text="Number of Microcontrollers matching your search : 0", foreground="red")
            else:
                self.Label_TRUE_Number_Supported_Microcontrollers_User_Input.config(
                    text="Number of Board matching your search : 0", foreground="red")



    def SmileDefineWidgetsAdapterSupport(self):

        self.TitleWindowLabel_Adapter = ttk.Label(master=self.SMILE_Tab_AdapterSUPPORT, text="OESdebug",
                                          font=(self.MAIN_TITLE_FONT, self.MAIN_TITLE_SIZE))

        self.User_Choice_Adapter_Existance = tk.IntVar()
        self.RadioButton_Adapter_Exists = tk.Radiobutton(master=self.SMILE_Tab_AdapterSUPPORT,
                                                text="Existing adapter", value=1,
                                                variable=self.User_Choice_Adapter_Existance,
                                                command=self.hideOrShowAdapter)

        self.RadioButton_Adapter_Does_Not_Exists = tk.Radiobutton(master=self.SMILE_Tab_AdapterSUPPORT, text="Create a custom adapter",
                                              value=2,
                                              variable=self.User_Choice_Adapter_Existance,
                                              command=self.hideOrShowAdapter)
        self.User_Choice_Adapter_Existance.set(1)



        self.Label_Frame_mainWindowWrapper_Adapter = ttk.LabelFrame(master=self.SMILE_Tab_AdapterSUPPORT,
                                                                text="Check Existing Adapter (Dongle) support")

        self.Label_Supported_Adapters = ttk.Label(master=self.Label_Frame_mainWindowWrapper_Adapter,
                                                  text="Nb of supported adapters by your OPENOCD : ",
                                                  font=(self.LABEL_FONTS, self.LABEL_SIZE))

        if self.Checkbox_Manual_Installation_OpenOCD.get() == 0:
            self.listOfKnown_Interface_Adapter_Dongle = self.readKnownInterfaces("/usr/share/openocd/scripts/interface/")
        else:
            pathInterface = self.Entry_Manual_Path_OpenOCD.get() + "/tcl/interface"
            print(pathInterface)
            self.listOfKnown_Interface_Adapter_Dongle = self.readKnownInterfaces(pathInterface)

        self.Label_Number_Supported_Adapters = ttk.Label(master=self.Label_Frame_mainWindowWrapper_Adapter,
                                                         text=len(self.listOfKnown_Interface_Adapter_Dongle),
                                                         font=(self.LABEL_FONTS, self.LABEL_SIZE))



        self.Label_Frame_Create_Adapter = ttk.LabelFrame(master=self.SMILE_Tab_AdapterSUPPORT,
                                                                    text="Define new adapter")


        self.Label_Microcontroller_Dongle = ttk.Label(master=self.Label_Frame_mainWindowWrapper_Adapter,
                                                      text="Adapter name : ",
                                                      font=(self.LABEL_FONTS, self.LABEL_SIZE))


        self.Label_Manufacturer_Dongle = ttk.Label(master=self.Label_Frame_Create_Adapter,
                                                   text="Manufacturer : ", font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.Label_Protocol_Dongle_Interface = ttk.Label(master=self.Label_Frame_Create_Adapter,
                                                   text="Interface protocol : ", font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.ComboBox_Variable_Protocol_Dongle_Interface = tk.StringVar()
        self.ComboBox_Supported_OpenOcd_Interfaces = self.listSupportedOpenOCDAdapterProtocolInterfaces()
        self.ComboBox_Protocol_Dongle_Interface = ttk.Combobox(master=self.Label_Frame_Create_Adapter,
                                                               values=self.ComboBox_Supported_OpenOcd_Interfaces,
                                                               textvariable=self.ComboBox_Variable_Protocol_Dongle_Interface)

        if len(self.ComboBox_Supported_OpenOcd_Interfaces):
            self.ComboBox_Protocol_Dongle_Interface.current(2)


        self.Label_Vendor_ID_Dongle = ttk.Label(master=self.Label_Frame_Create_Adapter, text="Vendor ID : ",
                                                font=(self.LABEL_FONTS, self.LABEL_SIZE))
        self.Label_Product_ID_Dongle = ttk.Label(master=self.Label_Frame_Create_Adapter, text="Product ID : ",
                                                 font=(self.LABEL_FONTS, self.LABEL_SIZE))

        # User defined Interface adapter Protocol
        self.selectedInterface_Adapter_Dongle = tk.StringVar()
        self.listOfKnown_Interface_Adapter_Dongle = self.readKnownInterfaces("/usr/share/openocd/scripts/interface/")
        self.ComboBox_Microcontroller_ID_Dongle = ttk.Combobox(master=self.Label_Frame_mainWindowWrapper_Adapter,
                                                               values=self.listOfKnown_Interface_Adapter_Dongle,
                                                               textvariable=self.selectedInterface_Adapter_Dongle)
        self.selectedInterface_Adapter_Dongle.trace("w", self._listOfMatchesWithYourInterface)

        self.Entry_Manufacturer_ID_Dongle = ttk.Entry(master=self.Label_Frame_Create_Adapter)

        self.Label_Protocol_Dongle_Interface_Speed = ttk.Label(master=self.Label_Frame_Create_Adapter,
                                                         text="Adapter interface speed : ",
                                                         font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.ComboBox_Variable_Protocol_Dongle_Interface_speed = tk.StringVar()
        self.ComboBox_Protocol_Dongle_Interface_speed = ttk.Combobox(master=self.Label_Frame_Create_Adapter,
                                                               values=["8","9600","115200"],
                                                               textvariable=self.ComboBox_Variable_Protocol_Dongle_Interface_speed)
        self.ComboBox_Protocol_Dongle_Interface_speed.current(0)

        # User defined Target Board Vendor_ID
        self.Entry_Vendor_ID_Dongle = ttk.Entry(master=self.Label_Frame_Create_Adapter)
        # User defined Target Board Product_ID
        self.Entry_Product_ID_Dongle = ttk.Entry(master=self.Label_Frame_Create_Adapter)

        self.Label_Supported_Adapters_User_Input = ttk.Label(master=self.Label_Frame_mainWindowWrapper_Adapter,
                                                             text="Is your Adapter supported : ",
                                                             font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.Label_Number_Supported_Adapters_User_Input = ttk.Label(master=self.Label_Frame_mainWindowWrapper_Adapter,
                                                                    text="<Choose Your Adapter>",
                                                                    font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.Label_TRUE_Number_Supported_Adapters_User_Input = ttk.Label(master=self.Label_Frame_mainWindowWrapper_Adapter,
                                                                         text="",
                                                                         font=(
                                                                             self.LABEL_FONTS, self.LABEL_SIZE))

        self.Button_ADD_MicroController_Product = ttk.Button(master=self.Label_Frame_Create_Adapter,
                                                             text="Find my Adapter pid,vid and manufacturer",
                                                             command=lambda: self.listUsbDevices("mcu"))

        self.Label_Frame_ControlButtonsAdapter = ttk.LabelFrame(master=self.SMILE_Tab_AdapterSUPPORT,
                                                            text="Control Buttons")

        self.Button_Previous_Adapter = ttk.Button(master=self.Label_Frame_ControlButtonsAdapter,
                                              text="Previous", command=self.GoToOpenOCDSupport)

        self.Button_Look_In_GitHub_Adapter = ttk.Button(master=self.Label_Frame_ControlButtonsAdapter,
                                                text="Test Your Adapter with OpenOCD",command=self.listSupportedOpenOCDAdapterProtocolInterfaces)

        self.Button_Next_Adapter = ttk.Button(master=self.Label_Frame_ControlButtonsAdapter,
                                          text="Next", command=self.GoToMCASupport)



    def SmilePlaceWidgetsAdapterSupport(self):
        self.TitleWindowLabel_Adapter.grid(row=0, column=0,pady=5,columnspan=2)

        self.RadioButton_Adapter_Exists.grid(row=1, column=0,pady=5)

        self.RadioButton_Adapter_Does_Not_Exists.grid(row=1, column=1,pady=5)

        self.Label_Frame_mainWindowWrapper_Adapter.grid(row=2, column=0,pady=5)
        self.Label_Supported_Adapters.grid(row=0,column=0,pady=5)
        self.Label_Number_Supported_Adapters.grid(row=0,column=1,pady=5)

        self.Label_Microcontroller_Dongle.grid(row=1, column=0, pady=5)
        self.ComboBox_Microcontroller_ID_Dongle.grid(row=1, column=1, pady=5)



       #Basic information required to create a dongle
        self.Label_Frame_Create_Adapter.grid(row=3, column=0, pady=5, padx=10)
        self.Label_Manufacturer_Dongle.grid(row=0,column=0,padx=10,pady=5)
        self.Entry_Manufacturer_ID_Dongle.grid(row=0,column=1,padx=10,pady=5)

        self.Label_Protocol_Dongle_Interface.grid(row=1,column=0,padx=10,pady=5)
        self.ComboBox_Protocol_Dongle_Interface.grid(row=1,column=1,padx=10,pady=5)

        self.Label_Vendor_ID_Dongle.grid(row=2,column=0,padx=10,pady=5)
        self.Entry_Vendor_ID_Dongle.grid(row=2,column=1,padx=10,pady=5)

        self.Label_Product_ID_Dongle.grid(row=3,column=0,padx=10,pady=5)
        self.Entry_Product_ID_Dongle.grid(row=3,column=1,padx=10,pady=5)


        self.Label_Protocol_Dongle_Interface_Speed.grid(row=5, column=0,padx=10,pady=5)
        self.ComboBox_Protocol_Dongle_Interface_speed.grid(row=5, column=1,padx=10,pady=5)

        self.Button_ADD_MicroController_Product.grid(row=8, column=0, padx=10, pady=5, columnspan=2)


        self.Label_Supported_Adapters_User_Input.grid(row=2,column=0,pady=5)
        self.Label_Number_Supported_Adapters_User_Input.grid(row=2,column=1,pady=5)
        self.Label_TRUE_Number_Supported_Adapters_User_Input.grid(row=7,column=0,columnspan=2,pady=5)

        # Adapter Tab Buttons
        self.Label_Frame_ControlButtonsAdapter.grid(row=4,column=0,padx=10,pady=5,columnspan=2)

        self.Button_Previous_Adapter.grid(row=0,column=0,padx=10,pady=5)
        self.Button_Look_In_GitHub_Adapter.grid(row=0,column=1,padx=10,pady=5)

        self.Button_Next_Adapter.grid(row=0,column=2,padx=10,pady=5)

        self.hideOrShowAdapter()



    def _listOfMatchesWithYourInterface(self, name='', index='', mode=''):
        userInterface = self.selectedInterface_Adapter_Dongle.get()
        if not userInterface:
            self.Label_TRUE_Number_Supported_Adapters_User_Input.config(text="")
            self.Label_Number_Supported_Adapters_User_Input.config(text="<Choose Your Adapter>", foreground="black")
            return

        nbMatchesInterface = 0
        matchFound = ""

        for subInterfaces in self.listOfKnown_Interface_Adapter_Dongle:
            if userInterface in subInterfaces:
                nbMatchesInterface += 1
                matchFound = subInterfaces
        if (matchFound == userInterface and nbMatchesInterface == 1):
            self.Label_Number_Supported_Adapters_User_Input.config(text="Perfect support!", foreground="green")
            self.Label_TRUE_Number_Supported_Adapters_User_Input.config(
                text="Your Adapter is fully supported, congratulation!", foreground="green")
            path = "/usr/share/openocd/scripts/interface/" + userInterface + ".cfg"
            #self.getVidPid(path)


        elif (nbMatchesInterface >= 1):
            self.Label_Number_Supported_Adapters_User_Input.config(text="Exact match is not found yet!",
                                                                   foreground="orange")
            textToDisplay = "Number of Adapters close to your search : " + str(nbMatchesInterface)
            self.Label_TRUE_Number_Supported_Adapters_User_Input.config(text=textToDisplay, foreground="orange")
        else:
            self.Label_Number_Supported_Adapters_User_Input.config(text="Not supported!",
                                                                   foreground="red")
            self.Label_TRUE_Number_Supported_Adapters_User_Input.config(
                text="Number of Adapters matching your search : 0", foreground="red")

    def GoToOpenOCDSupport(self):
        self.tabControl.select(self.SMILE_Tab_OPENOCDSUPPORT)

    def GoToAdapterSupport(self):
        self.tabControl.select(self.SMILE_Tab_AdapterSUPPORT)

    def GoToMCASupport(self):
        self.tabControl.select(self.SMILE_Tab_MicroControllerSUPPORT)

    def GoToFileCOnfigTab(self):
        self.tabControl.select(self.SMILE_Tab_ConfigFileGeneration)

    def downloadOpenOCD(self):
        if self.valueOfUpdateCheckBox.get() == 1:
            os.system("gnome-terminal -e 'bash -c \"sudo apt-get update; sudo apt-get install openocd\"'")
        else:
            os.system("gnome-terminal -e 'bash -c \"sudo apt-get install openocd\"'")


    def hideOrShowAdapter(self):
        if(self.User_Choice_Adapter_Existance.get()==2):
            self.Label_Frame_mainWindowWrapper_Adapter.grid_forget()

            self.Label_Frame_Create_Adapter.grid(row=3, column=0, pady=5, padx=10,columnspan=2)
        else:

            self.Label_Frame_mainWindowWrapper_Adapter.grid(row=2, column=0,pady=5,columnspan=2)

            self.Label_Frame_Create_Adapter.grid_forget()

    def hideOrShowMCU(self):
        if (self.User_Choice_MCU_Existance.get() == 2):
            self.Label_Frame_mainWindowWrapper_MCA.grid_forget()

            self.Label_Frame_mainWindowWrapper_NEW_SOC.grid(row=3, column=0, columnspan=3, pady=10)
            self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings.grid(row=3, column=5,columnspan=2,pady=10)

            self.showOrHideMemorySettings()
        else:

            self.Label_Frame_mainWindowWrapper_MCA.grid(row=2, column=0, columnspan=3, pady=10)

            self.Label_Frame_mainWindowWrapper_NEW_SOC.grid_forget()
            self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings.grid_forget()

    def showOrHideMemorySettings(self):
        if self.Configure_Memory.get() == 1:
            self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings.grid(row=3, column=5, columnspan=2, pady=10)
        else:
            self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings.grid_forget()


    def showOrHideSaveDirectory(self):
        if self.Configure_Memory.get() == 1:
            self.LabelFrame_Manual_Save_config.grid(row=3, column=0, padx=10, pady=5, columnspan=4)
        else:
            self.LabelFrame_Manual_Save_config.grid_forget()


    def listSupportedOpenOCDAdapterProtocolInterfaces(self):
        counter=0
        listOfProtocols = []
        try:

            #commandList = 'openocd -c "interface_list" > listAdapters.txt'
            cmd = ['openocd', '-c "interface_list"']
            p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()

            for i in (stderr.decode().split("\n")):
                counter+=1
                if(counter>5):
                    if(i.split(" ")[1]=="Debug"):
                        break
                    print(i.split(" ")[1])
                    listOfProtocols.append(i.split(" ")[1])
        except Exception as e:
            print(e)
        finally:
            return listOfProtocols

    def listSupportedOpenOCDMCUFamily(self):
        counter = 0
        listOfMCUsOpenOCD = []
        try:

            # commandList = 'openocd -c "interface_list" > listAdapters.txt'
            cmd = ['openocd', '-c', r'target types']
            p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            for i in (stderr.decode().split("\n")):
                counter += 1
                if (counter == 5):
                    # if (i.split(" ") == "Error"):
                    #     break
                    for realEntry in i.split(" "):
                        print(realEntry)
                        listOfMCUsOpenOCD.append(realEntry)
            listOfMCUsOpenOCD.sort()
        except Exception as e:
            print(e)
        finally:
            return listOfMCUsOpenOCD


    def getOpenOCDVersion(self):
        version = ""
        try:
            cmd = ['openocd']
            p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()

            version = stderr.decode().split("\n")[0]
        except Exception as e:
            print(e)
        finally:
            return version


    def listUsbDevices(self, buttonInvocation):
        self.windowUSB = tk.Toplevel(self.SmileMainWindow)
        style = ttk.Style(self.windowUSB)
        style.configure('Calendar.Treeview', rowheight=40)
        self.tree = ttk.Treeview(master=self.windowUSB, style='Calendar.Treeview')

        self.tree['columns'] = ('Bus ID', 'nb of devices os the bus', 'vid_pid', 'Manufacturer')
        self.tree.column('Bus ID', anchor='center')
        self.tree.heading("Bus ID", text="Bus ID")

        self.tree.column('nb of devices os the bus', anchor='center')

        self.tree.heading("nb of devices os the bus", text="nb of devices os the bus")

        self.tree.column('vid_pid', anchor='center')
        self.tree.heading("vid_pid", text="vid_pid")

        self.tree.column('Manufacturer', anchor='center')
        self.tree.heading("Manufacturer", text="Manufacturer")
        #if (buttonInvocation == "mcu"):
        #self.tree.bind('<ButtonRelease-1>', self.selectItem)
        #else:
        self.tree.bind('<ButtonRelease-1>', self.selectItemAdapter)
        # import re
        import subprocess
        counter = 0
        # device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.check_output("lsusb")
        # devices = []
        for i in df.splitlines():
            counter += 1
            if i:
                splittedUsb = str(i).split(" ")
                myValues = []
                tmp = ""
                mycount = 0
                for x in splittedUsb:
                    if (mycount == 1):
                        myValues.append(splittedUsb[1])
                    elif (mycount == 3):
                        myValues.append(splittedUsb[3].strip(":"))
                    elif (mycount == 5):
                        myValues.append(splittedUsb[5])
                    elif (mycount > 5):
                        if (mycount == 9):
                            tmp += splittedUsb[mycount] + "\n"
                        else:
                            tmp += splittedUsb[mycount] + " "
                    mycount += 1
                myValues.append(tmp)
                self.tree.insert('', 'end', text="Device " + str(counter), values=myValues)
                print(i)
        self.tree.pack()
        self.tree.grid(row=0, column=0)
        self.windowUSB.mainloop()




    def aboutDev(self):
        self.windowDev = tk.Toplevel(self.SmileMainWindow)

        self.Label_Title_OESDebug = ttk.Label(master=self.windowDev,
                                           text="OESdebug",
                                           font=(self.MAIN_TITLE_FONT, self.MAIN_TITLE_SIZE))

        self.pic = tk.PhotoImage(file='img/smile.png')

        self.devPic = tk.Label(master=self.windowDev, image=self.pic)
        self.devPic.photo = self.pic

        self.Label_Developpers = ttk.Label(master=self.windowDev,
                                                               text="Developped by : SMILE",
                                                               font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.Label_Title_OESDebug.grid(row=0,column=0)


        self.devPic.grid(row=5,column=0)
        self.Label_Developpers.grid(row=10,column=0)
        self.windowDev.mainloop()


    def checkAgainOPENOCDSupport(self):
        if self.detectOpenOCD(self.PATH_TO_OPENOCD):
            self.pic = tk.PhotoImage(file='img/validate_icon.gif')
            myText = self.getOpenOCDVersion() + " detected"
            self.detectingOpenOCD.configure(text=myText,foreground="green")
            self.can.configure(image=self.pic)

            self.getNumberOfKnownAdapters()
            self.parseFolderToGetKnownMCA("/usr/share/openocd/scripts/board/")
        else:
            self.detectingOpenOCD.configure(text="OPENOCD was not detected",
                                            font=(self.LABEL_FONTS, self.LABEL_SIZE), foreground="red")
            self.pic = tk.PhotoImage(file='img/no-x.gif')
            self.can.configure(image=self.pic)

    def selectItemAdapter(self, a):
        curItem = self.tree.focus()
        self.Entry_Manufacturer_ID_Dongle.delete(0, tk.END)
        self.Entry_Vendor_ID_Dongle.delete(0, tk.END)
        self.Entry_Product_ID_Dongle.delete(0, tk.END)

        self.Entry_Manufacturer_ID_Dongle.insert(0, str(self.tree.item(curItem)['values'][3]).replace("\n", " "))
        self.Entry_Vendor_ID_Dongle.insert(0, "0x" + self.tree.item(curItem)['values'][2].split(":")[0])
        self.Entry_Product_ID_Dongle.insert(0, "0x" + self.tree.item(curItem)['values'][2].split(":")[1])

        self.windowUSB.quit()
        self.windowUSB.destroy()

    def SmileDefineWidgetsConfigSupport(self):
        self.Label_Frame_mainWindowWrapper_Config = ttk.LabelFrame(master=self.SMILE_Tab_ConfigFileGeneration,
                                                                    text="OPENOCD Configuration file")

        # ---------------------------------------------- Define Scroll Text ------------------------------------------
        # ------------------------------------------------------------------------------------------------------------

        self.ScrolledText_Adapter_Config = ScrolledText(master=self.Label_Frame_mainWindowWrapper_Config, width=90, height=20)

        self.Label_Frame_mainWindowWrapper_Config_Buttons = ttk.LabelFrame(master=self.SMILE_Tab_ConfigFileGeneration,
                                                                   text="Control buttons")

        self.Button_Go_Back_To_Adapter_Settings = ttk.Button(master=self.Label_Frame_mainWindowWrapper_Config_Buttons,
                                               text="Previous",
                                               command=self.GoToMCASupport)

        self.Button_Generate_File = ttk.Button(master=self.Label_Frame_mainWindowWrapper_Config_Buttons, text="Generate File",
                                             command=self.generateConfigFile)

        self.Label_Log_Level = ttk.Label(master=self.Label_Frame_mainWindowWrapper_Config_Buttons,
                  text="Log Level : ",
                  font=(self.LABEL_FONTS, self.LABEL_SIZE))



        self.ComboBox_Variable_Log_Level = tk.StringVar()
        self.ComboBox_Log_Level = ttk.Combobox(master=self.Label_Frame_mainWindowWrapper_Config_Buttons,
                                                                     values=["0", "1", "2","3"],
                                                                     textvariable=self.ComboBox_Variable_Log_Level)
        self.ComboBox_Variable_Log_Level.set(0)



        self.Button_Update_File = ttk.Button(master=self.Label_Frame_mainWindowWrapper_Config_Buttons, text="Update file",
                                             command=self.updateFileContent)
        self.Button_Launch_OpenOCD = ttk.Button(master=self.Label_Frame_mainWindowWrapper_Config_Buttons,
                                             text="Start OpenOCD",
                                             command=self.launchOPENOCDAndDebug)

        self.save_config_file = tk.IntVar()

        self.CheckButton_Save_Config_File = ttk.Checkbutton(master=self.Label_Frame_mainWindowWrapper_Config_Buttons,
                                                                text="Save Config File",
                                                                variable=self.save_config_file,
                                                                onvalue=1, offvalue=0,
                                                                command=self.showOrHideSaveDirectory)
        self.save_config_file.set(0)

        self.LabelFrame_Manual_Save_config = ttk.LabelFrame(master=self.Label_Frame_mainWindowWrapper_Config_Buttons,
                                                                     text="Save configuration file")
        self.Label_Manual_Path_Save_Config = ttk.Label(master=self.LabelFrame_Manual_Save_config,
                                                   text="Directory path : ")

        self.Entry_Manual_Path_OpenOCD_Config = ttk.Entry(master=self.LabelFrame_Manual_Save_config)
        self.Entry_Manual_Path_OpenOCD_Config.delete(0, tk.END)
        self.Entry_Manual_Path_OpenOCD_Config.insert(0, "savedConfig/")

        self.Label_Config_File_Name = ttk.Label(master=self.LabelFrame_Manual_Save_config,
                                                       text="Filename : ")

        self.Entry_Config_FileName = ttk.Entry(master=self.LabelFrame_Manual_Save_config)



        self.Button_Manual_Path_OpenOCD_Save_Config_OpenOCD = tk.Button(master=self.LabelFrame_Manual_Save_config,
                                                    text="Browse", command=self.locateSaveConfigFolder)
        self.Label_Manual_Path_Save_Config_Info = ttk.Label(master=self.LabelFrame_Manual_Save_config,
                                                         text="default saving directory managed by OESdebug",
                                                         foreground="green")

        self.Button_Manual_Path_OpenOCD_Save_Config_OpenOCD_Write_Files = tk.Button(master=self.LabelFrame_Manual_Save_config,
                                                                       text="Save file", command=self.saveConfigurationFilesToDirectory)

    def showOrHideSaveDirectory(self):
        if self.save_config_file.get() == 1:
            self.LabelFrame_Manual_Save_config.grid(row=3, column=0, padx=10, pady=5, columnspan=4)
        else:
            self.LabelFrame_Manual_Save_config.grid_forget()


    def saveConfigurationFilesToDirectory(self):

        try:
            # save configuration file for openocd
            path = self.Entry_Manual_Path_OpenOCD_Config.get() + self.Entry_Config_FileName.get() + ".cfg"
            pathOESdebug = self.Entry_Manual_Path_OpenOCD_Config.get() + self.Entry_Config_FileName.get() + ".oes"


            fd = open(path, "w+")
            payload = self.ScrolledText_Adapter_Config.get(1.0, tk.END)
            fd.write(payload)
            fd.close()

            # save configuration file for OESdebug
            textPayload = ""
            fd_oes = open(pathOESdebug, "w+")

            if (self.User_Choice_Adapter_Existance.get() == 1):
                textPayload = "#Adapter_Found,"
                textPayload += self.ComboBox_Microcontroller_ID_Dongle.get() + "\n"
            else:
                textPayload = "#Adapter_New,"
                textPayload += self.ComboBox_Protocol_Dongle_Interface.get() + ","
                textPayload += self.Entry_Manufacturer_ID_Dongle.get() + ","

                textPayload += self.Entry_Vendor_ID_Dongle.get() + "," + self.Entry_Product_ID_Dongle.get() + ","
                textPayload += self.ComboBox_Protocol_Dongle_Interface_speed.get() + "\n"



            if self.User_Choice_MCU_Existance.get() == 1:
                if self.User_Choice_Card_MCA.get() == 2:
                    textPayload += "#MCU_Found,"
                    textPayload += self.ComboBox_Microcontroller_ID.get() + "\n"
                else:
                    textPayload += "#BOARD_Found,"
                    textPayload += self.ComboBox_Microcontroller_ID.get() + "\n"

            else:
                textPayload += "#CHIP_Not_Found,"
                textPayload += self.Entry_Chip_Name.get() + "," # define chip name
                textPayload += self.ComboBox_Chip_Type.get() + ","
                textPayload += self.ComboBox_Chip_Family.get() + ","

                textPayload += self.ComboBox_Chip_IR_Length.get() + ","

                textPayload += self.ComboBox_Chip_Endianness.get().split(" ")[0] + ","
                textPayload += self.Entry_Chip_Tap_ID.get() + "\n"

            if self.Configure_Memory_SDRAM.get() == 1:
                textPayload += "#Memory_Config,"
                textPayload += self.Entry_Chip_SDRAM_Start_Address.get() + "," + self.Entry_Chip_SDRAM_Size_Address.get() + ","
                if self.Type_SDRam_variable.get() == 1:
                    textPayload += "physical,"
                else:
                    textPayload += "virtual,"

                if self.Backup_SDRam_variable.get() == 2:
                    textPayload += "0"
                else:
                    textPayload += "1"
                textPayload += "\n"
            if self.Configure_Memory_FLASH.get() == 1:
                textPayload += "#Flash_Memory_Config,"
                if self.ComboBox_Chip_Flash_Type.get() == "Nor":
                    textPayload += "Nor,"
                    textPayload += str(self.selected_Flash_Driver_Name_Variable.get()) + ","
                    textPayload += self.ScrolledText_Nor_Flash_Command_Field.get(1.0, tk.END).strip() + ","

                    textPayload += str(self.Nor_Flash_variable.get()) + "\n"

                elif self.ComboBox_Chip_Flash_Type.get() == "Nand":
                    textPayload += "Nand,"
                    textPayload += str(self.selected_Nand_Flash_variable.get()) + ","
                    textPayload += self.ScrolledText_Nand_Flash_Command_Field.get(1.0, tk.END).strip() + "\n"

                elif self.ComboBox_Chip_Flash_Type.get() == "mFlash":
                    textPayload += "mFlash,"
                    textPayload += str(self.selected_mFlash_variable.get()) + ","
                    textPayload += self.ScrolledText_mFlash_Command_Field.get(1.0, tk.END).strip() + "\n"


            fd_oes.write(textPayload)
            fd_oes.close()

        except Exception as e:
            print(e)



    def SmilePlaceWidgetsConfigSupport(self):
        self.Label_Frame_mainWindowWrapper_Config.grid(row=0,column=0)
        self.ScrolledText_Adapter_Config.grid(row=0,column=0)
        self.Label_Frame_mainWindowWrapper_Config_Buttons.grid(row=1, column=0)

        self.Button_Go_Back_To_Adapter_Settings.grid(row=1, column=0,padx=10,pady=5)
        self.Button_Generate_File.grid(row=1, column=1,padx=10,pady=5)
        self.Button_Update_File.grid(row=1, column=2,padx=10,pady=5)

        self.Label_Log_Level.grid(row=2, column=0,padx=10,pady=5)
        self.ComboBox_Log_Level.grid(row=2, column=1,padx=10,pady=5)
        self.Button_Launch_OpenOCD.grid(row=2, column=2,padx=10,pady=5,columnspan=2)

        self.CheckButton_Save_Config_File.grid(row=3, column=0,padx=10,pady=5,columnspan=4)

        self.LabelFrame_Manual_Save_config.grid(row=4, column=0,padx=10,pady=5,columnspan=4)
        self.Label_Manual_Path_Save_Config.grid(row=0, column=0,padx=10,pady=5)
        self.Entry_Manual_Path_OpenOCD_Config.grid(row=0, column=1,padx=10,pady=5)

        self.Button_Manual_Path_OpenOCD_Save_Config_OpenOCD.grid(row=0, column=2,padx=10,pady=5)



        self.Label_Config_File_Name.grid(row=3, column=0, padx=10, pady=5)
        self.Entry_Config_FileName.grid(row=3, column=1, padx=10, pady=5, columnspan=2)

        self.Label_Manual_Path_Save_Config_Info.grid(row=4, column=0, padx=10, pady=5, columnspan=3)
        self.Button_Manual_Path_OpenOCD_Save_Config_OpenOCD_Write_Files.grid(row=5, column=0, padx=10, pady=5, columnspan=3)
        self.showOrHideOpenOCDManualInstall()

        self.showOrHideSaveDirectory()

    def mFlashGraphicalComponents(self):
        self.Label_Frame_mFlash_Wrapper = ttk.LabelFrame(master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_Flash,
                                                                   text="mFlash Configuration")


        self.Label_MFlash_Driver = ttk.Label(master=self.Label_Frame_mFlash_Wrapper, text="mFlash Driver : ",
                                                font=(self.LABEL_FONTS, self.LABEL_SIZE))
        self.selected_mFlash_variable = tk.StringVar()
        self.ComboBox_mFlash_Driver = ttk.Combobox(master=self.Label_Frame_mFlash_Wrapper,
                                                               textvariable=self.selected_mFlash_variable)
        self.selected_mFlash_variable.set("Select From List")
        self.selected_mFlash_variable.trace('w', self.setmFlashCommand)

        self.Label_mFlash_Command = ttk.Label(master=self.Label_Frame_mFlash_Wrapper,
                                                  text="Command mFlash OpenOCD : ",
                                                  font=(self.LABEL_FONTS, self.LABEL_SIZE))
        self.ScrolledText_mFlash_Command_Field = ScrolledText(master=self.Label_Frame_mFlash_Wrapper, width=45,
                                                                  height=5)

        self.Label_Frame_mFlash_Wrapper.grid(row=2,column=0,padx=10,pady=10,columnspan=2)
        self.Label_MFlash_Driver.grid(row=0,column=0,padx=10,pady=10)
        self.ComboBox_mFlash_Driver.grid(row=0,column=1,padx=10,pady=10)
        self.Label_mFlash_Command.grid(row=1,column=0,padx=10,pady=10,columnspan=2)
        self.ScrolledText_mFlash_Command_Field.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        self.listOfMFlashDrivers, self.commandOfListmFlashDrivers = self.discovermFlashDriverNamesAndCommands()
        self.ComboBox_mFlash_Driver['values'] = self.listOfMFlashDrivers

    def discovermFlashDriverNamesAndCommands(self):
        path = "config/list-mflash-drivers.txt"
        listOfMFlashDrivers = []
        commandOfListmFlashDrivers = []
        if (os.path.exists(path)):
            with open(path) as f:
                for line in f:
                    print(line)
                    listOfMFlashDrivers.append(line.strip().split(";")[0])
                    commandOfListmFlashDrivers.append(line.strip().split(";")[1])
        return listOfMFlashDrivers, commandOfListmFlashDrivers

    def setmFlashCommand(self, name='', index='', mode=''):
        positionOfCommand = self.listOfMFlashDrivers.index(self.ComboBox_mFlash_Driver.get())
        self.ScrolledText_mFlash_Command_Field.delete('1.0', tk.END)
        self.ScrolledText_mFlash_Command_Field.insert(tk.INSERT, self.commandOfListmFlashDrivers[positionOfCommand])

    def nandFlashGraphicalComponents(self):
        self.Label_Frame_Nand_Flash_Wrapper = ttk.LabelFrame(master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_Flash,
            text="Nand Configuration")

        self.Label_Nand_Flash_Driver = ttk.Label(master=self.Label_Frame_Nand_Flash_Wrapper, text="Nand Flash Driver : ",
                                             font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.selected_Nand_Flash_variable = tk.StringVar()
        self.ComboBox_Nand_Flash_values, self.nandFlashCommandNames = self.getNandDriverListNames("config/list-nand-drivers.txt")
        self.ComboBox_Nand_Flash_Driver = ttk.Combobox(master=self.Label_Frame_Nand_Flash_Wrapper,
                                                               values=self.ComboBox_Nand_Flash_values,
                                                               textvariable=self.selected_Nand_Flash_variable)
        self.selected_Nand_Flash_variable.set("Select From List")
        self.selected_Nand_Flash_variable.trace('w', self.setFlashCommand)

#        self.ComboBox_Nand_Flash_Driver.current(0)

        self.Label_Nand_Flash_Command = ttk.Label(master=self.Label_Frame_Nand_Flash_Wrapper,
                                                 text="Command Nand Flash OpenOCD : ",
                                                 font=(self.LABEL_FONTS, self.LABEL_SIZE))
        self.ScrolledText_Nand_Flash_Command_Field = ScrolledText(master=self.Label_Frame_Nand_Flash_Wrapper, width=45,
                                                        height=5)

        self.Label_Frame_Nand_Flash_Wrapper.grid(row=3,column=0,padx=10,pady=10,columnspan=2)
        self.Label_Nand_Flash_Driver.grid(row=0, column=0, padx=10, pady=10)
        self.ComboBox_Nand_Flash_Driver.grid(row=0, column=1, padx=10, pady=10)
        self.Label_Nand_Flash_Command.grid(row=1, column=0, padx=10, pady=10,columnspan=2)
        self.ScrolledText_Nand_Flash_Command_Field.grid(row=2, column=0, padx=10, pady=10,columnspan=2)

    def setFlashCommand(self, name='', index='', mode=''):
        positionOfCommand = self.ComboBox_Nand_Flash_values.index(self.ComboBox_Nand_Flash_Driver.get())
        self.ScrolledText_Nand_Flash_Command_Field.delete('1.0', tk.END)
        self.ScrolledText_Nand_Flash_Command_Field.insert(tk.INSERT, self.nandFlashCommandNames[positionOfCommand])

    def norFlashGraphicalComponents(self):
        self.Label_Frame_Nor_Flash_Wrapper = ttk.LabelFrame(master=self.Label_Frame_mainWindowWrapper_MCA_Memory_Settings_Flash,
            text="Nor Configuration")

        self.Label_Nor_Flash_Driver = ttk.Label(master=self.Label_Frame_Nor_Flash_Wrapper,
                                                 text="Nor Flash Driver : ",
                                                 font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.Nor_Flash_variable = tk.IntVar()
        self.RadioButton_Nor_Driver_Internal = tk.Radiobutton(
            master=self.Label_Frame_Nor_Flash_Wrapper,
            text="internal", value=1,
            variable=self.Nor_Flash_variable,command=self.getNorDriverListNames)

        self.RadioButton_Nor_Driver_External = tk.Radiobutton(
            master=self.Label_Frame_Nor_Flash_Wrapper, text="external",
            value=2,
            variable=self.Nor_Flash_variable,command=self.getNorDriverListNames)
        self.Nor_Flash_variable.set(1)

        self.Label_Nor_Flash_Driver_Name = ttk.Label(master=self.Label_Frame_Nor_Flash_Wrapper,
                                                text="Nor Flash Driver Name : ",
                                                font=(self.LABEL_FONTS, self.LABEL_SIZE))

        self.selected_Flash_Driver_Name_Variable = tk.StringVar()
        self.ComboBox_Flash_Driver_Name = ttk.Combobox(master=self.Label_Frame_Nor_Flash_Wrapper,
                                                   textvariable=self.selected_Flash_Driver_Name_Variable)
        self.selected_Flash_Driver_Name_Variable.set("Select From List")
        self.selected_Flash_Driver_Name_Variable.trace('w', self.setNorFlashCommand)

        self.Label_Nor_Flash_Command = ttk.Label(master=self.Label_Frame_Nor_Flash_Wrapper,
                                                  text="Command Nor Flash OpenOCD : ",
                                                  font=(self.LABEL_FONTS, self.LABEL_SIZE))
        self.ScrolledText_Nor_Flash_Command_Field = ScrolledText(master=self.Label_Frame_Nor_Flash_Wrapper, width=45,
                                                                  height=5)

        self.Label_Frame_Nor_Flash_Wrapper.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        self.Label_Nor_Flash_Driver.grid(row=0, column=0, padx=10, pady=10)
        self.RadioButton_Nor_Driver_Internal.grid(row=0, column=1, padx=10, pady=10)
        self.RadioButton_Nor_Driver_External.grid(row=0, column=2, padx=10, pady=10)
        self.Label_Nor_Flash_Driver_Name.grid(row=1, column=0, padx=10, pady=10)
        self.ComboBox_Flash_Driver_Name.grid(row=1, column=1, padx=10, pady=10,columnspan=2)
        self.Label_Nor_Flash_Command.grid(row=2, column=0, padx=10, pady=10,columnspan=3)
        self.ScrolledText_Nor_Flash_Command_Field.grid(row=3, column=0, padx=10, pady=10,columnspan=3)

        self.listOfNorDriversList, self.norCommandsList = self.getNorDriverListNames()



    def showOrHideMemoryType(self, name='', index='', mode=''):
        if self.ComboBox_Chip_Flash_Type.get()=="Nor":
            self.Label_Frame_Nor_Flash_Wrapper.grid(row=4, column=0, padx=10, pady=10, columnspan=2)
            self.Label_Frame_Nand_Flash_Wrapper.grid_forget()
            self.Label_Frame_mFlash_Wrapper.grid_forget()

        elif self.ComboBox_Chip_Flash_Type.get()=="Nand":
            self.Label_Frame_Nand_Flash_Wrapper.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
            self.Label_Frame_Nor_Flash_Wrapper.grid_forget()
            self.Label_Frame_mFlash_Wrapper.grid_forget()

        elif self.ComboBox_Chip_Flash_Type.get() == "mFlash":
            self.Label_Frame_mFlash_Wrapper.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
            self.Label_Frame_Nor_Flash_Wrapper.grid_forget()
            self.Label_Frame_Nand_Flash_Wrapper.grid_forget()

    def showOrHideOpenOCDManualInstall(self):
        if self.Checkbox_Manual_Installation_OpenOCD.get()==0:
            self.LabelFrame_Manual_Installation_OpenOCD.grid_forget()

        else:
            self.LabelFrame_Manual_Installation_OpenOCD.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

        self.getNumberOfKnownAdapters()
        self.parseFolderToGetKnownMCA("/usr/share/openocd/scripts/board/")

    def getNumberOfKnownAdapters(self):
        if self.Checkbox_Manual_Installation_OpenOCD.get() == 0:
            self.listOfKnown_Interface_Adapter_Dongle = self.readKnownInterfaces("/usr/share/openocd/scripts/interface/")
        else:
            pathInterface = self.Entry_Manual_Path_OpenOCD.get() + "/tcl/interface"
            print(pathInterface)
            self.listOfKnown_Interface_Adapter_Dongle = self.readKnownInterfaces(pathInterface)

        self.Label_Number_Supported_Adapters.config(text=len(self.listOfKnown_Interface_Adapter_Dongle))
        self.ComboBox_Microcontroller_ID_Dongle['values']=self.listOfKnown_Interface_Adapter_Dongle


    def setNorFlashCommand(self, name='', index='', mode=''):
        positionOfCommand = self.listOfNorDriversList.index(self.ComboBox_Flash_Driver_Name.get())
        self.ScrolledText_Nor_Flash_Command_Field.delete('1.0', tk.END)
        self.ScrolledText_Nor_Flash_Command_Field.insert(tk.INSERT, self.norCommandsList[positionOfCommand])



    def getmFlashDriverListNames(self,path):
        listOfMFlashDrivers = []
        commandOfMFlashDrivers = []
        if (os.path.exists(path)):
            with open(path) as f:
                for line in f:
                    print(line)
                    listOfMFlashDrivers.append(line.strip().split(";")[0])
                    commandOfMFlashDrivers.append(line.strip().split(";")[1])
            return listOfMFlashDrivers,commandOfMFlashDrivers
        else:
            return [],[]


    def getNandDriverListNames(self,path):
        listOfNandDrivers = []
        commandOfListDrivers = []
        if (os.path.exists(path)):
            with open(path) as f:
                for line in f:
                    print(line)
                    listOfNandDrivers.append(line.strip().split(";")[0])
                    commandOfListDrivers.append(line.strip().split(";")[1])
            return listOfNandDrivers,commandOfListDrivers
        else:
            return [],[]


    def getNorDriverListNames(self):
        listOfNorDrivers = []
        commandOfListDrivers = []
        path=""
        if self.Nor_Flash_variable.get()==1:
            path = "config/list-nor-internal-drivers.txt"
        else:
            path = "config/list-nor-external-drivers.txt"

        if (os.path.exists(path)):
            with open(path) as f:
                for line in f:
                    print(line)
                    listOfNorDrivers.append(line.strip().split(";")[0])
                    commandOfListDrivers.append(line.strip().split(";")[1])

        self.ComboBox_Flash_Driver_Name['values'] = listOfNorDrivers
       # if len(listOfNorDrivers) > 0:
        #    self.ComboBox_Flash_Driver_Name.current(0)
        self.listOfNorDriversList = listOfNorDrivers
        self.norCommandsList = commandOfListDrivers
        return listOfNorDrivers, commandOfListDrivers

    def generateConfigFile(self):
        textPayload = "# -----------------------------------------------\n"
        textPayload += "# -------- Auto generated file by OESdebug ------\n"
        textPayload += "# -----------------------------------------------\n\n"
        textPayload += "# ------------- Adapter speed settings ------------\n"
        textPayload += "adapter_khz " + self.ComboBox_Protocol_Dongle_Interface_speed.get() + "\n\n"

        textPayload += "# ------------- Define the interface ------------ \n"
        if (self.User_Choice_Adapter_Existance.get()==1):
            textPayload += "source [find interface/" + self.ComboBox_Microcontroller_ID_Dongle.get() + ".cfg]\n\n"
        else:
            textPayload += "interface " + self.ComboBox_Protocol_Dongle_Interface.get() + "\n"
            textPayload += self.ComboBox_Protocol_Dongle_Interface.get() + "_device_desc " + "\"" + self.Entry_Manufacturer_ID_Dongle.get() + "\"\n"
            textPayload += "# ------------ Define the VID and PID ----------- \n"

            textPayload += str(self.ComboBox_Protocol_Dongle_Interface.get()).replace("-",
                "_") + "_vid_pid " + self.Entry_Vendor_ID_Dongle.get() + " " + self.Entry_Product_ID_Dongle.get() + "\n"
        #textPayload += "# ------ SN is important to avoid conflicts ------ \n"
        #textPayload += "#" + self.ComboBox_Microcontroller_ID_Dongle.get() + "_serial" + ""
        #textPayload += "\n# ----------------------------------------------- \n"

        #textPayload += "# " + self.Entry_Vendor_ID_Dongle.get() + "\n"
        #textPayload += "# Contains " + self.ComboBox_Microcontroller_ID.get() + " system-on-chip\n\n"
        #textPayload += "set CHIPNAME " + self.ComboBox_Microcontroller_ID.get() + "\n\n"
        #textPayload += "# ------ Link OpenOCD with MCA Config File ------ \n"
        #textPayload += "source /usr/share/openocd/scripts/target/" + self.ComboBox_Microcontroller_ID.get() + ".cfg\n\n"
        if self.User_Choice_MCU_Existance.get() == 1:
            if self.User_Choice_Card_MCA.get() == 2:
                textPayload += "# ------ Link OpenOCD with MCU Config File ------- \n\n"
                textPayload += "source [find target/" + self.ComboBox_Microcontroller_ID.get() + ".cfg]\n\n"
            else:
                textPayload += "# ------ Link OpenOCD with Board Config File ----- \n\n"
                textPayload += "source [find board/" + self.ComboBox_Microcontroller_ID.get() + ".cfg]\n\n"

        else:
            textPayload += "\n\n# ------------------------------------------------ \n"
            textPayload += "# --- " + self.Entry_Chip_Name.get()  + " CHIP Settings --- \n"
            textPayload += "# ------------------------------------------------ \n"
            textPayload += "set _CHIPNAME " + self.Entry_Chip_Name.get() +  "\n\n"
            textPayload += "set _ENDIAN " + self.ComboBox_Chip_Endianness.get().split(" ")[0] + "\n\n"
            textPayload += "set _CPUTAPID " + self.Entry_Chip_Tap_ID.get() + "\n\n"
            textPayload += "# ----- Create a tap ID controller ------\n"
            textPayload += "jtag newtap $_CHIPNAME " + self.ComboBox_Chip_Type.get() + " -irlen " + self.ComboBox_Chip_IR_Length.get() + " -expected-id $_CPUTAPID \n\n"
            textPayload += "set _TARGETNAME $_CHIPNAME."+ self.ComboBox_Chip_Type.get() + "\n"
            textPayload += "target create $_TARGETNAME " + self.ComboBox_Chip_Family.get() + " -chain-position $_TARGETNAME\n\n"


        if self.Configure_Memory_SDRAM.get() == 1:
            textPayload += "$_TARGETNAME configure "
            if self.Type_SDRam_variable.get()==1 :
                textPayload += "-work-area-phys "
            else:
                textPayload += "-work-area-virt "

            textPayload += self.Entry_Chip_SDRAM_Start_Address.get() + " -work-area-size " + self.Entry_Chip_SDRAM_Size_Address.get()
            textPayload += " -work-area-backup "
            if self.Backup_SDRam_variable.get() == 2 :
                textPayload += "0\n"
            else:
                textPayload += "1\n"
        if self.Configure_Memory_FLASH.get()==1:
            if self.ComboBox_Chip_Flash_Type.get()=="Nor":
                textPayload += "# ---------- Nor Flash Config ----------\n"
                textPayload += self.ScrolledText_Nor_Flash_Command_Field.get(1.0, tk.END) + "\n"

            elif self.ComboBox_Chip_Flash_Type.get()=="Nand":
                textPayload += "# ---------- Nand Flash Config ----------\n"
                textPayload += self.ScrolledText_Nand_Flash_Command_Field.get(1.0, tk.END) + "\n"

            elif self.ComboBox_Chip_Flash_Type.get()=="mFlash":
                textPayload += "# ---------- mFlash Flash Config ----------\n"
                textPayload += self.ScrolledText_mFlash_Command_Field.get(1.0, tk.END) + "\n"

        textPayload += "# ------------- END Of Config File --------------\n"
        textPayload += "# -----------------------------------------------"
        # textPayload += self.Entry_Vendor_ID.grid(row=2, column=1, padx=5, pady=5)
        # textPayload += self.Entry_Product_ID.grid(row=3, column=1, padx=5, pady=5)

        fd = open("openocd.cfg", "w+")
        fd.write(textPayload)
        fd.close()

        # textPayload +=
        # self.ScrolledText_Adapter_Config.delete(0,tk.END)
        # self.ScrolledText_Adapter_Config.insert(0, textPayload)
        print(textPayload)
        self.ScrolledText_Adapter_Config.delete('1.0', tk.END)
        self.ScrolledText_Adapter_Config.insert(tk.INSERT, textPayload)
        print("Generated\n")

    def centerWindow(self):
        x = (self.SmileMainWindow.winfo_screenwidth() - self.SmileMainWindow.winfo_reqwidth()) / 2
        y = (self.SmileMainWindow.winfo_screenheight() - self.SmileMainWindow.winfo_reqheight()) / 2
        self.SmileMainWindow.geometry("+%d+%d" % (x, y))

    def updateFileContent(self):
        fd = open("openocd.cfg", "w+")
        payload = self.ScrolledText_Adapter_Config.get(1.0, tk.END)
        fd.write(payload)
        fd.close()

    def discoverTapID(self):
        fd = open("openocd-dicover.cfg", "w+")
        payload = ""
        if (self.User_Choice_Adapter_Existance.get()==1):
            payload += "source [find interface/" + self.ComboBox_Microcontroller_ID_Dongle.get() + ".cfg]\n\n"
        else:
            payload += "interface " + self.ComboBox_Protocol_Dongle_Interface.get() + "\n"
            payload += self.ComboBox_Protocol_Dongle_Interface.get() + "_device_desc " + "\"" + self.Entry_Manufacturer_ID_Dongle.get() + "\"\n"
            payload += "# ------------ Define the VID and PID ----------- \n"

            payload += str(self.ComboBox_Protocol_Dongle_Interface.get()).replace("-",
                "_") + "_vid_pid " + self.Entry_Vendor_ID_Dongle.get() + " " + self.Entry_Product_ID_Dongle.get() + "\n"
        payload += "reset_config trst_and_srst\n\n"
        payload += "jtag_rclk 8"
        fd.write(payload)
        fd.close()

        if self.Checkbox_Manual_Installation_OpenOCD.get() == 0:
            pathCmd = "gnome-terminal -e 'bash -c \"sudo openocd -s /usr/share/openocd/scripts/ -f openocd-dicover.cfg --debug " +\
                      self.ComboBox_Variable_Log_Level.get() + "; sleep 10\"'"
            print(pathCmd)
            os.system(pathCmd)
        else:
            pathCmd ="gnome-terminal -e 'bash -c \"sudo " + self.Entry_Manual_Path_OpenOCD.get() + "/src/openocd -s " + \
                  self.Entry_Manual_Path_OpenOCD.get()+"/tcl/ " + "-f " + os.getcwd() + "/openocd-dicover.cfg --debug " + \
                     self.ComboBox_Variable_Log_Level.get() + "; sleep 10\"'"
            print(pathCmd)
            os.system(pathCmd)



    def launchOPENOCDAndDebug(self):
        if self.Checkbox_Manual_Installation_OpenOCD.get() == 0:
            #if(self.launch_verbose_mode.get()==0):
            os.system("gnome-terminal -e 'bash -c \"sudo openocd -s /usr/share/openocd/scripts/ -f openocd.cfg; sleep 10\"'")

        else:
            pathCmd ="gnome-terminal -e 'bash -c \"sudo " + self.Entry_Manual_Path_OpenOCD.get() + "/src/openocd -s " + \
                  self.Entry_Manual_Path_OpenOCD.get()+"/tcl/ " + "-f " + os.getcwd() + "/openocd.cfg; sleep 10\"'"
            print(pathCmd)
            os.system(pathCmd)

    def displayGUI(self):
        # self.centerWindow()
        self.SmileMainWindow.bind("<Return>", self.checkAgainOPENOCDSupport)
        self.SmileMainWindow.mainloop()

Launcher = programLauncher()
Launcher.createTabsForNavigation()
Launcher.setMenuBar()
Launcher.SmileDefineWidgetsOpenOCDSupport()
Launcher.SmilePlaceWidgetsOpenOCDSupport()



Launcher.SmileDefineWidgetsAdapterSupport()
Launcher.SmilePlaceWidgetsAdapterSupport()


Launcher.SmileDefineWidgetsMCASupport()
Launcher.SmilePlaceWidgetsMCASupport()

Launcher.SmileDefineWidgetsConfigSupport()
Launcher.SmilePlaceWidgetsConfigSupport()
Launcher.displayGUI()
