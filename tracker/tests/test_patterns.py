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


def test_sin_return():
    notes = [1,2,3,3,3,4,4,5,6,7,7,0]
    dur = [1]*len(notes)
    xdict = {'notes': notes,
             'dur': dur}
    p_n = None
    nt = []
    dr = []
    # for idx, (n,d) in enumerate(zip(xdict['notes'].copy(),xdict['dur'].copy())):
    for idx  in range(len(notes)):
        if idx==0 or notes[idx] != notes[idx-1]:
            nt.append(xdict['notes'][idx])
            dr.append(xdict['dur'][idx])
        else:
            dr[-1]+=1

    xdict['notes']=nt
    xdict['dur']=dr

            # xdict['notes'].remove()
    assert xdict['notes'] == [1,2,3,4,5,6,7,0]
    assert xdict['dur'] == [1,1,3,2,1,1,2,1]