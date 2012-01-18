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
statement4.total_time	 #A number that can be safely used to compare two 
			 #statements chronologically.
statement4.alg_lambda    #This is a dictionary of user names and their 
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

def init(filename='', text=''):
    if text == '':
        t = open(filename)
        text = t.read()
        t.close()
    ##print text
    matches = re.findall(r"(\[(\d\d:\d\d)\] <(.*?)> (.*))\
|(\*\*\*) (.*?) (joined|left)", text)
    ##print 'matches list made'
        
        
    users_online = []; statements = []; statement.users = []

    #for calculating total_time
    intra_minute_count = 0
    prev_minute = 0
    prev_hour = 0
    day_count = 0

        
    for match in matches:
    
        time = match[1]
        issued_by = match[2]
        statement_text = match[3]
        
        if match[0] != '':
            statement.users.append(issued_by) #append user to universal list
            #in class statement
            ##print statement.users
            #calculate the total_time variable
            match2 = re.search(r"(\d\d):(\d\d)", time)
            hours = int(match2.group(1))
            minutes = int(match2.group(2))
            
            #reset intra minute count if required
            if prev_minute != minutes:
                intra_minute_count = 0
            #increment day count if the day has changed
            if hours < prev_hour:
                day_count += 1
            #assign value to total_time
            total_time = (day_count*24*3600)+(hours*3600)+(minutes*60)+(intra_minute_count)
            #increment intra minute count
            intra_minute_count+=1
            #update prev variables
            prev_minute = minutes
            prev_hour = hours
            
            #add stat to list of statements
            stat = statement(time, total_time, issued_by,clean(statement_text), \
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
    ##print statement.users
    return statements
    
   
class statement:
    
    users = []
    def __init__(self, time, total_time, issuing_user_name, statement_text, \
users_online):
        self.text = statement_text
        self.text_str = ' '.join(self.text)
        self.issued_by = issuing_user_name
        self.time = time
        self.users_online = users_online
        self.total_time = total_time
        
        self.alg_lambda = {}
        #Probability dicitonary to be used by the algorithm
        #as convinient to it. Please ensure that the probabilities are centered
        #around one, unless you are unsure, in which case this object should 
        #be empty. The value of '1' is considered neutral. For more detailed
        #information, refer to the Readme.
        self.alg_guess = ''
        #The algorithm can store its guess here, to use for processing 
        #subsequent statements
        
        
    def print_details(self, full_text=True, online=True, current=True, total_time=True): 
        print self.issued_by + ' at ' + self.time
	print
        if full_text == False:
            for word in self.text[:5]:
                print word,
        else:
            for word in self.text:
                print word,
        print; print
        if online==True:
            print "Users online:", sorted(self.users_online)
	print
        if total_time==True:
            print "Total time:", self.total_time
	print
            

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python parse_input.py <filename>"
        sys.exit(1)
    statements = init(sys.argv[1])
    for stat in statements:
        stat.print_details()
    


