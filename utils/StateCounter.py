from enums.State import State


class StateCounter:
    def __init__(self, model):
        """
        Initializes the StateCounter.

        Args:
            model (DisinformationModel): Reference to the model.
        """
        self.model = model
        self.history = {state: [] for state in State}

    def count_states(self):
        """
        Counts the number of agents in each state.

        Returns:
            dict: Keys are states, values are the number of agents in each state.
        """
        states = [agent.state for agent in self.model.agents]
        counts = {state: states.count(state) for state in State}
        return counts

    def record_history(self):
        """
        Records the current state counts to history.
        """
        counts = self.count_states()
        for state, count in counts.items():
            self.history[state].append(count)

    def get_history(self):
        """
        Retrieves the history of state counts.

        Returns:
            dict: History of state counts.
        """
        return self.history
