import random
import logging

from agents.UserAgent import UserAgent
from enums.AgeGroup import AgeGroup
from enums.SexGroup import SexGroup
from enums.State import State
from enums.SocialPlatform import SocialPlatform


class DisinformationModel:
    def __init__(self, N, alpha, beta, gamma, delta, theta, initial_believing_agents=0, selected_social_platforms=None):
        """
        Initializes the Disinformation Model.

        Args:
            N (int): Number of agents.
            alpha (float): Infection rate.
            beta (float): Probability of believing in disinformation.
            gamma (float): Skepticism rate.
            delta (float): Probability of recovering immunity.
            theta (float): Probability of re-exposure.
            initial_believing_agents (int): Number of agents initially believing in disinformation.
            selected_social_platforms (list of SocialPlatform): List of social platforms to assign to agents.
        """
        self.num_agents = N
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.theta = theta

        if selected_social_platforms is None or not selected_social_platforms:
            self.selected_social_platforms = list(SocialPlatform)
        else:
            self.selected_social_platforms = selected_social_platforms

        self.agents = []
        for i in range(self.num_agents):
            agent = UserAgent(
                unique_id=i,
                model=self,
                age_group=random.choice(list(AgeGroup)),
                sex_group=random.choice(list(SexGroup)),
                social_platform=random.choice(self.selected_social_platforms),
            )
            self.agents.append(agent)

        if initial_believing_agents > self.num_agents:
            initial_believing_agents = self.num_agents

        believing_agents = random.sample(self.agents, initial_believing_agents)
        for agent in believing_agents:
            agent.state = State.EXPOSED

        logging.info(f"Initialized model with {self.num_agents} agents, "
                     f"{initial_believing_agents} initially EXPOSED.")

    def step(self):
        """
        Executes one simulation step.
        Activates all agents in a random order.
        """
        random.shuffle(self.agents)
        for agent in self.agents:
            agent.step()
