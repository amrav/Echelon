import re

stat_scope = 1 #number of statements after the unknown statement which the algorithm will look at
text_scope = 0 #maximum number of letters after which bracket can start
user_lambda = 200000 #lambda this algorithm will assign

def run(statements):
    for i in range(len(statements)):
        stat = statements[i]
        stat.alg_lambda = {}
        if stat.issued_by == '$$$':
            for st in statements[i+1:i+1+stat_scope]:
                match = re.search(r'^.{0,'+str(text_scope)+r'}\(.*?\)',' '.join(st.text))
                if match != None:
                    stat.alg_lambda[st.issued_by] = user_lambda
