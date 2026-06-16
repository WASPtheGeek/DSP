import librosa
import numpy as np
from pathlib import Path

from src.utils.sound_utils import SoundHelper
from src.utils.file_utils import save_sound
from src.utils.filter_utils import FilterHelper

class AudioAnalyzer:
    def __init__(
        self,
        file_path: str,
    ):
        """
        The audio RMS analyzer.

        Params:
            file_path: the initial audio signal file path.
        """
        self.file_path = file_path

    def run(self):
        print("Analyzing the audio..")

        y, sr = SoundHelper.load_sound(self.file_path)

        # Take only 1 channel for simplicity
        if len(y.shape) >1:
            y = y[:, 0]

        if np.issubdtype(y.dtype, np.integer):
            # Int16 (-32768 to 32768) to float (-1.0 to 1.0)
            audio_float = y / 32768.0
        else:
            audio_float = y

        # Root medium square 
        rms = np.sqrt(np.mean(np.square(audio_float)))

        db1 = librosa.amplitude_to_db(rms, ref=1.0)
        db2 = 20 * np.log10(rms)

        print(f"File: {file_path}")
        print(f"RMS amplitude: {rms}")
        print(f"Loudness: {db1} dB FS")
        print(f"Loudness: {db2} dB FS")


if __name__ == "__main__":
    file_path = Path("data/processed/band_pass_filter.wav")

    task = AudioAnalyzer(
        file_path=file_path
    )
    
    task.run()        