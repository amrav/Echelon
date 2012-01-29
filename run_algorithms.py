from __future__ import division
import sys
import parse_input
from settings import alg_list
from settings import next_display_scope
from settings import prev_display_scope

class final_prob_statement(parse_input.statement):
    def init(self):
        self.final_lambda = {}
        self.alg_lambdas = {}
    
def run(logtext, answertext, alg_list):
    
    '''Takes a list of algorithms and assigns final probabilities to each 
statement in statements

Each module in alg_list must contain a function called run(). 
This function takes the list of statements as an argument and should 
populate a probability dictionary for users.

For more information, refer to the Readme.''' 
    
    if answertext:
        answers = answertext.split('\n')
    deleted_nicks = 0
    correct = 0
    wrong = 0
    unanswered = 0
    answer_list = []

    print '-----------------'*12
    print
    print 'Test using', alg_list
    print
    print '-----------------'*12
    print 
    print 

    statements = parse_input.init(text=logtext)
    final_statements = []
    for stat in statements:
        stat.__class__ = final_prob_statement
        stat.init()
        final_statements.append(stat)
        
    
    for alg in alg_list:
        for stat in statements:
            stat.alg_lambda = {}
        alg.run(statements)
        for i in range(len(statements)):
            final_statements[i].alg_lambdas[str(alg)] = statements[i].alg_lambda
            

    for i in range(len(final_statements)):
        stat = final_statements[i]
        if stat.issued_by == '$$$':
            deleted_nicks += 1
            for st in final_statements[(i-prev_display_scope):i+next_display_scope+1]:
                st.print_details()
                print
            for alg in alg_list:
                print
                print alg
                print stat.alg_lambdas[str(alg)]
                print
                for user in stat.alg_lambdas[str(alg)]:
                    if user not in stat.final_lambda:
                        stat.final_lambda[user]=1
                    stat.final_lambda[user] *= (stat.alg_lambdas[str(alg)][user])
            print 'Final Decision:',
            print stat.final_lambda
            print
            if len(stat.final_lambda)>0:
                answer = sorted(stat.final_lambda, key=lambda x: stat.final_lambda[x], reverse=True)[0]
            else:
                answer = ''
            answer_list.append(answer)
            if answer != '' and stat.final_lambda[answer]!=0:
                print 'Replacing $$$ by', answer
            else:
                print 'Leaving unanswered.'
            print
            if answertext:
                print 'Correct answer: ', answers[deleted_nicks-1]
                if answer == '':
                    unanswered += 1
                elif answer == answers[deleted_nicks-1]:
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
    if answertext:
        success = correct*100/(correct+wrong)
        score = 3*correct - wrong
        correct *= 100/deleted_nicks
        wrong *= 100/deleted_nicks
        unanswered *= 100/deleted_nicks


        print '----------------------'
        print 'RESULT:'
        print '----------------------'
        print
        print success, '% success,', correct, '% correct,', wrong, '% wrong,', unanswered, '% unanswered,', deleted_nicks, 'total.'
        print 'Score:', score
        print
    
    else:
        output = open("Output.txt", 'w')
        for ans in answer_list:
            print ans
            output.write(ans+',')
        output.close()
            

if __name__ == '__main__':
    if len(sys.argv)<2:
        print "Usage: python run_algorithms.py [--answers] test_filename"
        sys.exit(1)
    #print type(sys.argv[1])
    test_text = open(sys.argv[2]).read()
    if len(sys.argv) == 3 and sys.argv[1] == '--answers':
        answer_text = open(sys.argv[2][:-8]+'answers.txt').read()
        run(test_text, answer_text, alg_list)
    elif len(sys.argv) == 2:
        run(test_text, '', alg_list)
    else:
        print "Usage: python run_algorithms.py [--answers] test_filename"
        
                
                    
