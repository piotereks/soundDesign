


from tracker.app.isobar_fixes import *
from tracker.app.midi_dev import *

def test_wrk_midi_out():
    import ctypes
    def is_out_open(name='Microsoft GS Wavetable Synth 0'):
        # ctypes.windll.winmm.midiOutOpen(None,name, None, None, None)
        handle = ctypes.c_void_p()
        result = ctypes.windll.winmm.midiOutOpen(ctypes.byref(handle), name, None, None, None)
    #  WindowsPath('C:/Users/piote/PycharmProjects/soundDesign/tracker/saved_midi_files/xoutput.mid')
    #  WindowsPath('C:/Users/piote/PycharmProjects/soundDesign/tracker/saved_midi_files/xoutput.mid')
    device_name = 'Microsoft GS Wavetable Synth 0'
    xxx = mido.open_output(device_name, virtual=False)
    xxx.close()
    filename = (Path(__file__).resolve().parent / ".." / "saved_midi_files" / "xoutput.mid").resolve()
    midi_out = FileOut(filename=filename, device_name=device_name, send_clock=True,
                       virtual=False, ticks_per_beat=480)
    print('xxx')
