from src.utils.file_utils import save_sound
from src.utils.audio_utils import AudioHelper

class Synthesizer:
    def __init__(self, output_folder: str):
        self.output_folder = output_folder
    
    def run(self):
        tones = [250, 1000, 4000]  # Frequencies in Hz
        for freq in tones:
            print(f"Creating tone with frequency: {freq} Hz")
            audio_data = AudioHelper.create_tone(
                frequency=freq,
                sr=16000,
                duration=1.0,
                amplitude=0.5
            )
            save_sound(
                output_folder=self.output_folder,
                filename=f"tone_{freq}Hz",
                audio_data=audio_data,
                sr=16000
            )

if __name__ == "__main__":
    folder_path = "data/processed"
    task = Synthesizer(output_folder=folder_path)
    task.run()
    