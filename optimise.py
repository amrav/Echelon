import sys
import parse_input
from create_test_log import createlog
from settings import opt_alg

runs = 30

def check(testfile, answerfile, alg):
    stats = {} #stats[0] = answered, stats[1] = unanswered, stats[2] = total
    stats[0] = stats[1] = stats[2] = 0
    statements = parse_input.init(testfile)
    for stat in statements:
        stat.alg_lambda = {}
    alg.run(statements)
    answers = open(answerfile, 'r')
    for stat in statements:
        if stat.issued_by == '$$$':
            stats[2] += 1
            answer = answers.readline()[:-1] #to remove the \n 
            if stat.alg_lambda == {}:
                stats[1] += 1
            elif answer == stat.alg_lambda[sorted(stat.alg_lambda, key=stat.alg_lambda.get, reverse = True)[-1]]: #if answer == max value in alg_lambda
                stats[0] += 1
    return stats

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python optimise.py filename'
        sys.exit(1)
    for i in range(runs):
        lognames = createlog(sys.argv[1], answerflag = True)
        stats = check(lognames[0], lognames[1], opt_alg)
        print stats[0], 'correct,', stats[2]-stats[0]-stats[1], 'wrong,', stats[1], 'unanswered,', stats[2], 'total.'
        i += 1
