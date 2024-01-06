import pytest
from tracker.app.iso_midi_message import (
    CustMidiNote, MidiMetaMessageTempo, MidiMetaMessageKey, MidiMetaMessageTimeSig,
    MidiMetaMessageTrackName, MidiMetaMessageMidiPort, MidiMetaMessageEndTrack, MidiMessageControl
)


# Test CustMidiNote initialization and attributes
@pytest.mark.parametrize("test_id, channel, pitch, velocity, location, duration", [
    ("happy_path_1", 1, 60, 100, 0, 1),
    ("happy_path_2", 0, 127, 127, 10, 0.5),
    ("edge_case_min_values", 0, 0, 0, 0, None),
    ("edge_case_max_values", 15, 127, 127, 1000, 10),
    ("error_case_invalid_pitch", 1, 128, 100, 0, 1),
    ("error_case_invalid_velocity", 1, 60, 128, 0, 1),
    ("error_case_negative_channel", -1, 60, 128, 0, 1),
    ("error_case_channel_over_15", 16, 60, 128, 0, 1),
])
def test_cust_midi_note(test_id, channel, pitch, velocity, location, duration):
    # Arrange
    if "error_case" in test_id:
        with pytest.raises(ValueError):
            # Act
            CustMidiNote(channel, pitch, velocity, location, duration)
    else:
        # Act
        note = CustMidiNote(channel, pitch, velocity, location, duration)

        # Assert
        assert note.channel == channel
        assert note.pitch == pitch
        assert note.velocity == velocity
        assert note.location == location
        assert note.duration == duration


# Test MidiMetaMessageTempo to_meta_message method
@pytest.mark.parametrize("test_id, tempo, location, time", [
    ("happy_path_1", 500000, 0, 0),
    ("happy_path_2", 250000, 10, 1),
    ("edge_case_min_tempo", 0, 0, 0),
    ("edge_case_max_tempo", 16777215, 1000, 10),
    ("error_case_invalid_tempo", -1, 0, 0),
])
def test_midi_meta_message_tempo(test_id, tempo, location, time):
    # Arrange
    if "error_case" in test_id:
        with pytest.raises(ValueError):
            # Act
            MidiMetaMessageTempo(tempo, location, time=time)
    else:
        tempo_message = MidiMetaMessageTempo(tempo, location, time=time)

        # Act
        meta_message = tempo_message.to_meta_message()

        # Assert
        assert meta_message.tempo == tempo
        assert meta_message.time == time
        assert meta_message.type == 'set_tempo'


# Test MidiMetaMessageKey to_meta_message method
@pytest.mark.parametrize("test_id, key, location, time", [
    ("happy_path_1", "C", 0, 0),
    ("happy_path_2", "F#", 10, 1),
    ("error_case_invalid_key", "H", 0, 0),
])
def test_midi_meta_message_key(test_id, key, location, time):
    # Arrange
    if "error_case" in test_id:
        with pytest.raises(ValueError):
            # Act
            MidiMetaMessageKey(key, location, time=time)
    else:
        key_message = MidiMetaMessageKey(key, location, time=time)

        # Act
        meta_message = key_message.to_meta_message()

        # Assert
        assert meta_message.key == key
        assert meta_message.time == time
        assert meta_message.type == 'key_signature'


