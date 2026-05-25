import librosa
import numpy as np

from src.dsp.models.SoundPassportModel import SoundPassport

# Sound Helper functions for DSP project

class SoundHelper:
    @staticmethod
    def load_sound(
        file_path: str,
        sr: float | None = 22050,
    ) -> tuple[np.ndarray, int]:
        """
        Load a sound file and return the audio time series and sampling rate.

        Parameters:
        file_path (str): Path to the sound file.
        sr (float | None): Sampling rate to use when loading the sound. Optional.

        Returns:
        y (np.ndarray): Audio time series.
        sr (int): Sampling rate of the audio time series.
        """
        y, sr = librosa.load(file_path, sr=sr)

        return y, sr
    
    @staticmethod
    def get_duration(y: np.ndarray, sr: int) -> float:
        """
        Calculate the duration of an audio time series.

        Parameters:
        y (np.ndarray): The audio time series.
        sr (int): The sampling rate of the audio time series.

        Returns:
        duration (float): Duration of the audio in seconds.
        """
        duration = len(y) / sr

        return duration

    @staticmethod
    def get_sound_passport(y: np.ndarray, sr: int) -> SoundPassport:
        """
        Generate a sound passport containing key characteristics of the audio.

        Parameters:
        y (np.ndarray): The audio time series.
        sr (int): The sampling rate of the audio time series.

        Returns:
        passport (SoundPassport): A SoundPassport object containing the sound passport information.
        """
        duration = SoundHelper.get_duration(y, sr)
        mean_amplitude = np.mean(y)
        max_amplitude = np.max(y)
        min_amplitude = np.min(y)

        sample_rate = sr
        amplitude_range = max_amplitude - min_amplitude

        passport = SoundPassport(
            duration=duration,
            mean_amplitude=mean_amplitude,
            max_amplitude=max_amplitude,
            min_amplitude=min_amplitude,
            sample_rate=sample_rate,
            amplitude_range=amplitude_range,
            # "bit_depth": bit_depth
        )

        return passport
