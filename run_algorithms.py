import sys
import parse_input
import settings


class final_prob_statement(parse_input.statement):
    def init(self):
        self.final_lambda = {}
        self.alg_probs = {}

def run(logtext, answertext, alg_list):
    
    '''Takes a list of algorithms and assigns final probabilities to each 
statement in statements

Each module in alg_list must contain a function called run(). 
This function takes the list of statements as an argument and should 
populate a probability dictionary for users.

For more information, refer to the Readme.''' 
    
    answers = answertext.split('\n')
    deleted_nicks = 0
    correct = 0
    wrong = 0
    unanswered = 0

    print '-----------------'*4
    print
    print 'Test', filename, 'using', alg_list
    print
    print '-----------------'*4
    print 
    print 

    statements = parse_input.init(filetext=logtext)
    
    for stat in statements:
        stat.print_details(online = False)
        if stat.issued_by == '$$$':
            deleted_nicks += 1
            for alg in alg_list:
                stat.alg_lambda = {}
                alg.run(statements)
                print
                print alg
                print stat.alg_lambda
                print
                for user in stat.alg_lambda:
                    if user not in stat.final_lambda:
                        stat.final_lambda[user]=1
                    stat.final_lambda[user] *= (stat.alg_lambda[user]) 
            print 'Final Decision:'
            print stat.final_lambda
            if len(stat.final_lambda)>0:
                answer = sorted(stat.final_lambda, key=lambda x: stat.alg_lambda[x], reverse=True)
            else:
                answer = None
            if answer != None and stat.alg_lambda:
                print 'Replacing $$$ by', answer
            else:
                print 'Leaving unanswered.'
            print
            print 'Correct answer: ', answers[deleted_nicks-1]
            if answer == None:
                unanswered += 1
            elif answer = answers[deleted_nicks-1]:
                correct += 1
            else:
                wrong += 1
            print
            print 'So far:'
            print 'Correct: ', correct
            print 'Wrong:', wrong
            print 'Unanswered:', unanswered
            print

##print stat.alg_prob
                    #NEED TO ADD WEIGHTS. This function has to be looked
                    #carefully.
                    ##print user,final_prob
    
            

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print "Usage: python run_algorithms.py test_filename"
        sys.exit(1)
    #print type(sys.argv[1])
    run(sys.argv[1], settings.alg_list)
        
                
                    
