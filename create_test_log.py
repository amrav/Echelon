'''This module takes the name of a chat log file, and an optional --answers flag, and creates two files, which follow the name
of the log file, appended by '_test' and '_answers'. The test file contains the log file with nicknames randomly replaced by
'$$$'. The answers file contains the user names that were deleted, in the same order, seperated by newlines.'''

import re
import random
import sys


  
def createlog(filename='', filetext = '', create_file = False, answerflag = False):
  
  test_text = ''
  answer_text = ''
  
  if create_file == True:
    log = open(filename,"r")
    test_filename = re.search(r"(.*)\.", filename).group(1)
    test_file = open(test_filename+'_test.txt',"w")
    filetext = open(filename).read()
    answers = open(test_filename+'_answers.txt','w')
    log.close()
  
##print filetext
  lines = filetext.split('\n')
  
  
  counter = 0
  min_lines = 10
  
  for line in lines:
    line+='\n'
    match=re.search(r"^\[\d\d\:\d\d\] <(.+?)> .+",line)
    if match != None and random.randint(1,20)==1 and counter > min_lines:
      ##print match.group(1)
      counter = 0
      ##print line
      ##print match.group(0)
      test_line = line.replace(match.group(1),'$$$')
      ##print line
      answer_text += match.group(1) + '\n'
      if create_file == True:
        answers.write(match.group(1)+'\n')
    else:
      test_line = line
    test_text += test_line
    if create_file == True:
      test_file.write(test_line)
    counter += 1
  
  if create_file == True:
    lognames = [test_file.name]
    lognames.append(answers.name)
    return lognames
  else:
    texts = [test_text]
    texts.append(answer_text)
    return texts

if __name__=='__main__':
  
  if len(sys.argv)!=2:
    print "Usage: python create_test_log.py <filename>"
    sys.exit(1)
  
  createlog(sys.argv[1], create_file=True)
  print 'Created test and answer logs.'



  


