import sys
import settings
import parse_input

display_scope = 5

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python test_algorithm.py filename"
        sys.exit(1)
    from settings import test_alg
    statements = parse_input.init(sys.argv[1])
    answers_file=open(sys.argv[1][:-8]+'answers.txt','r') #opening the corresponding _answers.txt file 
    deleted_nicks=0 #counts how many $$$s were there
    correct_answers=0 #counts how many the algorithm got correct
    test_alg.run(statements)
    for i in range(len(statements)):
        if statements[i].issued_by == '$$$':
            print '-------------------------'*3
            deleted_nicks+=1
            print test_alg 
            print '-------------------------'*3
            print
            for stat in statements[i-display_scope:i+1]:
		print
                stat.print_details(full_text=True)
		print
            answer = ''
            for user in stat.alg_lambda:
                if stat.alg_lambda[user] == max(stat.alg_lambda.values())\
and user!='$$$':
                    answer = user
                    break
            print "Replacing $$$ by", answer
            correct_answer=answers_file.readline()[:-1]
            if correct_answer==answer:
                correct_answers+=1
                print "Answer is correct."
            else :
                print "Answer is wrong. Correct answer was "+correct_answer
            print stat.alg_lambda
            print
    print "Success percentage :",float(correct_answers)*100/deleted_nicks
    print correct_answers,"out of",deleted_nicks
