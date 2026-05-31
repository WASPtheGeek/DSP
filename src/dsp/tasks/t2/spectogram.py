from src.dsp.helpers.sound import SoundHelper

class CreateSpectrogramTask:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def run(self):
        print(f"Loading sound from: {self.file_path}")
        y, sr = SoundHelper.load_sound(self.file_path)

        spectogram = SoundHelper.create_spectrogram_plot(
            y, 
            sr,
            # show_plot=True
        )

        return spectogram

if __name__ == "__main__":
    file_path = "tests/data/sounds/DSP1.wav"
    task = CreateSpectrogramTask(file_path=file_path)
    task.run()