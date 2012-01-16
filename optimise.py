from __future__ import division
import sys
import parse_input
from create_test_log import createlog
from settings import opt_alg
from settings import opt_runs

runs = opt_runs

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
        
def findmax(filename, alg, printmax = True, result_filename = ''):
    ##print 'FINDMAX!'
    stats = {}
    count = 1
    all_stats = {}
    print 'Building parameter permutations...',
    param_perms = vary(alg.ranges, alg.steps)
    print 'Done.'
    print 'Loading chatlog...',
    logtextfile = open(filename)
    logtext = logtextfile.read()
    ##print logtext
    logtextfile.close()
    print 'Done.'
    print 'Looping through parameter permutations. '
    for param_perm_num in range(len(param_perms)):
        param_perm = param_perms[param_perm_num]
        print '\rTesting with parameters', param_perm, '.........', int((param_perm_num+1)*100/len(param_perms)), '%'
        
        stats['correct']=stats['unanswered']=stats['total']=0
        if printmax != True:
            print
            print
            print '----------'*4
            print 'Run', count, ': Testing with parameters,', param_perm
            print '----------'*4
        
        alg.params = param_perm
        
        for i in range(runs):
            texts = createlog(filetext = logtext) #returns a list of the test text and the answer text
            ##print 'Created logfile'
            ##print texts[1]
            ##print 'End print'
            run_stats = check(texts[0], texts[1], alg)
            stats['correct'] += run_stats['correct']
            stats['unanswered'] += run_stats['unanswered']
            stats['total'] += run_stats['total']
            if (i+1) % 13 == 0:
                sys.stdout.write('\rRun {0} of {1}.........{2}%'.format((i+1), runs, int((i+1)*100/runs)))
                sys.stdout.flush()
            i += 1
        sys.stdout.write('\r                                              \r{0} runs done.'.format(runs))
        sys.stdout.flush()
        print
        if stats['total'] != 0:
            stats['correct'] *= 100 / stats['total']
            stats['unanswered'] *= 100 / stats['total']
        
            if stats['unanswered'] != 100 and stats['correct'] not in all_stats:
                all_stats[str(param_perm)] = str(stats['correct']*100/(100-stats['unanswered'])) + ' % success, ' + str(stats['correct']) + ' % correct, ' + str(100-stats['correct']-stats['unanswered']) + \
' % wrong, ' + str(stats['unanswered']) + ' % unanswered, ' + str( stats['total']) + ' total. ' + \
'\nRun ' + str(count) + ': Testing with parameters, ' + str(param_perm) + '\n'
        
            ##print all_stats
        
        ##print all_stats[stats['correct']]

        if printmax != True:
            if stats['unanswered'] == 100:
                print 'None attempted.'
            else:
                print stats['correct'], '% correct,', 100-stats['correct']-stats['unanswered'], '% wrong,', stats['unanswered'], '% unanswered,', stats['total'], 'total,', \
stats['correct']*100/(100-stats['unanswered']), '% success.'
        count += 1
    
    print
    if printmax == True and result_filename != '':
        result = open(result_filename, 'w')
        result.write('''-----------------------------------------------------------------------
        
        
RESULTS
        
        
-----------------------------------------------------------------------\n\n''')
        result.write("Testing the file " + filename + '\n')
        result.write("Algorithm: " + str(alg)+'\n')
        result.write("Ranges: " + str(alg.ranges) + '\n')
        result.write("Steps: " + str(alg.steps) + '\n\n')
        
        for stat in sorted(all_stats, key=lambda x: float(all_stats[x][:3]), reverse = True):
            
            result.write(all_stats[stat]+'\n')
        result.close()

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
    if len(sys.argv) < 2:
        print 'Usage: python optimise.py filename [resultfilename]'
        sys.exit(1)
    if len(sys.argv) == 3:
        findmax(sys.argv[1], opt_alg, printmax = True, result_filename = sys.argv[2])
    else:
        findmax(sys.argv[1], opt_alg, printmax = True)


        
