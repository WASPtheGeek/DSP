import numpy as np
from pathlib import Path

from src.utils.sound_utils import SoundHelper
from src.utils.file_utils import save_sound


def destroy_phase(
    file_path: str,
    output_path: str,
    output_filename: str,
    show_plot: bool
):
    y, sr = SoundHelper.load_sound(file_path)

    if len(y.shape) > 1:
        y = y[:, 0]

    fft_result = np.fft.fft(y)
    magnitude = np.abs(fft_result)

    phase = np.angle(fft_result)

    print(f"Phase: {phase}")

    fake_fft = magnitude + 0j

    # create sound signal back
    y_no_phase = np.fft.ifft(fake_fft)
    y_no_phase = np.real(y_no_phase)

    # normalize loudness (peak normalization)
    y_no_phase = y_no_phase / np.max(np.abs(y_no_phase)) * 0.5

    save_sound(
        output_folder=output_path,
        filename=output_filename,
        audio_data=y_no_phase,
        sr=sr,
        show_plot=show_plot
    )


if __name__ == "__main__":
    file_path = Path("data/raw/DSP1.wav")
    output_path = Path("data/processed")
    output_filename = Path("destroyed_phase")

    destroy_phase(
        file_path=file_path,
        output_path=output_path,
        output_filename=output_filename,
        show_plot=True
    )