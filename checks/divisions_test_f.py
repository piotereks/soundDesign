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
import statistics
from fractions import Fraction as F

# succ = [None, {2,3,4},{4,6,10},{6},{8,12}, {10},{12},None,{16}]
rp = itertools.repeat

class DurationPatterns:
    def __init__(self):
        self.duration_patterns = None
    # allowed_successors = [None,
    #          {(2,2),(3,3,3),(5,5,5,5,5)},
    #          {(4,4),(6,6,6),(10,10,10,10,10)},
    #          {(6,6)},
    #          {(8,8),(12,12,12)},
    #          {(10,10)},
    #          {(12,12)},
    #          None,
    #          {(16,16)}]

        self.allowed_successors = [None,
                [(2,2),(3,3,3),(5,5,5,5,5), (4,2,4),(6,3,3,6),(6,3,6,3),(3,6,3,6),(10,5,5,5,5,10)
                ,(10,5,10,5,10,5,10)],

                [(4,4),(6,6,6),(10,10,10,10,10),(8,4,8),(12,6,6,12),(12,6,12,6),(6,12,6,12),(20,10,10,10,10,20)
                ,(20,10,20,10,20,10,20)],
                [(6,6),(12,6,12)],
                [(8,8),(12,12,12),(16,8,16)],
                [(10,10)],
                [(12,12)],
                None,
                [(16,16)]]

        self.allowed_successors=[[ list(map(lambda x:  F(1,x),succ)) for succ in succ_set or ()] for succ_set in self.allowed_successors] 
        # print(f"{self.allowed_successors=}")
        self.allowed_successors.extend(itertools.repeat(None,16))
        self.init_pat_lst=[[1],[4,2,4],[8,4,8,2],[2,8,4,8],[4,8,4,8,4],[6,3,3,6],[10,5,5,5,5,10],
                [10,5,10,5,10,5,10]
                ]
        # self.init_pat_lst=[[1]]
        self.init_pat_lst = [list(map(lambda x : F(1,x),pat)) for pat in self.init_pat_lst]
        # print(f"{self.init_pat_lst=}")


    def find_all_pattern_splits(self):

        for (pat_idx,pattern) in enumerate(self.init_pat_lst):  # better use enum here
            # print(f"pat_idx={(pat_idx,pattern)}")
            for (el_idx, element) in enumerate(pattern):
                # if el_idx>=2:
                #     return
                # print(f"---pat_lst={pat_lst}")
                # print(f"---el_idx={(el_idx, element)}")
                # if not succ[element]:
                if not self.allowed_successors[int(1/element)]:
                    continue
                # for (succ_idx, succesor) in enumerate(succ[element]):
                for (succ_idx, succesor) in enumerate(self.allowed_successors[int(1/element)]):
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

                    if xp not in self.init_pat_lst:
                        self.init_pat_lst.append(xp)
        print('-------------xxxx')

        # pprint.pprint(
        #   [(len(pat), pat, sum(map(lambda x: pow(x, -1),pat))) for pat in pat_lst ]
        # )
        # print('-------------')
        # print(len(pat_lst))
        self.duration_patterns = [{"pattern":pat} for pat in self.init_pat_lst]
        # return(self.duration_patterns)
        # print(self.duration_patterns)
        print(len(self.duration_patterns))

        # print(f"{[pat for pat in pat_lst]}")

    def calc_attributes(self):
        for pat in self.duration_patterns:
            ret_pattern = pat.get("pattern")
            pat["len"] = len(ret_pattern)
            # print(pat)
            pat["mean"] = statistics.mean(ret_pattern)
            pat["geo_mean"] = statistics.geometric_mean(ret_pattern)
            pat["harm_mean"] = statistics.harmonic_mean(ret_pattern)
            pat["pstdev"] = statistics.pstdev(ret_pattern)
            pat["pvariance"] = statistics.pvariance(ret_pattern)
            # print(ret_pattern)
            if len(ret_pattern)>1:
                pat["variance"] = statistics.variance(ret_pattern)
                pat["stdev"] = statistics.stdev(ret_pattern)
            else:
                pat["variance"]=0
                pat["stdev"]=0
                
            pat["max"] = max(ret_pattern)
            pat["min"] = min(ret_pattern)


# statistics.pstdev(data, mu=None)
# Return the population standard deviation
# statistics.pvariance(data, mu=None)
# Return the population variance of data, a non-empty sequence
# statistics.stdev(data, xbar=None)
# Return the sample standard deviation (the square root of the sample variance). See variance() for arguments and other details.

# statistics.variance(data, xbar=None)
# Return the sample variance of data, an iterable of at least two real-valued numbers. Variance, or second moment about the mean, is a measure of the variabili


durPat = DurationPatterns()
# print(f"{durPat=}")
durPat.find_all_pattern_splits()
# durPat.calc_attributes()
# print(f"{retd=}")
# pprint.pprint(f"{durPat.duration_patterns=}")

# print(durPat)
