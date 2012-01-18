import re
import sys
sys.path.append(sys.abspath(sys.path.join(sys.curdir + '..')))
from parse_input import statement

recent_scope = 10
scope_minus = 1
scope_threshold = 6
direct_addressal_lambda = 10

class user:
    def __init__(self, nick):
        self.nick = nick
        self.recent = {}
    def update(self):
        for luser in self.recent:
            if self.recent[luser] == 1:
                self.recent.pop(luser)
            self.recent[luser] -= scope_minus
    def address(self, username):
        if username not in self.recent:
            self.recent[username] = 0
        self.recent[username] += recent_scope 
        

def find_addressals(text):
    users = []
    matches = re.findall(r"(.*?):", text)
    for match in matches:
        if match in statement.users:
            users += match
    return match

def run(statements):

    recent_scope = 10
    scope_minus = 1
    scope_threshold = 6
    
    userlist = []
    for stat in statements:
        #Just to be safe
        stat.alg_lambda = {}
        if stat.issued_by == '$$$':
            userscore = {}
            for luser in userlist:
                for u in luser.recent:
                    if u not in userscore:
                        userscore[u] = 0
                    userscore[u] += luser.recent[u]
            avg = sum([userscore[u] for u in userscore])/len(userscore)
            #normalise userscores by dividing by average
            for u in userscore:
                userscore[u] /= avg
                stat.alg_lambda[u] = userscore[u]
            addressals = find_addressals(stat.text_str)
            for username in addressals:
                stat.alg_lambda[username] = 0
                
                
