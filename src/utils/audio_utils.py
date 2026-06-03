import numpy as np

class AudioHelper:
    @staticmethod
    def create_tone(
        frequency,
        sr=16000,
        duration=1.0,
        amplitude=0.5
    ):
        """
        Create a sine wave tone.

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
    
    @staticmethod
    def normalize_audio(
        audio_data: np.ndarray, 
        target_peak: float, 
        boost_quiet: bool = True
    ) -> np.ndarray:
        """
        Normalize the audio data to the range [-target_peak, target_peak].

        In case the max_peak is >1, we need to scale it down to prevent clipping.
        In case the max_peak is between 0 and 1, we can scale it to keep the same loudness.

        But we should skip the normalization in case we want to keep the original loudness, 
        for example, if there is a whisper and we want to keep it as a whisper, not make it louder.

        Parameters:
        audio_data (np.ndarray): The audio data to normalize.
        target_peak (float): The maximum peak value for the normalized audio.
        boost_quiet (bool): Whether to boost quiet sounds. If True, it will scale up quiet sounds to the desired amplitude.
        Returns:
        np.ndarray: The normalized audio data.
        """
        max_peak = np.max(np.abs(audio_data))

        if max_peak == 0:
            return audio_data # Avoid division by zero
        
        if max_peak < 1 and not boost_quiet:
            return audio_data # Keep the original loudness for quiet sounds
        
        # Scale the audio data to the desired amplitude
        normalized_audio = (audio_data / max_peak) * target_peak

        return normalized_audio