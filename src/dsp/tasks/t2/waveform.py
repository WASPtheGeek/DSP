from src.dsp.helpers.sound import SoundHelper

class CreateWaveformTask:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def run(self):
        print(f"Loading sound from: {self.file_path}")
        y, sr = SoundHelper.load_sound(self.file_path)

        waveplot = SoundHelper.create_waveform_plot(
            y, 
            sr,
            axis="time",
            # show_plot=True
        )

        return waveplot

if __name__ == "__main__":
    file_path = "tests/data/sounds/DSP1.wav"
    task = CreateWaveformTask(file_path=file_path)
    task.run()