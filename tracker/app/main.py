from .tracker import Tracker
from .trackergui import *


def main():
    log_call()
    this_dir = Path(__file__).resolve().parent
    config_file = this_dir / '../config/main_config.json'

    with open(config_file, 'r') as file:
        loaded_config = json.load(file)
        app_config = loaded_config['app']
        tracker_config = loaded_config['tracker']
        midi_mapping = loaded_config.get('midi_mapping')

    midi_out_flag = Tracker.MIDI_OUT_MIX_FILE_DEVICE

    tracker = Tracker(tracker_config=tracker_config, midi_mapping=midi_mapping, midi_out_mode=midi_out_flag)

    TrackerGuiApp(parm_rows=12, parm_cols=5, app_config=app_config, tracker_ref=tracker).run()


if __name__ == '__main__':
    main()
    print('Processing Done.')
