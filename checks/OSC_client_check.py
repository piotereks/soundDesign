"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import udp_client

def mk(midi_note):
  client.send_message("/midiKey", midi_note)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  # parser.add_argument("--ip", default="127.0.0.1",
  parser.add_argument("--ip", default="192.168.2.40",
                                          help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=5006,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  for x in range(10):
    print(x)
    # client.send_message("/filter", random.random())
    # client.send_message("/oscControl", random.random())
    # client.send_message("/slider1", random.random())
    client.send_message("/midiKey", int(random.random()*128))
    time.sleep(1)