# Test MidiMetaMessageTimeSig to_meta_message method
@pytest.mark.parametrize(
    "test_id, numerator, denominator, clocks_per_click, notated_32nd_notes_per_beat, location, time", [
        ("happy_path_1", 4, 4, 24, 8, 0, 0),
        ("happy_path_2", 3, 8, 12, 8, 10, 1),

        ("min_numerator", 1, 4, 1, 1, 0, 0),
        ("min_denominator", 4, 1, 1, 1, 0, 0),
        ("min_clocks_per_click", 4, 4, 1, 1, 0, 0),
        ("min_notated_32nd_notes_per_beat", 4, 4, 1, 1, 0, 0),

        ("max_numerator", 255, 4, 1, 1, 0, 0),
        ("max_denominator", 4, 2 ** 255, 1, 1, 0, 0),
        ("max_clocks_per_click", 4, 4, 255, 1, 0, 0),
        ("max_notated_32nd_notes_per_beat", 4, 4, 1, 255, 0, 0),

        ("error_case_invalid_numerator", -1, 4, 24, 8, 0, 0),
        ("error_case_invalid_denominator", 4, -1, 24, 8, 0, 0),
        ("error_case_non_power_of_two_denominator", 4, 5, 24, 8, 0, 0),
        ("error_case_negative_clocks_per_click", 4, 4, -1, 8, 0, 0),
        ("error_case_negative_notated_32nd_notes_per_beat", 4, 4, 24, -1, 0, 0),
        ("error_case_over_max_denominator", 4, 2 ** 256, 24, 8, 0, 0),
        ("error_case_over_max_clocks_per_click", 4, 4, 256, 8, 0, 0),
        ("error_case_over_max_notated_32nd_notes_per_beat", 4, 4, 24, 256, 0, 0)

    ])
def test_midi_meta_message_time_sig(test_id, numerator, denominator, clocks_per_click, notated_32nd_notes_per_beat,
                                    location, time):
    # Arrange
    if "error_case" in test_id:
        with pytest.raises(ValueError):
            # Act
            MidiMetaMessageTimeSig(numerator, denominator, clocks_per_click, notated_32nd_notes_per_beat, location,
                                   time=time)
    else:
        time_sig_message = MidiMetaMessageTimeSig(numerator, denominator, clocks_per_click, notated_32nd_notes_per_beat,
                                                  location, time=time)

        # Act
        meta_message = time_sig_message.to_meta_message()

        # Assert
        assert meta_message.numerator == numerator
        assert meta_message.denominator == denominator
        assert meta_message.clocks_per_click == clocks_per_click
        assert meta_message.notated_32nd_notes_per_beat == notated_32nd_notes_per_beat
        assert meta_message.time == time
        assert meta_message.type == 'time_signature'


@pytest.mark.parametrize("test_id, channel, cc, value, location, time, track_idx", [
    ("happy_path_1", 1, 64, 127, 2.0, 0, 0),
    ("happy_path_2", 15, 120, 0, 4.5, 10, 1),
    ("happy_path_3", 8, 50, 75, 1.0, 3, 5),
    ("edge_case_channel_0", 0, 100, 64, 1.5, 5, 2),
    ("edge_case_max_cc_value_and_value", 1, 127, 127, 0.0, 2, 3),
    ("edge_case_negative_location", 8, 50, 75, -1.0, 0, 4),
    ("edge_case_max_channel", 15, 60, 100, 3.5, 8, 5),
    ("edge_case_max_program_value", 14, 80, 127, 2.5, 6, 7),
    ("edge_case_zero_track_idx", 10, 40, 50, 1.0, 3, 0),
    ("edge_case_zero_track_idx", 12, 90, 120, 4.0, 12, 0),
    ("error_case_invalid_channel", -1, 75, 110, 2.0, 0, 0),
    ("error_case_invalid_cc", 6, 150, 180, 5.0, 15, 2),
    ("error_case_invalid_value", 9, 100, 300, 3.0, 10, 4),
    ("error_case_negative_time", 7, 45, 80, 1.5, -2, 1),
    ("error_case_negative_track_idx", 11, 30, 40, 0.5, 2, -3),
    # Add more test cases as needed
])
def test_midi_message_control(test_id, channel, cc, value, location, time, track_idx):
    # Arrange
    if "error_case" in test_id:
        with pytest.raises(ValueError):
            # Act
            MidiMessageControl(channel, cc, value, location, time, track_idx)
    else:
        # Act
        midi_message_control = MidiMessageControl(channel, cc, value, location, time, track_idx)

        # Assert
        assert midi_message_control.channel == channel
        assert midi_message_control.cc == cc
        assert midi_message_control.value == value
        assert midi_message_control.location == location
        assert midi_message_control.time == time
        assert midi_message_control.track_idx == track_idx