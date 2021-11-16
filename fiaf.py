#!/bin/python3

import subprocess 
import os
import sys 
from sys import platform
import time
import tkinter as tk 
from tkinter import Menu 
from tkinter import filedialog as fd 
from tkinter.messagebox import showinfo

# Global Vars
file_to_hide = "" 
file_to_camouflage = "" 
default_path = ""
result = ""

## GUI STUFF ##

# create the root window
root = tk.Tk()

#Set the geometry
root.eval('tk::PlaceWindow . center')
root.title('FIAF - (File Into Another File)')
root.resizable(0, 0)
root.geometry('') #auto resize

# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

# Create a menubar
menubar = Menu(root)
root.config(menu=menubar)

# create the file_menu
file_menu = Menu(
	menubar,
	tearoff=0
)

menubar.add_cascade(
	label="Options",
	menu=file_menu,
	underline=0
)

# create the Help menu
help_menu = Menu(
	menubar,
	tearoff=0
)

help_menu.add_command(label='About...')

# add the Help menu to the menubar
menubar.add_cascade(
	label="Help",
	menu=help_menu,
	underline=0
)

# Creating camouflaged_file label
label1 = tk.Label(root, text="Camouflage: ")
label1.grid(column=0, row=0, sticky=tk.W, padx=5, pady=10)

# Creating camouflaged file value
display_text = tk.StringVar()
display = tk.Label(root, textvariable=display_text, wraplength=350,width=50)
display.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

# Creating file_to_hide_label
label2 = tk.Label(root, text="File to hide in: ")
label2.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

# Creating file to hide value
display_text2 = tk.StringVar()
display2 = tk.Label(root, textvariable=display_text2, wraplength=350,width=50)
display2.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

## GUI STUFF

# Maybe in the future will do for windows :(
if platform == "linux" or platform == "linux2":
	# linux
	print("im in linux")
elif platform == "darwin":
	# OS X
    print("im in OSX")    
    showinfo(
		title='File as camouflage selected:',
		message="Sorry. It doesn't work on MAC. =(",
		icon="info"
	)
    sys.exit(1)
elif platform == "win32":
	# Windows
    print("im in Windows")
    showinfo(
		title='File as camouflage selected:',
		message="Sorry. It doesn't work on WINDOWS. =(",
		icon="info"
	)
    sys.exit(1)

# action to select a file to be camouflaged
def select_camouflaged_file():
	global file_to_camouflage
	global default_path

	filename_camouflage = fd.askopenfilename(
		title='Select a file as camouflage...',
		initialdir=str(default_path))

	file_to_camouflage = str(filename_camouflage)

	display_text.set(filename_camouflage)

	showinfo(
		title='File as camouflage selected:',
		message=filename_camouflage,
		icon="info"
	)

# action to select a file to be camouflaged
def select_tohide_file():
	global file_to_hide
	global default_path

	filename_tohide = fd.askopenfilename(
		title='File to hide...',
		initialdir=str(default_path))

	file_to_hide = str(filename_tohide)

	display_text2.set(filename_tohide)

	showinfo(
		title='File to hide selected:',
		message=filename_tohide,
		icon="info"
	)

# action triggered by button HIDE!
def hide_by_eof():
	seed=round(time.time() * 1000)
	filename=os.path.basename(file_to_camouflage)

	try:
		cmd = 'zip -j /tmp/%s.zip "%s"' % (seed, file_to_hide) #create a zip file. This zip contains a file to hide
		cmd2 = 'cp %s ./secret_%s' % (file_to_camouflage, filename) # making a copy of the original camouflaged file
		cmd3 = 'cat /tmp/%s.zip >> ./secret_%s' % (seed, filename) # add file at EOF into camuflaged file
		cmd4 = 'rm -f /tmp/%s.zip' % (seed) # garbage collector
		commands = cmd + " && " + cmd2 + " && " + cmd3 + " && " + cmd4

		button_hide['state'] = tk.DISABLED
		result = subprocess.check_output(commands, shell=True)

		showinfo(
		title='It works!:',
		message="Archivo creado con éxito!!!"
	)
	except Exception as ex:
		showinfo(
		title='Error:',
		message=str(ex),
		icon="error"
	)

# open camouflaged file to transform & extract
def search_for_camouflaged_files():
	file_to_check = fd.askopenfilename(
		title='Select camouflaged file...',
		initialdir=str(default_path))

	filename=os.path.basename(file_to_check)
	seed=round(time.time() * 1000)
	try:
		cmd='cp %s /tmp/%s' % (file_to_check, filename) # copy original file to temp directory for manipulate it
		cmd2='mv /tmp/%s /tmp/%s.zip' % (filename,seed) # change filename to .zip for extract hide file
		cmd3='unzip -B /tmp/%s.zip' % (seed) # extract file without overwrite the original one if exist
		cmd4='rm -f /tmp/%s.zip; rm -f /tmp/%s' % (seed,filename) # garbage collector
		commands = cmd + ";" + cmd2 + ";" + cmd3 + ";" + cmd4

		result = subprocess.check_output(commands, shell=True)

		showinfo(
			title='Camouflaged file selected:',
			message='File/s successfully extracted!',
			icon="info"
		)
	except Exception as ex:
		showinfo(
			title='Camouflaged file selected:',
			message=str(ex),
			icon="error"
		)

# add a submenu
sub_menu = Menu(file_menu, tearoff=0)
sub_menu.add_command(label='Set File to be camouflaged', command=select_camouflaged_file)
sub_menu.add_command(label='Set File to hide', command=select_tohide_file)

# add the File menu to the menubar
file_menu.add_cascade(label='Hide', menu=sub_menu)
file_menu.add_command(label='Unhide', command=search_for_camouflaged_files)

# add Exit menu item
file_menu.add_separator()
file_menu.add_command(
	label='Exit',
	command=root.destroy
)

# open file_to_hide button
button_hide = tk.Button(
	root,
	text="Hide!",
	command=hide_by_eof	
)
button_hide.grid(column=1, sticky=tk.EW, padx=5, pady=5)

# run the application
root.mainloop()
