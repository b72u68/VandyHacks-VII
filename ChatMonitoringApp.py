import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfile

HEIGHT = 700 #pixels
WIDTH = 800 #pixels
opt1,opt2,opt3 = 0,0,0
chat_file = ''
badWords_file = ''
filterWords_file = ''

#create base window
root = tk.Tk()

#Checkbutton for choosing monitoring option
optionsLabel = tk.Label(root, text="Choose type of monitoring:")
optionsLabel.pack()
#creating options i.e. "What kind of monitoring?"
option1 = tk.Checkbutton(frame, text = "Participation Grading", fg = "black")
option2 = tk.Checkbutton(frame, text = "Inappropriate Language", fg = "black")
option3 = tk.Checkbutton(frame, text = "Time Search", fg = "black")
#adding buttons to screen
option1.pack()
option2.pack()
option3.pack()


#function for opening files in read mode
def open_file():
	file = askopenfile(mode='r', filetypes = [("Text Files",".txt")])


#Open chat_file
chatFileLabel = tk.Label(frame, text = "Upload chat log:")
chatFileLabel.pack()
openChatFileButton = tk.Button(frame, text="Browse", command=lambda:open_file())
openChatFileButton.pack()


#Open badWords_file
badWordFileLabel = tk.Label(frame, text = "Upload list of inappropriate words:")
badWordFileLabel.pack()
openBadWordsFileButton = tk.Button(frame, text="Browse", command=lambda:open_file())
openBadWordsFileButton.pack()


#Open filterWords_file
filterWordsFileLabel = tk.Label(frame, text = "Upload list of filter words:")
filterWordsFileLabel.pack()
openFilterWordsButton = tk.Button(frame, text="Browse", command=lambda:open_file())
openFilterWordsButton.pack()


#creating a button
startButton = tk.Button(frame, text="Start", fg = "black", bg = "red", command = start())
#put button on screen
startButton.pack()


#defining startButton function
def start():
	exec = ZoomChatMonitoring(badWords_file, filterWords_file, chat_file)
	if opt1 == 1:
		exec.monitoring_messages()
	elif opt2 == 1:
		pass
	elif opt3 == 1:
		pass
	else:
		pass


#run application
root.mainloop()
