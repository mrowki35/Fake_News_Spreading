import random
import logging

from agents.UserAgent import UserAgent
from enums.State import State
from enums.SocialPlatform import SocialPlatform
from enums.distributions.EducationDistribution import EducationDistribution
from enums.distributions.PlatformAgeDistribution import PlatformAgeDistribution
from enums.distributions.SexDistribution import SexDistribution
from enums.groups.AgeGroup import AgeGroup
from enums.groups.EducationGroup import EducationGroup
from enums.groups.SexGroup import SexGroup


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
            social_platform = random.choice(self.selected_social_platforms)
            age_group = self._choose_age_group(social_platform)
            sex_group = self._choose_sex_group(social_platform)
            education_group = self._choose_education_group(social_platform)

            agent = UserAgent(
                unique_id=i,
                model=self,
                age_group=age_group,
                sex_group=sex_group,
                education_group=education_group,
                social_platform=social_platform,
            )
            self.agents.append(agent)

        if initial_believing_agents > self.num_agents:
            initial_believing_agents = self.num_agents

        believing_agents = random.sample(self.agents, initial_believing_agents)
        for agent in believing_agents:
            agent.state = State.EXPOSED

        logging.info(f"Initialized model with {self.num_agents} agents, "
                     f"{initial_believing_agents} initially EXPOSED.")

    def _choose_age_group(self, social_platform):
        """
        Chooses an age group based on the social platform's distribution.

        Args:
            social_platform (SocialPlatform): The social platform of the agent.

        Returns:
            AgeGroup: Selected age group for the agent.
        """
        distribution = PlatformAgeDistribution.get(social_platform)
        if not distribution:
            logging.warning(f"No age distribution defined for {social_platform.name}. Using uniform distribution.")
            return random.choice(list(AgeGroup))
        age_groups = list(distribution.keys())
        probabilities = list(distribution.values())
        return random.choices(age_groups, weights=probabilities, k=1)[0]

    def _choose_sex_group(self, social_platform):
        """
        Chooses a sex group based on the social platform's distribution.

        Args:
            social_platform (SocialPlatform): The social platform of the agent.

        Returns:
            SexGroup: Selected sex group for the agent.
        """
        distribution = SexDistribution.get(social_platform)
        if not distribution:
            logging.warning(f"No sex distribution defined for {social_platform.name}. Using uniform distribution.")
            return random.choice(list(SexGroup))
        sex_groups = list(distribution.keys())
        probabilities = list(distribution.values())
        return random.choices(sex_groups, weights=probabilities, k=1)[0]

    def _choose_education_group(self, social_platform):
        """
        Chooses an education group based on the social platform's distribution.

        Args:
            social_platform (SocialPlatform): The social platform of the agent.

        Returns:
            EducationGroup: Selected education group for the agent.
        """
        distribution = EducationDistribution.get(social_platform)
        if not distribution:
            logging.warning(
                f"No education distribution defined for {social_platform.name}. Using uniform distribution.")
            return random.choice(list(EducationGroup))
        education_groups = list(distribution.keys())
        probabilities = list(distribution.values())
        return random.choices(education_groups, weights=probabilities, k=1)[0]

    def step(self):
        """
        Executes one simulation step.
        Activates all agents in a random order.
        """
        random.shuffle(self.agents)
        for agent in self.agents:
            agent.step()
