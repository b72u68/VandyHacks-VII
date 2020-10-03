class ZoomChatMonitoring:

    def __init__(self, filter_word_file=''):
        self.filter_word_file = filter_word_file
        # filter_words: list of words to filter message (read from file)
        self.filter_words = []
        # student_messages: {student_name: {message_time: str, message: str}}
        self.student_messages = {}
        # student_questions: {student_name: {message_time: str, questions: []}}
        self.student_questions = {}

    # def read_file(self): get filter_words list

    # def check_message(self, message): return True if student message doesn't
    # contain words from filter_words, otherwise return False

    # def monitoring_messages(self): check if message is worth for credits ->
    # add to student_messages, if a question -> add to student_questions
