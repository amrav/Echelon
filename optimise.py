from __future__ import division
import sys
import parse_input
from create_test_log import createlog
from settings import opt_alg

runs = 100

def check(testfile_text, answerfile_text, alg):
    stats = {} #stats[0] = answered, stats[1] = unanswered, stats[2] = total
    stats[0] = stats[1] = stats[2] = 0
    ##print testfile_text[:50]
    statements = parse_input.init(text = testfile_text)
    ##print statements[1:3]
    for stat in statements:
        stat.alg_lambda = {}
    alg.run(statements)
    answers = answerfile_text.split('\n')
    answer_count = -1
    
    for i in range(len(statements)):
        stat = statements[i]
        if stat.issued_by == '$$$':
            ##stat.print_details()
            answer_count += 1
            stats[2] += 1
            if stat.alg_lambda == {}:
                stats[1] += 1
                continue
            alg_answer = sorted(stat.alg_lambda, key=stat.alg_lambda.get, reverse = True)[-1]
            ##print answer, alg_answer
            if answers[answer_count] == alg_answer: 
                stats[0] += 1
            ##stat.print_details()
            ##statements[i+1].print_details()

    return stats

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python optimise.py filename'
        sys.exit(1)
    stats = {} #for storing answered, unanaswered and total
    stats[0]=stats[1]=stats[2]=0
    logtextfile = open(sys.argv[1])
    logtext = logtextfile.read()
    ##print logtext
    logtextfile.close()
    for i in range(runs):
        texts = createlog(filetext = logtext) #returns a list of the test text and the answer text
        ##print texts[0]
        ##print 'End print'
        run_stats = check(texts[0], texts[1], opt_alg)
        stats[0] += run_stats[0]
        stats[1] += run_stats[1]
        stats[2] += run_stats[2]
        i += 1
    stats[0] *= 100 / stats[2]
    stats[1] *= 100 / stats[2]
    if stats[1] == 100:
        print 'None attempted.'
    else:
        print stats[0], '% correct,', 100-stats[0]-stats[1], '% wrong,', stats[1], '% unanswered,', stats[2], 'total,', stats[0]*100/(100-stats[1]), '% success.'
        
