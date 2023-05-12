from tracker.app.patterns import *
npat = NotePatterns()

def test_get_path_pattern():

    scale = iso.Scale()
    key = iso.Key(tonic=0,scale=scale)
    scale_interval = 7
    interval = scale.indexOf(scale_interval)
    xxx = npat.get_path_pattern(interval=interval,scale_interval=scale_interval, key=key )
    aaa = list(iso.PDegree(iso.PSequence(xxx[iso.EVENT_NOTE], repeats=1), scale)+key.tonic)
    # bbb = list(iso.PDegree(iso.PSequence(xxx[iso.EVENT_NOTE], repeats=1), key))
    exp_pattern = list(np.array([0, 2, 4, 5, 7])+key.tonic)
    assert aaa == exp_pattern
    # assert bbb == exp_pattern

    scale = iso.Scale.pelog
    key = iso.Key(tonic=0,scale=scale)
    scale_interval = 11
    interval = scale.indexOf(scale_interval)
    xxx = npat.get_path_pattern(interval=interval,scale_interval=scale_interval, key=key )
    aaa = list(iso.PDegree(iso.PSequence(xxx[iso.EVENT_NOTE], repeats=1), scale)+ key.tonic)
    # bbb = list(iso.PDegree(iso.PSequence(xxx[iso.EVENT_NOTE], repeats=1) )+ key.tonic)
    print(f"{scale.semitones=}")
    # exp_pattern = list(np.array([0, 2, 4, 5, 7])+key.tonic)
    exp_pattern = list(np.array(scale.semitones)+key.tonic)
    assert aaa == exp_pattern, "sdfasdfds"
    # assert bbb == exp_pattern

    assert True

def test_generic_get_indexOf():

    # scale = iso.Scale.minor
    for scale in iso.Scale.all():
        if scale.octave_size >12:
            continue
        if scale.semitones[-1]>11:
            continue
        print(scale.name)
    # print(scale.semitones)
        for t in range(0, 12):
            key = iso.Key(tonic=t, scale=scale)
            exp_result = list(np.array(scale.semitones)+key.tonic)
            assert [key.get(x) for x in range(len(scale.semitones))] == exp_result
            # print("\nreversed: ", [scale.indexOf(x) for x in exp_result])
            assert [scale.indexOf(x-key.tonic) for x in exp_result] == list(range(len(scale.semitones)))


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

def test_get_chord_improved_pattern():
    # scale = iso.Scale.minor
    # key = iso.Key(tonic=0,scale=scale)
    # scale_interval = 7
    # interval = scale.indexOf(scale_interval)
    # npat.get_chord_improved_pattern(interval=interval,scale_interval=scale_interval, key=key )
    key = iso.Key(tonic=0, scale=iso.Scale.minor)
    major = iso.Scale.major
    key_major = iso.Key(tonic=key.tonic, scale=major)
    chords_list = list()
    n = 3
    step = 2
    semit = major.semitones + list(np.array(major.semitones) + major.octave_size)
    for i in range(len(semit) // 2):
        tchord = np.array([semit[i + x * step] for x in range(n)])
        tchord = [semit[i + x * step]-semit[i] for x in range(n)]
        if tchord not in chords_list:
            chords_list.append(tchord)
        # tchord = list(tchord - tchord[0])
        pass
    minor = iso.Scale.minor
    xnote = 60
    cnote = key.nearest_note(60)-key.tonic
    cdix = minor.indexOf(cnote)
    sc = iso.Scale.major
    key = iso.Key(tonic=2, scale=sc)
    # tnc = key.tonic
    # aaa = [(x,key.nearest_note(x)) for x in range(60,73)]
    # bbb = [(x,key.nearest_note(x), sc.indexOf(key.nearest_note(x)), sc.indexOf(key.nearest_note(x)+tnc)
    #         ) for x in range(60,73)]
    aba = [major.get(x)+key.tonic for x in range(13)]
    # abb = [(x,key.nearest_note(x),key.nearest_note(x)-1, major.indexOf(key.nearest_note(x)-1)
    #         ) for x in range(1, 23)]
    abbc= [(x,  major.indexOf(key.nearest_note(x)-key.tonic)
            ) for x in aba]
    assert True

    # Scale.chromatic = Scale([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "chromatic")
    # Scale.major = Scale([0, 2, 4, 5, 7, 9, 11], "major")
    # Scale.maj7 = Scale([0, 2, 4, 5, 7, 9, 10], "maj7")
    # Scale.minor = Scale([0, 2, 3, 5, 7, 8, 11], "minor")
    # Scale.pureminor = Scale([0, 3, 7], "pureminor")
    # Scale.puremajor = Scale([0, 4, 7], "puremajor")
    # Scale.minorPenta = Scale([0, 3, 5, 7, 10], "minorPenta")
    # Scale.majorPenta = Scale([0, 2, 4, 7, 9], "majorPenta")
    # Scale.ritusen = Scale([0, 2, 5, 7, 9], "ritusen")
    # Scale.pelog = Scale([0, 1, 3, 7, 8], "pelog")
    # Scale.augmented = Scale([0, 3, 4, 7, 8, 11], "augmented")
    # Scale.augmented2 = Scale([0, 1, 4, 5, 8, 9], "augmented 2")
    # Scale.wholetone = Scale([0, 2, 4, 6, 8, 10], "wholetone")
    #
    # Scale.ionian = Scale([0, 2, 4, 5, 7, 9, 11], "ionian")
    # Scale.dorian = Scale([0, 2, 3, 5, 7, 9, 10], "dorian")
    # Scale.phrygian = Scale([0, 1, 3, 5, 7, 8, 10], "phrygian")
    # Scale.lydian = Scale([0, 2, 4, 6, 7, 9, 11], "lydian")
    # Scale.mixolydian = Scale([0, 2, 4, 5, 7, 9, 10], "mixolydian")
    # Scale.aeolian = Scale([0, 2, 3, 5, 7, 8, 10], "aeolian")
    # Scale.locrian = Scale([0, 1, 3, 5, 6, 8, 10], "locrian")
    # Scale.fourths = Scale([0, 2, 5, 7], "fourths")

# def test_sin_return():
#
#     scale = iso.Scale()
#     key = iso.Key(tonic=0,scale=scale)
#     scale_interval = 7
#     interval = scale.indexOf(scale_interval+5*scale.octave_size) - 5*len(scale.semitones)
#     npat.get_imp_sine_pattern(interval=interval,scale_interval=scale_interval, key=key )
#     assert True