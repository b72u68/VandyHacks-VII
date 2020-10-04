import tkinter as tk
import tkinter.font as tkFont
import subprocess
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from tkinter import filedialog
from tkinter import messagebox

HEIGHT = 1000 #pixels
WIDTH = 1000 #pixels
chat_file = ''
badWords_file = './default_word_files/badWords.txt'
filterWords_file = './default_word_files/filterWords.txt'
student_names = []
#searchOptionsWind = None
#nameMenuVal = None				#NEW!!!!
#monOptionVal = None				#NEW!!!

HourOptionList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18' ,'19', '20', '21', '22', '23']
MinuteOptionList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18' ,'19', '20', '21', '22', '23', '24', '25','26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38','39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51','52', '53', '54', '55', '56', '57', '58', '59']

background_color = 'wheat1'
#create base window
root = tk.Tk()
root.geometry("300x350")
root.configure(bg=background_color)
root.title("Zoom Chat Monitering")

#custom font
helv12 = tkFont.Font(family="Helvetica",size=12,underline=1)
helv10 = tkFont.Font(family="Helvetica",size=10)

tnr12 = tkFont.Font(family="Times New Roman",size=12)
tnr11 = tkFont.Font(family="Times New Roman",size=11)


monitorFrame = tk.Frame(root)									#NEW
monitorFrame.pack(side=tk.TOP)									#NEW

#Checkbutton for choosing monitoring option
optionsLabel = tk.Label(monitorFrame, text="Choose type of monitoring:", font=helv12,bg=background_color)		#NEW CHANGES
optionsLabel.pack()

opt1=IntVar()
opt2=IntVar()
opt3=IntVar()
#creating options i.e. "What kind of monitoring?"
option1 = tk.Checkbutton(monitorFrame, text = "Participation Grading", font=tnr11,bg=background_color, fg = "black", variable = opt1, onvalue = 1, offvalue = 0)		#NEW
option2 = tk.Checkbutton(monitorFrame, text = "Inappropriate Language", font=tnr11,bg=background_color, fg = "black", variable = opt2, onvalue = 1, offvalue = 0)		#NEW
option3 = tk.Checkbutton(monitorFrame, text = "Time Search", font=tnr11,bg=background_color, fg = "black", variable = opt3, onvalue = 1, offvalue = 0, command=lambda:openSearchOptions())	#NEW
#adding buttons to screen
option1.pack()
option2.pack()
option3.pack()

#Label for uploading files
uploadLabel = tk.Label(root, text="Upload Files:", font=helv12,bg=background_color)
uploadLabel.pack()


def openSearchOptions():
	global searchOptionsWind,startHourVal,startMinuteVal,startSecondVal,endHourVal,endMinuteVal,endSecondVal, monOptionVal			#NEW

	searchOptionsWind = tk.Toplevel(height=HEIGHT, width=WIDTH, bg=background_color)
	searchOptionsWind.title("Time Search")
	searchOptionsWind.geometry("250x250")

	startLabel = tk.Label(searchOptionsWind, text="Choose start time:", font=helv12,bg=background_color)
	startLabel.pack(side=tk.TOP)													#NEW

	f1 = tk.Frame(searchOptionsWind)												#NEW
	f1.pack(side=tk.TOP)															#NEW

	startHourVal = StringVar()														#NEW
	startHour = OptionMenu(f1, startHourVal, *HourOptionList)						#NEW
	startHour.pack(side=tk.LEFT)													#NEW

	startMinuteVal = StringVar()													#NEW
	startMinute = OptionMenu(f1, startMinuteVal, *MinuteOptionList)					#NEW
	startMinute.pack(side=tk.LEFT)													#NEW

	startSecondVal = StringVar()													#NEW
	startSecond = OptionMenu(f1, startSecondVal, *MinuteOptionList)					#NEW
	startSecond.pack(side=tk.LEFT)													#NEW


	endLabel = tk.Label(searchOptionsWind, text="Choose end time:", font=helv12,bg=background_color)
	endLabel.pack(side=tk.TOP)														#NEW

	f2 = tk.Frame(searchOptionsWind)												#NEW
	f2.pack(side=TOP)																#NEW


	endHourVal = StringVar()														#NEW
	endHour = OptionMenu(f2, endHourVal, *HourOptionList)							#NEW
	endHour.pack(side=tk.LEFT)														#NEW

	endMinuteVal = StringVar()														#NEW
	endMinute = OptionMenu(f2, endMinuteVal, *MinuteOptionList)						#NEW
	endMinute.pack(side=tk.LEFT)													#NEW

	endSecondVal = StringVar()														#NEW
	endSecond = OptionMenu(f2, endSecondVal, *MinuteOptionList)						#NEW
	endSecond.pack(side=tk.LEFT)													#NEW


	optionMonLabel = tk.Label(searchOptionsWind, text="Use filtering?",bg=background_color)
	optionMonLabel.pack()

	monOptionVal = StringVar()
	monOption = OptionMenu(searchOptionsWind, monOptionVal, "No", "Yes")				#NEW CHANGES
	monOption["menu"].config(bg="khaki1",activebackground="green3")
	monOption.pack()


	saveButton = tk.Button(searchOptionsWind, text="Save", command=save)
	saveButton.pack()

#
def save():																				#NEW
	searchOptionsWind.withdraw()														#NEW


def searchStudents():																	#NEW:
	file = open(chat_file, 'rt')														#NEW
	for data in file.readlines():														#NEW
		data_split = data.split(' ', 1)													#NEW
		student_name = data_split[1].split(" : ")[0][len("From")+1:]					#NEW
		if student_name not in student_names:											#NEW
			student_names.append(student_name)											#NEW
	student_names.sort()																#NEW^^^


