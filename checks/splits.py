"""
4/4 =>1|1|1|1   1/ 2/ 3/ 4/ same
.... 4.=8+8+8 =>4.+8 = 2
1|
2-2|3-3-3|2.+4|5-5-5-5-5
2-4-4|2-6-6-6|2+4.+8|4-4-4-4|3-3-6-6|4.+4.+4|10 x10| 5x4 + 10+10
3/4=>1|1|1
as 4/4

6/8 => 4.|4.|  ..9/8, 12/8
4.|8.+8.|8+8+8|

6/4 =>2.|2. .. 9/4 , 12/4
2.|4.-4.|4-4-4|4-4- 12-12-12| 4-4 20 x5

5/4 =>2.|2
7/4 => 2.|2|2
..
10/4 (10/12) =>2.|2.|2|2
11/4 (11/12)=>  2.|2.|2.|2 or
=================
1/ 2/ 3/ 4/
base splits
======base splits
1
2-2
3-3-3
2.-4
5-5-5-5-5
--
1
1,1
1,1,1
3,1
1,1,1,1,1

=======dot splits
1.
2.-2.
3.-3.-3. ?? (is this correct?) - correct, but shall apply it?
5. x5 (is this correct)  - correct, but shall apply it?
2..-4. (is this correct - to be applied?) - not correct
===
3/ 6/ 9/ 12/
1. (1.5)
2.,2.
2,2,2
1,1
1,1,1
1,1,1,1,1
===
5/
1., 1

7/
1.| 1| 1
===
1,1,1
1.5, 1.5
1,1,1


===
do not mix 3 and 5 in hierarchy split (I don't want that).
do not mix 3 and 3  also 5 and 5
use minimal split 20 (but that depends on  /4 ...what about /2 /1 and /8 and /16?) ..treat as /20 compare to /4 which is 1.
for /8 will be 0.5 and /10, for /2 will be 2 and /40 and for /1 will be 4 and /80
==
adapt time split vs beat per bar
"""
import networkx as nx
from pprint import pprint

DG = nx.MultiDiGraph()
# DG = nx.DiGraph()
order = 0


def init_graph():
    global DG
    global order

    def mult_add_edge_old(fr, to, n):
        global order
        for _ in range(n):
            print(f"x:,{n=},{fr=},{to=},{order=}")
            DG.add_edge(fr, to, order=order)
            # print(DG.edges[fr,to,0])
            # print(DG.edge)
            order+=1

    def mult_add_edge(fr, n):
        global order
        for _ in range(n):
            print(f"x:,{n=},{fr=},{n*fr=},{order=}")
            DG.add_edge(fr, n*fr, order=order)
            # print(DG.edges[fr,to,0])
            # print(DG.edge)
            order+=1

    # mult_add_edge(1,2,2)
    # mult_add_edge(1,3,3)
    # mult_add_edge(1,5,5)
    #
    # mult_add_edge(2,4,2)
    # mult_add_edge(2,6,3)
    # mult_add_edge(2,10,5)
    #
    # mult_add_edge(3,6,2)
    #
    # mult_add_edge(4,8,2)
    # mult_add_edge(4,12,3)
    # # mult_add_edge(4,5,10)
    #
    # mult_add_edge(5, 19, 3)

    mult_add_edge(1, 2)
    mult_add_edge(1, 3)
    mult_add_edge(1, 5)

    mult_add_edge(2, 2)
    mult_add_edge(2, 3)
    mult_add_edge(2, 5)

    mult_add_edge(3, 2)

    mult_add_edge(4, 2)
    mult_add_edge(4, 3)
    # mult_add_edge(4,5,10)

    # mult_add_edge(5, 2)
    # mult_add_edge(6, 2)

    mult_add_edge(8, 2)
    # mult_add_edge(16, 2)



# G.add_edge(1, 3)
# G[1][3]['color'] = "blue"
# G.edges[1, 2]['color'] = "red"
# G.edges[1, 2]



def splits(x):
    div_norm = [(1,1),(1,1,1),(1,1,1,1,1),(3,1),(1,3)]
    div_dot =  [(1,1),(1,1,1),(1,1,1,1,1)]


init_graph()
# print(DG.nodes,'=>', DG.edges)
# pprint(DG.adj)

# print(list(nx.all_simple_paths(DG,1,16)))
# print(list(nx.chain_decomposition(DG)))
pprint(list(DG.adj[1]))
pprint(list(DG.adj[2]))
pprint(list(DG[2]))
pprint(list(DG.pred[2]))
pprint(list(DG.predecessors(2)))
pprint(list(DG.succ[2]))
pprint(list(DG.successors(2)))

leaves =  [n for n in DG.nodes if DG.out_degree(n) == 0]

all_leaves = [list(nx.all_simple_paths(DG,1,n)) for n in DG.nodes if DG.out_degree(n) == 0]
all_leaves = [list(map(lambda x: x[-1],nx.all_simple_paths(DG,1,n))) for n in DG.nodes if DG.out_degree(n) == 0]
nbr_of_paths=len(list(nx.all_simple_paths(DG,1,12)))
parent = list(DG.predecessors(12))[0]
DG.remove_edge(4,12)

print("uuu: ", leaves)

first_succ = list(DG.successors(1))
fi = first_succ[0]
xxx = list(map(lambda x: x[-1],nx.all_simple_paths(DG, 1,fi)))