from pathlib import Path

import librosa
import numpy as np
from scipy import stats
from src.models.SoundPassportModel import SoundPassport

class SoundHelper:
    @staticmethod
    def load_sound(
        file_path: str,
        sr: float | None = None,
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
        if not Path(file_path).exists():
            raise Exception(f"File {file_path} not found")

        y, sr_result = librosa.load(file_path, sr=sr)

        return y, sr_result
    
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
    
    @staticmethod
    def create_tone(
        frequency,
        sr=16000,
        duration=1.0,
        amplitude=0.5
    ):
        """
        Create a sine wave tone.

        Parameters:
        frequency (float): The frequency of the tone in Hz.
        sr (int): The sample rate. 
        duration (float): The duration per tone in seconds.
        amplitude (float): The amplitude of the synthesized sound.
        """
        # Create the time array for the duration of the sound
        t = np.linspace(0, duration, int(sr * duration), endpoint=False)
        tone = amplitude * np.sin(2 * np.pi * frequency * t)

        return tone
    
    @staticmethod
    def get_mini_stft(
        y: np.ndarray,
        n_fft=2048, 
        hop_length=512
    ):
        """
        Gets a spectogram of sound signal using SFTF.
        Just a mini sample.
        Use librosa.sftf or scipy.signal.stft - (optimized for parallel processing & add padding etc).

        Parameters:
            y: the sound signal,
            sr: the signal sample rate,
            n_fft: Fourier transform window size,
            hop_length: the 1 step size
        """
        # validate hop lenght and frame overlay
        if hop_length > n_fft:
            raise Exception(f"Hop lenght {hop_length} should not exceed the frame length {n_fft}!")
        
        if n_fft // hop_length < 2:
            print("WARNING: spectogram data may be inaccurate as hop lenght and frame lenght overlay is less than 50%!")
        
        if len(y.shape) > 1:
            y = y[:, 0]

        # Hanning window for 1 frame
        window = np.hanning(n_fft)

        num_frames = (len(y) - n_fft) // hop_length + 1 # x axis (aka time in seconds)
        num_frequencies = n_fft // 2 + 1 # this gonna be the y axis of our spectogram

        # Create empty matrix
        sftf_matrix = np.zeros((num_frequencies, num_frames))
        print(f"The STFT matrix sizes: y (frequencies): {num_frequencies}, x (time): {num_frames}. Matrix shapes: {sftf_matrix.shape}")

        # sliding (hop_length) loop
        for frame_i in range(num_frames):
            start_sample = frame_i * hop_length
            end_sample = start_sample + n_fft

            y_chunk = y[start_sample: end_sample]
            y_windowed = y_chunk * window
            fft_result = np.fft.fft(y_windowed)

            fft_half = fft_result[:num_frequencies] # we don't need the other half as it is mirrored
            fft_normalized = np.abs(fft_half) # complex numbers to normal
            magnitude = fft_normalized / n_fft # noramlize scale (magnitude in scale [0.0, 1.0])
            
            # 20 * log10. Added 1e-10 to avoid log10(0) which bursts into -inf
            magnitude_db = 20 * np.log10(magnitude + 1e-10)

            sftf_matrix[:, frame_i] = magnitude_db

        return sftf_matrix
            
    @staticmethod
    def extract_sdt(
            y: np.ndarray,
            sr: int,
            frame_length: int = 1024,
            hop_length: int = 512,
            silence_threshold: int = -45,
            print_values: bool = True
    ):
        """
        Gets the noise and signal standart deviation values from the file.

        frame_length: defines the size of one frames (how many samples there are in 1 frame)
        hop_length: the step size
        signal_threshold: the signal threshold in db FS. everything below the threshold is considered as noise

        Returns:
            mean_noise: mean noise in db FS
            mean_signal: mean signal in db FS
            std_mean: avg standart deviation between noise and signal
        """
        if len(y.shape) > 1:
            y = y[:,0]

        # Calculate each frame avg dB FS
        num_frames = 1 + (len(y) - frame_length) // hop_length
        frame_db = []

        for i in range(num_frames):
            start = i * hop_length
            end = start + frame_length
            frame = y[start:end]

            rms = np.sqrt(np.mean(frame**2) + 1e-10) # add micro epsillon to avoid log(0)
            db = 20 * np.log10(rms)
            frame_db.append(db)

        frame_db = np.array(frame_db)
        noise_frames = frame_db[frame_db < silence_threshold]
        signal_frames = frame_db[frame_db >= silence_threshold]

        mean_noise = np.mean(noise_frames)
        mean_signal = np.mean(signal_frames)

        std_dev = (np.std(noise_frames) + np.std(signal_frames)) // 2

        if print_values:
            print("\n" + "---------Signal data---------" + "\n" )
            print(f"Mean noise: {mean_noise}")
            print(f"Mean signal: {mean_signal}")
            print(f"Standard deviation: {std_dev}")


        return mean_noise, mean_signal, std_dev

    @staticmethod
    def calculate_sdt_probabilities(
            mean_noise: int,
            mean_signal: int,
            std_dev: int,
            threshold: int,
            print_values: bool = True
    ):
        """
        Signal Detection Theory probalibilites.

        threshold (int): criterion

        Returns:
            d_prime: sensitivity, 0 - signal and noise are same lvl, real world sensitivity: 1.5-2, ideal sensitivity >=4
            p_hit: probability of correct positive
            p_false_alarm: probability of false alarm
        """
        d_prime = (mean_signal - mean_noise) / std_dev

        p_false_alarm = stats.norm.sf(threshold, loc=mean_noise, scale=std_dev)
        p_hit = stats.norm.sf(threshold, loc=mean_signal, scale=std_dev)

        if print_values:
            print("\n" + "="*40 + "\n")
            print(f"Sensitivity (d): {d_prime:.2f}")
            print(f"Threshold: {threshold} dB FS")
            print(f"Hit probability: {p_hit * 100:.1f}%")
            print(f"False alarm probability: {p_false_alarm * 100:.1f}%")
            print(f"Miss probability: {(1 - p_hit) * 100:.1f}%")
            print(f"Correct rejection probability: {(1 - p_false_alarm) * 100:.1f}%")

        return d_prime, p_hit, p_false_alarm