import librosa
import numpy as np
from pathlib import Path

from src.utils.sound_utils import SoundHelper
from src.utils.plot_utils import PlotHelper


def compute_mini_stft(
    file_path: str,
    output_path: str,
    output_filename: str,
    n_fft=2048, 
    hop_length=512,
    show_plot: bool = False,
):
    y, sr = SoundHelper.load_sound(file_path)

    spectogram = SoundHelper.get_mini_stft(
        y,
        n_fft=n_fft,
        hop_length=hop_length
    )

    PlotHelper.save_spectogram_plot(
        title=f"The file {file_path} spectogram",
        xlabel="Time (sec)",
        ylabel=("Frequency Hz"),
        colorbar_label="Loudness dB FS",
        ylim=8000,
        data=spectogram,
        extent=[0, len(y)/sr, 0, sr/2],
        output_filename=output_filename,
        output_path=output_path,
        show_plot= show_plot
    )
    

if __name__ == "__main__":
    file_path = Path("data/raw/DSP1.wav")
    output_path = Path("reports/figures")
    output_filename = Path("my_voice_spectrogram")
    
    # 2048 & 512; hop_length = n_fft // 4 = 75% overlay
    n_fft=2048
    hop_length=512

    
    # 2048 & 1024; hop_length = n_fft // 2 = 50% overlay
    # n_fft=2048
    # hop_length=1024

    compute_mini_stft(
        file_path=file_path,
        output_filename=output_filename,
        output_path=output_path,
        show_plot=True
    )