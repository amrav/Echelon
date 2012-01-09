import sys
import parse_input
import settings


def run(filename='', alg_list=[]):
    '''Takes a list of algorithms and assigns final probabilities to each 
statement in statements

Each module in alg_list must contain a function called final_alg_probability. 
This function takes the list of statements, the statement number as 
arguments, and should return a probability dictionary for users.''' 
    
    statements = parse_input.init(filename)
    for stat_no in range(len(statements)):
        stat = statements[stat_no]
        if stat.issued_by == '$$$':
            for alg in alg_list:
                alg_prob = alg.final_alg_probability(statements, stat_no)
                for user in alg_prob:
                    if user not in stat.final_prob:
                        stat.final_prob[user]=1
                    stat.final_prob[user] *= (alg_prob[user]) 
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
        
                
                    
