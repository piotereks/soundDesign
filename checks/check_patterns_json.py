import json
# from scipy.stats import rv_histogram
import numpy as np
def read_config_file():
    # print('reading config')
    config_file = '../tracker/duration_patterns.json'
    # if IN_COLAB:
    #     config_file = '/content/SoundDesign/tracker/' + config_file

    with open(config_file, 'r') as file:
        patterns = json.load(file)
    return patterns


# pat["len"] = len(ret_pattern)  # type: ignore
# pat["mean"] = statistics.mean(ret_pattern)  # type: ignore
# pat["geo_mean"] = statistics.geometric_mean(ret_pattern)  # type: ignore
# pat["pstdev"] = statistics.pstdev(ret_pattern)  # type: ignore
#
# pat["max"] = max(ret_pattern)  # type: ignore
# pat["min"] = min(ret_pattern)  # type: ignore
#
# assign_attrib("all2", self.all_twos(ret_pattern))
# assign_attrib("any2", self.any_twos(ret_pattern))
# assign_attrib("all3", self.all_threes(ret_pattern))
# assign_attrib("any3", self.any_threes(ret_pattern))
# assign_attrib("all5", self.all_fives(ret_pattern))
# assign_attrib("any5", self.any_fives(ret_pattern))


patterns = read_config_file()

mx = max([p.get("mean") for p in patterns])
print(f"mean max: {mx}")


mn = min([p.get("mean") for p in patterns])
print(f"mean min: {mn}")

mx = max([p.get("geo_mean") for p in patterns])
print(f"geo_mean max: {mx}")

mn = min([p.get("geo_mean") for p in patterns])
print(f"geo_mean min: {mn}")

mx = max([p.get("pstdev") for p in patterns])
print(f"pstdev max: {mx}")

mn = min([p.get("pstdev") for p in patterns])
print(f"pstdev min: {mn}")

lbl = set(ks for p in patterns for ks in p.keys() if 'any' in ks or 'all' in ks)
print(lbl)
# for p in patterns:
#     for ks in p.keys()

# [entry for tag in tags for entry in entries if tag in entry]

# lbl = set(ks for p in patterns for ks in p.keys() if 'any' in ks or 'all' in ks)
for p in patterns:
    # if not [ks for ks in p.keys() if 'any' in ks]:
    #     print(p)
    if not [ks for ks in p.keys() if 'align' in ks]:
        print(p)


bins = 10
hist = np.histogram([p.get("pstdev") for p in patterns], bins=bins)

for x in range(bins):
    print(hist[1][x],hist[0][x])
print()
print(hist)
print([x for x in hist])