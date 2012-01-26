from __future__ import division
import sys
import re
import parse_input


# Test algorithm for usage of emoticons

userlist = {}
emoticons = [':D',':P',':[)]',':[/]' , ':[|]' , ';[)]' , ':0' ,':O']  #add list of emoticons to track in regular expression form
curr_users = {}

params = []
ranges = []
steps = []


params +=  [6] #uplimit
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
    for emoticon in emoticons:
      self.emo[emoticon]=0 

def emoticons_search (statements, downlimit, uplimit):

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
            if curr_users[usr].emo[emoticon] != 0:
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
  



