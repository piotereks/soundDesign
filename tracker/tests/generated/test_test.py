import mido
import pytest
from tracker.app.cust_iso_midi_file_in import CustMidiFileInputDevice
from tracker.app.iso_midi_message import ( MidiMetaMessageTempo, MidiMessageControl, MidiMessageProgram, MidiMessagePitch, MidiMessageAfter, MidiMessagePoly)
from unittest.mock import MagicMock, Mock
import mido


# Parametrized test cases
import pytest
from unittest.mock import MagicMock, Mock
from tracker.app.cust_iso_midi_file_in import CustMidiFileInputDevice

import pytest
from unittest.mock import Mock

@pytest.mark.parametrize("objects, track_idx, expected_calls, test_id", [
    # Happy path tests
    ([MidiMetaMessageTempo(tempo=500000, location = 0)], 0, {'set_tempo': 1, 'text': 1}, 'happy_path_tempo'),
    # ([MidiMessageControl(cc=1, value=64, channel=0)], 0, {'control': 1}, 'happy_path_control'),
    # ([MidiMessageProgram(program=1, channel=0)], 0, {'program_change': 1}, 'happy_path_program'),
    # ([MidiMessagePitch(pitch=8192, channel=0)], 0, {'pitch_bend': 1}, 'happy_path_pitch'),
    # ([MidiMessageAfter(value=64, channel=0)], 0, {'aftertouch': 1}, 'happy_path_after'),
    # ([MidiMessagePoly(note=60, value=64, channel=0)], 0, {'polytouch': 1}, 'happy_path_poly'),

    # Edge cases
    ([], 0, {}, 'edge_case_empty_list'),
    (None, 0, {}, 'edge_case_none_object')
])

def test_test_midi_message_obj(objects, track_idx, expected_calls, test_id):
    # Arrange
    timeline_inner_mock = Mock()
    timeline_inner_mock.output_device = Mock()
    timeline_inner_mock.output_device.miditrack = {0: []}
    timeline_inner_mock.output_device.get_channel_track = Mock(return_value=0)
    set_tempo_callback_mock = Mock()

    cust_midi_file_input_device = CustMidiFileInputDevice()

    # Act
    cust_midi_file_input_device.midi_message_obj(timeline_inner_mock, objects, track_idx)

    # Assert
    if 'set_tempo' in expected_calls:
        assert timeline_inner_mock.set_tempo.call_count == expected_calls['set_tempo']
        set_tempo_callback_mock.assert_called_once()
    if 'text' in expected_calls:
        assert len(timeline_inner_mock.output_device.miditrack[0]) == expected_calls['text']
    if 'control' in expected_calls:
        assert timeline_inner_mock.output_device.control.call_count == expected_calls['control']
    if 'program_change' in expected_calls:
        assert timeline_inner_mock.output_device.program_change.call_count == expected_calls['program_change']
    if 'pitch_bend' in expected_calls:
        assert timeline_inner_mock.output_device.pitch_bend.call_count == expected_calls['pitch_bend']
    if 'aftertouch' in expected_calls:
        assert timeline_inner_mock.output_device.aftertouch.call_count == expected_calls['aftertouch']
    if 'polytouch' in expected_calls:
        assert timeline_inner_mock.output_device.polytouch.call_count == expected_calls['polytouch']