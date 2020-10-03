import datetime
import os
import csv
import json

class ZoomChatMonitoring:

    # add default filename later
    def __init__(self, bad_word_file, filter_word_file):
        self.filter_word_file = filter_word_file
        self.bad_word_file = bad_word_file

        # filter_words: list of words to filter message (read from file)
        self.filter_words = []

        #question_words: list of words used to determine if message is a question
        self.question_words = ['who', 'what', 'when', 'where', 'why', 'how']

        # bad_words: list of bad words (read from file)
        self.bad_words = []

        # student_messages: {student_email: [{message_time: str, message: str}]}
        self.student_messages = {}
        # student_questions: {student_email: [{message_time: str, questions: str}]}
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

    def is_question(self, message):
        """
        return True if message is a question
        return False otherwise
        """
        text = message.split(' ')

        # get first word of message
        firstWord = text[0]
        # get punctuation
        lastWord = text[-1][-1]

        if firstWord in self.question_words or lastWord == '?':
            return True

        return False

    def monitoring_messages(self, json_data):
        """monitoring and storing message from json_data"""

        # get list of message data (json_data = placeholder)
        chat_log = json.loads(json_data)

        # iterate through messages
        for message_obj in chat_log["messages"]:
            # get student student_email
            student_email = message_obj["sender"]

            # get student message
            msg = message_obj["message"]
            # get message time as a string
            time = message_obj["date_time"].split('T')[1][0:-1]

            # check if message is worth for student credits
            if self.check_message(msg) == 1:
                # if message is a question
                if self.is_question(msg):
                    # check if student_email key exists in student_questions
                    if not self.student_questions[student_email]:
                        self.student_questions[student_email] = []

                    # add to student_questions
                    self.student_questions[student_email].append({'message_time': time, 'message': msg})

                #if not question, but worth for credits
                else:
                    # check if student_email key exists in student_messages
                    if not self.student_messages[student_email]:
                        self.student_messages[student_email] = []

                    # add to student_messages
                    self.student_messages[student_email].append({'message_times': time, 'message': msg})

    def write_csv(self):
        """write students who get credits to csv file"""
        current_date = datetime.datetime.now()
        filename = f'{current_date.month}-{current_date.day}-{current_date.year}.csv'

        try:
            # create directory zoom_logs if not exist
            os.mkdir('./zoom_logs')
        except OSError:
            # the directory has already existed
            pass

        filepath = './zoom_logs' + filename

        with open(filepath, mode='w') as zoom_log_file:
            fieldnames = ['student_email', 'point']
            writer = csv.DictWriter(zoom_log_file, fieldnames=fieldnames)

            writer.writeheader()
            for student in self.student_messages:
                writer.writerow({'name': student.student_email, 'point': 1})
            for student in self.student_questions:
                if student not in self.student_messages:
                    writer.writerow({'name': student.student_email, 'point': 1})
