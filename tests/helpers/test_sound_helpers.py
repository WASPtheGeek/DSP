import os
import numpy as np
import soundfile as sf

def create_simple_mock_sound(file_path: str, sr: int = 22050, duration: float = 1.0) -> tuple[str, int, float, np.ndarray]:
    '''
    Create a test sound file with a simple sine wave and save it to the specified path.
    Parameters:
    file_path (str): The path where the test sound file will be saved.
    sr (int): The sampling rate of the audio file. Default is 22050 Hz.
    duration (float): The duration of the audio file in seconds. Default is 1.0 seconds.
    
    Returns:
    file_path, sr, duration, y: The path to the created sound file, its sampling rate, duration, and audio time series.
    '''
    y = (0.3 * np.sin(2*np.pi*440*np.linspace(0, duration, int(sr*duration), False))).astype('float32')

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    sf.write(file_path, y, sr)

    return file_path, sr, duration, y