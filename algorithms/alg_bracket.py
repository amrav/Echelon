from __future__ import division
import re

params = []
ranges = []
steps = []

params +=  [1] #stat_scope: number of statements after the unknown statement which the algorithm will look at
ranges += [(1, 5)]
steps += [1]

params += [0] #text_scope: maximum number of letters after which bracket can start
ranges += [(0,10)]
steps += [3]

params += [1] #time_diff: roughly, the number of minutes after which the bracket can appear
ranges += [(0,2)]
steps += [1]

user_lambda = 60


def run(statements):
    stat_scope = params[0]
    text_scope = params[1]
    time_diff = params[2]
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
