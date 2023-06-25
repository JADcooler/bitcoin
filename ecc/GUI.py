import subprocess

def execute_file(filename, input_data):
    command = ['python', filename]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate(input=input_data)
    return stdout, stderr

#we open main.py, main_f.py, mainB.py and attach it to a subprocess

tx = subprocess.Popen(['python','main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
rx = subprocess.Popen(['python','main_f.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
m = subprocess.Popen(['python','mainB.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

def tell(proc, inp):
    out,err = proc.communicate(input = inp)
    return out,err


textVar = StringVar()

def pubkeyhash():
    print("DEBIUG")
    out,err = tell(tx, 0)
    print(out)
    textVar.set(out)
    



from tkinter import *
from tkinter import ttk

root = Tk()
s = ttk.Style()
mainframe = ttk.Frame(root, width=500, height=500, style='Danger.TFrame').grid(column=0, row=0, columnspan=3, rowspan=3)

ttk.Button(mainframe, text= "Show public key hash",command = pubkeyhash).grid(column = 1, row = 1)
hashLabel = ttk.Label(mainframe,  text = "test")
hashLabel.grid(column = 1, row = 2)
hashLabel['textvariable'] = textVar


root.mainloop()