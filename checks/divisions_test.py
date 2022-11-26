import itertools
MAX_PATH_LEN=16
dividors = [0,1,2,3,4,5]
divisions = [0 if x==0 else 1/x for x in dividors ]

print(divisions)

# for x in itertools.product(range(1,17),divisions):
#     print(x)


for x in range(1,4):
    print(x)