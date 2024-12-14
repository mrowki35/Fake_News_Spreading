import tkinter as tk
import logging

from models.DisinformationModel import DisinformationModel
from ui.SimulationApp import SimulationApp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_model():
    # Model parameters
    N = 1000  # Number of agents
    alpha = 0.05  # Infection rate
    beta = 0.1  # Probability of believing in disinformation
    gamma = 0.05  # Skepticism rate
    delta = 0.02  # Probability of recovering immunity
    theta = 0.01  # Probability of re-exposure

    model = DisinformationModel(N, alpha, beta, gamma, delta, theta)

    root = tk.Tk()
    app = SimulationApp(root, model, num_steps=1000, update_frequency=1)
    root.mainloop()


if __name__ == "__main__":
    run_model()
