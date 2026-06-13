import librosa
import numpy as np

# Sound Helper functions for the DSP project
class AudioHelper:
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
    
    @staticmethod
    def normalize_audio(
        audio_data: np.ndarray, 
        target_peak: float, 
        boost_quiet: bool = True
    ) -> np.ndarray:
        """
        Normalize the audio data to the range [-target_peak, target_peak].

        In case the max_peak is >1, we need to scale it down to prevent clipping.
        In case the max_peak is between 0 and 1, we can scale it to keep the same loudness.

        But we should skip the normalization in case we want to keep the original loudness, 
        for example, if there is a whisper and we want to keep it as a whisper, not make it louder.

        Parameters:
        audio_data (np.ndarray): The audio data to normalize.
        target_peak (float): The maximum peak value for the normalized audio.
        boost_quiet (bool): Whether to boost quiet sounds. If True, it will scale up quiet sounds to the desired amplitude.
        Returns:
        np.ndarray: The normalized audio data.
        """
        max_peak = np.max(np.abs(audio_data))

        if max_peak == 0:
            return audio_data # Avoid division by zero
        
        if max_peak < 1 and not boost_quiet:
            return audio_data # Keep the original loudness for quiet sounds
        
        # Scale the audio data to the desired amplitude
        normalized_audio = (audio_data / max_peak) * target_peak

        return normalized_audio
    
    @staticmethod
    def create_noise(
        amplitude: float,
        duration: int,
        sr: int,
    ) -> np.ndarray:
        """
        Creates a white noise.

        Params:
            amplitude (float): the 
            duration (int): the audio signal duration in seconds.
            sr: the audio signal sample rate

        Returns:
            The white noise audio signal.
        """
        t = np.linspace(0, duration, int(duration * sr), endpoint=False)
        result = np.random.normal(0, amplitude, size=len(t))

        return result