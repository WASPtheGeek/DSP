from pathlib import Path

from src.utils.sound_utils import SoundHelper
from src.utils.file_utils import save_sound
from src.utils.filter_utils import FilterHelper

class BandPassFilter:
    def __init__(
        self,
        file_path: str,
        output_folder: str,
        low_cutoff: float,
        high_cutoff: float,
        order: int,
        output_filename: str,
        show_plot: bool = False
    ):
        """
        

        Params:
            file_path: the initial audio signal file path.
            output_folder: the target folder to save the results.
            low_cutoff: the low frequency from which the filter starts to cut the signal.
            high_cutoff: the high frequency from which the filter starts to cut the signal.
            order: the "agressivity" with which the low pass filter is applied.
            output_filename (str): the output file name
            show_plot (bool): whether to show the spectogram plot of the final result
        """
        self.file_path = file_path
        self.output_folder = output_folder
        self.order = order
        self.output_filename = output_filename
        self.show_plot = show_plot
        self.low_cutoff = low_cutoff
        self.high_cutoff = high_cutoff

    def run(self):
        print("Creating the band-pass filter..")

        y, sr = SoundHelper.load_sound(self.file_path)

        filtered_signal = FilterHelper.band_pass_filter(
            data=y,
            low_cutoff=self.low_cutoff,
            high_cutoff=self.high_cutoff,
            sr=sr,
            order=self.order
        )

        save_sound(
            output_folder=self.output_folder,
            filename=self.output_filename,
            audio_data=filtered_signal,
            sr=sr,
            show_plot=self.show_plot
        )


if __name__ == "__main__":
    file_path = Path("data/processed/noise_masking.wav")
    output_folder = "data/processed"
    output_filename = "band_pass_filter"
    order = 6
    low_cutoff = 950.0
    high_cutoff = 1050.0

    task = BandPassFilter(
        file_path=file_path,
        low_cutoff=low_cutoff,
        high_cutoff=high_cutoff,
        order=order,
        output_folder=output_folder,
        output_filename=output_filename,
        show_plot=True
    )
    
    task.run()        