import tkinter as tk
from tkinter import ttk

import lttngust
import logging
import time

logging.basicConfig()
logger = logging.getLogger('logger-lttng')

click_counter=0

# Creating a TKinter window
myWindow = tk.Tk()
myWindow.title("LTTng recorded window")

def ChangeTitle():
    logger.debug('debug message')
    LABEL_Text_Modify.config(text="Sent to LTTng")
    incrementNbClicks()


def incrementNbClicks():
    global click_counter
    click_counter += 1
    LABEL_Text_Counter.config(text="Number of clicks : "+str(click_counter))


LABEL_MAIN_TITLE = ttk.Label(master=myWindow, text="Tracing App using LTTng", font=("Arial",30),foreground="red")
LABEL_MAIN_TITLE.grid(row=0,column=0,padx=10,pady=10,columnspan=2)

LABEL_Text_Modify = ttk.Label(master=myWindow, text="Click to send to LTTng")
LABEL_Text_Modify.grid(row=1,column=0,padx=10,pady=10,columnspan=2)

LABEL_Text_Counter = ttk.Label(master=myWindow, text="Number of clicks : 0")
LABEL_Text_Counter.grid(row=2,column=1,padx=10,pady=10)

SMILE_Click_Button = tk.Button(master=myWindow, text="Send log",command=ChangeTitle)
SMILE_Click_Button.grid(row=2,column=0,padx=10,pady=10)

myWindow.mainloop() # start python GUI
