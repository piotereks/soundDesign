from tracker.app.patterns import *
npat = NotePatterns()

def test_all_suitable_patterns():
    for x in range(10000):
        print(f"{x=}")
        # assert len(npat.all_suitable_patterns(-12))>0
        assert len(random.choice([pattern for pattern in npat.all_suitable_patterns(-12)])) != []