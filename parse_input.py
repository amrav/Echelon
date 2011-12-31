import sys
import nltk
import re

global chatlog_nltk 
global chatlog_words
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
    return cleantext_str.split(' ')
    

def tokenize (filename):
    '''tokenize the text at filename''' 
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

#def build_user_list_special (chatlog_words) :
 #   for i in range(len(chatlog_words-10)):
  #      if chatlog_words[i] == '*':
   #         if chatlog_words[i+1] == '*' and chatlog_words[i+2] == '*':
                
        

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python parse_input filename"
        #sys.exit(1)
    else:
        filename = sys.argv[1]
    #tokenize(filename)

    

