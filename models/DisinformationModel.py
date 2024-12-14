import random

from agents.UserAgent import UserAgent
from enums.AgeGroup import AgeGroup
from enums.SexGroup import SexGroup
from enums.SocialPlatform import SocialPlatform
from enums.State import State


class DisinformationModel:
    def __init__(self, N, alpha, beta, gamma, delta, theta):
        """
        Initializes the Disinformation Model.

        Args:
            N (int): Number of agents.
            alpha (float): Infection rate.
            beta (float): Probability of believing in disinformation.
            gamma (float): Skepticism rate.
            delta (float): Probability of recovering immunity.
            theta (float): Probability of re-exposure.
        """
        self.num_agents = N
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.theta = theta

        self.agents = []
        for i in range(self.num_agents):
            agent = UserAgent(
                unique_id=i,
                model=self,
                age_group=random.choice(list(AgeGroup)),
                sex_group=random.choice(list(SexGroup)),
                social_platform=random.choice(list(SocialPlatform))
            )
            self.agents.append(agent)

        self.running = True

    def step(self):
        """
        Executes one simulation step.
        Activates all agents in a random order.
        """
        random.shuffle(self.agents)
        for agent in self.agents:
            agent.step()

    def get_state_counts(self):
        """
        Counts the number of agents in each state.

        Returns:
            dict: Keys are states, values are the number of agents in each state.
        """
        states = [agent.state for agent in self.agents]
        counts = {state: states.count(state) for state in State}
        return counts
