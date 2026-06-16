import numpy as np
from pathlib import Path

from src.utils.sound_utils import SoundHelper
from src.utils.file_utils import save_sound
from utils.plot_utils import PlotHelper


def run_noise_cancellation(
    file_path: str,
    output_path: str,
    output_filename: str,
    show_plot: bool
):
    y, sr = SoundHelper.load_sound(file_path)

    if len(y.shape) > 1:
        y = y[:, 0]

    y_inverted = -1 * y
    y_silence = y + y_inverted

    # validate result
    max_val = np.max(np.abs(y_silence))
    print(f"Max peak in the silence file {max_val}")

    save_sound(
        output_folder=output_path,
        filename=output_filename,
        audio_data=y_silence,
        sr=sr,
        show_plot=False
    )

    spectrogram_silence = SoundHelper.get_mini_stft(y_silence)
    
    PlotHelper.save_spectogram_plot(
        title="Spectrogram of Perfect Silence (Phase Cancellation)",
        xlabel="Time (sec)",
        ylabel="Frequency (Hz)",
        colorbar_label="Loudness (dB FS)",
        ylim=8000,
        data=spectrogram_silence,
        extent=[0, len(y_silence)/sr, 0, sr/2],
        output_filename="silence_spectrogram",
        output_path=Path("reports/figures"),
        show_plot=show_plot,
        vmin=-90,
        vmax=-20
    )


if __name__ == "__main__":
    file_path = Path("data/raw/DSP1.wav")
    output_path = Path("data/processed")
    output_filename = Path("perfect_silence")

    run_noise_cancellation(
        file_path=file_path,
        output_path=output_path,
        output_filename=output_filename,
        show_plot=True
    )