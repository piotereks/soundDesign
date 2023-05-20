from tracker.app.patterns import *

from tracker.app.isobar_fixes import *
read_config_file_scales()

npat = NotePatterns()


def test_get_path_pattern():

    scale = iso.Scale()
    key = iso.Key(tonic=0,scale=scale)
    scale_interval = 7
    interval = scale.indexOf(scale_interval)
    base_pattern = npat.get_path_pattern(interval=interval,scale_interval=scale_interval, key=key )
    pdegree_pattern = list(iso.PDegree(iso.PSequence(base_pattern[iso.EVENT_NOTE], repeats=1), key))
    exp_pattern = list(np.array([0, 2, 4, 5, 7])+key.tonic)
    assert pdegree_pattern == exp_pattern

    scale = iso.Scale.byname('pelog')
    key = iso.Key(tonic=0, scale=scale)
    scale_interval = 11
    interval = scale.indexOf(scale_interval)
    base_pattern = npat.get_path_pattern(interval=interval,scale_interval=scale_interval, key=key )
    pdegree_pattern = list(iso.PDegree(iso.PSequence(base_pattern[iso.EVENT_NOTE], repeats=1), key))
    print(f"{scale.semitones=}")
    exp_pattern = list(np.array(scale.semitones)+key.tonic)
    assert pdegree_pattern == exp_pattern

def test_get_chord_improved_pattern():
    scale = iso.Scale.major
    key = iso.Key(tonic=0, scale=scale)
    from_note = 60
    # from_note_idx = key.scale.indexOf(key.nearest_note(from_note - key.tonic))
    chord = npat.get_chord_improved_pattern(from_note=from_note, key=key)
    assert chord[iso.EVENT_NOTE] == [(0, 2, 4), 0], f"Chord idx for scale {key.scale.name} not correct"
    chord = npat.get_chord_improved_pattern(from_note=from_note+1, key=key)
    assert chord[iso.EVENT_NOTE] == [(0, 2, 4), 0], f"Chord idx1 for scale {key.scale.name} not correct"
    chord = npat.get_chord_improved_pattern(from_note=from_note+6, key=key)
    assert chord[iso.EVENT_NOTE] == [(0, 2, 4), 0], f"Chord idx6 for scale {key.scale.name} not correct"

    scale = iso.Scale.byname('pelog')  # [0, 1, 3, 7, 8]
    key = iso.Key(tonic=0, scale=scale)
    from_note = 60
    chord = npat.get_chord_improved_pattern(from_note=from_note, key=key)
    assert chord[iso.EVENT_NOTE] == [(0, 2, 3), 0], f"Chord idx for scale {key.scale.name} not correct"
    chord = npat.get_chord_improved_pattern(from_note=from_note+1, key=key)
    assert chord[iso.EVENT_NOTE] == [0, 0], f"Chord idx1 for scale {key.scale.name} not correct"
    chord = npat.get_chord_improved_pattern(from_note=from_note+6, key=key)
    assert chord[iso.EVENT_NOTE] == [0, 0], f"Chord idx6 for scale {key.scale.name} not correct"

    scale = iso.Scale.minor
    key = iso.Key(tonic=0, scale=scale)
    from_note = 60
    # from_note_idx = key.scale.indexOf(key.nearest_note(from_note - key.tonic))
    chord = npat.get_chord_improved_pattern(from_note=from_note, key=key)
    assert chord[iso.EVENT_NOTE] == [(0, 2, 4), 0], f"Chord idx for scale {key.scale.name} not correct"
    chord = npat.get_chord_improved_pattern(from_note=from_note+1, key=key)
    assert chord[iso.EVENT_NOTE] == [(0, 2, 4), 0], f"Chord idx1 for scale {key.scale.name} not correct"
    chord = npat.get_chord_improved_pattern(from_note=from_note+6, key=key)
    assert chord[iso.EVENT_NOTE] == [(0, 2, 4), 0], f"Chord idx6 for scale {key.scale.name} not correct"

def test_generic_get_indexOf():
    scale = iso.Scale(semitones=[0, 2, 4, 6, 8, 10], name="test_scale", octave_size=12,
                      semitones_down=[0, 1, 3, 5, 7, 9, 11])

    # scale = iso.Scale.minor
    for scale in iso.Scale.all():
        print(scale.name)
        if hasattr(scale, "semitones_down") and scale.semitones_down:
            print("scale_down tested too")
        for t in range(0, 12):
            key = iso.Key(tonic=t, scale=scale)
            exp_result = list(np.array(scale.semitones)+key.tonic)
            assert [key.get(x) for x in range(len(scale.semitones))] == exp_result, "IndexOf UP1"
            assert [scale.indexOf(x-key.tonic) for x in exp_result] == list(range(len(scale.semitones))), "IndexOf UP2"
            
            if hasattr(scale,"semitones_down") and scale.semitones_down:
                exp_result = list(np.array(scale.semitones_down) + key.tonic)
                assert [key.get(x, scale_down=True) for x in range(len(scale.semitones_down))] == exp_result, "IndexOf DOWN1"
                assert [scale.indexOf(x - key.tonic, scale_down=True) for x in exp_result] == list(range(len(scale.semitones_down))), "IndexOf DOWN2"


def test_all_suitable_patterns():
    _ = npat.all_suitable_patterns(0)
    for n in range(1, 16):
        assert all([pattern[-1] > 0 for pattern in npat.all_suitable_patterns(n)])
    for n in range(-16, -1):
        assert all([pattern[-1] < 0 for pattern in npat.all_suitable_patterns(n)])


def test_all_suitable_diminution():
    _ = npat.all_suitable_diminutions(0)
    for n in range(1, 16):
        assert all([pattern[-1] > 0 for pattern in npat.all_suitable_diminutions(n)])
    for n in range(-16, -1):
        assert all([pattern[-1] < 0 for pattern in npat.all_suitable_diminutions(n)])




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

