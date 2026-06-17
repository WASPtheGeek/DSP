import json
import time
import numpy as np
from pathlib import Path

from src.utils.audio_utils import AudioHelper


def save_sound(
        output_folder: str, 
        filename: str, 
        audio_data: np.ndarray, 
        sr: int,
        show_plot: bool = False
    ) -> None:
    """
    Save the synthesized sound to the output folder.

    Parameters:
    output_folder (str): The folder where the output file will be saved.
    filename (str): The name of the output file (without extension).
    audio_data (np.ndarray): The audio data to save.
    sr (int): The sample rate of the audio data.
            show_plot (bool): whether to show the spectogram plot of the final result.
    """
    from scipy.io import wavfile

    full_path = f"{output_folder}/{filename}.wav"
    output_path = Path(full_path)
    wavfile.write(output_path, sr, audio_data.astype(np.float32))
    print(f"Sound saved to: {output_path}")

    if (show_plot):
        AudioHelper.create_spectrogram_plot(
            audio_data, 
            sr,
            show_plot=True
        )

def save_results(
    data: any,
    output_folder: str | Path,
    base_filename: str, 
    extension: str = "txt",
):
    """
    Save the experiment data results to a file.

    Parameters:
    data: the results as str or object to save
    output_folder (str): The folder where the output file will be saved.
    base_filename (str): The name of the output file (without extension).
    extension (str): the file extension (txt or json)
    """
    if extension != "txt" and extension != "json":
         print(f"⚠️ Unsupported extension for data export: {extension}")

         return
    
    if not data:
            print(f"⚠️ No results to export")

            return
        
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{base_filename}_{timestamp}.{extension}"
    file_path = output_folder / filename

    with open(file_path, "w", encoding="utf-8") as f:
        if extension == "json":
            json.dump(data, f, ensure_ascii=False, indent=4)

        elif extension == "txt":
            f.write(data)

    print(f"\n💾 Results successfully exported to: {file_path}")

def read_json_results(file: str):
    """
    Returns the results data from the json file.
    """
    input_file = Path(file)
    
    if not input_file.exists():
        raise FileNotFoundError(f"⚠️ File path not founded: {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        return json.load(f)
    