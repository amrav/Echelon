import re
import sys
import nltk
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import parse_input

dict_file = open("Dictionary.txt")
dictionary = set(word.strip().lower() for word in dict_file)

alg_lambda = 2

params = []
ranges = []
steps = []

params += [11] #search_scope
ranges += [(1,20)]
steps += [1]



def check_correct(statements, pos, search_scope):
    for stat in statements[pos+1:pos+search_scope+1]:
        match = re.match(r"(^\*.+)|(^s/.+/.+)", stat.text_str)
        if match:
            match = match.group()
            ##print 'CORRECTION:', match 
            return stat.issued_by
    return None

def check_typo(statements, pos, search_scope):
    stats = statements[pos-search_scope:pos]
    stats.reverse()
    for stat in stats:
        for word in nltk.word_tokenize(stat.text_str):
            word = word.strip('.').strip("'").lower()
            if len(word) > 3 and word not in dictionary and word not in [user.lower() for user in parse_input.statement.users]:
                return stat.issued_by
    return statements[pos-1].issued_by

def run(statements):
    search_scope = params[0]
    
    for i in range(len(statements)):
        stat = statements[i]
        stat.alg_lambda = {}
        ##stat.print_details()
        if stat.issued_by == '$$$':
            user = check_correct(statements, i, 1)
            if user:
                stat.alg_lambda[user] = alg_lambda
                continue
            for word in nltk.word_tokenize(stat.text_str):
                word = word.strip('.').strip("'").lower()
                ##print word
                if len(word)<=3:
                    continue
                if word not in dictionary and word not in [user.lower() for user in parse_input.statement.users]:
                    ##print 'Incorrect:', word
                    user = check_correct(statements, i, search_scope) 
                    if user and user != '$$$':
                        ##print 'Corrected by:', user
                        stat.alg_lambda[user] = alg_lambda
                
            match = re.match(r"(^\*.+)|(^s/.+/.+)", stat.text_str)
            if match:
                match = match.group()
                ##print 'Correction:', match
                user = check_typo(statements, i, search_scope)
                if user:
                    ##print 'Mistake made by:',  user
                    stat.alg_lambda[user] = alg_lambda
            ##print stat.alg_lambda
