import datetime
import os
import csv

class ZoomChatMonitoring:

    def __init__(self, bad_word_file, filter_word_file, chat_file):
        # init .txt files
        self.chat_file = chat_file
        self.filter_word_file = filter_word_file
        self.bad_word_file = bad_word_file

        # filter_words: list of words to filter message (read from file)
        self.filter_words = []

        #question_words: list of words used to determine if message is a question
        self.question_words = ['who', 'what', 'when', 'where', 'why', 'how']

        # bad_words: list of bad words (read from file)
        self.bad_words = []

        # student_messages: {student_name: [{message_time: str, message: str}]}
        self.student_messages = {}
        # student_questions: {student_name: [{message_time: str, questions: str}]}
        self.student_questions = {}
        #student_badwords: {student_name: [{message_time: str, inappropriateMsg: str}]}
        self.student_badwords = {}

        # all messages
        self.all_messages = []

        try:
            file = open(self.chat_file, 'rt')
            for data in file.readlines():
                # spl1: message_time\t | From student_name : message\n
                data_split = data.split(' ', 1)
                message_time = data_split[0][:-1]
                student_name = data_split[1].split(" : ")[0][len("From")+1:]
                message= data_split[1].split(" : ")[1]

                self.all_messages.append({'message_time': message_time, 'student_name': student_name, 'message': message})

        except Exception as e:
            print('[-] Error occurred while reading chat file')

    def read_word_file(self, filename):
        """
        read words from file
        """
        words = []
        try:
            file = open(filename, 'rt')
            words = [word[:-1] for word in file.readlines()]

        except Exception as e:
            print(f'[-] Error occurred while reading word file: {e}')

        return words

    def read_chat_file(self):
        """
        read chat file
        """
        # get word lists
        self.get_filter_word_list()
        self.get_bad_word_list()

        try:
            file = open(self.chat_file, 'rt')
            for data in file.readlines():
                # spl1: message_time\t | From student_name : message\n
                data_split = data.split(' ', 1)
                message_time = data_split[0][:-1]
                student_name = data_split[1].split(" : ")[0][len("From")+1:]
                message= data_split[1].split(" : ")[1]

                if self.check_message(message) == 1:
                    self.monitoring_messages(message_time, student_name, message)
                elif self.check_message(message) == -1:
                    self.monitoring_badWords(message_time, student_name, message)

            print('[+] Process chat file successfully!')

        except Exception as e:
            print(f'[-] Exception occurred while reading chat file: {e}')

        # write the results to files
        self.write_csv_messages()
        self.write_csv_badwords()


    def get_bad_word_list(self):
        """
        get bad words from file
        """
        self.bad_words = self.read_word_file(self.bad_word_file)

    def get_filter_word_list(self):
        """
        get filter words from file
        """
        self.filter_words = self.read_word_file(self.filter_word_file)

    def check_message(self, message):
        """
        return -1 if message contains bad words -> remove
        return 0 if message contains filter words -> no credits
        return 1 if message can be counted as credits
        """
        for word in self.bad_words:
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
        first_word = text[0]
        # get punctuation
        last_word = text[-1][-1]

        if first_word in self.question_words or last_word == '?':
            return True

        return False

    def monitoring_messages(self, message_time, student_name, message):
        """
        monitoring and storing message from chat_file for class participation
        """
        # if message is a question
        if self.is_question(message):
            # check if student_name key exists in student_questions
            if student_name not in self.student_questions:
                self.student_questions[student_name] = []

            # add to student_questions
            self.student_questions[student_name].append({'message_time': message_time, 'message': message})

        # if not question, but worth for credits
        else:
            # check if student_name key exists in student_messages
            if student_name not in self.student_messages:
                self.student_messages[student_name] = []

            # add to student_messages
            self.student_messages[student_name].append({'message_time': message_time, 'message': message})

    def monitoring_badWords(self, message_time, student_name, message):
        """
        monitoring and storing message from chat_file to monitor for
        inappropriate language
        """
        # check if student_email key exists in student_messages
        if student_name not in self.student_badwords:
            self.student_badwords[student_name] = []

        # add to student_messages
        self.student_badwords[student_name].append({'message_time': message_time, 'message': message})

    def write_csv_messages(self):
        """
        write students who get credits to csv file
        """
        current_date = datetime.datetime.now()
        filename = 'partial_credits.csv'

        try:
            # create directory zoom_logs if not exist
            os.mkdir(f'./zoom_logs/{current_date.month}-{current_date.day}-{current_date.year}')
        except OSError:
            # the directory has already existed
            pass

        filepath = f'./zoom_logs/{current_date.month}-{current_date.day}-{current_date.year}/' + filename

        with open(filepath, mode='w') as zoom_log_file:
            fieldnames = ['name', 'point']
            writer = csv.DictWriter(zoom_log_file, fieldnames=fieldnames)

            writer.writeheader()
            for student_name in self.student_messages:
                writer.writerow({'name': student_name, 'point': 1})
            for student_name in self.student_questions:
                if student_name not in self.student_messages:
                    writer.writerow({'name': student_name, 'point': 1})

    def write_csv_badwords(self):
        """
        write students who use inappropriate words to csv file
        """
        current_date = datetime.datetime.now()
        filename = 'inappropriate_chats.csv'

        try:
            # create directory zoom_logs if not exist
            os.mkdir(f'./zoom_logs/{current_date.month}-{current_date.day}-{current_date.year}')
        except OSError:
            # the directory has already existed
            pass

        filepath = f'./zoom_logs/{current_date.month}-{current_date.day}-{current_date.year}/' + filename

        with open(filepath, mode='w') as zoom_log_file:
            fieldnames = ['name', 'message']
            writer = csv.DictWriter(zoom_log_file, fieldnames=fieldnames)

            writer.writeheader()
            for student_name in self.student_badwords:
                for inappropriateMsg in self.student_badwords[student_name]:
                    writer.writerow({'name': student_name, 'message': inappropriateMsg})

    def search_messages(self, student_name, start, end):
        """
        search for messages in given time
        """
        result_messages = []

        def string_time_to_second(time):
            """
            convert string time to second for easier comparision
            """
            time_split = time.split(':')
            hour = int(time_split[0])
            minute = int(time_split[1])
            second = int(time_split[2])
            return 3600*hour + 60*minute + second

        # assign value to start and end if no argument is passed
        if not start:
            start = self.all_messages[0]['message_time']
        if not end:
            end = self.all_messages[-1]['message_time']

        start_time = string_time_to_second(start)
        end_time = string_time_to_second(end)

        for i in range(len(self.all_messages)):
            time = string_time_to_second(self.all_messages[i]['message_time'])
            if start_time <= time <= end_time:
                if not student_name:
                    result_messages.append(self.all_messages[i])
                else:
                    if student_name in self.all_messages[i]['student_name']:
                        result_messages.append(self.all_messages[i])

        return result_messages
