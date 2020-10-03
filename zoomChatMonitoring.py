import json

class ZoomChatMonitoring:

    # add default filename later
    def __init__(self, bad_word_file='', filter_word_file=''):
        self.filter_word_file = filter_word_file
        self.bad_word_file = bad_word_file

        # filter_words: list of words to filter message (read from file)
        self.filter_words = []

        #question_words: list of words used to determine if message is a question
        self.question_words = ['who', 'what', 'when', 'where', 'why', 'how']

        # bad_words: list of bad words (read from file)
        self.bad_words = []


        # student_messages: {student_name: {message_time: str, message: str}}
        self.student_messages = {}
        # student_questions: {student_name: {message_time: str, questions: []}}
        self.student_questions = {}

    def read_file(self, filename):
        """
        read words from file
        """
        words = []
        try:
            file = open(filename, 'rt')
            words = [word for word in file.readlines()]

        except Exception as e:
            print(f'[-] Error Occurred: {e}')

        return words

    def get_bad_word_list(self):
        """get bad words from file"""
        self.bad_words= self.read_file(self.bad_word_file)

    def get_filter_word_list(self):
        """get filter words from file"""
        self.filter_words = self.read_file(self.filter_word_file)

    def check_message(self, message):
        """
        return -1 if message contains bad words -> remove
        return 0 if message contains filter words -> no credits
        return 1 if message can be counted as credits
        """
        for word in  self.bad_word_file:
            if word in message:
                return -1
        for word in self.filter_words:
            if word in message:
                return 0
        return 1


    #def is_question(self,message): return True if student message is a question,
    #otherwise return False
    def is_question(self,message):
        text = message.split(' ')               #split message into individual words
        lastWord = text[len(text)-1]            #saving last word for ease of use later
        if text[0] is in question_words:        #if first word is a question word
            return True                             #return True (it is a question)
        elif lastWord[:len(lastWord)-2:-1] == '?' #if last character of last word is a '?'
            return True                             #return True (it is a question)
        else:                                   #else, it is not a question
            return False

    # def monitoring_messages(self): check if message is worth for credits ->

    # def monitoring_messages(self, message): check if message is worth for credits ->

    # add to student_messages, if a question -> add to student_questions
    def monitoring_messages(self,json_data):
        chat_log = json.loads(json_data)                                    #get list of message data (json_data = placeholder)
        for x in chat_log["messages"]                                       #iterate through messages
            student_email = x["sender"]                                         #get student student_email
            msg = x["message"]                                                  #get student message
            time = x["date_time"][11:len(x["date_time"]-1)]                     #get message time as a string
            if check_message(msg):                                              #check if message is worth for student credits
                if is_question(msg):                                                    #if message is a question
                    student_questions[student_email].append({message: [time, questions[msg]})   #add to student_questions
                else:                                                                   #if not question, but worth for credits
                    student_messages[student_email].append({message: [time, msg]})              #add to student_messages
