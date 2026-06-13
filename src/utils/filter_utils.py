import numpy as np
from scipy.signal import butter, lfilter

class FilterHelper:
    @staticmethod
    def butter_lowpass_filter(
        data: np.ndarray,
        cutoff_frequency: float,
        sr: int,
        order: int=5
    ) -> np.ndarray:
        """
        Applies the low pass filter starting from the specified frequency on the target sound signal.

        Parameters:
            data: the sound signal data
            cutoff_frequency (float): the frequency where the cutoff starts
            sr: the sample rate
            order (int): the "agrressivity" of the filter
        """
        # Calculate the Nyquist frequency - highest file signal frequency that can be applied
        # without making a distortions into a file
        nyq = sr * 0.5
        normal_cutoff = cutoff_frequency / nyq

        b, a = butter(order, normal_cutoff, btype="low", analog=False)

        print(b,a)
        # actually apply a low pass filter fn
        y = lfilter(b, a, data)

        return y