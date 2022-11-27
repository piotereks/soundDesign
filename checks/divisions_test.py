"""
1->2,3,5

2->4,6,10

3->6
5->10
4->8,12

6->12
8->16
"""

import itertools
import pprint

succ = [None, {2,3,4},{4,6,10},{6},{8,12}, {10},{12},None,{16}]


# succ = [None, {2,3,4},{4,6,10},{6},{8,12}, {10},{12},None,{16},
#         None, {20}, None, {24}, None, None, None, {32},
#         ]
# succ.extend(itertools.repeat(None,16))

pat_lst=[[1]]

pat_lst=[[1]]


for (pat_idx,pattern) in enumerate(pat_lst):  # better use enum here
  # print(f"pat_idx={(pat_idx,pattern)}, {pat_lst}")
  for (el_idx, element) in enumerate(pattern):
    # print(f"---pat_lst={pat_lst}")
    # print(f"---el_idx={(el_idx, element)}")
    if not succ[element]:
      continue
    for (succ_idx, succesor) in enumerate(succ[element]):
      # print(f"------pat_lst={pat_lst}")
      # print(f"------{pattern}, {(el_idx,element)}, {succesor}")
      # print(f"------succ_idx={(succ_idx,succesor)}")
      xp = pattern.copy()
      del xp[el_idx]
      # print(f"succ:{succesor}/el:{element}={succesor/element}")
      # xp.insert(el_idx,list(itertools.repeat( succesor,int(succesor/element))))
      for x in itertools.repeat( succesor,int(succesor/element)):
        xp.insert(el_idx,x)
      # xp.insert(el_idx,15)
      # print(f"-------push xp:{xp}")
      # print(f"-------pat_lst:{pat_lst}")

      if xp not in pat_lst:
        pat_lst.append(xp)
print('-------------')
# pprint.pprint(pat_lst, map(1/x,pat_lst[]))
pprint.pprint(
  [(pat, sum(map(lambda x: pow(x, -1),pat))) for pat in pat_lst]
)
print('-------------')
print(len(pat_lst))

# tst_lst = [1,2,3]
# take next list
# for arch element
#   for each succ
#     create new list


# for t in tst_lst:
#   # print(t)
#   tst_lst.append(t+10)
#   if t+10>30:
#     break
# print(tst_lst)