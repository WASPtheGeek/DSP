from pathlib import Path

from src.utils.sound_utils import SoundHelper

class CreateWaveformTask:
    def __init__(self, file_path: str, show_plot: bool = False):
        self.file_path = file_path
        self.show_plot = show_plot

    def run(self):
        print(f"Loading sound from: {self.file_path}")
        y, sr = SoundHelper.load_sound(self.file_path)

        waveplot = SoundHelper.create_waveform_plot(
            y, 
            sr,
            axis="time",
            show_plot=self.show_plot
        )

        return waveplot

if __name__ == "__main__":
    file_path = Path("data/raw/DSP1.wav")
    task = CreateWaveformTask(file_path=file_path, show_plot=True)
    task.run()