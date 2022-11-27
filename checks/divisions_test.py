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

# succ = [None, {2,3,4},{4,6,10},{6},{8,12}, {10},{12},None,{16}]
rp = itertools.repeat

succ2 = [None,
         {(2,2),(3,3),(4,4)},
         {(4,2),(6,3),(10,5)},
         {(6,2)},
         {(8,2),(12,3)},
         {(10,2)},
         {(12,2)},
         None,
         {(16,2)}]


# succ2 = [None,
#          {rp(2,2),rp(3,3),rp(4,4)},
#          {rp(4,2),rp(6,3),rp(10,5)},
#          {rp(6,2)},
#          {rp(8,2),rp(12,3)},
#          {rp(10,2)},
#          {rp(12,2)},
#          None,
#          {rp(16,2)}]

succ2 = [None,
         {(2,2),(3,3,3),(5,5,5,5,5)},
         {(4,4),(6,6,6),(10,10,10,10,10)},
         {(6,6)},
         {(8,8),(12,12,12)},
         {(10,10)},
         {(12,12)},
         None,
         {(16,16)}]



succ2 = [None,
         {(2,2),(3,3,3),(5,5,5,5,5), (4,2,4),(6,3,3,6),(6,3,6,3),(3,6,3,6),(10,5,5,5,5,10)
          ,(10,5,10,5,10,5,10)},

         {(4,4),(6,6,6),(10,10,10,10,10),(8,4,8),(12,6,6,12),(12,6,12,6),(6,12,6,12),(20,10,10,10,10,20)
          ,(20,10,20,10,20,10,20)},
         {(6,6),(12,6,12)},
         {(8,8),(12,12,12),(16,8,16)},
         {(10,10)},
         {(12,12)},
         None,
         {(16,16)}]


# succ = [None, {2,3,4},{4,6,10},{6},{8,12}, {10},{12},None,{16},
#         None, {20}, None, {24}, None, None, None, {32},
#         ]
# succ.extend(itertools.repeat(None,16))
succ2.extend(itertools.repeat(None,16))
pat_lst=[[1],[4,2,4],[8,4,8,2],[2,8,4,8],[4,8,4,8,4],[6,3,3,6],[10,5,5,5,5,10],
         [10,5,10,5,10,5,10]
         ]

pat_lst=[[1]]


for (pat_idx,pattern) in enumerate(pat_lst):  # better use enum here
  # print(f"pat_idx={(pat_idx,pattern)}, {pat_lst}")
  for (el_idx, element) in enumerate(pattern):
    # print(f"---pat_lst={pat_lst}")
    # print(f"---el_idx={(el_idx, element)}")
    # if not succ[element]:
    if not succ2[element]:
      continue
    # for (succ_idx, succesor) in enumerate(succ[element]):
    for (succ_idx, succesor) in enumerate(succ2[element]):
      # print(f"------pat_lst={pat_lst}")
      # print(f"------{pattern}, {(el_idx,element)}, {succesor}")
      # print(f"------succ_idx={(succ_idx,succesor)}")
      xp = pattern.copy()
      del xp[el_idx]
      # print(f"succ:{succesor}/el:{element}={succesor/element}")
      # xp.insert(el_idx,list(itertools.repeat( succesor,int(succesor/element))))
      # for x in itertools.repeat( succesor,int(succesor/element)):
      #   xp.insert(el_idx,x)
      # for x in list(rp(*succesor)):
      # a = list(succesor)
      # b = list(succesor)
      # succesor, succesor_copy = itertools.tee(succesor)
      for x in succesor:
          xp.insert(el_idx, x)
      # succesor.reset()
      # xp.insert(el_idx,15)
      # print(f"-------push xp:{xp}")
      # print(f"-------pat_lst:{pat_lst}")

      if xp not in pat_lst:
        pat_lst.append(xp)
print('-------------')
# pprint.pprint(pat_lst, map(1/x,pat_lst[]))
pprint.pprint(
  [(len(pat), pat, sum(map(lambda x: pow(x, -1),pat))) for pat in pat_lst ]
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