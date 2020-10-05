import os
import csv
import ntpath
import string

class ZoomChatMonitoring:

    def __init__(self, bad_word_file, filter_word_file, chat_file):
        # filter_words: list of words to filter message (read from file)
        self.filter_words = self.read_word_file(filter_word_file)

        # bad_words: list of bad words (read from file)
        self.bad_words = self.read_word_file(bad_word_file)

        # student_messages: {student_name: [{message_time: str, message: str}]}
        self.student_messages = {}

        # student_questions: {student_name: [{message_time: str, questions: str}]}
        self.student_questions = {}

        #student_badwords: {student_name: [{message_time: str, inappropriateMsg: str}]}
        self.student_badwords = {}

        # all messages
        self.all_messages = self.get_all_messages(chat_file)

        # directory for loggings
        self.log_directory = self.create_log_directory(chat_file)

    def read_word_file(self, filename):
        """
        read words from file
        """
        words = []
        try:
            file = open(filename, 'rt', encoding='utf8')
            words = [word[:-1] for word in file.readlines()]

        except Exception as e:
            print(f'[-] ERROR: read_word_file({filename}): {e}')

        return words

    def read_chat_file(self):
        """
        read chat file
        """
        try:
            for message_obj in self.all_messages:
                message_time = message_obj['message_time']
                student_name = message_obj['student_name']
                message = message_obj['message']

                if self.check_message(message) == 1:
                    self.monitoring_messages(message_time, student_name, message)
                elif self.check_message(message) == -1:
                    self.monitoring_badWords(message_time, student_name, message)

            print('[+] Process chat file successfully!')

            # write the results to files
            self.write_csv_messages()
            self.write_csv_badwords()

        except Exception as e:
            print(f'[-] ERROR: read_chat_file(): {e}')

    def get_all_messages(self, chatfile):
        """
        get all messages and store them in the array
        """
        messages = []

        try:
            file = open(chatfile, 'rt', encoding='utf8')
            for data in file.readlines():
                # data_split: message_time\t | From student_name : message\n
                data_split = data.split(' ', 1)
                message_time = data_split[0][:-1]
                student_name = data_split[1].split(" : ")[0][len("From")+1:]
                message= data_split[1].split(" : ")[1]

                messages.append({'message_time': message_time, 'student_name': student_name, 'message': message})

        except Exception as e:
            print(f'[-] ERROR: get_all_messages(): {e}')

        return messages

    def check_message(self, message):
        """
        return -1 if message contains bad words -> remove
        return 0 if message contains filter words -> no credits
        return 1 if message can be counted as credits
        """
        # split message into separated words
        message_words = message.split(' ')

        # strip punctuation out of words
        message_words = [word.translate(str.maketrans('', '', string.punctuation)) for word in message_words]

        for word in self.bad_words:
            if word in message_words:
                return -1
        for word in self.filter_words:
            if word in message_words:
                return 0
        return 1

    def is_question(self, message):
        """
        return True if message is a question
        return False otherwise
        """
        text = message.split(' ')

        question_words = ['who', 'what', 'when', 'where', 'why', 'how', 'is', 'are']

        # get first word of message
        first_word = text[0]
        # get punctuation
        last_word = text[-1][-1]

        if first_word in question_words or last_word == '?':
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
        filename = 'partial_credits.csv'
        filepath = self.log_directory + '/' + filename

        with open(filepath, mode='w', encoding='utf8') as zoom_log_file:
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
        filename = 'inappropriate_chats.csv'
        filepath = self.log_directory + '/' + filename

        with open(filepath, mode='w', encoding='utf8') as zoom_log_file:
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
            start = self.get_start_time()
        if not end:
            end = self.get_end_time()

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

    def get_student_list(self):
        """
        return a list of students in the class (might missing some students since
        not everyone uses chat)
        """
        student_set = {message_obj['student_name'] for message_obj in self.all_messages}

        return list(student_set)

    def get_start_time(self):
        """
        return time of first message in the lecture
        """
        return self.all_messages[0]['message_time']

    def get_end_time(self):
        """
        return time of last message the lecture
        """
        return self.all_messages[-1]['message_time']

    def create_log_directory(self, chatfile):
        """
        create directory for logs
        """

        def get_filename_from_directory(directory):
            head, tail = ntpath.split(directory)
            return tail or ntpath.basename(head)

        chatfile_name = get_filename_from_directory(chatfile).split('.')[0]
        directory = f'./zoom_logs/{chatfile_name}'
        directory_uniq = 1

        while os.path.exists(directory):
            directory = f'{directory}_({directory_uniq})'
            directory_uniq += 1

        try:
            # create directory zoom_logs if not exist
            os.mkdir(directory)
        except OSError:
            # the directory has already existed
            pass

        return directory
