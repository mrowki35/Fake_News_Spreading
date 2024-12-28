import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread, Event
import time
import pandas as pd
import logging

from enums.groups.EducationGroup import EducationGroup
from enums.groups.SexGroup import SexGroup
from ui.Plotter import Plotter
from utils.StateCounter import StateCounter
from enums.State import State
from models.DisinformationModel import DisinformationModel
from enums.SocialPlatform import SocialPlatform


class SimulationApp:
    def __init__(self, root, num_steps=100, update_frequency=10):
        """
        Initializes the SimulationApp.

        Args:
            root (tk.Tk): The main Tkinter window.
            num_steps (int): Number of simulation steps to run.
            update_frequency (int): Frequency of plot updates (every N steps).
        """
        self.root = root
        self.num_steps = num_steps
        self.update_frequency = update_frequency
        self.current_step = 0
        self.is_running = False
        self.stop_event = Event()
        self.updating_slider = False

        self.root.title("Disinformation Spread Simulation")

        self.plotter = Plotter(self.root)

        # Control Frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, pady=10)

        # Start Button
        self.start_button = ttk.Button(control_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=0, column=0, padx=5)

        # Stop Button
        self.stop_button = ttk.Button(control_frame, text="Stop Simulation", command=self.stop_simulation,
                                      state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        # Restart Button
        self.restart_button = ttk.Button(control_frame, text="Restart Simulation", command=self.restart_simulation,
                                         state=tk.DISABLED)
        self.restart_button.grid(row=0, column=2, padx=5)

        # Save Results Button
        self.save_button = ttk.Button(control_frame, text="Save Results", command=self.save_results, state=tk.DISABLED)
        self.save_button.grid(row=0, column=3, padx=5)

        # Slider Frame
        slider_frame = ttk.Frame(self.root)
        slider_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)

        ttk.Label(slider_frame, text="Step:").pack(side=tk.LEFT, padx=5)
        self.step_slider = ttk.Scale(slider_frame, from_=1, to=self.num_steps, orient=tk.HORIZONTAL,
                                     command=self.on_slider_move)
        self.step_slider.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=5)

        self.step_label = ttk.Label(slider_frame, text="0")
        self.step_label.pack(side=tk.LEFT, padx=5)

        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Simulation Parameters")
        settings_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        # Number of Agents
        ttk.Label(settings_frame, text="Number of Agents:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.num_agents_var = tk.IntVar(value=1000)
        self.num_agents_entry = ttk.Entry(settings_frame, textvariable=self.num_agents_var)
        self.num_agents_entry.grid(row=0, column=1, padx=5, pady=2)

        # Number of Initial Believing Agents
        ttk.Label(settings_frame, text="Initial Believing Agents:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.initial_believing_var = tk.IntVar(value=50)
        self.initial_believing_entry = ttk.Entry(settings_frame, textvariable=self.initial_believing_var)
        self.initial_believing_entry.grid(row=1, column=1, padx=5, pady=2)

        # Alpha
        ttk.Label(settings_frame, text="Alpha:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.alpha_var = tk.DoubleVar(value=0.05)
        self.alpha_entry = ttk.Entry(settings_frame, textvariable=self.alpha_var)
        self.alpha_entry.grid(row=2, column=1, padx=5, pady=2)

        # Beta
        ttk.Label(settings_frame, text="Beta:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.beta_var = tk.DoubleVar(value=0.1)
        self.beta_entry = ttk.Entry(settings_frame, textvariable=self.beta_var)
        self.beta_entry.grid(row=3, column=1, padx=5, pady=2)

        # Gamma
        ttk.Label(settings_frame, text="Gamma:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.gamma_var = tk.DoubleVar(value=0.05)
        self.gamma_entry = ttk.Entry(settings_frame, textvariable=self.gamma_var)
        self.gamma_entry.grid(row=4, column=1, padx=5, pady=2)

        # Delta
        ttk.Label(settings_frame, text="Delta:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        self.delta_var = tk.DoubleVar(value=0.02)
        self.delta_entry = ttk.Entry(settings_frame, textvariable=self.delta_var)
        self.delta_entry.grid(row=5, column=1, padx=5, pady=2)

        # Theta
        ttk.Label(settings_frame, text="Theta:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=2)
        self.theta_var = tk.DoubleVar(value=0.01)
        self.theta_entry = ttk.Entry(settings_frame, textvariable=self.theta_var)
        self.theta_entry.grid(row=6, column=1, padx=5, pady=2)

        # Social Media Platforms
        ttk.Label(settings_frame, text="Social Media Platform:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=2)
        self.selected_platform_var = tk.StringVar(value="")

        platforms = [platform.name for platform in SocialPlatform]
        for idx, platform in enumerate(platforms):
            rb = ttk.Radiobutton(settings_frame, text=platform, variable=self.selected_platform_var, value=platform)
            rb.grid(row=7 + idx // 4, column=1 + idx % 4, sticky=tk.W, padx=5, pady=2)

        # State Counts Frame
        counts_frame = ttk.LabelFrame(self.root, text="Agent States")
        counts_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.state_labels = {}
        self.percent_labels = {}
        for idx, state in enumerate(State):
            label = ttk.Label(counts_frame, text=f"{state.name}: 0")
            label.grid(row=idx, column=0, sticky=tk.W, pady=2)
            self.state_labels[state] = label

            percent_label = ttk.Label(counts_frame, text=f"{state.name} (%): 0.00%")
            percent_label.grid(row=idx, column=1, sticky=tk.W, pady=2)
            self.percent_labels[state] = percent_label

        self.selected_platforms_label = ttk.Label(counts_frame, text="Selected Platform: None",
                                                  font=('Helvetica', 10, 'bold'))
        self.selected_platforms_label.grid(row=len(State), column=0, columnspan=2, sticky=tk.W, pady=2)

        # Additional State Counts for Sex and Education
        education_frame = ttk.LabelFrame(self.root, text="Agent Demographics")
        education_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.education_labels = {}
        for idx, edu in enumerate(EducationGroup):
            label = ttk.Label(education_frame, text=f"{edu.name}: 0")
            label.grid(row=idx, column=0, sticky=tk.W, pady=2)
            self.education_labels[edu] = label

        self.sex_labels = {}
        for idx, sex in enumerate(SexGroup):
            label = ttk.Label(education_frame, text=f"{sex.name}: 0")
            label.grid(row=idx, column=1, sticky=tk.W, pady=2)
            self.sex_labels[sex] = label

    def start_simulation(self):
        """
        Starts the simulation in a separate thread.
        """
        if not self.is_running:
            try:
                N = self.num_agents_var.get()
                initial_believing = self.initial_believing_var.get()
                alpha = self.alpha_var.get()
                beta = self.beta_var.get()
                gamma = self.gamma_var.get()
                delta = self.delta_var.get()
                theta = self.theta_var.get()

                if initial_believing > N:
                    raise ValueError("Initial believing agents cannot exceed total number of agents.")
                if not (0 <= alpha <= 1):
                    raise ValueError("Alpha must be between 0 and 1.")
                if not (0 <= beta <= 1):
                    raise ValueError("Beta must be between 0 and 1.")
                if not (0 <= gamma <= 1):
                    raise ValueError("Gamma must be between 0 and 1.")
                if not (0 <= delta <= 1):
                    raise ValueError("Delta must be between 0 and 1.")
                if not (0 <= theta <= 1):
                    raise ValueError("Theta must be between 0 and 1.")

                selected_platform_name = self.selected_platform_var.get()
                if not selected_platform_name:
                    raise ValueError("Please select one social media platform.")

                selected_platform = SocialPlatform[selected_platform_name]

                self.model = DisinformationModel(
                    N=N,
                    alpha=alpha,
                    beta=beta,
                    gamma=gamma,
                    delta=delta,
                    theta=theta,
                    initial_believing_agents=initial_believing,
                    selected_social_platforms=[selected_platform]
                )

                self.state_counter = StateCounter(self.model)
                self.plotter.reset_plot()
                self.current_step = 0
                self.step_slider.set(0)
                self.step_label.config(text="0")

                counts = self.state_counter.count_states()
                self.state_counter.record_history()
                self.update_state_labels(counts)

                self.plotter.update_plot(self.state_counter.get_history())

                platforms_text = selected_platform_name
                self.selected_platforms_label.config(text=f"Selected Platform: {platforms_text}")
                logging.info(f"Selected Social Media Platform: {platforms_text}")

                self.is_running = True
                self.stop_event.clear()
                self.save_button.config(state=tk.NORMAL)  #
                self.thread = Thread(target=self.run_simulation)
                self.thread.start()
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.restart_button.config(state=tk.NORMAL)
                logging.info("Simulation started.")
            except Exception as e:
                logging.error(f"Error starting simulation: {e}")
                messagebox.showerror("Error", str(e))

    def stop_simulation(self):
        """
        Stops the simulation.
        """
        if self.is_running:
            self.stop_event.set()
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.restart_button.config(state=tk.NORMAL)
            logging.info("Simulation stopped.")

    def restart_simulation(self):
        """
        Restarts the simulation by resetting the model and state counter.
        """
        self.stop_simulation()
        try:
            N = self.num_agents_var.get()
            initial_believing = self.initial_believing_var.get()
            alpha = self.alpha_var.get()
            beta = self.beta_var.get()
            gamma = self.gamma_var.get()
            delta = self.delta_var.get()
            theta = self.theta_var.get()

            if initial_believing > N:
                raise ValueError("Initial believing agents cannot exceed total number of agents.")
            if not (0 <= alpha <= 1):
                raise ValueError("Alpha must be between 0 and 1.")
            if not (0 <= beta <= 1):
                raise ValueError("Beta must be between 0 and 1.")
            if not (0 <= gamma <= 1):
                raise ValueError("Gamma must be between 0 and 1.")
            if not (0 <= delta <= 1):
                raise ValueError("Delta must be between 0 and 1.")
            if not (0 <= theta <= 1):
                raise ValueError("Theta must be between 0 and 1.")

            selected_platform_name = self.selected_platform_var.get()
            if not selected_platform_name:
                raise ValueError("Please select one social media platform.")

            selected_platform = SocialPlatform[selected_platform_name]

            self.model = DisinformationModel(
                N=N,
                alpha=alpha,
                beta=beta,
                gamma=gamma,
                delta=delta,
                theta=theta,
                initial_believing_agents=initial_believing,
                selected_social_platforms=[selected_platform]
            )

            self.state_counter = StateCounter(self.model)
            self.plotter.reset_plot()
            self.current_step = 0
            self.step_slider.set(0)
            self.step_label.config(text="0")

            counts = self.state_counter.count_states()
            self.state_counter.record_history()
            self.update_state_labels(counts)

            self.plotter.update_plot(self.state_counter.get_history())

            platforms_text = selected_platform_name
            self.selected_platforms_label.config(text=f"Selected Platform: {platforms_text}")
            logging.info(f"Selected Social Media Platform: {platforms_text}")

            self.is_running = True
            self.stop_event.clear()
            self.thread = Thread(target=self.run_simulation)
            self.thread.start()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.restart_button.config(state=tk.NORMAL)
            logging.info("Simulation restarted.")
        except Exception as e:
            logging.error(f"Error restarting simulation: {e}")
            messagebox.showerror("Error", str(e))

    def run_simulation(self):
        """
        Runs the simulation steps and updates the plot.
        """
        for _ in range(self.num_steps):
            if self.stop_event.is_set():
                break
            self.model.step()
            self.current_step += 1

            counts = self.state_counter.count_states()
            self.state_counter.record_history()

            self.update_state_labels(counts)

            if self.current_step % self.update_frequency == 0:
                self.update_plot()
                self.update_slider()

            if counts.get(State.RECOVERED, 0) == self.model.num_agents:
                logging.info("All agents have recovered. Ending simulation.")
                break

            time.sleep(0.05)

        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)

    def update_plot(self):
        """
        Updates the plot with the latest history data.
        """
        history = self.state_counter.get_history()
        self.plotter.update_plot(history)

    def update_plot_to_step(self, step):
        """
        Updates the plot to a specific step.

        Args:
            step (int): The step to which the plot should be updated.
        """
        history = self.state_counter.get_history()
        self.plotter.update_plot_to_step(history, step)

    def update_slider(self):
        """
        Updates the slider position based on the current step.
        """
        current_max = self.current_step if self.current_step < self.num_steps else self.num_steps
        self.updating_slider = True
        self.step_slider.configure(to=current_max)
        self.step_slider.set(self.current_step)
        self.step_label.config(text=str(self.current_step))
        self.updating_slider = False

    def on_slider_move(self, val):
        """
        Handles the slider movement to update the plot to a specific step.

        Args:
            val (str): The current value of the slider.
        """
        if self.updating_slider:
            return

        try:
            step = int(float(val))
            history = self.state_counter.get_history()
            max_step = min([len(history[state]) for state in State])

            if step > max_step:
                step = max_step
                self.updating_slider = True
                self.step_slider.set(step)
                self.updating_slider = False

            self.step_label.config(text=str(step))
            self.update_plot_to_step(step)
            counts = {state: history[state][step - 1] if step > 0 else 0 for state in State}
            self.update_state_labels(counts)
        except Exception as e:
            logging.error(f"Error in on_slider_move: {e}")
            messagebox.showerror("Error", f"Failed to update plot: {e}")

    def update_state_labels(self, counts):
        """
        Updates the state labels with current counts and percentages.

        Args:
            counts (dict): Current counts of agents in each state.
        """
        total = sum(counts.values())
        for state, label in self.state_labels.items():
            count = counts.get(state, 0)
            label.config(text=f"{state.name}: {count}")

            percent = (count / total * 100) if total > 0 else 0
            self.percent_labels[state].config(text=f"{state.name} (%): {percent:.2f}%")

        sex_counts = {sex: 0 for sex in SexGroup}
        education_counts = {edu: 0 for edu in EducationGroup}

        for agent in self.model.agents:
            sex_counts[agent.sex_group] += 1
            education_counts[agent.education_group] += 1

        for sex, label in self.sex_labels.items():
            label.config(text=f"{sex.name}: {sex_counts.get(sex, 0)}")

        for edu, label in self.education_labels.items():
            label.config(text=f"{edu.name}: {education_counts.get(edu, 0)}")

    def save_results(self):
        """
        Saves the simulation results to two CSV files:
        1. simulation_steps.csv - zawiera wyniki symulacji krok po kroku.
        2. agent_details.csv - zawiera szczegółowe dane każdego agenta.
        """
        from tkinter import filedialog

        history = self.state_counter.get_history()
        agents = self.model.agents

        df_steps = pd.DataFrame({
            "Step": range(1, len(history[next(iter(history))]) + 1)
        })
        for state in State:
            df_steps[state.name] = history[state]

        agent_data = [agent.to_dict() for agent in agents]
        df_agents = pd.DataFrame(agent_data)

        directory = filedialog.askdirectory(title="Select Directory to Save Results")
        if not directory:
            return

        base_filename = tk.simpledialog.askstring("Input", "Enter base filename (without extension):",
                                                  parent=self.root)
        if not base_filename:
            base_filename = "results"

        filepath_steps = f"{directory}/{base_filename}_simulation_steps.csv"
        filepath_agents = f"{directory}/{base_filename}_agent_details.csv"

        try:
            df_steps.to_csv(filepath_steps, index=False)
            logging.info(f"Simulation steps saved to {filepath_steps}")

            df_agents.to_csv(filepath_agents, index=False)
            logging.info(f"Agent details saved to {filepath_agents}")

            messagebox.showinfo("Success", f"Results saved to:\n{filepath_steps}\n{filepath_agents}")
        except Exception as e:
            logging.error(f"Error saving results: {e}")
            messagebox.showerror("Error", f"Failed to save results: {e}")
