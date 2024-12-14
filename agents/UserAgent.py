import random

from enums.AgeGroup import AgeGroup
from enums.SexGroup import SexGroup
from enums.State import State


class UserAgent:
    def __init__(self, unique_id, model, age_group, sex_group):
        """
        Initializes a user agent.

        Args:
            unique_id (int): Unique identifier for the agent.
            model (DisinformationModel): Reference to the model.
            age_group (AgeGroup): Age group of the agent.
            sex_group (SexGroup): Sex of the agent.
        """
        self.unique_id = unique_id
        self.model = model
        self.age_group = age_group
        self.sex_group = sex_group
        self.state = State.SUSCEPTIBLE  # Initial state of the agent

    def step(self):
        """
        Method executed in each simulation step.
        Determines state transitions based on probabilities.
        """
        if self.state == State.SUSCEPTIBLE:
            self._susceptible_to_exposed()
        elif self.state == State.EXPOSED:
            self._exposed_transition()
        elif self.state == State.INFECTED:
            self._infected_to_recovered()
        elif self.state == State.DOUBTFUL:
            self._doubtful_to_exposed()
        # RECOVERED is a terminal state; no transitions

    def _susceptible_to_exposed(self):
        """
        Transition from S (Susceptible) to E (Exposed) with probability alpha.
        """
        alpha = self.model.alpha
        if random.random() < alpha:
            self.state = State.EXPOSED

    def _exposed_transition(self):
        """
        Transition from E (Exposed) to I (Infected) with probability beta
        or to D (Doubtful) with probability gamma.
        """
        beta = self.model.beta
        gamma = self.model.gamma
        rand = random.random()
        if rand < beta:
            self.state = State.INFECTED
        elif rand < beta + gamma:
            self.state = State.DOUBTFUL

    def _infected_to_recovered(self):
        """
        Transition from I (Infected) to R (Recovered) with probability delta.
        """
        delta = self.model.delta
        if random.random() < delta:
            self.state = State.RECOVERED

    def _doubtful_to_exposed(self):
        """
        Transition from D (Doubtful) to E (Exposed) with probability theta.
        """
        theta = self.model.theta
        if random.random() < theta:
            self.state = State.EXPOSED

    def __repr__(self):
        return (f"UserAgent(id={self.unique_id}, age_group={self.age_group.name}, "
                f"sex_group={self.sex_group.name}, state={self.state.name})")

    def to_string(self):
        """
        Returns a detailed string representation of the UserAgent.
        """
        return (f"UserAgent [ID: {self.unique_id}, Age Group: {self.age_group.name}, "
                f"Sex Group: {self.sex_group.name}, State: {self.state.name}]")
