
from pathlib import Path
import time
import numpy as np
import sounddevice as sd

from src.utils.file_utils import save_results


class Audiogram:
    def __init__(
        self, 
        output_folder: str,
        patient_name: str = ""
    ):
        self.output_folder = Path(output_folder)
        # Most commonly used frequency checkpoints
        self.standard_frequencies = [250, 500, 1000, 2000, 4000] # 8000 doesn't work on home PC
        self.patient_name = patient_name
        self.sr = 44100 # sample rate for tones that will be played

        self.results = {
            "left": {},
            "right": {}
        }

    def export_to_json(self):
        """ Saves the results to a json file """
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S")

        result_data = {
            "timestamp": timestamp_str,
            "patient_name": self.patient_name,
            "results": {
                "left": self.results["left"],
                "right": self.results["right"]
            }
        }

        save_results(
            result_data,
            self.output_folder,
            f"audiogram_{self.patient_name}",
            "json"
        )

    def export_to_txt(self):
        """ Saves the results to a text file """
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_lines = []

        report_lines.append(f"=== BINAURAL AUDIOGRAM TEST REPORT ===\n")
        report_lines.append(f"Patient Name: {self.patient_name}\n")
        report_lines.append(f"Date/Time: {timestamp}\n")
        report_lines.append(f"=============================\n\n")
        report_lines.append(f"Frequency (Hz) | Left Ear (dB FS) | Right Ear (dB FS)\n")
        report_lines.append(f"-----------------------------------------------------\n")
        for freq in self.standard_frequencies:
            left_val = self.results["left"].get(freq, float('nan'))
            right_val = self.results["right"].get(freq, float('nan'))
            
            left_str = f"{left_val:16.1f}" if not np.isnan(left_val) else "        N/A     "
            right_str = f"{right_val:17.1f}" if not np.isnan(right_val) else "        N/A     "
            
            report_lines.append(f"{freq:14d} | {left_str} | {right_str}\n")

        full_txt_report = "".join(report_lines)

        save_results(
            data=full_txt_report,
            output_folder=self.output_folder,
            base_filename=f"audiogram_{self.patient_name}",
            extension="txt"
        )

    def __generate_tone(
        self,
        frequency: float,
        db_fs: float,
        channel: str,
        duration: int = 1.5
    ): 
        """
        Generates a tone for the specified frequency in the specified channel.

        frequency(float): the frequency in Hz
        db_fs(float): the volume in db full scale [-90, 0]
        channel (str): sound (ear) channel - left or right
        duration(float): the sound duration in seconds

        Returns:
            tone (np.ndarray) - the generated tone
        """
        t = np.linspace(0, duration, int(duration * self.sr), endpoint=False)

        if (db_fs < -90 or db_fs > 0):
            print(f"ERROR: db_fs provided is incorrect: {db_fs}")
            
            return np.zeros((len(t), 2))
        
        amplitude = 10 ** (db_fs / 20) # mim 0.0; max 1.0; gain is non-linear
        tone = amplitude * np.sin(2 * np.pi * frequency * t)

        # make sure sound doesn't start and end abruptly
        fade_len = int(self.sr * 0.1) # 100 ms
        window = np.ones_like(tone)
        window[:fade_len] = np.linspace(0, 1, fade_len)
        window[-fade_len:] = np.linspace(1, 0, fade_len)
        tone = tone * window
        
        stereo_tone = np.zeros((len(tone), 2))

        if channel == "left":
            stereo_tone[:, 0] = tone
        elif channel == "right":
            stereo_tone[:, 1] = tone

        return stereo_tone


    def __test_frequency(self, frequency: int, channel: str):
        """
        Runs the adaptive test (10 down, 5 up) for a single frequency (Houson-Westlake method). 

        Return:
            threshold (float): a threshold for the provided frequency
        """

        print(f"Testing frequency: {frequency} Hz")
        print(f"Instruction: Hear signal = press ENTER; Silence = type 'n' + ENTER")
        time.sleep(1)

        # Volume dB FS
        current_db = -30.0 # hopefully this won't hurt 
        history = []
        threshold_candidates = {}
        
        while True:
            # Double-double check - make sure sound is not too loud
            if current_db < -90:
                print("✅ You hear ideal zero! 🤔")
                
                return -90
            
            if current_db > 0:
                print("❌ The sound is too loud! Stopping here.")
                return 0.0
            
            tone = self.__generate_tone(frequency, current_db, channel=channel)
            sd.play(tone, self.sr)

            user_input = input(f"Volume {current_db:5.1f} db FS. Can you hear? (Enter / n):").strip().lower()
            sd.stop()

            heard = (user_input != 'n')

            # Staircase
            if heard:
                if history and not history[-1]['heard']:
                    threshold_candidates[current_db] = threshold_candidates.get(current_db, 0) + 1
                    if threshold_candidates[current_db] == 2:
                        print(f"✅ Threshold for the {frequency} Hz is : {current_db} dB FS")
                        
                        return current_db
                    
                history.append({'db': current_db, 'heard': True})
                current_db -= 10.0
            else:
                history.append({'db': current_db, 'heard': False})
                current_db += 5.0

    def __test_ear(self, channel: str):
        """
        channel (str): right or left ear
        """
        ear_channel_str = "Left" if channel == "left" else "Right"

        print("\n" + "🎧"*5 + f"Testing {ear_channel_str} ear" + "🎧"*5)

        for freq in self.standard_frequencies:
            threshold = self.__test_frequency(freq, channel=channel)
            self.results[channel][freq] = threshold

    def run_test(self):
        """
        =================== !!WARNING!! ===================
        Reduce PC volume to 20-30% before running this test. Your headphones aren't calibrated!

        Run the real audiogram test.

        The results are saved to the txt file.
        """
        print(f"Starting the audiogram test...")
        print("\n" + "="*10 + "!! WARNING !!"+ "="*10 + "\n")
        print(f"Reduce PC volume to 20-30% before running this test. Your headphones aren't calibrated!")

        time.sleep(2)

        print(f"Friendly reminder: close windows and doors. Get ready...")
        input(f"Press ENTER to start...")

        self.__test_ear(channel="left")
        
        print("\n⏸️ Left ear test complete. Take a 5-second breath...")
        time.sleep(5)

        self.__test_ear(channel="right")

        print("\n" + "="*10 + " RESULTS "+ "="*10 + "\n")
        print("Frequency (Hz) | Left Ear (dB FS) | Right Ear (dB FS)")
        print("-" * 53)

        for freq in self.standard_frequencies:
            l_res = self.results["left"][freq]
            r_res = self.results["right"][freq]
            print(f"{freq:14d} | {l_res:16.1f} | {r_res:17.1f}")

        self.export_to_txt()
        self.export_to_json()

        print("The end.")


if __name__ == "__main__":
    output_folder = "reports/audiogram_tests"

    # systemctl --user restart pipewire wireplumber

    audiogram = Audiogram(output_folder, patient_name="Me Myself ho hearing aids highest")
    audiogram.run_test()