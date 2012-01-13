from __future__ import division
import re

stat_scope = 1 #number of statements after the unknown statement which the algorithm will look at
text_scope = 0 #maximum number of letters after which bracket can start
user_lambda = 60 #lambda this algorithm will assign
time_diff = 100 #roughly, the number of minutes after which the bracket can appear

def run(statements):
    for i in range(len(statements)):
        stat = statements[i]
        stat.alg_lambda = {}
        if stat.issued_by == '$$$':
            for st in statements[i+1:i+1+stat_scope]:
                diff = (st.total_time - stat.total_time)/60
                match = re.search(r'^.{0,'+str(text_scope)+r'}\(.*?\)',' '.join(st.text))
                if match != None and diff<time_diff:
                    stat.alg_lambda[st.issued_by] = user_lambda
		    ##stat.print_details(full_text=True, online=False)
		    ##st.print_details(full_text=True, online=False)	
