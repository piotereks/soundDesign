from tracker.app.isobar_fixes import *
from tracker.app.midi_dev import *
# import isobar as iso

import logging
logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s")

midi_in_loop_name = 'KB loopMIDI Port 0'
midi_out_loop_name = 'KB loopMIDI Port 1'
midi_out_play_name = 'Microsoft GS Wavetable Synth 0'
counter = 0
midi_out = midi_out_play_name

midi_out_device = FileOut(device_name=midi_out, filename='aaaa1x1.mid', send_clock=True,  virtual=False)
# midi_out_device = iso.MidiOutputDevice(device_name=midi_out, send_clock=True,  virtual=False)
# midi_out_device = iso.MidiFileOutputDevice(filename='xaaaa1x1.mid')

timeline = iso.Timeline(output_device=midi_out_device)
timeline.stop_when_done = True
timeline.schedule(

    {"note" : iso.PSequence([55,70,62,68], repeats=1),
     "duration" : 1
     }


                  )

# timeline.schedule(
#
#     {iso.EVENT_NOTE : iso.PSequence([55,70,62,68], repeats=16),
#      iso.EVENT_DURATION : 1
#      }
        # ,output_device=midi_out_device
        #           )

# player_thread.start()
timeline.run()
midi_out_device.write()
# timeline.background()
x = 1

# return self.timeline.schedule({
#     "action": lambda: self.beat(),
#     # "duration": 4
#     "duration": 4 * self.time_signature['numerator'] / self.time_signature['denominator']
#     # "quantize": 1
# },
#     remove_when_done=False)