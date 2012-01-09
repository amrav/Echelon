from __future__ import division
import sys
import nltk
import re


#define various structures

#global chatlog_nltk #Should these be global?
#global chatlog_words 
global users
#global statements
#user_scope = {}



#define various constants


def clean(text):
    '''clean raw text file and return a list of tokens'''
    cleantext_str = ''
    for line in text:
        for word in line:
            for char in word:
                if char != '\n':
                    cleantext_str+=char
                else:
                    cleantext_str+=' '
    return cleantext_str.split(' ')

def init(filename):
    t = open(filename)
    text = t.read()
    matches = re.findall(r"(\[([0-9][0-9]\:[0-9][0-9])\] <(.*?)> (.*))\
|(\*\*\*) (.*?) (joined|left)", text)
    
        
        
    users = []; users_online = []; statements = []
    
    
    for match in matches:
        
        time = match[1]
        issued_by = match[2]
        statement_text = match[3]

        if match[0] != '':
            users.append(issued_by) #how useful is this?
            
        #add stat to list of statements
            
            stat = statement(time,issued_by,clean(statement_text), \
users_online) 
            statements.append(stat)    
        else:
            if match[6] == 'joined':
                users_online.append(match[5])
            else:
                if match[5] in users_online:
                    users_online.remove(match[5])
    
    #remove duplicates
    users = set(users)
    statement.users = users
    return statements
    
   
class statement:
    
    users = []
    def __init__(self, time, issuing_user_name, statement_text, \
users_online):
        ##print "init called!"
        self.text = statement_text
        self.issued_by = issuing_user_name
        self.time = time
        self.users_online = users_online
                
        self.alg_prob = {}
        #Probability dicitonary to be used by the algorithm
        #as convinient to it. Please ensure that the probabilities are centered
        #around one, unless you are unsure, in which case this object should 
        #be empty.

        
        
    def print_details(self, full_text=False, online=True, current=True\
,probabilities = True): 
        print self.issued_by + ' at ' + self.time
        if full_text == False:
            for word in self.text[:5]:
                print word,
        else:
            for word in self.text:
                print word,
        print
        if online==True:
            print "Users online:", self.users_online
        if probabilities == True:
            if self.final_prob!={}:
                print "Final Probabilities:", self.final_prob
            else:
                print "Algorithm Probabilities:", self.alg_prob
        print

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print "Usage: python parse_input.py"
        sys.exit(1)
    #filename = sys.argv[1]
    #statements = init(filename)
    #test_module1(statements)
    #for stat in statements:
     #   stat.print_details()
#    for stat in statements:
 #       if stat.issued_by == '$$$':
  #          print stat.issued_by, stat.time
   #         print stat.text
    #print "!!!", current_scope
    #tokenize(filename)


