import argparse
import os
from zoomChatMonitoring import ZoomChatMonitoring

def parse_args():
    parser = argparse.ArgumentParser(description='Zoom Chat Monitoring for student extra credits')
    parser.add_argument('chatfile', help='Add chat file directory for monitoring')
    parser.add_argument('-m', '--monitor', help='(Monitoring mode) Monitoring student chat for partial credit. Default value = 1, change to 0 to turn off mode', type=int, default=1)
    parser.add_argument('-bw', '--badwords', help='(Monitoring mode) Include file contains inappropriate words', default='./default_word_files/badWords.txt')
    parser.add_argument('-fw', '--filterwords', help='(Monitoring mode) Include file contains words to filter messages', default='./default_word_files/filterWords.txt')
    parser.add_argument('-s', '--search', help='(Search mode) Search student messages in given time. Default value = 0, change to 1 to use Search mode', type=int, default=0)
    parser.add_argument('-n', '--name', help='(Search mode) Enter student name to search', type=str, default='')
    parser.add_argument('-st', '--start', help='(Search mode) Start time. Format: hh:mm:ss', type=str, default='')
    parser.add_argument('-e', '--end', help='(Search mode) End time. Format: hh:mm:ss', type=str, default='')
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

    # check if user select monitor mode
    if args.monitor == 1:
        chat_monitoring.read_chat_file()

    # check if user select search mode
    if args.search == 1:
        print('[+] Search result: ')
        print(chat_monitoring.search_messages(args.name, args.start, args.end))

if __name__ == '__main__':
    main()
