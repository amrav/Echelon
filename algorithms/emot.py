from __future__ import division
import sys
import re
import os

#so that parse_input can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import parse_input

# Test algorithm for usage of emoticons

userlist = {}

def build_emoticons():
#build emoticons list from the Emoticons.txt file 
  emoticons = open("Emoticons.txt").read().split()
  new_emots = []
  for emot in emoticons:
  #Also include :) for :-)
    if len(emot) > 2 and emot[1] == '-':
      new_emots.append([emot[:1]+emot[2:]])

  for emo in new_emots:
    emoticons += emo
  ##print emoticons
  new_emots = []

  for emot in emoticons:
  #make sure that parenthesis are preceded by '\'
    new_emot = ''
    for i in range(len(emot)):
      letter = emot[i]
      ##print letter
      match = re.match(r"\W", letter)
      if match:
        new_emot += '\\' + letter
        ##print new_emot
      else:
        new_emot += letter
    ##print new_emot
    new_emots.append(new_emot)
  return set(new_emots)

##print emoticons

params = []
ranges = []
steps = []


params +=  [12] #uplimit
ranges += [(1, 15)]
steps += [1]




class emoticon_statement(parse_input.statement):
  scope = {}
  
  def __init__(self):
   ## self.curr_users= {}
    self.emoticon_sum = {}
   

class user:   
  def __init__(self):
    self.emo = {}
    self.statement_number = 0
      ##print 'initatiated', self.name
    

def emoticons_search (statements, downlimit, uplimit):

  emoticons = build_emoticons()

  for i in range(len(statements)):
    if statements[i].issued_by == '$$$':
      #initialise curr_users
      curr_users = {}
      #make sure that we are not very near the beginning or the end of the file
      if i> uplimit and i < len(statements)- downlimit :
        #start checking for emoticons in the specified range
        for j in range(i-uplimit , i+downlimit+1 ):       
          stat = statements[j]
          #don't using statements issued by unknown users
          if stat.issued_by != '$$$':
            #initialise if necessary
            if stat.issued_by not in curr_users:
              curr_users[stat.issued_by] = user()
            #increment the number of statements made by that user
            curr_users[stat.issued_by].statement_number += 1
            #search for any emoticons in the statement text
            for emoticon in emoticons:
              ma = re.findall(emoticon,stat.text_str)
              #if any are found, increment emo for that user for that emoticon
              if ma:
                if emoticon not in curr_users[stat.issued_by].emo:
                  curr_users[stat.issued_by].emo[emoticon] = 0
                curr_users[stat.issued_by].emo[emoticon] += len(ma)
      
      for users in curr_users:
        for emot in curr_users[users].emo:
          #normalise emo for users by dividing by number of statements made by users 
          curr_users[users].emo[emot]/= curr_users[users].statement_number
        

    
      for emoticon in emoticons:
        m = re.findall(emoticon,statements[i].text_str)
        if m:
          for usr in curr_users: #not users online it should be current users from line_context
              #print usr , curr_users[usr].emo[emoticon]
              #if curr_users[usr].emo[emoticon] > 0:
            if emoticon in curr_users[usr].emo and curr_users[usr].emo[emoticon] != 0:
              statements[i].alg_lambda[usr] = 1 + curr_users[usr].emo[emoticon]/10   # use this 10 as parameter to va'''

            
            

##def print_details():
  #for users in curr_users:
   # print users, curr_users[users].emo                
 
def run(statements):
  
  downlimit = params[0]
  uplimit = params[0]

  for stat in statements:
    stat.__class__ = emoticon_statement
  emoticons_search(statements, downlimit, uplimit)   
  ##print_details()
   
    

if __name__ == '__main__':
  run(statements)
  



