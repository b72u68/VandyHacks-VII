import tkinter as tk
import tkinter.font as tkFont
import subprocess
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from tkinter import filedialog


HEIGHT = 1000 #pixels
WIDTH = 1000 #pixels
chat_file = ''
badWords_file = './default_word_files/badWords.txt'
filterWords_file = './default_word_files/filterWords.txt'
student_names = []
searchOptionsWind = None

HourOptionList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18' ,'19', '20', '21', '22', '23']
MinuteOptionList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18' ,'19', '20', '21', '22', '23', '24', '25','26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38','39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51','52', '53', '54', '55', '56', '57', '58', '59']

#create base window
root = tk.Tk()
root.geometry("300x300")


#Checkbutton for choosing monitoring option
optionsLabel = tk.Label(root, text="Choose type of monitoring:")
optionsLabel.pack()

opt1=IntVar()
opt2=IntVar()
opt3=IntVar()
#creating options i.e. "What kind of monitoring?"
option1 = tk.Checkbutton(root, text = "Participation Grading", fg = "black", variable = opt1, onvalue = 1, offvalue = 0)
option2 = tk.Checkbutton(root, text = "Inappropriate Language", fg = "black", variable = opt2, onvalue = 1, offvalue = 0)
option3 = tk.Checkbutton(root, text = "Time Search", fg = "black", variable = opt3, onvalue = 1, offvalue = 0, command=lambda:openSearchOptions())
#adding buttons to screen
option1.pack()
option2.pack()
option3.pack()


def openSearchOptions():
	searchOptionsWind = tk.Toplevel(height=HEIGHT, width=WIDTH)

	startLabel = tk.Label(searchOptionsWind, text="Choose start time:")
	startLabel.pack()


	startHourVal = IntVar()
	startHour = OptionMenu(searchOptionsWind, startHourVal, *HourOptionList)
	startHour.pack()

	startMinuteVal = IntVar()
	startMinute = OptionMenu(searchOptionsWind, startMinuteVal, *MinuteOptionList)
	startMinute.pack()

	startSecondVal = IntVar()
	startSecond = OptionMenu(searchOptionsWind, startSecondVal, *MinuteOptionList)
	startSecond.pack()


	endLabel = tk.Label(searchOptionsWind, text="Choose end time:")
	endLabel.pack()


	endHourVal = IntVar()
	endHour = OptionMenu(searchOptionsWind, endHourVal, *HourOptionList)
	endHour.pack()

	endMinuteVal = IntVar()
	endMinute = OptionMenu(searchOptionsWind, endMinuteVal, *MinuteOptionList)
	endMinute.pack()

	endSecondVal = IntVar()
	endSecond = OptionMenu(searchOptionsWind, endSecondVal, *MinuteOptionList)
	endSecond.pack()


	optionMonLabel = tk.Label(searchOptionsWind, text="Use filtering?")
	optionMonLabel.pack()

	monOptionVal = StringVar()
	monOption = OptionMenu(searchOptionsWind, monOptionVal, "Yes", "No")
	monOption.pack()



#function for opening files in read mode
def open_chatFile():
	global chat_file
	chat_file_temp = filedialog.askopenfilename()
	if chat_file_temp:
		chat_file = chat_file_temp

def open_badWordsFile():
	global badWords_file
	badWords_file_temp = filedialog.askopenfilename()
	if badWords_file_temp:
		badWords_file = badWords_file_temp

def open_filterChatFile():
	global filterWords_file
	filterWords_file_temp = filedialog.askopenfilename()
	if filterWords_file_temp:
		filterWords_file = filterWords_file_temp


#Open chat_file
chatFileLabel = tk.Label(root, text = "Upload chat log:")
chatFileLabel.pack()
openChatFileButton = tk.Button(root, text="Browse", command=lambda:open_chatFile())
openChatFileButton.pack()


#Open badWords_file
badWordFileLabel = tk.Label(root, text = "Upload list of inappropriate words:")
badWordFileLabel.pack()
openBadWordsFileButton = tk.Button(root, text="Browse", command=lambda:open_badWordsFile())
openBadWordsFileButton.pack()


#Open filterWords_file
filterWordsFileLabel = tk.Label(root, text = "Upload list of filter words:")
filterWordsFileLabel.pack()
openFilterWordsButton = tk.Button(root, text="Browse", command=lambda:open_filterChatFile())
openFilterWordsButton.pack()



def start():
	if opt1.get() == 1:
			subprocess.run(['python3', 'main.py', '-fw', filterWords_file, chat_file], shell=False, capture_output=False)
	elif opt2.get() == 1:
		subprocess.run(['python3', 'main.py', '-bw', badWords_file, chat_file], shell=False, capture_output=False)
	elif opt3.get() == 1:
		useFilt = 0
		if monOptionVal == "Yes":
			useFilt=1
			#subprocess.run(['python3', 'main.py', '-s', useFilt, '-n', <student name> '-st' startHourVal:startMinuteVal:startSecondVal, '-e' endHourVal:endMinuteVal:endSecondVal, 'chat_file'])
	else:
		pass



#creating a button
startButton = tk.Button(root, text="Start", fg = "black", bg = "red", command=start)
#put button on screen
startButton.pack()

#run application
root.mainloop()
