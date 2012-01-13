from __future__ import division
from math import log
import sys
import re
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
##print sys.path
import parse_input

params = []
ranges = []
steps = []


params += [5]  #issue_scope
ranges += [(1,10)]
steps += [1]

params += [5] #scope_weight
ranges +=  [(1,10)]
steps += [1]

params += [3] #scope_weight_minus
ranges += [(0,10)]
steps += [1]

class context_statement(parse_input.statement):
    scope = {}
    #for debugging:
    def set_curr_users(self, curr_users):
        self.curr_users = curr_users
    def print_details(self):
        parse_input.statement.print_details(self)
        print "Current Users: ", self.curr_users
        if self.alg_lambda != {}:
            print "Algorithm lambdas: ", self.alg_lambda
        print 
        print
        print

def run_alg(statements):
    #inititalise parameters
    issue_scope = params[0]
    scope_weight = params[1]
    scope_weight_minus = params[2]
#function that runs the line context algorithm      
    for stat in statements:
        #assign user_lambdas if required:
        if stat.issued_by == '$$$':
            stat.alg_lambda = {} 
            if len(context_statement.scope) == 0: #if nothing is in scope, no guesses may be made
                continue
            else:
                ##print context_statement.scope.values()
                avg = sum([log(value) for value in context_statement.scope.values()])
                avg /= len(context_statement.scope)
            ##print avg

            for user in context_statement.scope: #Normalise the scope scores by dividing by the average
                if avg != 0:
                    stat.alg_lambda[user] = log(context_statement.scope[user])/avg
                ##print stat.alg_lambda[user],
            ##print
        #Otherwise update scope
        elif stat.issued_by not in context_statement.scope:
            context_statement.scope[stat.issued_by] = scope_weight*issue_scope
        else:
            context_statement.scope[stat.issued_by] += scope_weight
        
        #list of users fallling out of scope
        popped_users = []
        for user in context_statement.scope:
            context_statement.scope[user] -= scope_weight_minus
            if context_statement.scope[user]<=0:
                popped_users.append(user)
        for user in popped_users:
            context_statement.scope.pop(user)
        #for debugging
        stat.curr_users = context_statement.scope.items()
        
        
    

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
    run(statements)
    for stat in statements:
        ##if stat.issued_by == '$$$':
        stat.print_details()
