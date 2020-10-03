import argparse
import os
from zoomChatMonitoring import ZoomChatMonitoring

def parse_args():
    parser = argparse.ArgumentParser(description='Zoom Chat Monitoring for student extra credits')
    parser.add_argument('chatfile', help='add chat file directory for monitoring')
    parser.add_argument('-bw', '--badwords', help='include file contains inappropriate words', default='./badWords.txt')
    parser.add_argument('-fw', '--filterwords', help='include file contains words to filter messages', default='./filterWords.txt')
    return parser.parse_args()

def main():
    # check if log directory exists
    try:
        os.mkdir('./zoom_logs')
    except OSError:
        # directory already exists
        pass

    # parse user's arguments
    args = parse_args()
    chat_file = args.chatfile
    bad_word_file = args.badwords
    filter_word_file = args.filterwords

    # new monitoring
    chat_monitoring = ZoomChatMonitoring(bad_word_file, filter_word_file, chat_file)
    chat_monitoring.read_chat_file()

if __name__ == '__main__':
    main()
