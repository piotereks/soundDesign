import contextlib

import pytest
from pathlib import Path
import json
import random

# from tracker.app.isobar_fixes import *
# from isobar_ext import *
import isobar_ext as iso
from tracker.app.tracker import Tracker

# read_config_file_scales()

this_dir = Path(__file__).resolve().parent
config_file = this_dir / '../config/main_config.json'

with open(config_file, 'r') as file:
    loaded_config = json.load(file)
    app_config = loaded_config['app']
    tracker_config = loaded_config['tracker']
    midi_mapping = loaded_config.get('midi_mapping')

# midi_out_flag = Tracker.MIDI_OUT_DUMMY
midi_out_flag = Tracker.MIDI_OUT_MIX_FILE_DEVICE
tracker = Tracker(tracker_config=tracker_config, midi_mapping=midi_mapping, midi_out_mode=midi_out_flag)

ACCENT_BIG_FACTOR = 1.5
ACCENT_MED_FACTOR = 1.25
ACCENT_DEFAULT = 45
ACCENT_BIG = int(ACCENT_DEFAULT * ACCENT_BIG_FACTOR)
ACCENT_MED = int(ACCENT_DEFAULT * ACCENT_MED_FACTOR)


@pytest.fixture()
def init_tracker(numerator):
    tracker.time_signature['numerator'] = numerator
    tracker.time_signature['denominator'] = 4
    tracker.set_default_duration()
    tracker.set_metro_seq()


@pytest.mark.parametrize("numerator, out_patterns", [
    (1, {'note': [32],
         'amplitude': [ACCENT_BIG],
         'duration': [1]}),
    (2, {'note': [32, 37],
         'amplitude': [ACCENT_BIG, ACCENT_MED],
         'duration': [1, 1]}),
    (3, {'note': [32, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_MED],
         'duration': [1, 1, 1]}),
    (4, {'note': [32, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT],
         'duration': [1, 1, 1, 1]}),
    (5, {'note': [32, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT],
         'duration': [1.5, 1.5, 1, 1]}),
    (6, {'note': [32, 37, 37, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT],
         'duration': [1, 1, 1, 1, 1, 1]}),
    (7, {'note': [32, 37, 37, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT],
         'duration': [1.5, 1.5, 1, 1, 1, 1]}),
    (8, {'note': [32, 37, 37, 37, 37, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT,
                       ACCENT_DEFAULT, ACCENT_DEFAULT],
         'duration': [1, 1, 1, 1, 1, 1, 1, 1, ]}),
    (9, {'note': [32, 37, 37, 37, 37, 37, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT,
                       ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT],
         'duration': [1, 1, 1, 1, 1, 1, 1, 1, 1]}),
    (10, {'note': [32, 37, 37, 37, 37, 37, 37, 37],
          'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT,
                        ACCENT_DEFAULT, ACCENT_DEFAULT, ],
          'duration': [1.5, 1.5, 1.5, 1.5, 1, 1, 1, 1]}),
    (11, {'note': [32, 37, 37, 37, 37, 37, 37, 37],
          'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT,
                        ACCENT_DEFAULT, ACCENT_DEFAULT],
          'duration': [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1, 1]}),
    (12, {'note': [32, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37],
          'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT,
                        ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT],
          'duration': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})
])
def test_metro_play(init_tracker, numerator, out_patterns):
    # sys.stdout = open(os.devnull, 'w')
    tracker.metro_play()
    assert list(tracker.metro_play_patterns['note']) == out_patterns['note']
    assert list(tracker.metro_play_patterns['amplitude']) == out_patterns['amplitude']
    assert list(tracker.metro_play_patterns['duration']) == out_patterns['duration']


