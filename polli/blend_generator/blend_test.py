from itertools import islice
import random
import math
import re


l1 = 'Mei greeted'
l2 = 'NULL ({ }) Mei ({ 1 }) le ({ 2 }) saludo ({ })'

#l1 = 'Cesar greeted me and I said hi'
#l2 = 'NULL ({ }) Cesar ({ }) me ({ 1 }) saludo ({ 2 }) y ({ 3 }) yo ({ 4 }) lo ({ 5 }) salude ({ 6 7 })'

'''
align_toks = re.findall(r'(.*?) \(\{([\d ]+)\}\)', l2)
align_toks = [[t[0].strip(), t[1].strip(), False] for t in align_toks]
for t in align_toks:
    t[1] = [int(j) for j in t[1].split(' ')] if t[1] != '' else []

print align_toks

l1_parts = l1.split(' ')
blends = []

for i in range(len(l1_parts)):

    blends.append({
        'l1': l1_parts[i],
    })

    t_index = None
    for j in range(len(align_toks)):
        if align_toks[j][1] != '' and (i+1) in align_toks[j][1]:
            align_toks[j][2] = True
            t_index = j
            blends[i]['l2'] = align_toks[j][0] if align_toks[j][0]!='NULL' else ''

    # Check Item to the Right
    if t_index is not None and t_index < (len(align_toks) - 1):
        if not align_toks[t_index + 1][1] and align_toks[t_index + 1][2] == False:
            align_toks[t_index + 1][2] = True
            blends[i]['l2'] += ' {}'.format(align_toks[t_index + 1][0])

    # Check Item to the Left
    if t_index is not None and (t_index - 1) > 0:
        if not align_toks[t_index - 1][1] and align_toks[t_index - 1][2] == False:
            align_toks[t_index - 1][2] = True
            blends[i]['l2'] = '{} {}'.format(align_toks[t_index - 1][0], blends[i]['l2'])

print blends
'''

# Generate Blends

# Attempt 1
BLEND_LEVELS = 5

blends = [{'l2': 'Cesar me', 'l1': 'Cesar'}, {'l2': 'saludo', 'l1': 'greeted'}, {'l2': 'y', 'l1': 'and'}, {'l2': 'yo', 'l1': 'I'}, {'l2': 'deje', 'l1': 'said'}, {'l2': 'uste', 'l1': 'you'},
          {'l2': 'eres', 'l1': 'are'}, {'l2': 'una persona', 'l1': 'a person'}, {'l2': 'que', 'l1': 'that'}, {'l2': 'I like', 'l1': 'me gusta'}, {'l2': 'mucho', 'l1': 'a lot'}]

for b in blends:
    b['blend_level'] = random.randint(1, BLEND_LEVELS)

print blends