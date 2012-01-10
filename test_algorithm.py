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
    test_alg.run(statements)
    for i in range(len(statements)):
        if statements[i].issued_by == '$$$':
            print '-------------------------'*3
            print test_alg 
            print '-------------------------'*3
            print
            for stat in statements[i-display_scope:i+1]:
                stat.print_details(full_text=True)
            answer = ''
            for user in stat.alg_lambda:
                if stat.alg_lambda[user] == max(stat.alg_lambda.values())\
and user!='$$$':
                    answer = user
                    break
            print "Replacing $$$ by", answer
            print stat.alg_lambda
            print
    
