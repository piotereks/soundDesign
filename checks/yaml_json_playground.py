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
    config_file_json = Path('tracker/duration_patterns.json')

    with open(config_file_json, 'r') as file:
        # with open('reviewed_pattern_cfg.yaml', 'r') as file:
        patterns_json = json.load(file)
        pass


# t1 = time.process_time()
# read_config_file_yaml() 
# print('Processing done')
# t2 = time.process_time()
# elapsed_time = t2 - t1
# print(f"{elapsed_time=}")

# t1 = t2
t1 = time.process_time()
read_config_file_json() 
t2 = time.process_time()
elapsed_time = t2 - t1
print(f"{elapsed_time=}")

