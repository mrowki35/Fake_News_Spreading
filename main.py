import tkinter as tk
import logging

from ui.SimulationApp import SimulationApp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_model():
    root = tk.Tk()
    app = SimulationApp(root, num_steps=200, update_frequency=1)
    root.mainloop()


if __name__ == "__main__":
    run_model()
