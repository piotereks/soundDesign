import yaml
import json
from pathlib import Path
import time

def read_config_file_yaml():
    # print('reading config')

    config_file_yaml = Path('tracker/duration_patterns.yaml')
    # config_file_json = Path('tracker/duration_patterns.json')

    with open(config_file_yaml, 'r') as file:
        # with open('reviewed_pattern_cfg.yaml', 'r') as file:
        patterns_yaml = yaml.safe_load(file)

def read_config_file_json():
    # print('reading config')

    # config_file_yaml = Path('tracker/duration_patterns.yaml')
    # config_file_json = Path('tracker/duration_patterns.json')
    config_file_json = Path('../tracker/config/note_patterns.json')

    with open(config_file_json, 'r') as file:
        # with open('reviewed_pattern_cfg.yaml', 'r') as file:
        patterns_json = json.load(file)
        pass


def cvt_yaml_json():
    # print('reading config')

    config_file_yaml = Path('../tracker/reviewed_pattern_cfg.yaml')

    config_file_json = Path('../tracker/config/note_patterns.json')
    # config_file_json = Path('tracker/duration_patterns.json')

    with open(config_file_yaml, 'r') as file:
        # with open('reviewed_pattern_cfg.yaml', 'r') as file:
        patterns = yaml.safe_load(file)
    with open(config_file_json, 'w') as file_out:
        json.dump(patterns, file_out, indent=4)


# t1 = time.process_time()
# read_config_file_yaml() 
# print('Processing done')
# t2 = time.process_time()
# elapsed_time = t2 - t1
# print(f"{elapsed_time=}")

# t1 = t2
# t1 = time.process_time()
read_config_file_json()
# t2 = time.process_time()
# elapsed_time = t2 - t1
# print(f"{elapsed_time=}")


# cvt_yaml_json()

