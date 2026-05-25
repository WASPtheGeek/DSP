# Load Sound Task

import os
from src.dsp.models.SoundPassportModel import SoundPassport
from src.dsp.helpers.sound import SoundHelper
from src.dsp.helpers.config import ConfigHelper

class LoadSoundTask:
    def __init__(self, config_file: str | None = None):
        self.config_helper = ConfigHelper(config_file)

    def run(self):
        # Get root directory from config file using ConfigHelper
        print("Loading configuration...")
        root_dir = self.config_helper.get_root_dir()
        file_path = os.path.join(root_dir, "data/sounds/DSP1.wav")

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