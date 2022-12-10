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
import yaml
import numpy as np
from fractions import Fraction as F

# succ = [None, {2,3,4},{4,6,10},{6},{8,12}, {10},{12},None,{16}]
rp = itertools.repeat

class DurationPatterns:
    def __init__(self):

        self.new_succ_divdors = \
        {20:
            [
                (1,1)
            ],

        21:  [
                (1,3),(3,1)
            ],
        30: [
               (1,1,1)
            ],
        31: [
                (1,2),(2,1)
            ],
        50: [
                (1,1,1,1,1)
            ] #,
        # 51: [
        #         (2,1,2),(1,2,1,1),(1,1,2,1),
        #         (2,3),(3,2),(1,4),(4,1)
        #     ],
        # 52: [
        #         (1,9),(9,1),(3,7),(7,3)
        #     (1,2,1,2,1,2,1),(1,2,2,2,1,1,1),(1,1,1,2,2,2,1)
        #     ]
        }
        self.succ_idx = {
        1:[20,21,30,31,50],
        2:[20,21,30,31,50],
        3:[20],
        4:[20,21,30,31],
        5:[20],
        6:[20],
        8:[20]
        }

        # self.init_pat_lst=[[1],[4,2,4],[8,4,8,2],[2,8,4,8],[4,8,4,8,4],[6,3,3,6],[10,5,5,5,5,10],
        #         [10,5,10,5,10,5,10]
        #         ]

        self.init_pat_lst=[[1]]

    def recalc(self):
        for (pat_idx,pattern) in enumerate(self.init_pat_lst):
            for (el_idx, element) in enumerate(pattern):
                idx_map=self.succ_idx.get(element)
                # print(f"\nppppppp={pattern=}, {element=}, {idx_map=}")
                if not idx_map:
                    continue
                for idx in idx_map:
                    # print(f"{idx=}, {self.new_succ_divdors[idx]}")
                    for dividor_tup in self.new_succ_divdors[idx]: 
                        
                        # print(f"{dividor_tup=},{sum(dividor_tup)=},{sum(dividor_tup)/np.array(dividor_tup)}")
                        
                        div_array = element*sum(dividor_tup)/np.array(dividor_tup)
                        xp = pattern.copy()

                        del xp[el_idx]

                        for x in np.flip(div_array):
                            xp.insert(el_idx, x.tolist())

                        # print(type(xp))
                        #
                        #
                        # dumped_dur = yaml.dump(list(xp), default_flow_style=None, sort_keys=False)
                        # print(dumped_dur)

                        if xp not in self.init_pat_lst:
                            self.init_pat_lst.append(xp)
                            # print(f"{xp=}")

                        # dumped_dur = yaml.dump(self.init_pat_lst.append, default_flow_style=None, sort_keys=False)
                        # print(dumped_dur)
        self.duration_patterns = [{"pattern":pat} for pat in self.init_pat_lst]
        # return(self.patterns)
        print(len(self.duration_patterns))



    def check_dur_sizes(self,pattern:list, dividor:int, any_all="any"):
        div_tab ={
        2: [1,2,4,8,16,32,64],
        3: [1,3,6,12,24],
        5: [1,5,10,20]
        }
        if any_all == "any":
            func = any
        else:
            func = all

        return func([elem in div_tab[dividor] for elem in pattern])

        
    def all_twos(self, pat):
        return self.check_dur_sizes( pattern = pat, dividor = 2, any_all ="all")


    def any_twos(self, pat):
        return self.check_dur_sizes( pattern = pat, dividor = 2, any_all ="any")


    def all_threes(self, pat):
        return self.check_dur_sizes( pattern = pat, dividor = 3, any_all ="all")


    def any_threes(self, pat):
        return self.check_dur_sizes( pattern = pat, dividor = 3, any_all ="any")


    def all_fives(self, pat):
        return self.check_dur_sizes( pattern = pat, dividor = 5, any_all ="all")


    def any_fives(self, pat):
        return self.check_dur_sizes( pattern = pat, dividor = 5, any_all ="any")


    def calc_attributes(self):
        def assign_attrib(attr:str, val:bool):
            if val:
                pat[attr] = val

        for pat in self.duration_patterns:
            ret_pattern = pat.get("pattern")
            if not ret_pattern:
                break
      
            pat["len"] = len(ret_pattern)  # type: ignore
            # print(pat)
            pat["mean"] = statistics.mean(ret_pattern) # type: ignore
            pat["geo_mean"] = statistics.geometric_mean(ret_pattern) # type: ignore
            # pat["harm_mean"] = statistics.harmonic_mean(ret_pattern) # type: ignore
            pat["pstdev"] = statistics.pstdev(ret_pattern) # type: ignore

            pat["max"] = max(ret_pattern) # type: ignore
            pat["min"] = min(ret_pattern) # type: ignore

            assign_attrib("all2",self.all_twos(ret_pattern))
            assign_attrib("any2",self.any_twos(ret_pattern))
            assign_attrib("all3", self.all_threes(ret_pattern))
            assign_attrib("any3", self.any_threes(ret_pattern))
            assign_attrib("all5",self.all_fives(ret_pattern))
            assign_attrib("any6",self.any_fives(ret_pattern))

            # pat["all2"] = self.all_twos(ret_pattern) # type: ignore
            # pat["any2"] = self.any_twos(ret_pattern) # type: ignore

            # pat["all3"] = self.all_trees(ret_pattern) # type: ignore
            # pat["any3"] = self.any_trees(ret_pattern) # type: ignore
            #
            # pat["all5"] = self.all_fives(ret_pattern) # type: ignore
            # pat["any5"] = self.any_fives(ret_pattern) # type: ignore



durPat = DurationPatterns()
durPat.recalc()
# print(f"{durPat=}")
# durPat.find_all_pattern_splits()
durPat.calc_attributes()
# print(f"{retd=}")
# pprint.pprint(f"{durPat.patterns=}")
# pprint.pprint([pat for pat in durPat.patterns if pat["all5"]])
# cities = sorted(cities, key=lambda city: city['population'])
# pprint.pprint(sorted(durPat.patterns, key = lambda x : -x["pstdev"]))
# print(durPat)
print("bef dump")
# dumped_dur = yaml.dump(durPat.duration_patterns,default_flow_style=None, sort_keys=False)
# print(dumped_dur)
# print("aft dump")
with open('patterns.yaml', 'w') as f:
    data = yaml.dump(durPat.duration_patterns,f, default_flow_style=None, sort_keys=False)
print('after writing')
