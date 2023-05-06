from tracker.app.patterns import *
npat = NotePatterns()

def test_all_suitable_patterns():
    _ = npat.all_suitable_patterns(0)
    for n in range(1, 16):
        assert all([pattern[-1] > 0 for pattern in npat.all_suitable_patterns(n)])
    for n in range(-16, -1):
        assert all([pattern[-1] < 0 for pattern in npat.all_suitable_patterns(n)])

def test_all_suitable_diminunitions():
    _ = npat.all_suitable_diminunitions(0)
    for n in range(1, 16):
        assert all([pattern[-1] > 0 for pattern in npat.all_suitable_diminunitions(n)])
    for n in range(-16, -1):
        assert all([pattern[-1] < 0 for pattern in npat.all_suitable_diminunitions(n)])

def test_get_sine_pattern():
    scale = iso.Scale()
    key = iso.Key(tonic=0,scale=scale)
    scale_interval = 7
    interval = scale.indexOf(scale_interval)
    npat.get_sine_pattern(interval=interval,scale_interval=scale_interval, key=key )
    assert True