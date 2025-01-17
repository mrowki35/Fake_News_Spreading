import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from enums.State import State
import tkinter as tk


class Plotter:
    def __init__(self, root):
        """
        Initializes the Plotter.

        Args:
            root (tk.Tk): The main Tkinter window.
        """
        self.root = root
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.ax.set_title("Disinformation Spread Over Time")
        self.ax.set_xlabel("Steps")
        self.ax.set_ylabel("Number of Agents")
        self.lines = {}
        for state in State:
            if not state == State.SUSCEPTIBLE:
                line, = self.ax.plot([], [], label=f"{state.name}: 0")
                self.lines[state] = line
        self.legend = self.ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25),
                                     ncol=len(State), fontsize='small')

        self.fig.tight_layout(rect=[0, 0.05, 1, 1])

    def update_plot(self, history):
        """
        Updates the plot with new data.

        Args:
            history (dict): A dictionary containing the history of states.
        """
        for state, line in self.lines.items():
            line.set_data(range(len(history[state])), history[state])
            latest_count = history[state][-1] if history[state] else 0
            line.set_label(f"{state.name}: {latest_count}")
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25),
                       ncol=len(State), fontsize='small')
        self.fig.tight_layout(rect=[0, 0.05, 1, 1])
        self.canvas.draw()

    def update_plot_to_step(self, history, step):
        """
        Updates the plot to a specific step.

        Args:
            history (dict): A dictionary containing the history of states.
            step (int): The step to which the plot should be updated.
        """
        max_step = min([len(history[state]) for state in State])
        if step > max_step:
            step = max_step
        for state, line in self.lines.items():
            line.set_data(range(step), history[state][:step])
            latest_count = history[state][step - 1] if step > 0 else 0
            line.set_label(f"{state.name}: {latest_count}")
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25),
                       ncol=len(State), fontsize='small')
        self.fig.tight_layout(rect=[0, 0.05, 1, 1])
        self.canvas.draw()

    def reset_plot(self):
        """
        Resets the plot by clearing all lines.
        """
        for state, line in self.lines.items():
            line.set_data([], [])
            line.set_label(f"{state.name}: 0")
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25),
                       ncol=len(State), fontsize='small')
        self.fig.tight_layout(rect=[0, 0.05, 1, 1])
        self.canvas.draw()
