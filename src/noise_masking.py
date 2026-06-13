from src.utils.file_utils import save_sound
from src.utils.audio_utils import AudioHelper
from src.utils.sound_utils import SoundHelper

class NoiseMasking:
    def __init__(self, output_folder: str):
        self.output_folder = output_folder
        self.amplitude = 0.5  # 0.1 - Quiet
        self.sr = 16000
        self.frequency = 1000
        self.duration = 3.0
    
    def run(self):
        tone = SoundHelper.create_tone(
            frequency=self.frequency,
            sr=self.sr,
            duration=self.duration,
            amplitude=self.amplitude
        )

        noisy_signal = AudioHelper.create_noise(
            amplitude=self.amplitude + 0.05,  # Slightly louder noise
            sr=self.sr,
            duration=self.duration
        )

        mixed_signal = noisy_signal + tone

        result = AudioHelper.normalize_audio(
            mixed_signal,
            target_peak=0.5,
            boost_quiet=True
        )

        save_sound(
            output_folder=self.output_folder,
            filename="noise_masking_tets",
            audio_data=result,
            sr=self.sr
        )

if __name__ == "__main__":
    folder_path = "data/processed"
    task = NoiseMasking(output_folder=folder_path)
    task.run()
    