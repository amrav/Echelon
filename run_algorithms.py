import sys
import parse_input
import settings


class final_prob_statement(parse_input.statement):
    def init(self):
        self.final_prob = {}

def run(filename, alg_list):
    
    '''Takes a list of algorithms and assigns final probabilities to each 
statement in statements

Each module in alg_list must contain a function called run(). 
This function takes the list of statements as an argument and should 
populate a probability dictionary for users.

For more information, refer to the Readme.''' 
    
    statements = parse_input.init(filename)
    for stat in statements:
        stat.__class__ = final_prob_statement
        stat.init()
    for alg in alg_list:
        alg.run(statements)
        for stat in statements:
            if stat.issued_by == '$$$':
                for user in stat.alg_lambda:
                    if user not in stat.final_prob:
                        stat.final_prob[user]=1
                    stat.final_prob[user] *= (stat.alg_lambda[user]) 
                    ##print stat.alg_prob
                    #NEED TO ADD WEIGHTS. This function has to be looked
                    #carefully.
                    ##print user,final_prob
            

def print_decisions(statements):
    for i in range(len(statements)):
        
        if statements[i].issued_by == '$$$':
            print_range = 5
            print "--------------------------------------------------"
            print "Context:"
            for stat in statements[i-print_range:i+1]: 
                stat.print_details(full=True)
            stat = statements[i]
            for user in stat.final_prob:
             if stat.final_prob[user] == max(stat.final_prob.keys()):
                 print "Replacing $$$ by", user
            print stat.final_prob
            print
                
            

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print "Usage: python run_algorithms.py logfile"
        sys.exit(1)
    #print type(sys.argv[1])
    run('log.txt', settings.alg_list)
        
                
                    
