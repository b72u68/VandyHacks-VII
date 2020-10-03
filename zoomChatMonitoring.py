

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

        self.student_messages = {}
        # student_questions: {student_name: [{message_time: str, questions: str}]}
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
