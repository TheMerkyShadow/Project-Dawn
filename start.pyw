import os
import sys

import subprocess

import platform
import webbrowser

import tkinter as tk
import tkinter.scrolledtext as st

import update

window = tk.Tk()
window.title('Dawn')
window.geometry('500x500')
window.resizable(False, False)

log_window = st.ScrolledText(window, font = ("Times New Roman", 12))
log_window.place(relx=0.50, rely=0.40, relwidth=0.95, relheight=0.75, anchor=tk.CENTER)

class TextWrapper:
    def __init__(self, widget):
        self.widget = widget
        
    def write(self, text):
        self.widget.config(state="normal")
        self.widget.insert(tk.INSERT, text)
        self.widget.see(tk.END)
        self.widget.config(state="disabled")
        
    def flush(self):
        pass

sys.stdout = TextWrapper(log_window) 

print( "Welcome To Dawn!" )
print( "Created by TheMerkyShadow!" )

def Update():
    update.GitManager().Sync()
    return

def Play():
    print( "Launching Minecraft @", update.Minecraft() )
    subprocess.Popen([ update.Minecraft(), '--workDir', os.path.join(os.getcwd(),'dawn') ])
    return
    
window.play = tk.Button(window, text='Play')
window.play.place(relx=0.30, rely=0.88, relwidth=0.25, relheight=0.075, anchor=tk.CENTER)
window.play.config(command=(lambda : Play() ) )

window.update = tk.Button(window, text='Update')
window.update.place(relx=0.70, rely=0.88, relwidth=0.25, relheight=0.075, anchor=tk.CENTER)
window.update.config(command=( lambda : Update()  ) )

window.mainloop()
