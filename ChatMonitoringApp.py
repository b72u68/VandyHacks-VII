import os
import sys
import platform
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
#nameMenuVal = None
#monOptionVal = None

HourOptionList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18' ,'19', '20', '21', '22', '23']
MinuteOptionList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18' ,'19', '20', '21', '22', '23', '24', '25','26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38','39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51','52', '53', '54', '55', '56', '57', '58', '59']

background_color = 'wheat1'

#create base window
root = tk.Tk()
root.geometry("300x350")
root.configure(bg=background_color)
root.title("Zoom Chat Monitering")

#custom font
helv12 = tkFont.Font(family="Helvetica", size=12, underline=1)
helv10 = tkFont.Font(family="Helvetica", size=10)

tnr12 = tkFont.Font(family="Times New Roman", size=12)
tnr11 = tkFont.Font(family="Times New Roman", size=11)

monitorFrame = tk.Frame(root,bg=background_color)
monitorFrame.pack(side=tk.TOP)

#Checkbutton for choosing monitoring option
optionsLabel = tk.Label(monitorFrame, text="Choose type of monitoring:", font=helv12, bg=background_color)
optionsLabel.pack()

opt1 = IntVar()
opt2 = IntVar()
opt3 = IntVar()

#creating options i.e. "What kind of monitoring?"
option1 = tk.Checkbutton(monitorFrame, text="Participation Grading", font=tnr11, bg=background_color, fg="black", variable=opt1, onvalue=1, offvalue=0)
option2 = tk.Checkbutton(monitorFrame, text="Inappropriate Language", font=tnr11, bg=background_color, fg="black", variable=opt2, onvalue=1, offvalue=0)
option3 = tk.Checkbutton(monitorFrame, text="Time Search", font=tnr11, bg=background_color, fg="black", variable=opt3, onvalue=1, offvalue=0, command=openSearchOptions())

#adding buttons to screen
option1.pack()
option2.pack()
option3.pack()

#Label for uploading files
uploadLabel = tk.Label(root, text="Upload Files:", font=helv12,bg=background_color)
uploadLabel.pack()

def openSearchOptions():
    global searchOptionsWind, startHourVal, startMinuteVal, startSecondVal, endHourVal, endMinuteVal, endSecondVal, monOptionVal

    searchOptionsWind = tk.Toplevel(height=HEIGHT, width=WIDTH, bg=background_color)
    searchOptionsWind.title("Time Search")
    searchOptionsWind.geometry("250x250")

    startLabel = tk.Label(searchOptionsWind, text="Choose start time:", font=helv12, bg=background_color)
    startLabel.pack(side=tk.TOP)

    f1 = tk.Frame(searchOptionsWind)
    f1.pack(side=tk.TOP)

    startHourVal = StringVar()
    startHour = OptionMenu(f1, startHourVal, *HourOptionList)
    startHour.pack(side=tk.LEFT)

    startMinuteVal = StringVar()
    startMinute = OptionMenu(f1, startMinuteVal, *MinuteOptionList)
    startMinute.pack(side=tk.LEFT)

    startSecondVal = StringVar()
    startSecond = OptionMenu(f1, startSecondVal, *MinuteOptionList)
    startSecond.pack(side=tk.LEFT)

    endLabel = tk.Label(searchOptionsWind, text="Choose end time:", font=helv12, bg=background_color)
    endLabel.pack(side=tk.TOP)

    f2 = tk.Frame(searchOptionsWind)
    f2.pack(side=TOP)

    endHourVal = StringVar()
    endHour = OptionMenu(f2, endHourVal, *HourOptionList)
    endHour.pack(side=tk.LEFT)

    endMinuteVal = StringVar()
    endMinute = OptionMenu(f2, endMinuteVal, *MinuteOptionList)
    endMinute.pack(side=tk.LEFT)

    endSecondVal = StringVar()
    endSecond = OptionMenu(f2, endSecondVal, *MinuteOptionList)
    endSecond.pack(side=tk.LEFT)

    optionMonLabel = tk.Label(searchOptionsWind, text="Use filtering?", bg=background_color)
    optionMonLabel.pack()

    monOptionVal = StringVar()
    monOption = OptionMenu(searchOptionsWind, monOptionVal, "No", "Yes")
    monOption["menu"].config(bg="khaki1", activebackground="green3")
    monOption.pack()

    saveButton = tk.Button(searchOptionsWind, text="Save", command=save)
    saveButton.pack()

def save():
    """
    save search option result
    """
    searchOptionsWind.withdraw()

def searchStudents():
    """
    search for student name in class file
    """
    file = open(chat_file, 'rt')
    for data in file.readlines():
        data_split = data.split(' ', 1)
        student_name = data_split[1].split(" : ")[0][len("From")+1:]
        if student_name not in student_names:
            student_names.append(student_name)
    student_names.sort()

