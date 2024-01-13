import pytest
import json
# import os
from pathlib import Path

from tracker.app.patterns import DurationPatterns
from unittest.mock import mock_open, patch

# Constants for test paths and files
TEST_DIR = Path(__file__).resolve().parent
CONFIG_DIR = TEST_DIR / '../config'
TEST_CONFIG_FILE = CONFIG_DIR / 'duration_patterns.json'


# Helper function to write a temporary config file for testing
# def write_test_config_file(content):
#     os.makedirs(CONFIG_DIR, exist_ok=True)
#     with open(TEST_CONFIG_FILE, 'w') as file:
#         json.dump(content, file)


# Test cases for happy path, edge cases, and error cases
# @pytest.mark.parametrize("test_id, config_content, expected", [
#     # Happy path tests
#     ("HP-1", {"pattern1": "P1"}, {"pattern1": "P1"}),
#     ("HP-2", {"pattern2": "P2", "pattern3": "P3"}, {"pattern2": "P2", "pattern3": "P3"}),
#
#     # Edge cases
#     ("EC-1", {}, {}),  # Empty config file
#
#     # Error cases
#     ("ERR-1", None, FileNotFoundError),  # Config file does not exist
#     ("ERR-2", "Not a JSON", json.JSONDecodeError),  # Invalid JSON content
# ])
# def test_duration_patterns(test_id, config_content, expected):
#     # Arrange
#     if config_content is not None:
#         write_test_config_file(config_content)
#     else:
#         if os.path.exists(TEST_CONFIG_FILE):
#             os.remove(TEST_CONFIG_FILE)
#
#     # Act
#     if isinstance(expected, type) and issubclass(expected, Exception):
#         with pytest.raises(expected):
#             DurationPatterns()
#     else:
#         duration_patterns = DurationPatterns()
#
#     # Assert
#     if not isinstance(expected, type):
#         assert duration_patterns.patterns == expected


@pytest.fixture
def mocker_file_content():
    return '{"pattern1": 5, "pattern2": 10}'


def test_read_config_file(mocker, mocker_file_content):
    mocker.patch('builtins.open', mock_open(read_data=mocker_file_content))
    duration_patterns = DurationPatterns()
    expected_patterns = {"pattern1": 5, "pattern2": 10}

    assert duration_patterns.patterns == expected_patterns