import numpy as np

from src.utils.file_utils import save_sound
from src.utils.audio_utils import AudioHelper

class Superposition:
    def __init__(self, output_folder: str):
        self.output_folder = output_folder
        self.amplitude = 0.5  # Desired amplitude for the final superposition
    
    def run(self):
        tonesHz = [442, 440]  # Frequencies in Hz
        tones = []
        for freq in tonesHz:
            print(f"Creating tone with frequency: {freq} Hz")
            audio_data = AudioHelper.create_tone(
                frequency=freq,
                sr=16000,
                duration=3.0,
                amplitude=self.amplitude
            )
            tones.append(audio_data)

        # Sum the tones to create a superposition
        mixed_signal = np.sum(tones, axis=0)

        normalized_signal = AudioHelper.normalize_audio(
            mixed_signal, 
            target_peak=self.amplitude
        )

        save_sound(
            output_folder=self.output_folder,
            filename="superposition",
            audio_data=normalized_signal,
            sr=16000
        )


if __name__ == "__main__":
    folder_path = "data/processed"
    task = Superposition(output_folder=folder_path)
    task.run()
    