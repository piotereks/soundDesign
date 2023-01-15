# import sys
# from importlib import reload
# sys.path.append('/content/SoundDesign/tracker')

from patterns import *
# reload(patterns)
# reload(sys.modules['patterns'])

note_ptrn = NotePatterns()
# print(list(ptrn.patterns))
# print(list(ptrn.pattern_size_for_interval))
# pprint.pprint(ptrn.patterns_config['play_over']['patterns'])
# print(list(map(lambda x : x['pattern'],ptrn.patterns_config['play_over']['patterns'])))
interval = 3
print('gsp:', interval, note_ptrn.all_suitable_patterns(interval))
print('gsp:', -interval, note_ptrn.all_suitable_patterns(-interval))

interval = 3
print('grp:', interval, note_ptrn.get_random_pattern(interval))
print('grp:', -interval, note_ptrn.get_random_pattern(-interval))

interval = 10
xxx = note_ptrn.get_random_pattern(interval)
print('xxx:', interval, xxx)
print('grp:', interval, note_ptrn.get_random_pattern(interval))
print('grp:', -interval, note_ptrn.get_random_pattern(-interval))