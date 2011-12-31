import sys
import nltk
import re

global chatlog_nltk 
global chatlog_words 
global users
global statements
#the tokenized chatlog

def clean (text):
    '''clean a raw text file and return a list of tokens'''
    cleantext_str = ''
    for line in text:
        for word in line:
            for char in word:
                if char != '\n':
                    cleantext_str+=char
                else:
                    cleantext_str+=' '
    #text = text.strip('\n') Why isn't this working instead of the above?
    matches = re.findall(r"\[([0-9][0-9]\:[0-9][0-9])\] <(.*?)> (.*)",text)
    statements = []
    users = []
    for match in matches:
        #times.append(match[0])
        users.append(match[1])
        stat = statement(match[0],match[1],match[2]) 
        statements.append(stat)
    for stat in statements:
        print stat.text
    return cleantext_str.split(' ')
   

def init (filename):
    '''tokenize the text at filename and build various global lists''' 
    #print filename
    text = open(filename,'rU').read()
    #print type(text)
    chatlog_words = clean(text)
    #print chatlog_words
    #print words2
    chatlog_nltk = nltk.Text(chatlog_words)
    #print chatlog
    #print type(tokens)
    #print type(chatlog)
    #print chatlog_nltk.concordance('He')
    #build_user_list_special(chatlog_words)

def build_user_list_special(words):
    users = []
    for i in range(len(words)):
        if words[i] == '***' and words[i+2] == 'joined':  
            if words[i+1] not in users:
                users.append(words[i+1])
            i+=3
    #for user in user_list:
     #   print user
        
#def build_statement_list(words):
    

class statement:
    def __init__(self, time, issuing_user_name, statement_text):
        self.text = statement_text
        self.issued_by = issuing_user_name
        self.time = time


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python parse_input filename"
        sys.exit(1)
    filename = sys.argv[1]
    init(filename)
    #tokenize(filename)


