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
from pprint import pprint
import statistics
import yaml
import json
import numpy as np
from fractions import Fraction as F
import jsbeautifier


# succ = [None, {2,3,4},{4,6,10},{6},{8,12}, {10},{12},None,{16}]
rp = itertools.repeat

class DurationPatterns:
    def __init__(self):
        self.duration_patterns = None
        self.new_succ_divdors = \
        {20:
            [(1,1)],
        30: [(1,1,1)],
        50: [(1,1,1,1,1)]
        }
        self.succ_idx = {
        1:[20,30,50],
        2:[20,30,50],
        3:[20],
        4:[20,30],
        5:[20],
        8:[20]
        }

        self.succ_dot_idx = {
        1:[20,30],
        # 2:[20,30,50],
        2:[20],
        3:[20,50],
        4:[20],
        6:[20],
        8:[20]
        }

        # self.init_pat_lst=[[1]]

    def recalc(self, succesors, type='norm'):
        self.init_pat_lst = [[1]]
        for (pat_idx,pattern) in enumerate(self.init_pat_lst):
            # print(f"{(pat_idx,pattern)=}")
            for (el_idx, element) in enumerate(pattern):
                idx_map=succesors.get(element)
                if not idx_map:
                    continue
                for idx in idx_map:
                    for dividor_tup in self.new_succ_divdors[idx]:

                        div_array = element*sum(dividor_tup)/np.array(dividor_tup)
                        xp = pattern.copy()

                        del xp[el_idx]

                        for x in np.flip(div_array):
                            xp.insert(el_idx, x.tolist())

                        if xp not in self.init_pat_lst:
                            self.init_pat_lst.append(xp)
        if type == 'norm':
            self.init_pat_lst.append([66,66])
        print("# of patterns: ", len(self.init_pat_lst))
        duration_patterns = [{"pattern":pat, type: True} for pat in self.init_pat_lst]
        # return(self.patterns)
        if self.duration_patterns is None:
            self.duration_patterns = duration_patterns
        else:
            pattern_check_list = list(map(lambda x: x["pattern"], self.duration_patterns))
            for durp in duration_patterns:
                # if durp in self.duration_patterns:
                if durp["pattern"] in pattern_check_list:
                    # idx=self.duration_patterns.index(durp)
                    idx=pattern_check_list.index(durp["pattern"])
                    self.duration_patterns[idx].update(durp)
                else:
                    self.duration_patterns.append(durp)
        if type == 'norm':
            self.duration_patterns_norm = duration_patterns.copy()
        else:
            self.duration_patterns_dot = duration_patterns.copy()

            s1 = [s["pattern"] for s in self.duration_patterns_norm]
            s2 = [s["pattern"] for s in self.duration_patterns_dot]
            sx = [s for s in s1 if s not in s2]
            sy = [s for s in s2 if s not in s1]
            # assert len(sx)>0
            # assert len(sy)>0

        print("# of patterns: ", len(duration_patterns))
        return duration_patterns


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


        def align_rng(step=1):
            return set((np.arange(0,1,1/step)+1/step).round(5))   


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
            assign_attrib("any5",self.any_fives(ret_pattern))

            # pat["all2"] = self.all_twos(ret_pattern) # type: ignore
            # pat["any2"] = self.any_twos(ret_pattern) # type: ignore

            # pat["all3"] = self.all_trees(ret_pattern) # type: ignore
            # pat["any3"] = self.any_trees(ret_pattern) # type: ignore
            #
            # pat["all5"] = self.all_fives(ret_pattern) # type: ignore
            # pat["any5"] = self.any_fives(ret_pattern) # type: ignore

            for dd in (2,3,4,5,6,8,10,12):
                alignment_set=align_rng(dd)
                ret_pattern_set=set((1/np.array(ret_pattern)).cumsum().round(5))

# a = set(map(lambda x : round(x,5), (1/tst).cumsum()))

                assign_attrib(f"align{dd}",alignment_set & ret_pattern_set == alignment_set)

durPat = DurationPatterns()
_ = durPat.recalc(succesors=durPat.succ_idx, type="norm")
_ = durPat.recalc(succesors=durPat.succ_dot_idx, type="dot")
# durPat.duration_patterns.update(durPat.recalc(succesors=durPat.succ_dot_idx, type="dot"))

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
# with open('patterns.yaml', 'w') as f:
#     data = yaml.dump(durPat.duration_patterns,f, default_flow_style=None, sort_keys=False)

opts = jsbeautifier.default_options()
opts.indent_size = 2

# jsbeautifier.beautify(json.dumps(d), opts)
# json.dumps(durPat.duration_patterns)

with open('xpatterns.json', 'w') as f:
    # jsbeautifier.beautify(json.dump(durPat.duration_patterns, f, indent = 4)
    print(jsbeautifier.beautify(json.dumps(durPat.duration_patterns), opts),file=f)
print('after writing')