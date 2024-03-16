

from isobar_ext import *
# from tracker.app.isobar_fixes import *
# from tracker.app.midi_dev import *


def test_wrk_midi_out():
    #  WindowsPath('C:/Users/piote/PycharmProjects/soundDesign/tracker/saved_midi_files/xoutput.mid')
    #  WindowsPath('C:/Users/piote/PycharmProjects/soundDesign/tracker/saved_midi_files/xoutput.mid')
    filename = (Path(__file__).resolve().parent / ".." / "saved_midi_files" / "xoutput.mid").resolve()
    midi_out = FileOut(filename=filename, device_name='Microsoft GS Wavetable Synth 0', send_clock=True,
                       virtual=False, ticks_per_beat=480)
    print('xxx')