def test_play_from_to_result(step=3, subset_div=5):
    """
    step=3 to improve time of test in full test suite should be step=1
    """
    # self.play_from_to(from_note, to_note, in_pattern=True)
    # step, subset_div = 1, 1
    # random.choices(list, k=n)
    scale = iso.Scale.major
    scales = iso.Scale.all()
    if subset_div > 1:
        scales = random.choices(scales, k=len(scales) // subset_div)

    for scale in scales:
        octave5_start = 5 * scale.octave_size
        print(f"{scale.name=}")
        for t in range(0, scale.octave_size, step):
            # print(t)
            key = iso.Key(t % scale.octave_size, scale)
            test_semitones = [x + octave5_start + key.tonic for x in key.scale.semitones]
            # test_semitones = [x+60+key.tonic for x in key.scale.semitones]
            # print(f"{key.scale.__dict__=},{key.scale.__dict__.get('semitones')=}")

            tracker.key = key
            tracker.note_patterns.set_pattern_function('path')
            from_note = octave5_start + key.tonic
            to_note = from_note + key.scale.octave_size
            tracker.quants_state = {'5': 'normal', '3': 'normal', '2': 'normal'}
            with contextlib.redirect_stdout(None):
                tracker.put_to_queue(from_note)
                tracker.put_to_queue(to_note)

                patt = tracker.play_from_to(from_note, to_note, in_pattern=False)

                print(list(patt[iso.EVENT_NOTE]))
                print()

            assert list(
                patt[iso.EVENT_NOTE]) == test_semitones, f"Play_from_to pattern mismatch {(t,from_note,to_note)=}"


def test_play_from_to_sin(step=3, subset_div=5):
    """
    step=3 to improve time of test in full test suite should be step=1
    """
    # step, subset_div = 1, 1
    # scale = iso.Scale.major

    scales = iso.Scale.all()

    if subset_div > 1:
        scales = random.choices(scales, k=len(scales) // subset_div)

    for scale in scales:
        print(f"{scale.name=}")
        octave5_start = 5 * scale.octave_size
        for t in range(0, scale.octave_size, step):
            key = iso.Key(t % scale.octave_size, scale)
            test_semitones = [x + octave5_start + key.tonic for x in key.scale.semitones]

            tracker.key = key
            tracker.note_patterns.set_pattern_function('sine')
            from_note = octave5_start + key.tonic
            to_note = from_note + key.scale.octave_size
            tracker.quants_state = {'5': 'normal', '3': 'normal', '2': 'normal'}
            with contextlib.redirect_stdout(None):
                pass
                tracker.put_to_queue(from_note)
                tracker.put_to_queue(to_note)

                patt = tracker.play_from_to(from_note, to_note, in_pattern=False)

            print(list(patt[iso.EVENT_NOTE]))
            assert list(patt[iso.EVENT_NOTE])[0] == t + octave5_start, f"problem with {scale.name=}, tonic={t}"
            # break
        # break


def test_play_from_to_result_rev():
    scale = iso.Scale.major
    scale = iso.Scale(semitones=[0, 2, 4, 6, 8, 10], name="test_scale", octave_size=12,
                      semitones_down=[0, 1, 3, 5, 7, 9, 11])

    for scale in iso.Scale.all():
        if not hasattr(scale, 'semitones_down') or not scale.semitones_down:
            continue
        print(f"{scale.name=}")
        octave5_start = 5 * scale.octave_size
        for t in range(scale.octave_size):
            key = iso.Key(t % scale.octave_size, scale)
            test_semitones = key.scale.semitones_down if hasattr(key.scale, 'semitones_down') else key.scale.semitones
            test_semitones = [x + octave5_start + key.tonic for x in test_semitones]
            test_semitones.reverse()
            rev_semitones = [test_semitones[-1] + key.scale.octave_size] + test_semitones[:-1]
            test_semitones = rev_semitones
            tracker.key = key
            tracker.note_patterns.set_pattern_function('path')
            from_note = octave5_start + key.scale.octave_size + key.tonic
            to_note = from_note - key.scale.octave_size
            tracker.quants_state = {'5': 'normal', '3': 'normal', '2': 'normal'}
            with contextlib.redirect_stdout(None):
                pass
                tracker.put_to_queue(from_note)
                tracker.put_to_queue(to_note)

                patt = tracker.play_from_to(from_note, to_note, in_pattern=False)

                print(list(patt[iso.EVENT_NOTE]))
                print()

            assert list(
                patt[iso.EVENT_NOTE]) == test_semitones, f"Play_from_to pattern mismatch {(t,from_note,to_note)=}"


def test_ch(step=3, subset_div=5):
    """
    step=3 to improve time of test in full test suite should be step=1
    """
    scale = iso.Scale.byname('pelog')
    key = iso.Key(tonic=4, scale=scale)
    tracker.note_patterns.set_pattern_function('chord_improved')
    from_note = 60
    from_note = key.nearest_note(from_note)
    # to_note = from_note+key.scale.octave_size
    tracker.quants_state = {'5': 'normal', '3': 'normal', '2': 'normal'}
    with contextlib.redirect_stdout(None):
        pass
    tracker.put_to_queue(from_note)
    # tracker.put_to_queue(to_note)  # This value should not have meaning

    patt0a = tracker.play_from_to(from_note + 0, 0, in_pattern=False)
    patt4a = tracker.play_from_to(from_note + 4, 0, in_pattern=False)
    patt7a = tracker.play_from_to(from_note + 7, 0, in_pattern=False)
    patt16a = tracker.play_from_to(from_note + 16, 0, in_pattern=False)
    patt12a = tracker.play_from_to(from_note + 12, 0, in_pattern=False)
    patt0b = tracker.play_from_to(from_note + 0, 0, in_pattern=False)
    patt4b = tracker.play_from_to(from_note + 4, 0, in_pattern=False)
    patt7b = tracker.play_from_to(from_note + 7, 0, in_pattern=False)
    patt16b = tracker.play_from_to(from_note + 16, 0, in_pattern=False)
    patt12b = tracker.play_from_to(from_note + 12, 0, in_pattern=False)
    assert True


@pytest.mark.skip  # Skipped because new chords checks are more dynamic and sometimes random used when both chords suit
def test_play_from_to_chord_improved(step=3, subset_div=5):
    """
    step=3 to improve time of test in full test suite should be step=1
    """
    step, subset_div = 1, 1
    scale = iso.Scale.major

    scales = iso.Scale.all()

    if subset_div > 1:
        scales = random.choices(scales, k=len(scales) // subset_div)
    tst = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24]
    for scalex in scales:
        print(f"{scale.name=}")
        octave5_start = 5 * scale.octave_size
        for t in range(5, scale.octave_size, step):
            key = iso.Key(t % scale.octave_size, scale)
            test_semitones = [x + octave5_start + key.tonic for x in key.scale.semitones]

            tracker.key = key
            tracker.note_patterns.set_pattern_function('chord_improved')
            from_note = octave5_start + key.tonic
            # from_note = octave5_start
            from_note = key.nearest_note(from_note)
            # to_note = from_note+key.scale.octave_size
            tracker.quants_state = {'5': 'normal', '3': 'normal', '2': 'normal'}
            with contextlib.redirect_stdout(None):
                pass
            tracker.put_to_queue(from_note)
            # tracker.put_to_queue(to_note)  # This value should not have meaning

            patt1 = tracker.play_from_to(from_note, 0, in_pattern=False)
            assert list(patt1[iso.EVENT_NOTE]) == [(60 + t, 64 + t, 67 + t)], f"problem with {scale.name=}, tonic={t}"

            patt2 = tracker.play_from_to(from_note + 2, 0, in_pattern=False)
            assert list(patt2[iso.EVENT_NOTE]) == [(62 + t, 65 + t, 69 + t)], f"problem with {scale.name=}, tonic={t}"

            patt3 = tracker.play_from_to(from_note + 4, 0, in_pattern=False)
            assert list(patt3[iso.EVENT_NOTE]) == [(64 + t, 67 + t, 71 + t)], f"problem with {scale.name=}, tonic={t}"

            patt4 = tracker.play_from_to(from_note + 5, 0, in_pattern=False)
            assert list(patt4[iso.EVENT_NOTE]) == [(65 + t, 69 + t, 72 + t)], f"problem with {scale.name=}, tonic={t}"

            patt5 = tracker.play_from_to(from_note + 7, 0, in_pattern=False)
            assert list(patt5[iso.EVENT_NOTE]) == [(67 + t, 71 + t, 74 + t)], f"problem with {scale.name=}, tonic={t}"

            patt6 = tracker.play_from_to(from_note + 9, 0, in_pattern=False)
            assert list(patt6[iso.EVENT_NOTE]) == [(69 + t, 72 + t, 76 + t)], f"problem with {scale.name=}, tonic={t}"

            patt7 = tracker.play_from_to(from_note + 11, 0, in_pattern=False)
            assert list(patt7[iso.EVENT_NOTE]) == [(71 + t, 74 + t, 77 + t)], f"problem with {scale.name=}, tonic={t}"

            # 0, 4, 7
            # 2, 5, 9
            # 4, 7, 11
            # 5, 9, 12
            # 7, 11, 14
            # 9, 12, 16
            # 11, 14, 17

            # break
        break
