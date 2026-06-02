from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SoundPassport:
    duration: float
    mean_amplitude: float
    max_amplitude: float
    min_amplitude: float
    sample_rate: int
    amplitude_range: float

    def print(self):
        print("Sound Passport:")
        print(f"Sample Rate: {self.sample_rate} Hz")
        print(f"Duration: {self.duration:.2f} seconds")
        print(f"Max Amplitude: {self.max_amplitude:.4f}")
        print(f"Min Amplitude: {self.min_amplitude:.4f}")
        print(f"Mean Amplitude: {self.mean_amplitude:.4f}")
        print(f"Amplitude Range: {self.amplitude_range:.4f}")
        # print(f"Bit Depth: {self.bit_depth} bits")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "duration": self.duration,
            "mean_amplitude": self.mean_amplitude,
            "max_amplitude": self.max_amplitude,
            "min_amplitude": self.min_amplitude,
            "sample_rate": self.sample_rate,
            "amplitude_range": self.amplitude_range
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SoundPassport':
        return SoundPassport(
            duration=data.get('duration', 0.0),
            mean_amplitude=data.get('mean_amplitude', 0.0),
            max_amplitude=data.get('max_amplitude', 0.0),
            min_amplitude=data.get('min_amplitude', 0.0),
            sample_rate=data.get('sample_rate', 0),
            amplitude_range=data.get('amplitude_range', 0.0)
        )