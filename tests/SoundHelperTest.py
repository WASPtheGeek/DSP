import argparse
import os
from time import time
import numpy as np
from src.models.SoundPassportModel import SoundPassport
from src.utils.sound_utils import SoundHelper
from tests.utils.test_sound_utils import create_simple_mock_sound
from src.utils.audio_utils import AudioHelper

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

    @staticmethod
    def test_create_waveform(file_path: str):
        y, sr = SoundHelper.load_sound(file_path)
        max_points = 500
        transpose = True
        x_label = "234234 asdd"
        y_label = "sdfdf 34"
        title = "Test Waveform"
        waveplot = AudioHelper.create_waveform_plot(
            y, 
            sr, 
            show_plot=False,
            max_points=max_points,
            transpose=transpose,
            title=title,
            label_x=x_label,
            label_y=y_label
        )

        assert waveplot is not None, "Waveform plot should not be None"
        assert waveplot.sr == sr, "Waveform plot should have the correct sampling rate"
        assert waveplot.max_samples == max_points, "Waveform plot should have the correct maximum samples"
        assert waveplot.transpose == transpose, "Waveform plot should have the correct transpose attribute"
        assert waveplot.ax.title.get_text() == title, "Waveform plot should have the correct title"
        assert waveplot.ax.get_xlabel() == x_label, "Waveform plot should have the correct x-axis label"
        assert waveplot.ax.get_ylabel() == y_label, "Waveform plot should have the correct y-axis label"

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
        "test_get_sound_passport": SoundHelperTest.test_get_sound_passport,
        "test_create_waveform": SoundHelperTest.test_create_waveform
    }

    total_tests = len(test_methods)

    for i, (test_name, test) in enumerate(test_methods.items(), start=1):
        print(f"({i}/{total_tests}) Running {test.__name__}...")
        
        m_start = time()
        test(file_path)
        m_end = time()

        print(f"{test.__name__} passed in {m_end - m_start:.2f} seconds\n")