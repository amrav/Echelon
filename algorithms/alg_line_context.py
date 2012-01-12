from __future__ import division
import sys
import re
import parse_input


current_scope = 10
scope_weight = 4
scope_weight_minus = 5
addressed_weight = 4
inverse_recent_weight = 1

class context_statement(parse_input.statement):
    def init(self):
        self.current_users = {}
    def add_current_user(self, user,scope=0):
        self.current_users[user] = scope
    def delete_current_user(self, user):
        self.current_users.pop(user)

def run_alg(statements):
#function that runs the line context algorithm      
    
    for stat in statements:
        stat.init()
        text = ''
        for word in stat.text:
            text+=word
        address = re.match(r"(.*?):", text)
        if address != None:
            addressed_user = address.group(1)
            if addressed_user in parse_input.statement.users:
                stat.current_users[addressed_user] = \
current_scope*addressed_weight

    #update current_users list
        if stat.issued_by not in stat.current_users:
            stat.add_current_user(stat.issued_by, current_scope*scope_weight)
        for user in stat.current_users:
            stat.current_users[user]-=1*scope_weight_minus
            if stat.current_users[user]<0:
                stat.delete_current_user(user)
            
    for i in range(len(statements)):
        if statements[i].issued_by == '$$$':
            cumulative_scope = {}
            for stat in statements[(i-current_scope):i+1]:
                for user in stat.current_users:
                    scope = stat.current_users[user]
                    if user not in cumulative_scope:
                        cumulative_scope[user]=scope
                    else:
                        cumulative_scope[user]+=scope
            for user in cumulative_scope:
                if user in statements[i].current_users:
                    #This function needs to be refined. Perhaps exponential?
                    cumulative_scope[user]+=\
int(statements[i].current_users[user]\
/(scope_weight*inverse_recent_weight))#/scope_weight
            max_scope = 0
            for user in cumulative_scope:
                if cumulative_scope[user]>max_scope and user!='$$$'\
and (user+':') not in stat.text:
                    answer = user
                    max_scope = cumulative_scope[user]
            for user in cumulative_scope:
                statements[i].alg_lambda = cumulative_scope 
    for stat in statements:
        if stat.issued_by == '$$$' and stat.alg_lambda!=None and stat.alg_lambda!={}:
            avg = sum(stat.alg_lambda.values())/len(stat.alg_lambda.keys())
            #Divide by average to normalise values around 1 ?
            for user in stat.alg_lambda:
                stat.alg_lambda[user]/=avg
                #If user is referred to, his lamda becomes zero.
                if user+':' in stat.text:
                    stat.alg_lambda[user] = 0
    return statements    

def run(statements):
    #Populates alg_lamda in each statement
    for stat in statements:
        stat.__class__ = context_statement
    run_alg(statements)
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python alg_line_context.py filename"
        sys.exit(1)
    statements = parse_input.init(sys.argv[1])
    for stat in statements:
        stat.__class__ = context_statement
    run_alg(statements)
    for stat in statements:
        if stat.issued_by == '$$$':
            stat.print_details()
