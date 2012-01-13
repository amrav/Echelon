from __future__ import division
import sys
import parse_input
from create_test_log import createlog
from settings import opt_alg

runs = 300

def check(testfile, answerfile, alg):
    stats = {} #stats[0] = answered, stats[1] = unanswered, stats[2] = total
    stats[0] = stats[1] = stats[2] = 0
    statements = parse_input.init(testfile)
    for stat in statements:
        stat.alg_lambda = {}
    alg.run(statements)
    answers_file = open(answerfile, 'r')
    answers = answers_file.read().split('\n')
    answers_file.close()
    answer_count = -1
    for stat in statements:
        if stat.issued_by == '$$$':
            answer_count += 1
            stats[2] += 1
            if stat.alg_lambda == {}:
                stats[1] += 1
                continue
            alg_answer = sorted(stat.alg_lambda, key=stat.alg_lambda.get, reverse = True)[-1]
            ##print answer, alg_answer
            if answers[answer_count] == alg_answer: 
                stats[0] += 1
            
    return stats

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python optimise.py filename'
        sys.exit(1)
    stats = {}
    stats[0]=stats[1]=stats[2]=0
    for i in range(runs):
        lognames = createlog(sys.argv[1], answerflag = True)
        run_stats = check(lognames[0], lognames[1], opt_alg)
        stats[0] += run_stats[0]
        stats[1] += run_stats[1]
        stats[2] += run_stats[2]
        i += 1
    stats[0] *= 100 / stats[2]
    stats[1] *= 100 / stats[2]
    print stats[0], '% correct,', 100-stats[0]-stats[1], '% wrong,', stats[1], '% unanswered,', stats[2], 'total,', stats[0]*100/(100-stats[1]), '% success.'
        
