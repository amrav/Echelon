from __future__ import division
import re
import math

class user:
    def __init__(self):
        self.words = {}
    
params = []
ranges = []
steps = []

params += [5] #match_threshold
ranges += [(5,15)]
steps += [2]

params += [80] #lambda_threshold
ranges += [(20,99)]
steps += [5]

def build_user_words(statements):
    users = {}
    for stat in statements:
        if stat.issued_by != '$$$':
            if stat.issued_by not in users:
                users[stat.issued_by] = user()
            matches = re.findall(r"\W?(\w+)\W?", stat.text_str)
            for match in matches:
                if len(match)>3:
                    ##print users[stat.issued_by]
                    if match not in users[stat.issued_by].words:
                        users[stat.issued_by].words[match] = 0
                    users[stat.issued_by].words[match] += 1
    return users

def run(statements):

    match_threshold = params[0]
    lambda_threshold = params[1]/100

    users = build_user_words(statements)
    
    ''' for luser in users:
        maxes = sorted(users[luser].words, key = lambda x: users[luser].words[x], reverse=True)[:5]
        print luser, ':',
        for max in maxes:
            print max, users[luser].words[max], ';' ,
        print'''

    userscore = {}
    for stat in statements:
##        stat.print_details()
        matches = re.findall(r"\W?(\w+)\W?", stat.text_str)
        if stat.issued_by == '$$$':
            userscore = {}
            for luser in users:
                for match in matches:
                    if len(match) > 3 and match in users[luser].words and users[luser].words[match] > match_threshold:
                        if luser not in userscore:
                            userscore[luser] = 0
                        userscore[luser] += users[luser].words[match]

            if len(userscore) != 0:
                avg = sum([math.log(x) for x in userscore.values()])
                avg /= len(userscore)
                if avg != 0:
                    for luser in userscore:
                        sc = math.log(userscore[luser])/avg
                        if sc != 0:
                            stat.alg_lambda[luser] = sc
                else:
                    stat.alg_lambda[luser] = {}
            else:
                stat.alg_lambda = {}

            maxes = sorted(stat.alg_lambda.values(), reverse = True)
            if len(maxes) >= 2:
                ##print maxes[1]/maxes[0]
                if maxes[1]/maxes[0] > lambda_threshold:
                    stat.alg_lambda = {}



            


                
    
