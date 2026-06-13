import numpy as np
from typing import Tuple
from scipy.signal import butter, lfilter

class FilterHelper:
    @staticmethod
    def butter_band_pass(
        cutoff_frequency: Tuple[float, float],
        sr: int,
        order: int = 6
    ) -> Tuple:
        """
        Creates a butter filter koefficients for the band pass filter. 

        Parameters:
            cutoff_frequency (Tuple[float, float]): the low and high cutoff frequencies.
            sr (int): sample rate
            order (int): the "aggresivity" of the filter
        
        Returns:
            b, a: koefficients for the filter
        """
        # Normalize the cutoffs against the Nyquist frequency (to prevent the sound distortion)
        nyq = sr * 0.5

        if (len(cutoff_frequency) != 2):
            raise Exception("Band pass filter should have 2 cutoff thresholds (low and high).")

        normalized_low = cutoff_frequency[0] / nyq
        normalized_high = cutoff_frequency[1] / nyq

        b, a = butter(order, [normalized_low, normalized_high], btype="band", analog=False)

        return b, a
        

    @staticmethod
    def butter_low_pass(
        cutoff_frequency: float,
        sr: int,
        order: int = 6
    ) -> Tuple:
        """
        Creates a butter filter koefficients for the low filter. 

        Parameters:
            cutoff_frequency (float): the frequency from which to start the cutoff.
            sr (int): sample rate
            order (int): the "aggresivity" of the filter
        
        Returns:
            b, a: koefficients for the filter
        """
        # Calculate the Nyquist frequency - highest file signal frequency that can be applied
        # without making a distortions into a file
        nyq = sr * 0.5
        normal_cutoff = cutoff_frequency / nyq

        b, a = butter(order, normal_cutoff, btype="low", analog=False)

        return b, a
        

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
        # get butter koefficients for the filter
        b, a = FilterHelper.butter_low_pass(
            order,
            cutoff_frequency,
            sr
        )
        
        # actually apply a low pass filter fn
        y = lfilter(b, a, data)

        return y
    
    @staticmethod
    def band_pass_filter(
        data: np.ndarray,
        sr: int,
        low_cutoff: float,
        high_cutoff: float,
        order: int = 6
    ) -> np.ndarray:
        """
        Applies a band pass filter the provided sound signal.

        Parameters:
            data: the inital sound signal to which the filter will be applied.
            sr: sample rate,
            low_cutoff (float): the low cutoff frequency from which the noise will be removed
            high_cutoff (float): the upper cutoff frequency from which the noise will be removed
            order: the "aggresivity" with which the filter will be applied.
        """
        # Get koefficients for the band pass filter
        b, a = FilterHelper.butter_band_pass(
            [low_cutoff, high_cutoff],
            sr,
            order
        )

        y = lfilter(b, a, data)

        return y