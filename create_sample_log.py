import re
import random
import sys
def main():
  if len(sys.argv)!=2 and len(sys.argv)!=3 :
    print "usage: python samplecreator.py <file-to-read> [--answers]"
    sys.exit(1)
  flag=False
  if len(sys.argv)==3 and sys.argv[2]=='--answers':
    flag=True
  createsample(sys.argv[1],flag)

def createsample(filename,answerflag=False):
  fin=open(filename,"r")
  fout=open(filename[:-4]+'_sample.txt',"w")
  while 1:
    line=fin.readline()
    if not line: break
    match=re.search(r"\[\d\d:\d\d\] <(\S+)>",line)
    if match and random.randint(1,10)==1:
      line=line.replace(match.group(1),'$$$')
      if answerflag:line+='\n\n\n\n\n\n\n\nanswer='+match.group(1)+'\n\n\n'
    fout.write(line)
  fin.close()
  fout.close()

if __name__=='__main__':
  main()
  
