from pathlib import Path

from src.utils.sound_utils import SoundHelper
from src.utils.audio_utils import AudioHelper

class CreateSpectrogram:
    """
    Creates spectogram using librosa built-in functions.
    For the manual calculation sample see the SoundHelper.get_mini_stft!
    """
    def __init__(self, file_path: str, show_plot: bool = False):
        self.file_path = file_path
        self.show_plot = show_plot

    def run(self):
        print(f"Loading sound from: {self.file_path}")
        y, sr = SoundHelper.load_sound(self.file_path)

        spectogram = AudioHelper.create_spectrogram_plot(
            y, 
            sr,
            show_plot=self.show_plot
        )

        return spectogram

if __name__ == "__main__":
    # file_path = Path("data/processed/low_pass_filter.wav")
    file_path = Path("data/processed/low_pass_filter_1.wav")

    task = CreateSpectrogram(
        file_path=file_path,
        show_plot=True
    )

    task.run()