from pathlib import Path
import numpy as np


class Synthesizer:
    def __init__(self, output_folder: str):
        self.output_folder = output_folder

    def save_sound(self, filename: str, audio_data: np.ndarray, sr: int):
        """
        Save the synthesized sound to the output folder.

        Parameters:
        filename (str): The name of the output file (without extension).
        audio_data (np.ndarray): The audio data to save.
        sr (int): The sample rate of the audio data.
        """
        from scipy.io import wavfile

        full_path = f"{self.output_folder}/{filename}.wav"
        output_path = Path(full_path)
        wavfile.write(output_path, sr, audio_data.astype(np.float32))
        print(f"Sound saved to: {output_path}")

    def create_tone(
        self, 
        frequency,
        sr=16000,
        duration=1.0,
        amplitude=0.5
    ):
        """
        Synthesize a sound and save it to the output folder.

        Parameters:
        frequency (float): The frequency of the tone in Hz.
        sr (int): The sample rate. 
        duration (float): The duration per tone in seconds.
        amplitude (float): The amplitude of the synthesized sound.
        """
        # Create the time array for the duration of the sound
        t = np.linspace(0, duration, int(sr * duration), endpoint=False)
        tone = amplitude * np.sin(2 * np.pi * frequency * t)

        return tone
    
    def run(self):
        tones = [250, 1000, 4000]  # Frequencies in Hz
        for freq in tones:
            print(f"Creating tone with frequency: {freq} Hz")
            audio_data = self.create_tone(
                frequency=freq,
                sr=16000,
                duration=1.0,
                amplitude=0.5
            )
            self.save_sound(filename=f"tone_{freq}Hz", audio_data=audio_data, sr=16000)

if __name__ == "__main__":
    folder_path = "data/processed"
    task = Synthesizer(output_folder=folder_path)
    task.run()
    