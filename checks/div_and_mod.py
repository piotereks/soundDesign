import random
import numpy as np

SPLIT_SIZE = int(16/4)
def xsplit_no(interval, max_len = SPLIT_SIZE):
    interval -=1
    margin = interval % max_len
    margin+=1
    parts_no = interval // max_len
    parts_no+=1
    return (parts_no, margin)

def split_no(interval, max_len = SPLIT_SIZE):
    interval -=1

    parts_no16 = interval // max_len
    parts_no16+=1
    parts_no4 = interval // int(max_len/4)
    parts_no4+=1


    return (parts_no16, parts_no4)


# print(random.randint(5,12))

# for x in range(1,33):
#     print(x, split(x))

pattern_len = 25
parts_no16, parts_no4 = split_no(pattern_len, 16)
print(parts_no16, parts_no4)
rnd_parts= random.randint(parts_no16, parts_no4 )
print(rnd_parts, pattern_len, pattern_len/rnd_parts)

# lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
# lol(x, 4)
xxx = np.arange(0, rnd_parts, pattern_len)
print(list(xxx))
print(-(-pattern_len/rnd_parts))
print(-(-pattern_len//rnd_parts))

# while pattern_len>0:
#     part=-(-pattern_len//rnd_parts)
#     print(f"{part=}")
#     pattern_len-=part
#     rnd_parts-=1
    
print('xxxxx')   
for i in range(0,pattern_len, -(-pattern_len//rnd_parts)):
    print(f"{i=} {i-(-pattern_len//rnd_parts)}")