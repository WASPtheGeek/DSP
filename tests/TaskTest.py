# Test for DSP tasks

import argparse
import os
import numpy as np
from unittest.mock import patch
from src.dsp.models.SoundPassportModel import SoundPassport
from src.dsp.tasks.t1.task1_load_sound import LoadSoundTask
from tests.helpers.test_sound_helpers import create_simple_mock_sound

DURATION = 1.2  # Duration of the mock sound in seconds
SR = 22050  # Sampling rate of the mock sound in Hz

def test_load_sound():
    task = LoadSoundTask()
    result = task.run()

    # Add assertions to validate the results
    assert result is not None, "Result should not be None"
    y, sr, passport = result
    assert isinstance(y, np.ndarray), "Audio time series should be a numpy array"
    assert isinstance(sr, int), "Sampling rate should be an integer"
    assert isinstance(passport, SoundPassport), "Sound passport should be a SoundPassport instance"
    assert round(passport.sample_rate) == SR, f"Sample rate should be {SR} Hz"
    assert round(passport.duration, 1) == DURATION, f"Duration should be approx {DURATION} seconds"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests for DSP tasks.")

    args = parser.parse_args()

    test_methods = {
        "test_load_sound": test_load_sound,
    }

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_file_path = os.path.join(root_dir, "tests/data/test_sound_task1.wav")
    mock_file_path, mock_sr, mock_duration, mock_y = create_simple_mock_sound(test_file_path, duration=DURATION, sr=SR)

    with patch("librosa.load", return_value=(mock_y, mock_sr)):
        for test_name, test_method in test_methods.items():
            print(f"Running test: {test_name}")
            test_method()
        print(f"Test {test_name} passed!\n")
