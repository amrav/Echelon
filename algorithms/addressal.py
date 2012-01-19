from __future__ import division
import re
import sys
import os
import math
sys.path.append(os.path.abspath(os.path.join(os.curdir + '..')))
from parse_input import statement

class user:
    def __init__(self):
        self.recent = {}
    def update(self, scope_minus):
        popped_users = []
        for luser in self.recent:
            self.recent[luser] -= scope_minus
            if self.recent[luser] == 0:
                popped_users.append(luser)
        for luser in popped_users:
            self.recent.pop(luser)

    def address(self, username, recent_scope):
        if username not in self.recent:
            self.recent[username] = 0
        self.recent[username] += recent_scope 
        

def find_addressals(text):
    users = []
    matches = re.findall(r"(.*?):", text)
    for match in matches:
        ##print match
        if match in statement.users:
            users.append(match)
    ##print users
    return users

def search_forward(statements, userscore, pos, end, recent_scope):
    
    #initialise unknown addressals, if any
    unknown_addressals = find_addressals(statements[pos].text_str)
    ##print unknown_addressals
    for i in range(pos+1,end):
        stat = statements[i]
        addressals = find_addressals(stat.text_str)
        for username in addressals:
            #inititalise each addressed username if required
            if username not in userscore:
                userscore[username] = 0
            userscore[username] += recent_scope - (i-pos) #normalise each luser's score, depending on how far from 
            ##print 'Forward addressal found! :', username, userscore[username]
#the unknown statement it is determined
            #if statement addresses the same username as the unknown statement, then award high bonus to the issuer
            if username in unknown_addressals:
                if stat.issued_by not in userscore:
                    userscore[stat.issued_by] = 1
                userscore[stat.issued_by] *= recent_scope - (i-pos)
        #if the person addressed in the unknown statement addresses a user, assign the highest score to the addressee(s)
        ##print unknown_addressals, '!!!!!!!!!!!!!!!!', stat.issued_by
        for luser in unknown_addressals:
            ##print luser
            if stat.issued_by == luser:
                for u in addressals:
                    userscore[u] *= pow(recent_scope- (i-pos),3)
                    
                    ##print "Found Answer!!!!", stat.issued_by, u, userscore[u]
    
def run(statements):

    recent_scope = 5
    forward_scope = 2
    scope_minus = 1

    userlist = {}
    for i in range(len(statements)):
        stat = statements[i]
        ##stat.print_details(online=False)
        #Just to be safe
        stat.alg_lambda = {}
        addressals = find_addressals(stat.text_str)
        if stat.issued_by == '$$$':
            #initialise userscore dictionary
            userscore = {}
            #for each u in any luser's recent dictionary, add his (normalised?) recent score to his userscore
            for luser in userlist:
                ##print len(userlist)
                for u in userlist[luser].recent:
                    if u not in userscore:
                        userscore[u] = 0
                    userscore[u] += userlist[luser].recent[u] / recent_scope
                    ##print 'Recent scores', u, ':', userscore[u]
            ##print'!!!!!!!!!!!!'
            ##for luser in userscore:
                ##print luser, '::', userscore[luser]
            ##print '!!!!!!!!!!!'
#initialise entry of username if not addressed before
            for username in addressals:

                #if the addressed username is in any luser's dictionary, increase (how?) luser's score
                #depending on how recently luser addressed username
                for luser in userlist:
                    if username in userlist[luser].recent:
                        if luser not in userscore:
                            userscore[luser] = 1
                        userscore[luser] *= userlist[luser].recent[username]
                        ##print 'Addressing same person.', luser, userscore[luser], 'recently = ', userlist[luser].recent[username]
                #assign high bonus to the addressed luser's recently addressed u's
                if username in userlist:
                    for u in userlist[username].recent:
                        if u not in userscore:
                            userscore[u] = 1
                        userscore[u] *= pow(userlist[username].recent[u],4)
                        ##print "Addressee's recently addressed scores: ", u, userscore[u]
            #Do search for addressals forward of the unknown statement
            search_forward(statements, userscore, i, i+forward_scope, recent_scope)
            
            #if directly addressed, set userscore to zero.
            for luser in addressals:
                userscore[luser] = 0

            ##print userscore
            if len(userscore) != 0:
                avg = sum([userscore[u] for u in userscore])/len(userscore)
                #normalise userscores by dividing by average
                if avg != 0:
                    for u in userscore:
                        userscore[u] /= avg
                        ##print u, ':', userscore[u]
                    
                    
            ##stat.alg_guess = sorted(stat.alg_lambda, key = lambda u: stat.alg_lambda[u], reverse=True)[0]""" 
            
    #finally assign these values as lambdas
            for luser in userscore:
                stat.alg_lambda[luser] = userscore[luser]

        else:
            if len(addressals)!=0:
                if stat.issued_by not in userlist:
                    userlist[stat.issued_by] = user()
                for username in addressals:
                    if username not in userlist:
                        userlist[username] = user()
                    userlist[username].address(stat.issued_by, recent_scope)
                    userlist[stat.issued_by].address(username, recent_scope)
        for u in userlist:
            userlist[u].update(scope_minus)
                
            
        ##print
        ##stat.print_details(online=False)
        ##for u in userlist:
            ##print u, ':', userlist[u].recent
        ##print stat.alg_lambda
        
        ##print statement.users
