import time
import inspect
import isobar as iso

midi_out = iso.DummyOutputDevice()
timeline = iso.Timeline(120, output_device=midi_out)
timeline.background()  # use background instead of run to enable live performing (async notes passing)
def ts():
    timeline.stop()

def whoami_print():
    print(timeline.current_time)
    print(" hello, I'm %s, daddy is %s" % (whoami(), whosdaddy()))


def whoami():
    return inspect.stack()[2][3]


def whosdaddy():
    return inspect.stack()[3][3]



def mprint(x):
    global gap
    print(x)
    whoami_print()


x=1
metronome_print = timeline.schedule({
    "action":  lambda x: mprint(1),
    # "action": mprint(),
    "duration": 1,
    # "quantize": 0
}
, quantize=1
, remove_when_done=False)

