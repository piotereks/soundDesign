import random

def split_no(interval, max_len=16):
    pattern_len = interval


    interval -= 1

    parts_no16 = interval// max_len
    parts_no16 += 1
    # parts_no4 = interval // int(max_len / 4)
    # parts_no4 += 1

    # rnd_parts = random.randint(parts_no16, parts_no4)
    rnd_parts = random.choice([parts_no16,parts_no16*2,parts_no16*4])

    splt_array = []
    while pattern_len > 0:
        part = -(-pattern_len // rnd_parts)
        splt_array.append(part)
        # print(f"x:{part=}")
        pattern_len -= part
        rnd_parts -= 1
    # print(splt_array)

    # return (parts_no16, parts_no4)
    return (splt_array)


split_no(22)
split_no(22)
split_no(22)
split_no(22)
split_no(22)
split_no(22)
split_no(22)
split_no(22)