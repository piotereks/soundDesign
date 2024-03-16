from tracker.app.isobar_fixes import *
snoop.install(enabled=False)

read_config_file_scales()

def test_single_scale():
    scale = iso.Scale.major
    key = iso.Key(tonic=0, scale=scale)
    key.tonic = 1
    snoop.install(enabled=False)
    key.nearest_note(62)
    pass


def test_key_nearest_note():
    scale = iso.Scale.major

    for scale in iso.Scale.all():
        key = iso.Key(tonic=0, scale=scale)

        # for t in range(128):
        for t in range(0, 12):

            print('\n' + scale.name)
            key.tonic = t
            key = iso.Key(tonic=t, scale=scale)
            x = key.nearest_note(60)
            # test_pattern_midi_nr = [x+key.tonic for x in key.scale.semitones]
            octave5_start = 5 * key.scale.octave_size
            test_pattern_midi_nr = [x + octave5_start + key.tonic for x in key.scale.semitones]
            # result_pattern = [key.nearest_note(x) for x in test_pattern_midi_nr]
            result_pattern = [key.nearest_note(x) for x in test_pattern_midi_nr]
            print(result_pattern)
            assert test_pattern_midi_nr == result_pattern, "Assert Scale Up"

            negative_test_pattern_midi_nr = [x + octave5_start + key.tonic for x in range(key.scale.octave_size)
                                             if x not in key.scale.semitones]
            # print(test_pattern_midi_nr,negative_test_pattern_midi_nr )
            negative_result_flags = [key.nearest_note(x) != x for x in negative_test_pattern_midi_nr]
            assert all(
                negative_result_flags), f"{[(key.nearest_note(x), x, key.nearest_note(x) != x) for x in negative_test_pattern_midi_nr]}"

            if hasattr(scale, 'semitones_down') and scale.semitones_down:
                print("semitones down")
                test_pattern_midi_nr = [x + key.tonic for x in key.scale.semitones_down]
                result_pattern = [key.nearest_note(x, scale_down=True) for x in test_pattern_midi_nr]
                print(result_pattern)
                assert test_pattern_midi_nr == result_pattern, "Assert Scale Down"

                negative_test_pattern_midi_nr = [x + octave5_start + key.tonic for x in range(key.scale.octave_size)
                                                 if x not in key.scale.semitones_down]
                # print(test_pattern_midi_nr,negative_test_pattern_midi_nr )
                negative_result_flags = [key.nearest_note(x, scale_down=True) != x for x in
                                         negative_test_pattern_midi_nr]
                assert all(
                    negative_result_flags), f"{[(key.nearest_note(x, scale_down=True), x, key.nearest_note(x, scale_down=True) != x) for x in negative_test_pattern_midi_nr]}"
