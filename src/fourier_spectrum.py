import librosa
import numpy as np
from pathlib import Path

from src.utils.sound_utils import SoundHelper
from src.utils.plot_utils import PlotHelper


def analyze_fourier(
    file_path: str,
    output_path: str,
    output_filename: str,
    show_plot: bool
):
    y, sr = SoundHelper.load_sound(file_path)

    if len(y.shape) > 1:
        y = y[:, 0]

    # take only 1 sec
    n_samples = min(len(y), sr)
    y_chunk = y[:n_samples]

    # add windows
    window = np.hanning(n_samples)
    y_windowed = y_chunk * window

    fft_result = np.fft.fft(y_chunk, n_samples)
    
    # Convert complex numbers to real ones
    magnitudes = np.abs(fft_result) / n_samples
    magnitudes_db = librosa.amplitude_to_db(magnitudes, ref=1.0)

    frequencies = np.fft.fftfreq(n_samples, d=1/sr)

    # As spectrum is simmetrical, take only half
    half = n_samples // 2
    frequencies = frequencies[:half]
    magnitudes_db = magnitudes_db[:half]

    print(f"n_samples: {n_samples}")
    print(f"half: {half}")

    PlotHelper.save_plot(
        title="Fourier amplitude spectrum",
        xlabel="Frequency Hz",
        ylabel="Magnitude dB FS",
        xdata=frequencies,
        ydata=magnitudes_db,
        xlim=5000,
        show_plot=show_plot,
        output_filename=output_filename,
        output_path=output_path
    )


if __name__ == "__main__":
    file_path = Path("data/processed/band_pass_filter.wav")
    output_path = Path("reports/figures")
    output_filename = Path("fourier_spectrum_magnitudeDB")

    analyze_fourier(
        file_path=file_path,
        output_filename=output_filename,
        output_path=output_path,
        show_plot=True
    )