from pathlib import Path

from src.utils.sound_utils import SoundHelper
from src.utils.file_utils import save_sound
from src.utils.filter_utils import FilterHelper
from src.utils.audio_utils import AudioHelper

class LowPassFilter:
    def __init__(
        self,
        file_path: str,
        output_folder: str,
        cutoff_frequency: float,
        order: int,
        output_filename: str,
    ):
        """
        The low-pass filter cuts everything below the specified cutoff frequency.

        Params:
            file_path: the initial audio signal file path.
            output_folder: the target folder to save the results.
            cutoff_frequency: frequency from which the filter starts to cut the signal.
            order: the "agressivity" with which the low pass filter is applied.
            output_filename (str): the output file name
        """
        self.file_path = file_path
        self.output_folder = output_folder
        self.cutoff_frequency = cutoff_frequency
        self.order = order
        self.output_filename = output_filename

    def run(self):
        print("Creating the low-pass filter..")
        y, sr = SoundHelper.load_sound(self.file_path)

        filtered_signal = FilterHelper.butter_lowpass_filter(
            data=y,
            cutoff_frequency=self.cutoff_frequency,
            sr=sr,
            order=self.order
        )


        save_sound(
            output_folder=self.output_folder,
            filename=self.output_filename,
            audio_data=filtered_signal,
            sr=sr
        )


if __name__ == "__main__":
    file_path = Path("data/processed/noise_masking.wav")
    output_folder = "data/processed"
    output_filename = "low_pass_filter_t"
    cutoff_frequency = 1200.0
    order = 6

    task = LowPassFilter(
        file_path=file_path,
        cutoff_frequency=cutoff_frequency,
        order=order,
        output_folder=output_folder,
        output_filename=output_filename)
    task.run()