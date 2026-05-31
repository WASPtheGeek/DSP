import librosa
import numpy as np

from src.dsp.models.SoundPassportModel import SoundPassport

# Sound Helper functions for DSP project

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
    def create_waveform_plot(
        y: np.ndarray,
        sr: int,
        max_points: int = 11025,
        axis: str = "time", # "time" or "h", "m", "s", "ms", "lag", "lag_h", "lag_m", "lag_s", "lag_ms", "none"
        offset: float = 0.0,
        marker: str = "o",
        where: str = "post", # "pre", "post", or "mid"
        title: str | None = "Waveform",
        transpose: bool = False,
        ax: any = None,
        label_x: str = "Time (s)",
        label_y: str = "Amplitude",
        show_plot: bool = False,
    ) -> librosa.display.AdaptiveWaveplot:
        """
        Create a waveform visualization of the audio time series.

        Parameters:
        y (np.ndarray): The audio time series.
        sr (int): The sampling rate of the audio time series.
        max_points (int): Maximum number of points to plot for the waveform. Default is 11025 (0.5 seconds at 22050 Hz).
        axis (str): The x-axis representation. Default is "time".
        offset (float): Time offset in seconds to apply to the x-axis. Default is 0.0.
        marker (str): Marker style for the waveform points. Default is "o".
        where (str): Position of the markers ("pre", "post", or "mid"). Default is "post".
        label (str | None): Label for the waveform plot. Default is "Waveform".
        transpose (bool): If True, display the wave vertically instead of horizontally. Default is False.
        ax (any): Axes to plot on instead of the default plt.gca().
        show_plot (bool): If True, display the plot. Default is False.

        Returns:
        waveplot (librosa.display.AdaptiveWaveplot): The waveform plot object.
        """
        import matplotlib.pyplot as plt

        plt.figure(figsize=(14, 5))

        waveplot: librosa.display.AdaptiveWaveplot = librosa.display.waveshow(
            y,
            sr=sr,
            max_points=max_points,
            axis=axis,
            offset=offset,
            marker=marker,
            where=where,
            ax=ax,
            transpose=transpose
        )

        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        if show_plot:
            plt.show()
       
        return waveplot

    @staticmethod
    def create_spectrogram_plot(
        y: np.ndarray,
        sr: int,
        n_fft: int = 2048,
        hop_length: int = 512,
        win_length: int | None = None,
        window: str = "hann",
        center: bool = True,
        pad_mode: str = "constant",
        title: str | None = "Spectrogram",
        label_x: str = "Time (s)",
        label_y: str = "Frequency (Hz)",
        show_plot: bool = False,
    ) -> librosa.display.Spectrogram:
        """
        Create a spectrogram visualization of the audio time series.

        Parameters:
        y (np.ndarray): The audio time series.
        sr (int): The sampling rate of the audio time series.
        n_fft (int): Length of the FFT window. Default is 2048.
        hop_length (int): Number of samples between successive frames. Default is 512.
        win_length (int | None): Each frame of audio is windowed by `window()`. The window will be of length `win_length` and then padded with zeros to match `n_fft`. If unspecified, defaults to `n_fft`. Default is None.
        window (str): Type of window function to use. Default is "hann".
        center (bool): If True, the signal `y` is padded so that frame `D[:, t]` is centered at `y[t * hop_length]`. Default is True.
        pad_mode (str): If `center=True`, the padding mode to use at the edges of the signal. Default is "constant".
        title (str | None): Title for the spectrogram plot. Default is "Spectrogram".
        label_x (str): Label for the x-axis. Default is "Time (s)".
        label_y (str): Label for the y-axis. Default is "Frequency (Hz)".
        show_plot (bool): If True, display the plot. Default is False.

        Returns:
        spectrogram_plot (librosa.display.Spectrogram): The spectrogram plot object.
        """
        import matplotlib.pyplot as plt

        plt.figure(figsize=(14, 5))

        # Short-time Fourier transform (STFT)
        sftf = librosa.stft(
            y, 
            n_fft=n_fft, 
            hop_length=hop_length, 
            win_length=win_length, 
            window=window, 
            center=center, 
            pad_mode=pad_mode
        )

        # Adjust the amplitude to decibels
        sftf_db = librosa.amplitude_to_db(sftf, ref=np.max)

        spectrogram_plot: librosa.display.Spectrogram = librosa.display.specshow(
            sftf_db,
            sr=sr,
            hop_length=hop_length,
            x_axis='time',
            y_axis='log',
            ax=None
        )

        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        if show_plot:
            # Set the colorbar to show decibel values (magma colormap)
            plt.colorbar(format="%+2.0f dB")
            plt.show()
       
        return spectrogram_plot