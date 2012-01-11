'''This module takes the name of a chat log file, and an optional --answers flag, and creates two files, which follow the name
of the log file, appended by '_test' and '_answers'. The test file contains the log file with nicknames randomly replaced by
'$$$'. The answers file contains the user names that were deleted, in the same order, seperated by newlines.'''

import re
import random
import sys


  
def createlog(filename, answerflag = False):
  
  log = open(filename,"r")
  test_filename = re.search(r"(.*)\.", filename).group(1)
  test_file = open(test_filename+'_test.txt',"w")
  if answerflag == True:
    answers = open(test_filename+'_answers.txt','w')
  
  line = log.readline()
  
  while line:
    match=re.search(r"\[\d\d:\d\d\] <(.+?)>",line)
    if match!=None and random.randint(1,20)==1:
      line=line.replace(match.group(1),'$$$')
      if answerflag == True:
        answers.write(match.group(1)+'\n')
    test_file.write(line)
    line=log.readline()

if __name__=='__main__':
  
  if len(sys.argv)<2:
    print "Usage: python create_test_log.py [--answers] <filename>"
    sys.exit(1)
  
  if len(sys.argv)==3 and sys.argv[1]=='--answers':
    createlog(sys.argv[2],answerflag=True)
  else:
    createlog(sys.argv[2])



  


