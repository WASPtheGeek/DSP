from dataclasses import dataclass
from pathlib import Path
import time
from typing import Optional, Dict
from matplotlib import pyplot as plt
from src.utils.file_utils import read_json_results


@dataclass
class EarThresholds:
    """ Ear thresholds interface """
    frequencies: Dict[int, float]

    @classmethod
    def from_raw_dict(cls, data: Dict[str, float]) -> "EarThresholds":
        return cls(frequencies={int(k): float(v) for k, v in data.items()})
    
    def to_raw_dict(self) -> Dict[str, float]:
        return {str(k): v for k, v in self.frequencies.items()}

@dataclass
class AudiogramResult:
    """ Audiogram result interface """
    timestamp: str
    patient_name: Optional[str]
    left_ear: EarThresholds
    right_ear: EarThresholds

    @classmethod
    def from_dict(cls, data: dict) -> "AudiogramResult":
        results = data.get("results", {})

        return cls(
            timestamp = data.get("timestamp", ""),
            patient_name = data.get("patient_name", ""),
            left_ear = EarThresholds.from_raw_dict(results.get("left", {})),
            right_ear = EarThresholds.from_raw_dict(results.get("right", {}))
        )
    
    def to_dict(self) -> dict:
        return {
            "timestamp" : self.timestamp,
            "patient_name" : self.patient_name,
            "results" : {
                "left" : self.left_ear.to_raw_dict(),
                "right" : self.right_ear.to_raw_dict()
            }
        }

def plot_audiogram(
    data: Dict[str, AudiogramResult],
    title: str,
    output_folder: str | Path,
    show_plot: bool = False
):
    """
    Plots an audiogram result data.

    Parameters:
        data: an actual audiogram result with name
        title (str): the plot title
        utput_folder (str): The folder where the output file will be saved.
        show_plot (bool): whether to show the audiogram plot of the final result.
    """
    freq = set()
    
    for result in data.values():
        freq.update(result.left_ear.frequencies.keys())
        freq.update(result.right_ear.frequencies.keys())

    frequencies = sorted(list(freq))

    num_plots = len(data)
    fig, axes = plt.subplots(1, num_plots, figsize=(6 * num_plots, 6), sharey=True, squeeze=False)
    fig.suptitle(title, fontsize =16, fontweight='bold')

    for ax, (test_name, result) in zip(axes[0], data.items()):
        left_channel = [result.left_ear.frequencies.get(f) for f in frequencies]
        right_channel = [result.right_ear.frequencies.get(f) for f in frequencies]

        # Draw on plot
        ax.plot(
            frequencies,
            left_channel,
            color='#1f77b4',
            linestyle='-',
            marker='x',
            markersize=10,
            label='Left Ear',
            linewidth=2
        )

        ax.plot(
            frequencies,
            right_channel,
            color='#d62728',
            linestyle='-',
            marker='o',
            markersize=8,
            label='Right Ear',
            linewidth=2
        )

        # Styling
        ax.set_title(test_name, fontsize=13, fontweight='bold', pad=10)
        ax.set_xlabel("Frequency (Hz)", fontsize=11)
        ax.set_xscale('log')  
        ax.set_xticks(frequencies)
        ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
        ax.grid(True, which="both", linestyle="--", alpha=0.5)
        ax.set_ylim(0, -80)

    axes[0][0].set_ylabel("Threshold Level (db FS)", fontsize=11)
    axes[0][0].legend(loc="lower left")

    plt.tight_layout()

    if output_folder:
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"audiogram_results_plot_{timestamp}.png"
        file_path = output_folder / filename

        plt.savefig(file_path, dpi=300, bbox_inches='tight')

        print(f"Audiogram plot saved to {file_path}")

    if show_plot:
        plt.show()
    

def read_results(file: str) -> AudiogramResult:
    """ Read the audiogram results """
    raw_data = read_json_results(file)

    return AudiogramResult.from_dict(raw_data)
    

if __name__ == "__main__":
    files = {
        "No hearing aids" : "reports/audiogram_tests/audiogram_Me_Myself_no_hearing_aids_20260617_120001.json",
        "Phonak infinio sphere" : "reports/audiogram_tests/audiogram_Me_Myself_phonak_infinio_20260617_123000.json",
        "Widex Evoke" : "reports/audiogram_tests/audiogram_Me_Myself_widex_evoke_20260617_121500.json"
    }

    data = {}

    for file_name, file_path in files.items():
        data[file_name] = read_results(file_path)

    plot_audiogram(
        data,
        title="Hearing Device Benchmark: Audiometry (Home Test)",
        output_folder="reports/figures",
        show_plot=True
    )