def get_chatFile():
    """
    read and get input chat file
    """
    global chat_file
    chat_file_temp = filedialog.askopenfilename()
    if chat_file_temp:
        chat_file = chat_file_temp
    if opt3.get() == 1:
        global nameMenuVal
        searchStudents()
        nameLabel = tk.Label(root, text="Which student would you like to search for?")
        nameLabel.pack()

        nameMenuVal = StringVar()
        nameMenu = OptionMenu(root, nameMenuVal, *student_names)
        nameMenu.pack()

def get_badWordsFile():
    """
    get bad word file from input
    """
    global badWords_file
    badWords_file_temp = filedialog.askopenfilename()
    if badWords_file_temp:
        badWords_file = badWords_file_temp
    w1.withdraw()

def get_filterChatFile():
    """
    get filter word file from input
    """
    global filterWords_file
    filterWords_file_temp = filedialog.askopenfilename()
    if filterWords_file_temp:
        filterWords_file = filterWords_file_temp
    w2.withdraw()


#Open chat_file
chatFileLabel = tk.Label(root, text = "Upload chat log:", font=tnr11, bg=background_color)
chatFileLabel.pack()
openChatFileButton = tk.Button(root, text="Browse", font=helv10, bg='khaki1', command=get_chatFile())
openChatFileButton.pack()


#Open badWords_file
badWordFileLabel = tk.Label(root, text = "Upload list of inappropriate words:", font=tnr11,bg=background_color)
badWordFileLabel.pack()
#openBadWordsFileButton = tk.Button(root, text="Browse", font=helv10, bg='khaki1', command=open_badWordsFile())
#openBadWordsFileButton.pack()

#Use default or custom file?
badOpt1 = badOpt2 = None
bad1 = tk.Checkbutton(root, text="Default", font=tnr11, bg=background_color, fg="black", variable=badOpt1, onvalue=1, offvalue=0)
bad1.pack()
bad2 = tk.Checkbutton(root, text="Custom", font=tnr11, bg=background_color, fg="black", variable=badOpt2, onvalue=1, offvalue=0, command=badSearch())
bad2.pack()

#Prompt for custom file
def badSearch():
    """
    browse bad word file
    """
    global w1
    w1 = tk.Toplevel(height=(HEIGHT/2), width=(WIDTH/2), bg=background_color)
    w1.title("Browse File")
    #w1.geometry("250x250")

    openBadWordsFileButton = tk.Button(w1, text="Browse", command=get_badWordsFile())
    openBadWordsFileButton.pack()


#Open filterWords_file
filterWordsFileLabel = tk.Label(root, text="Upload list of filter words:", font=tnr11, bg=background_color)
filterWordsFileLabel.pack()
#openFilterWordsButton = tk.Button(root, text="Browse", font=helv10, bg='khaki1', command=open_filterChatFile())
#openFilterWordsButton.pack()

#Use default or custom file?
filterOpt1 = filterOpt2 = None
filter1 = tk.Checkbutton(root, text="Default", font=tnr11, bg=background_color, fg="black", variable=filterOpt1, onvalue=1, offvalue=0)
filter1.pack()
filter2 = tk.Checkbutton(root, text="Custom", font=tnr11, bg=background_color, fg="black", variable=filterOpt2, onvalue=1, offvalue=0, command=filterSearch())
filter2.pack()

def filterSearch():
    """
    browse filter word file
    """
    global w2
    w2 = tk.Toplevel(height=(HEIGHT/2), width=(WIDTH/2), bg=background_color)
    w2.title("Browse File")
    #w2.geometry("250x250")

    openFilterWordsButton = tk.Button(w2, text="Browse", font=helv10, bg='khaki1', command=get_filterChatFile())
    openFilterWordsButton.pack()

def start():
    python_command = 'python3'
    # python_path = sys.executable
    machine_os = platform.system()
    if machine_os == 'Windows':
        # python_command = python_path.split('\\')[-1].split('.')[0]
        python_command = 'python'

    command = [python_command, 'main.py']

    if opt1.get() == 1:
        command.extend(['-fw', filterWords_file])

    if opt2.get() == 1:
        command.extend(['-bw', badWords_file])

    # elif opt3.get() == 1:
        # s = 1
        # useFilt = 0
        # if monOptionVal.get() == "Yes":
            # useFilt=1
        # result = subprocess.run(['python3', 'main.py', '-m', f'{useFilt}', '-s', f'{s}', '-n', f'{nameMenuVal.get()}', '-st', f'{startHourVal.get()}:{startMinuteVal.get()}:{startSecondVal.get()}', '-e', f'{endHourVal.get()}:{endMinuteVal.get()}:{endSecondVal.get()}', chat_file], shell=False, capture_output=True)
        # messagebox.showinfo(title="Search Results",message=result.stdout)

        # add chat file to the end of command
        command.append(chat_file)

        # run the command
        result = subprocess.run(command, shell=False, capture_output=True)
        messagebox.showinfo(title="Results", message=result.stdout)

    else:
        messagebox.showerror(title="Error", message="You must select one monitoring option.")

#creating a button
startButton = tk.Button(root, text="Start", fg="black", bg="green3", command=start, font=helv12)

#put button on screen
startButton.pack()

#run application
root.mainloop()
