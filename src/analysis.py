# -*- coding: utf-8 -*-

from src.visualization import population_stats_plot, animal_stats_plot, predator_prey
from examples.graphs import food_objects, animal_objects
import numpy as np
import matplotlib.pyplot as plt
import os


def fourier_analysis(stats: dict, ax: plt.Axes, N_ignore=100, freq_cut=(1, 40), **kwargs) -> None:
    """Plot the Fourier analysis on the given ax"""
    ft_stats = np.fft.rfft(stats[N_ignore:])
    ft_freqs = np.fft.rfftfreq(stats[N_ignore:].shape[0], 1)
    ax.plot(ft_freqs[freq_cut[0]:freq_cut[1]], np.abs(ft_stats[freq_cut[0]:freq_cut[1]]), **kwargs)


def analyse_single(path: str, skipdata=0) -> None:
    """Analyse the data in a filepath. You can skip the first skipdata points in the analysis (startup fluctuations)"""
    # Load the data
    stats = np.load(f"{path}/stats.npy")
    genes = np.load(f"{path}/genes.npy")

    # Plot a bunch of crap
    population_stats_plot(stats[skipdata:], food_objects, animal_objects, title=path)

    predator_prey(stats[skipdata:, 2], stats[skipdata:, 1])
    predator_prey(stats[skipdata:, 1], stats[skipdata:, 0])

    for i, animal in enumerate(animal_objects.keys()):
        animal_stats_plot(genes[::, i, ::, ::], title=animal, labels=(0, 2))
        animal_stats_plot(genes[::, i, ::, ::], title=animal, labels=(2, 8))

    fig, ax = plt.subplots(figsize=(8, 6))

    # Carrot, Fox, Rabbit population Fourier analysis
    fourier_analysis(stats[::, 0], ax, skipdata, label="carrots", color="orange")
    fourier_analysis(stats[::, 1], ax, skipdata, label="fox", color="red")
    fourier_analysis(stats[::, 2], ax, skipdata, label="rabbit", color="grey")

    ax.legend()
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Units")
    fig.show()


if __name__ == "__main__":
    # analyse_single(path="generated/finding_parameters/2021-05-20t154250699648-possiblestable-std0")
    analyse_single("singleruns/2021-05-20t172219201553-evolution_largemap-std0.0")

    # Uncomment to batch process a folder
    """
    path = "generated/finding_parameters/"
    folders = os.listdir(path)
    for directory in folders:
        print(path+directory)
        analyse_single(path+directory)
    """
