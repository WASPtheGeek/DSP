
from pathlib import Path
import time
import numpy as np
import sounddevice as sd


class Audiogram:
    def __init__(
        self, 
        output_folder: str,
        patient_name: str = ""
    ):
        self.output_folder = Path(output_folder)
        # Most commonly used frequency checkpoints
        self.standard_frequencies = [250, 500, 1000, 2000, 4000, 8000]
        self.patient_name = patient_name
        self.sr = 44100 # sample rate for tones that will be played

        self.results = {}

    def export_to_txt(self):
        """ Saves the results to a text file """
        if not self.results:
            print(f"⚠️ No results to export")

            return
        
        self.output_folder.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"audiogram_{self.patient_name}_{timestamp}.txt"
        file_path = self.output_folder / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"=== AUDIOGRAM TEST REPORT ===\n")
            f.write(f"Patient Name: {self.patient_name}\n")
            f.write(f"Date/Time: {timestamp}\n")
            f.write(f"=============================\n\n")
            f.write(f"Frequency (Hz) | Threshold (dB FS)\n")
            f.write(f"---------------------------------\n")
            for freq, db in self.results.items():
                f.write(f"{freq:14d} | {db:15.1f}\n")

        print(f"\n💾 Results successfully exported to: {file_path}")

    def __generate_tone(
        self,
        frequency: float,
        db_fs: float,
        duration: int = 1.5
    ): 
        """
        Generates a tone for the specified frequency.

        frequency(float): the frequency in Hz
        db_fs(float): the volume in db full scale [-90, 0]
        duration(float): the sound duration in seconds

        Returns:
            tone (np.ndarray) - the generated tone
        """
        t = np.linspace(0, duration, int(duration * self.sr), endpoint=False)

        if (db_fs < -90 or db_fs > 0):
            print(f"ERROR: db_fs provided is incorrect: {db_fs}")
            
            return t
        
        amplitude = 10 ** (db_fs / 20) # mim 0.0; max 1.0
        tone = amplitude * np.sin(2 * np.pi * frequency * t)

        # make sure sound doesn't start and end abruptly
        fade_len = int(self.sr * 0.1) # 100 ms
        window = np.ones_like(tone)
        window[:fade_len] = np.linspace(0, 1, fade_len)
        window[-fade_len:] = np.linspace(1, 0, fade_len)

        return tone * window


    def __test_frequency(self, frequency: int):
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
            
            tone = self.__generate_tone(frequency, current_db)
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

        for freq in self.standard_frequencies:
            threshold = self.__test_frequency(freq)
            self.results[freq] = threshold

        print("\n" + "="*10 + " RESULTS "+ "="*10 + "\n")

        for freq, db in self.results.items():
            print(f"Frequency {freq:4d} Hz: {db:5.1f} dB FS")

        self.export_to_txt()

        print("The end.")


if __name__ == "__main__":
    output_folder = "reports/audiogram_tests"

    audiogram = Audiogram(output_folder, patient_name="Me Myself evoke")
    audiogram.run_test()