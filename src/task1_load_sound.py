from pathlib import Path

from src.models.SoundPassportModel import SoundPassport
from src.utils.sound_utils import SoundHelper

class LoadSoundTask:
    def run(self):
        file_path = Path("data/raw/DSP1.wav")

        print(f"Loading sound from: {file_path}")

        # Example usage of the SoundHelper to load a sound file
        y, sr = SoundHelper.load_sound(file_path)
        passport: SoundPassport = SoundHelper.get_sound_passport(y, sr)
        
        # Print the sound passport information
        passport.print()

        return y, sr, passport

if __name__ == "__main__":
    task = LoadSoundTask()
    task.run()