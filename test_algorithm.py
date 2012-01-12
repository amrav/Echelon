from __future__ import division
import sys
import settings
import parse_input
import re

display_scope = 3

if __name__ == '__main__':
    
    help_text = '''
Usage: python test_algorithm.py [options] filename
--online : Show users online.
--help : Display usage.
'''
    
    if len(sys.argv)<2:
        print help_text
        sys.exit(1)
        
    if sys.argv[1] == '--help':
        print help_text
        sys.exit(0)

    show_online = False
    #command line options

    if len(sys.argv)>2:
        for option in sys.argv[1:-1]:
            if option == '--online':
                show_online = True
            if option == '--help':
                print help_text
                sys.exit(0)
            else:
                print "Invalid option."
                print help_text
                sys.exit(1)
    
    from settings import test_alg
    
    statements = parse_input.init(sys.argv[1])
    answers_file=open(sys.argv[1][:-8]+'answers.txt','r') #opening the corresponding _answers.txt file 
    deleted_nicks=0 #counts how many $$$s were there
    correct_answers=0 #counts how many the algorithm got correct
    test_alg.run(statements)
    for i in range(len(statements)):
        if statements[i].issued_by == '$$$':
            deleted_nicks+=1
            print '-------------------------'*3
            print test_alg 
            print '-------------------------'*3
            print
            for stat in statements[i-display_scope:i+1]:
		print
                stat.print_details(full_text=True, online = show_online)
		print
            answer = ''
            stat = statements[i]
            for user in stat.alg_lambda:
                if stat.alg_lambda[user] == max(stat.alg_lambda.values())\
and stat.alg_lambda[user]!=0:
                    answer = user
                    break
            print "Replacing $$$ by", answer
            correct_answer=answers_file.readline()[:-1] #to remove the \n
            if correct_answer==answer:
                correct_answers+=1
                print "Answer is correct."
            else :
                print "Answer is wrong. Correct answer was ", correct_answer
            print
            print stat.alg_lambda
            print
            print 'Success percentage so far:', correct_answers*100/deleted_nicks
            print
            print
    print '----------------------'*3
    print "Final success percentage :", correct_answers*100/deleted_nicks
    print correct_answers,"out of", deleted_nicks
    print '----------------------'*3
    print
