'''The famous parse_input file.

The function parse_input.init() takes a filename as an argument and returns 
a list of objects of the class 'statement'. For example, if an object
'statement4' belongs to the class 'statement', all the attributes
accessible from 'statement4' are:

statement4.issued_by  #The name of the user issuing the statement.
statement4.time       #The time at which the statement was issued.
statement4.text       #The text of the statement itself, which is
                      #returned as a LIST of words.
statement4.users_online  #A list of users online at that time.
statement4.alg_prob  #This is a dictionary of user names and their 
                     #corresponding lambdas. Populate this in your
                     #algorithm.

For more information on how to use the parse_input.statement class to
write your own algorithms, please read the Readme.'''

from __future__ import division
import sys
import nltk
import re


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
    
        
        
    users_online = []; statements = []
    
    
    for match in matches:
        
        time = match[1]
        issued_by = match[2]
        statement_text = match[3]

        if match[0] != '':
            statement.users.append(issued_by) #append user to universal list
            #in class statement
            
            #add stat to list of statements
            stat = statement(time,issued_by,clean(statement_text), \
users_online) 
            statements.append(stat)    
        
        #if it is a system statement
        else:
            if match[6] == 'joined':
                users_online.append(match[5])
            else:
                if match[5] in users_online:
                    users_online.remove(match[5])
    
    #remove duplicates
    statement.users = set(statement.users)
    
    return statements
    
   
class statement:
    
    users = []
    def __init__(self, time, issuing_user_name, statement_text, \
users_online):
        self.text = statement_text
        self.issued_by = issuing_user_name
        self.time = time
        self.users_online = users_online
                
        self.alg_prob = {}
        #Probability dicitonary to be used by the algorithm
        #as convinient to it. Please ensure that the probabilities are centered
        #around one, unless you are unsure, in which case this object should 
        #be empty. The value of '1' is considered neutral. For more detailed
        #information, refer to the readme.

        
        
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
    


