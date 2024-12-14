import tkinter as tk
from tkinter import ttk
from threading import Thread, Event
import time
import logging

from models.DisinformationModel import DisinformationModel
from ui.Plotter import Plotter
from utils.StateCounter import StateCounter
from enums.State import State


class SimulationApp:
    def __init__(self, root, model, num_steps, update_frequency=10):
        """
        Initializes the SimulationApp.

        Args:
            root (tk.Tk): The main Tkinter window.
            model (DisinformationModel): The simulation model.
            num_steps (int): Number of simulation steps to run.
            update_frequency (int): Frequency of plot updates (every N steps).
        """
        self.root = root
        self.model = model
        self.num_steps = num_steps
        self.update_frequency = update_frequency
        self.current_step = 0
        self.is_running = False
        self.stop_event = Event()

        self.root.title("Disinformation Spread Simulation")

        # Initialize Plotter
        self.plotter = Plotter(self.root)

        # Initialize StateCounter
        self.state_counter = StateCounter(self.model)

        # Control Frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, pady=10)

        # Start Button
        self.start_button = ttk.Button(control_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=0, column=0, padx=5)

        # Stop Button
        self.stop_button = ttk.Button(control_frame, text="Stop Simulation", command=self.stop_simulation, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        # Restart Button
        self.restart_button = ttk.Button(control_frame, text="Restart Simulation", command=self.restart_simulation, state=tk.DISABLED)
        self.restart_button.grid(row=0, column=2, padx=5)

        # Slider Frame
        slider_frame = ttk.Frame(self.root)
        slider_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)

        ttk.Label(slider_frame, text="Step:").pack(side=tk.LEFT, padx=5)
        self.step_slider = ttk.Scale(slider_frame, from_=1, to=self.num_steps, orient=tk.HORIZONTAL, command=self.on_slider_move)
        self.step_slider.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=5)

        self.step_label = ttk.Label(slider_frame, text="0")
        self.step_label.pack(side=tk.LEFT, padx=5)

    def start_simulation(self):
        """
        Starts the simulation in a separate thread.
        """
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self.thread = Thread(target=self.run_simulation)
            self.thread.start()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.restart_button.config(state=tk.NORMAL)
            logging.info("Simulation started.")

    def stop_simulation(self):
        """
        Stops the simulation.
        """
        if self.is_running:
            self.stop_event.set()
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            logging.info("Simulation stopped.")

    def restart_simulation(self):
        """
        Restarts the simulation by resetting the model and state counter.
        """
        self.stop_simulation()
        # Reset the model
        self.model = DisinformationModel(
            N=self.model.num_agents,
            alpha=self.model.alpha,
            beta=self.model.beta,
            gamma=self.model.gamma,
            delta=self.model.delta,
            theta=self.model.theta
        )
        # Reset the state counter
        self.state_counter = StateCounter(self.model)
        # Reset the plot
        self.plotter.reset_plot()
        # Reset the slider
        self.step_slider.set(0)
        self.step_label.config(text="0")
        self.current_step = 0
        logging.info("Simulation restarted.")

    def run_simulation(self):
        """
        Runs the simulation steps and updates the plot.
        """
        for _ in range(self.num_steps):
            if self.stop_event.is_set():
                break
            self.model.step()
            self.current_step += 1

            # Update state counts and history
            counts = self.state_counter.count_states()
            self.state_counter.record_history()

            # Update the plot at specified frequency
            if self.current_step % self.update_frequency == 0:
                self.update_plot()
                self.update_slider()

            # Check for termination condition
            if counts.get(State.RECOVERED, 0) == self.model.num_agents:
                logging.info("All agents have recovered. Ending simulation.")
                break

            time.sleep(0.05)  # Short pause for visualization

        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_plot(self):
        """
        Updates the plot with the latest history data.
        """
        history = self.state_counter.get_history()
        self.plotter.update_plot(history)

    def update_slider(self):
        """
        Updates the slider position based on the current step.
        """
        self.step_slider.set(self.current_step)
        self.step_label.config(text=str(self.current_step))

    def on_slider_move(self, val):
        """
        Handles the slider movement to update the plot to a specific step.

        Args:
            val (str): The current value of the slider.
        """
        step = int(float(val))
        self.step_label.config(text=str(step))
        history = self.state_counter.get_history()
        self.plotter.update_plot_to_step(history, step)
