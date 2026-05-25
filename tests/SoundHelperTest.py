import argparse
import os
from time import time
import numpy as np
from src.dsp.models.SoundPassportModel import SoundPassport
from src.dsp.helpers.sound import SoundHelper
from tests.helpers.test_sound_helpers import create_simple_mock_sound

DURATION = 2.0
SAMPLE_RATE = 22050

class SoundHelperTest:
    @staticmethod
    def test_load_sound(file_path: str):
        y, sr = SoundHelper.load_sound(file_path)

        assert isinstance(y, np.ndarray), "Audio time series should be a numpy array"
        assert isinstance(sr, int), "Sampling rate should be an integer"

    @staticmethod
    def test_get_duration(file_path: str):
        y, sr = SoundHelper.load_sound(file_path)
        duration = SoundHelper.get_duration(y, sr)

        assert isinstance(duration, float), "Duration should be a float"
        assert duration > 0, "Duration should be greater than 0"
        assert abs(duration - DURATION) < 0.1, f"Duration should be approximately {DURATION} seconds"

    @staticmethod
    def test_get_sound_passport(file_path: str):
        y, sr = SoundHelper.load_sound(file_path)
        passport: SoundPassport = SoundHelper.get_sound_passport(y, sr)

        assert isinstance(passport, SoundPassport), "Sound passport should be a SoundPassport instance"
        assert hasattr(passport, "duration"), "Sound passport should contain 'duration'"
        assert hasattr(passport, "mean_amplitude"), "Sound passport should contain 'mean_amplitude'"
        assert hasattr(passport, "max_amplitude"), "Sound passport should contain 'max_amplitude'"
        assert hasattr(passport, "min_amplitude"), "Sound passport should contain 'min_amplitude'"
        assert hasattr(passport, "sample_rate"), "Sound passport should contain 'sample_rate'"
        assert hasattr(passport, "amplitude_range"), "Sound passport should contain 'amplitude_range'"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests for SoundHelper class.")

    args = parser.parse_args()

    # Create mock sound
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_file_path = os.path.join(root_dir, "tests/data/test_sound.wav")
    file_path, sr, duration, y = create_simple_mock_sound(test_file_path, duration=DURATION, sr=SAMPLE_RATE)

    print("Running SoundHelper tests...\n")

    test_methods = {
        "test_load_sound": SoundHelperTest.test_load_sound, 
        "test_get_duration": SoundHelperTest.test_get_duration,
        "test_get_sound_passport": SoundHelperTest.test_get_sound_passport
    }

    for test_name, test in test_methods.items():
        print(f"Running {test.__name__}...")
        
        m_start = time()
        test(file_path)
        m_end = time()

        print(f"{test.__name__} passed in {m_end - m_start:.2f} seconds\n")