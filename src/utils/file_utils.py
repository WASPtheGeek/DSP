from pathlib import Path

import numpy as np

from utils.audio_utils import AudioHelper


def save_sound(
        output_folder: str, 
        filename: str, 
        audio_data: np.ndarray, 
        sr: int,
        show_plot: bool = False
    ) -> None:
    """
    Save the synthesized sound to the output folder.

    Parameters:
    output_folder (str): The folder where the output file will be saved.
    filename (str): The name of the output file (without extension).
    audio_data (np.ndarray): The audio data to save.
    sr (int): The sample rate of the audio data.
            show_plot (bool): whether to show the spectogram plot of the final result.
    """
    from scipy.io import wavfile

    full_path = f"{output_folder}/{filename}.wav"
    output_path = Path(full_path)
    wavfile.write(output_path, sr, audio_data.astype(np.float32))
    print(f"Sound saved to: {output_path}")

    if (show_plot):
        AudioHelper.create_spectrogram_plot(
            audio_data, 
            sr,
            show_plot=True
        )