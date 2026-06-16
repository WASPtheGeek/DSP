import os
from typing import Tuple
from matplotlib import pyplot as plt
import numpy as np
from src.models.SoundPassportModel import SoundPassport

class PlotHelper:
    @staticmethod
    def save_plot(
        title: str,
        xlabel: str,
        ylabel: str,
        xdata: np.ndarray,
        ydata: np.ndarray,
        xlim: int,
        output_path: str,
        output_filename: str,
        grid: bool = True,
        show_plot: bool = False,
    ):
        """
        Saves a plot for the specified values
        """

        plt.figure(figsize=(10, 4))
        plt.plot(xdata, ydata, color="purple")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(grid)

        # Only show from 0 to x Hz
        plt.xlim(0, xlim)

        if output_path:
            if output_filename:
                output_path = os.path.join(output_path, f"{output_filename}.png")

            plt.savefig(output_path)
            print(f"Plot {title} successfully saved to {output_path}")

        if show_plot:
            plt.show()

    @staticmethod
    def save_spectogram_plot(
        title: str,
        xlabel: str,
        ylabel: str,
        colorbar_label: str,
        data: np.ndarray,
        ylim: int,
        output_path: str,
        output_filename: str,
        extent: Tuple[float, float, float, float],
        show_plot: bool = False,
        vmin: int = -90,
        vmax: int = -20,
    ):
        """
        Saves a plot for the spectogram
        """

        plt.figure(figsize=(12, 6))

        img = plt.imshow(
            data,
            cmap="magma",
            origin="lower",
            aspect="auto",
            vmin=vmin,
            vmax=vmax,
            extent=extent
        )

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        cbar = plt.colorbar(img)
        cbar.set_label(colorbar_label)

        plt.ylim(0, ylim)

        if output_path:
            if output_filename:
                output_path = os.path.join(output_path, f"{output_filename}.png")

            plt.savefig(output_path)
            print(f"Plot {title} successfully saved to {output_path}")

        if show_plot:
            plt.show()
        