#function for opening files in read mode
def open_chatFile():
	global chat_file
	chat_file_temp = filedialog.askopenfilename()
	if chat_file_temp:
		chat_file = chat_file_temp
	if opt3.get() == 1:
		global nameMenuVal																	#NEW
		searchStudents()																	#NEW
		nameLabel = tk.Label(root, text="Which student would you like to search for?")		#NEW
		nameLabel.pack()																	#NEW

		nameMenuVal = StringVar()															#NEW
		nameMenu = OptionMenu(root, nameMenuVal, *student_names)							#NEW
		nameMenu.pack()																		#NEW^^^

def open_badWordsFile():
	global badWords_file
	badWords_file_temp = filedialog.askopenfilename()
	if badWords_file_temp:
		badWords_file = badWords_file_temp
	w1.withdraw()

def open_filterChatFile():
	global filterWords_file
	filterWords_file_temp = filedialog.askopenfilename()
	if filterWords_file_temp:
		filterWords_file = filterWords_file_temp
	w2.withdraw()


#Open chat_file
chatFileLabel = tk.Label(root, text = "Upload chat log:", font=tnr11,bg=background_color)		#NEW CHANGES
chatFileLabel.pack()
openChatFileButton = tk.Button(root, text="Browse", font=helv10, bg='khaki1', command=lambda:open_chatFile())			#NEW CHANGES
openChatFileButton.pack()


#Open badWords_file
badWordFileLabel = tk.Label(root, text = "Upload list of inappropriate words:", font=tnr11,bg=background_color)					#NEW
badWordFileLabel.pack()
#openBadWordsFileButton = tk.Button(root, text="Browse", font=helv10, bg='khaki1', command=lambda:open_badWordsFile())
#openBadWordsFileButton.pack()

#Use default or custom file?
badOpt1 = badOpt2 = None																				#NEW
bad1 = tk.Checkbutton(root, text = "Default", font=tnr11,bg=background_color, fg = "black", variable = badOpt1, onvalue = 1, offvalue = 0)		#NEW
bad1.pack()																				#NEW
bad2 = tk.Checkbutton(root, text = "Custom", font=tnr11,bg=background_color, fg = "black", variable = badOpt2, onvalue = 1, offvalue = 0,command=lambda:badSearch())		#NEW
bad2.pack()

#Prompt for custom file
def badSearch():
	global w1
	w1 = tk.Toplevel(height=(HEIGHT/2), width=(WIDTH/2), bg=background_color)
	w1.title("Browse File")
	#w1.geometry("250x250")

	openBadWordsFileButton = tk.Button(w1, text="Browse", command=lambda:open_badWordsFile())
	openBadWordsFileButton.pack()


#Open filterWords_file
filterWordsFileLabel = tk.Label(root, text = "Upload list of filter words:", font=tnr11,bg=background_color)
filterWordsFileLabel.pack()
#openFilterWordsButton = tk.Button(root, text="Browse", font=helv10, bg='khaki1', command=lambda:open_filterChatFile())
#openFilterWordsButton.pack()

#Use default or custom file?
filterOpt1 = filterOpt2 = None																				#NEW
filter1 = tk.Checkbutton(root, text = "Default", font=tnr11,bg=background_color, fg = "black", variable = filterOpt1, onvalue = 1, offvalue = 0)		#NEW
filter1.pack()																				#NEW
filter2 = tk.Checkbutton(root, text = "Custom", font=tnr11,bg=background_color, fg = "black", variable = filterOpt2, onvalue = 1, offvalue = 0,command=lambda:filterSearch())		#NEW
filter2.pack()

def filterSearch():
	global w2
	w2 = tk.Toplevel(height=(HEIGHT/2), width=(WIDTH/2), bg=background_color)
	w2.title("Browse File")
	#w2.geometry("250x250")

	openFilterWordsButton = tk.Button(w2, text="Browse", font=helv10, bg='khaki1', command=lambda:open_filterChatFile())
	openFilterWordsButton.pack()


def start():
	if opt1.get() == 1:
		result = subprocess.run(['python3', 'main.py', '-fw', filterWords_file, chat_file], shell=False, capture_output=True)		#NEW CHANGES
		messagebox.showinfo(title="Search Results",message=result.stdout)															#NEW
	elif opt2.get() == 1:
		result = subprocess.run(['python3', 'main.py', '-bw', badWords_file, chat_file], shell=False, capture_output=True)				#NEW CHANGES
		messagebox.showinfo(title="Search Results",message=result.stdout)															#NEW
	elif opt3.get() == 1:
		s = 1
		useFilt = 0
		if monOptionVal.get() == "Yes":
			useFilt=1																	#NEW (below)
		result = subprocess.run(['python3', 'main.py', '-m', f'{useFilt}', '-s', f'{s}', '-n', f'{nameMenuVal.get()}', '-st', f'{startHourVal.get()}:{startMinuteVal.get()}:{startSecondVal.get()}', '-e', f'{endHourVal.get()}:{endMinuteVal.get()}:{endSecondVal.get()}', chat_file], shell=False, capture_output=True)
		messagebox.showinfo(title="Search Results",message=result.stdout)				#NEW

	else:
		messagebox.showerror(title="Error",message="You must select one monitoring option.")			#NEW



#creating a button
startButton = tk.Button(root, text="Start", fg = "black", bg = "green3", command=start, font=helv12)
#put button on screen
startButton.pack()

#run application
root.mainloop()
