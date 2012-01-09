from __future__ import division
import sys
import nltk
import re


#define various structures

global chatlog_nltk #Should these be global?
global chatlog_words 
global users
global statements
user_scope = {}


#define various constants

current_scope = 4
scope_weight = 3
scope_weight_minus = 5
addressed_weight = 5
inverse_recent_weight = 1

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
    text = open(filename).read()
    matches = re.findall(r"(\[([0-9][0-9]\:[0-9][0-9])\] <(.*?)> (.*))\
|(\*\*\*) (.*?) (joined|left)", text)
    
        
    global statements
    users = []; users_online = []; statements = []
    current_users = {}
    for match in matches:
        
        time = match[1]
        issued_by = match[2]
        statement_text = match[3]

        if match[0] != '':
            users.append(issued_by) #how useful is this?
            
            #direct address should reflect in current users
            address = re.match(r"(.*?):", statement_text)
            if address != None:
                addressed_user = address.group(1)
                ##print "ADRESSED USER ", addressed_user, ' ', time
                if addressed_user in users:
                    current_users[addressed_user] = \
current_scope*addressed_weight
                    ##print "WEIGHT" , current_users[addressed_user]

            
            
            #update current_users list
            current_users[issued_by]=current_scope*scope_weight
            for user in current_users:
                current_users[user]-=1*scope_weight_minus
                if current_users[user]<0:
                    current_users[user]=0
            
            #create a list of tuples of current users and 
            #scope for this statement
            stat_current_users = [(user,current_users[user]) \
for user in current_users.keys() if current_users[user]!=0]
            

            #finally add stat to list of statements
            
            stat = statement(time,issued_by,clean(statement_text), \
users_online, stat_current_users) 
            statements.append(stat)    
        
        else:
            if match[6] == 'joined':
                users_online.append(match[5])
            else:
                if match[5] in users_online:
                    users_online.remove(match[5])
    
    #remove duplicates
    users = set(users)
    
   
class statement:
    
    def __init__(self, time, issuing_user_name, statement_text, \
users_online, current_users):
        self.text = statement_text
        self.issued_by = issuing_user_name
        self.time = time
        self.users_online = users_online
        self.current_users = current_users
        
    def print_details(self, full_text=False, online=True, current=True): 
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
        if current==True:
            print "Current users:", [user for user,_ in self.current_users]
        print


def test_module1():  #ToDo: WARNING! Alters global statements list. 
#Do not use in conjunction with other functions relying on unknown statements.

    for i in range(len(statements)):
        if statements[i].issued_by == '$$$':
            cumulative_scope = {}
            print "--------------------------------------------------"
            print "Context:"
            for stat in statements[(i-current_scope):i+1]:
                stat.print_details(full_text=True,current=True, online=False)
                for user,scope in stat.current_users:
                    if user not in cumulative_scope:
                        cumulative_scope[user]=scope
                    else:
                        cumulative_scope[user]+=scope
                for user in cumulative_scope:
                    #This function needs to be refined. Perhaps exponential?
                    if len([s for u,s in statements[i].current_users \
if u==user]) == 1:
                        cumulative_scope[user]+=int([s for u,s \
in statements[i].current_users if u==user][0]/(scope_weight*\
inverse_recent_weight))#/scope_weight
            max_scope = 0
            for user in cumulative_scope:
                if cumulative_scope[user]>max_scope and user!='$$$'\
and (user+':') not in stat.text:
                    answer = user
                    max_scope = cumulative_scope[user]
                    print 
                
            print "Replacing $$$ with", answer
            print "Cumulative scopes: ", [(u,cumulative_scope[u]) for u \
in cumulative_scope]
            print
        

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python parse_input.py filename"
        sys.exit(1)
    filename = sys.argv[1]
    init(filename)
    test_module1()
    #for stat in statements:
     #   stat.print_details()
#    for stat in statements:
 #       if stat.issued_by == '$$$':
  #          print stat.issued_by, stat.time
   #         print stat.text
    #print "!!!", current_scope
    #tokenize(filename)


