from __future__ import division
import sys
import parse_input
from create_test_log import createlog
from settings import opt_alg

runs = 5

def nonint_range(lower, upper, step):
    i = lower
    list = []
    while i <= upper:
        list.append(i)
        i += step
    return list

def vary(ranges, param_steps):
    if len(ranges) == 1:
        return [[i] for i in nonint_range(ranges[0][0], ranges[0][1], param_steps[0])]
    else:
        perms = []
        for perm in vary(ranges[:-1], param_steps[:-1]):
            ##print perm
            for i in nonint_range(ranges[-1][0], ranges[-1][1], param_steps[-1]):
                ##print param_steps[-1]
                perms.append(perm + [i])
        return perms
        
def findmax(testfile_text, answerfile_text, alg):
    stats = {}
    
    param_perms = vary(alg.ranges, alg.steps)
    for param_perm in param_perms:
        stats['correct']=stats['unanswered']=stats['total']=0
        print
        print
        print '----------'*3
        print 'Testing with parameters,', param_perm
        print '----------'*3
        alg.params = param_perm
        for i in range(runs):
            texts = createlog(filetext = logtext) #returns a list of the test text and the answer text
            ##print texts[0]
            ##print 'End print'
            run_stats = check(texts[0], texts[1], alg)
            stats['correct'] += run_stats['correct']
            stats['unanswered'] += run_stats['unanswered']
            stats['total'] += run_stats['total']
            i += 1
            
        stats['correct'] *= 100 / stats['total']
        stats['unanswered'] *= 100 / stats['total']
        if stats['unanswered'] == 100:
            print 'None attempted.'
        else:
            print stats['correct'], '% correct,', 100-stats['correct']-stats['unanswered'], '% wrong,', stats['unanswered'], '% unanswered,', stats['total'], 'total,', \
stats['correct']*100/(100-stats['unanswered']), '% success.'
        



def check(testfile_text, answerfile_text, alg):
    stats = {} #answered, unanswered, total
    stats['correct'] = stats['unanswered'] = stats['total'] = 0
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
            stats['total'] += 1
            if stat.alg_lambda == {}:
                stats['unanswered'] += 1
                continue
            alg_answer = sorted(stat.alg_lambda, key=stat.alg_lambda.get, reverse = True)[-1]
            ##print answer, alg_answer
            if answers[answer_count] == alg_answer: 
                stats['correct'] += 1
            ##stat.print_details()
            ##statements[i+1].print_details()

    
    return stats

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python optimise.py filename'
        sys.exit(1)
    stats = {} #for storing answered, unanaswered and total
    stats['correct']=stats['unanswered']=stats['total']=0
    logtextfile = open(sys.argv[1])
    logtext = logtextfile.read()
    ##print logtext
    logtextfile.close()
    for i in range(runs):
        texts = createlog(filetext = logtext) #returns a list of the test text and the answer text
        ##print texts[0]
        ##print 'End print'
        run_stats = check(texts[0], texts[1], opt_alg)
        stats['correct'] += run_stats['correct']
        stats['unanswered'] += run_stats['unanswered']
        stats['total'] += run_stats['total']
        i += 1
        findmax(texts[0], texts[1], opt_alg)
    stats['correct'] *= 100 / stats['total']
    stats['unanswered'] *= 100 / stats['total']
    if stats['unanswered'] == 100:
        print 'None attempted.'
    else:
        print stats['correct'], '% correct,', 100-stats['correct']-stats['unanswered'], '% wrong,', stats['unanswered'], '% unanswered,', stats['total'], 'total,', \
stats['correct']*100/(100-stats['unanswered']), '% success.'


        
