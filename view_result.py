from __future__ import division
import re
import sys

class result:
    def __init__(self, success, correct, wrong, unanaswered, total, text):
        self.success = success
        self.correct = correct
        self.wrong = wrong
        self.unanswered = unanswered
        self.total = total
        self.text = text
        self.score = (3*self.correct - self.wrong)*self.total/100
    def print_details(self):
        ##self.bogus = ''
        print self.text
        print "Score: ", self.score
        print

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python view_result.py option filename'
    
    option = sys.argv[1]
    result_text = open(sys.argv[2]).read()
    results = []
    header = re.search(r"(?s)(.*)>>>", result_text).group(1)
    ##print header
    matches = re.findall(r"(.*\n.*?(\d+\.\d+) % success, (\d+\.\d+) % correct, (\d+\.\d+) % wrong, (\d+\.\d+) % unanswered, (\d+) total\.)", result_text)
    for match in matches:
        success = float(match[1])
        ##print 'success=', success
        correct = float(match[2])
        wrong = float(match[3])
        unanswered = float(match[4])
        total = int(match[5])
        text = match[0]
        results.append(result(success, correct, wrong, unanswered, total, text))

    #print the header
    print header
    #now print the remaining file sorted according to the option
    if option == '--success':
        for res in sorted(results, key = lambda r: r.success, reverse=True):
            res.print_details()

    elif option == '--correct':
        for res in sorted(results, key = lambda r: r.correct, reverse=True):
            res.print_details()
            
    elif option == '--wrong':
        for res in sorted(results, key = lambda r: r.wrong, reverse=True):
            res.print_details()
            
    elif option == '--unanswered':
        for res in sorted(results, key = lambda r: r.unanswered, reverse=True):
            res.print_details()
            
    elif option == '--total':
        for res in sorted(results, key = lambda r: r.total, reverse=True):
            res.print_details()
    
    elif option == '--score':
        for res in sorted(results, key = lambda r: r.score, reverse=True):
            res.print_details()
            
    
