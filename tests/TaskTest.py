# Test for DSP tasks

import argparse
import os
import numpy as np
from unittest.mock import patch
from src.dsp.tasks.t2.spectogram import CreateSpectrogramTask
from src.dsp.tasks.t2.waveform import CreateWaveformTask
from src.dsp.models.SoundPassportModel import SoundPassport
from src.dsp.tasks.t1.task1_load_sound import LoadSoundTask
from tests.helpers.test_sound_helpers import create_simple_mock_sound

DURATION = 1.2  # Duration of the mock sound in seconds
SR = 22050  # Sampling rate of the mock sound in Hz

def test_load_sound(mock_file_path: str = None):
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

def test_create_waveform(mock_file_path: str = None):
    assert mock_file_path is not None, "Mock file path should not be None"
    task = CreateWaveformTask(file_path=mock_file_path)
    waveplot = task.run()

    # Add assertions to validate the results
    assert waveplot is not None, "Waveform plot should not be None"

def test_create_spectrogram(mock_file_path: str = None):
    assert mock_file_path is not None, "Mock file path should not be None"

    task = CreateSpectrogramTask(file_path=mock_file_path)
    spectrogram = task.run()

    # Add assertions to validate the results
    assert spectrogram is not None, "Spectrogram should not be None"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests for DSP tasks.")

    args = parser.parse_args()

    test_methods = {
        "test_load_sound": test_load_sound,
        "test_create_waveform": test_create_waveform,
        "test_create_spectrogram": test_create_spectrogram,
    }

    print("Setting up mock sound data for tests...\n")

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_file_path = os.path.join(root_dir, "tests/data/test_sound_task1.wav")
    mock_file_path, mock_sr, mock_duration, mock_y = create_simple_mock_sound(test_file_path, duration=DURATION, sr=SR)

    with patch("librosa.load", return_value=(mock_y, mock_sr)):
        total_tests = len(test_methods)
        for i, (test_name, test_method) in enumerate(test_methods.items(), start=1):

            print(f"({i}/{total_tests}) Running test: {test_name}\n")
            test_method(mock_file_path)
            print(f"Test {test_name} passed!\n")
