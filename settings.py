import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'algorithms/')))

import line_context
import bracket
import addressal
import user_words
import typo
import emot

#for test_algorithm.py
prev_display_scope = 4
next_display_scope = 4

alg_list = [line_context, bracket, addressal, user_words, typo, emot]
test_alg = emot
opt_alg = emot
opt_runs = 100

