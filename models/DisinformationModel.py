import random
import logging

from agents.UserAgent import UserAgent
from enums.SocialPlatform import SocialPlatform
from enums.State import State
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
            alpha (float): Base infection rate.
            beta (float): Base probability of believing in disinformation.
            gamma (float): Base skepticism rate.
            delta (float): Base probability of recovering immunity.
            theta (float): Base probability of re-exposure.
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

        self.alpha_modifiers = self._define_alpha_modifiers()
        self.beta_modifiers = self._define_beta_modifiers()
        self.gamma_modifiers = self._define_gamma_modifiers()
        self.delta_modifiers = self._define_delta_modifiers()
        self.theta_modifiers = self._define_theta_modifiers()

        self.agents = []
        for i in range(self.num_agents):
            social_platform = random.choice(self.selected_social_platforms)
            age_group = self._choose_age_group(social_platform)
            sex_group = self._choose_sex_group(social_platform)
            education_group = self._choose_education_group(social_platform, age_group)

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

    def _define_alpha_modifiers(self):
        """
        Define modifiers for alpha based on age, sex, and education.
        """
        age_mod = {
            AgeGroup.from00to09: 0.5,
            AgeGroup.from10to19: 0.7,
            AgeGroup.from20to29: 1.0,
            AgeGroup.from30to39: 1.0,
            AgeGroup.from40to49: 0.9,
            AgeGroup.from50to59: 0.8,
            AgeGroup.from60to69: 0.7,
            AgeGroup.from70to79: 0.6,
            AgeGroup.from80toXX: 0.5,
        }

        sex_mod = {
            SexGroup.MALE: 1.0,
            SexGroup.FEMALE: 0.9,
            SexGroup.OTHER: 0.8,
        }

        edu_mod = {
            EducationGroup.PRIMARY: 0.5,
            EducationGroup.SECONDARY: 0.7,
            EducationGroup.HIGHER: 1.0,
            EducationGroup.VOCATIONAL: 0.8,
        }

        return {
            'age': age_mod,
            'sex': sex_mod,
            'education': edu_mod,
        }

    def _define_beta_modifiers(self):
        """
        Define modifiers for beta based on age, sex, and education.
        """
        # Przykładowe modyfikatory
        age_mod = {
            AgeGroup.from00to09: 0.4,
            AgeGroup.from10to19: 0.6,
            AgeGroup.from20to29: 1.0,
            AgeGroup.from30to39: 1.0,
            AgeGroup.from40to49: 0.8,
            AgeGroup.from50to59: 0.7,
            AgeGroup.from60to69: 0.6,
            AgeGroup.from70to79: 0.5,
            AgeGroup.from80toXX: 0.4,
        }

        sex_mod = {
            SexGroup.MALE: 1.0,
            SexGroup.FEMALE: 0.95,
            SexGroup.OTHER: 0.9,
        }

        edu_mod = {
            EducationGroup.PRIMARY: 0.6,
            EducationGroup.SECONDARY: 0.8,
            EducationGroup.HIGHER: 1.0,
            EducationGroup.VOCATIONAL: 0.85,
        }

        return {
            'age': age_mod,
            'sex': sex_mod,
            'education': edu_mod,
        }

    def _define_gamma_modifiers(self):
        """
        Define modifiers for gamma based on age, sex, and education.
        """
        # Przykładowe modyfikatory
        age_mod = {
            AgeGroup.from00to09: 1.2,
            AgeGroup.from10to19: 1.1,
            AgeGroup.from20to29: 1.0,
            AgeGroup.from30to39: 1.0,
            AgeGroup.from40to49: 1.1,
            AgeGroup.from50to59: 1.2,
            AgeGroup.from60to69: 1.3,
            AgeGroup.from70to79: 1.4,
            AgeGroup.from80toXX: 1.5,
        }

        sex_mod = {
            SexGroup.MALE: 1.0,
            SexGroup.FEMALE: 1.1,
            SexGroup.OTHER: 1.2,
        }

        edu_mod = {
            EducationGroup.PRIMARY: 1.5,
            EducationGroup.SECONDARY: 1.2,
            EducationGroup.HIGHER: 1.0,
            EducationGroup.VOCATIONAL: 1.3,
        }

        return {
            'age': age_mod,
            'sex': sex_mod,
            'education': edu_mod,
        }

    def _define_delta_modifiers(self):
        """
        Define modifiers for delta based on age, sex, and education.
        """
        # Przykładowe modyfikatory
        age_mod = {
            AgeGroup.from00to09: 0.8,
            AgeGroup.from10to19: 0.9,
            AgeGroup.from20to29: 1.0,
            AgeGroup.from30to39: 1.0,
            AgeGroup.from40to49: 1.1,
            AgeGroup.from50to59: 1.2,
            AgeGroup.from60to69: 1.3,
            AgeGroup.from70to79: 1.4,
            AgeGroup.from80toXX: 1.5,
        }

        sex_mod = {
            SexGroup.MALE: 1.0,
            SexGroup.FEMALE: 1.1,
            SexGroup.OTHER: 1.2,
        }

        edu_mod = {
            EducationGroup.PRIMARY: 1.3,
            EducationGroup.SECONDARY: 1.1,
            EducationGroup.HIGHER: 1.0,
            EducationGroup.VOCATIONAL: 1.2,
        }

        return {
            'age': age_mod,
            'sex': sex_mod,
            'education': edu_mod,
        }

    def _define_theta_modifiers(self):
        """
        Define modifiers for theta based on age, sex, and education.
        """
        # Przykładowe modyfikatory
        age_mod = {
            AgeGroup.from00to09: 1.5,
            AgeGroup.from10to19: 1.3,
            AgeGroup.from20to29: 1.0,
            AgeGroup.from30to39: 1.0,
            AgeGroup.from40to49: 1.2,
            AgeGroup.from50to59: 1.4,
            AgeGroup.from60to69: 1.6,
            AgeGroup.from70to79: 1.8,
            AgeGroup.from80toXX: 2.0,
        }

        sex_mod = {
            SexGroup.MALE: 1.0,
            SexGroup.FEMALE: 1.2,
            SexGroup.OTHER: 1.4,
        }

        edu_mod = {
            EducationGroup.PRIMARY: 1.6,
            EducationGroup.SECONDARY: 1.4,
            EducationGroup.HIGHER: 1.0,
            EducationGroup.VOCATIONAL: 1.5,
        }

        return {
            'age': age_mod,
            'sex': sex_mod,
            'education': edu_mod,
        }

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

    def _choose_education_group(self, social_platform, age_group):
        """
        Chooses an education group based on the social platform's distribution and age group.

        Args:
            social_platform (SocialPlatform): The social platform of the agent.
            age_group (AgeGroup): The age group of the agent.

        Returns:
            EducationGroup: Selected education group for the agent.
        """
        distribution = EducationDistribution.get(social_platform)
        if not distribution:
            logging.warning(
                f"No education distribution defined for {social_platform.name}. Using uniform distribution.")
            return random.choice(list(EducationGroup))

        if age_group in [AgeGroup.from00to09, AgeGroup.from10to19]:
            adjusted_distribution = {
                EducationGroup.PRIMARY: distribution.get(EducationGroup.PRIMARY, 0),
                EducationGroup.SECONDARY: distribution.get(EducationGroup.SECONDARY, 0)
            }
            total = sum(adjusted_distribution.values())
            if total == 0:
                logging.warning(
                    f"No specific education distribution for age group {age_group.name} on {social_platform.name}. Using original distribution.")
                education_groups = list(distribution.keys())
                probabilities = list(distribution.values())
            else:
                education_groups = list(adjusted_distribution.keys())
                probabilities = [v / total for v in adjusted_distribution.values()]
        else:
            education_groups = list(distribution.keys())
            probabilities = list(distribution.values())

        return random.choices(education_groups, weights=probabilities, k=1)[0]

    def get_alpha_modifier(self, agent):
        """
        Gets the alpha modifier based on agent's attributes.

        Args:
            agent (UserAgent): The agent.

        Returns:
            float: The modifier for alpha.
        """
        mod = 1.0
        mod *= self.alpha_modifiers['age'].get(agent.age_group, 1.0)
        mod *= self.alpha_modifiers['sex'].get(agent.sex_group, 1.0)
        mod *= self.alpha_modifiers['education'].get(agent.education_group, 1.0)
        return mod

    def get_beta_modifier(self, agent):
        """
        Gets the beta modifier based on agent's attributes.

        Args:
            agent (UserAgent): The agent.

        Returns:
            float: The modifier for beta.
        """
        mod = 1.0
        mod *= self.beta_modifiers['age'].get(agent.age_group, 1.0)
        mod *= self.beta_modifiers['sex'].get(agent.sex_group, 1.0)
        mod *= self.beta_modifiers['education'].get(agent.education_group, 1.0)
        return mod

    def get_gamma_modifier(self, agent):
        """
        Gets the gamma modifier based on agent's attributes.

        Args:
            agent (UserAgent): The agent.

        Returns:
            float: The modifier for gamma.
        """
        mod = 1.0
        mod *= self.gamma_modifiers['age'].get(agent.age_group, 1.0)
        mod *= self.gamma_modifiers['sex'].get(agent.sex_group, 1.0)
        mod *= self.gamma_modifiers['education'].get(agent.education_group, 1.0)
        return mod

    def get_delta_modifier(self, agent):
        """
        Gets the delta modifier based on agent's attributes.

        Args:
            agent (UserAgent): The agent.

        Returns:
            float: The modifier for delta.
        """
        mod = 1.0
        mod *= self.delta_modifiers['age'].get(agent.age_group, 1.0)
        mod *= self.delta_modifiers['sex'].get(agent.sex_group, 1.0)
        mod *= self.delta_modifiers['education'].get(agent.education_group, 1.0)
        return mod

    def get_theta_modifier(self, agent):
        """
        Gets the theta modifier based on agent's attributes.

        Args:
            agent (UserAgent): The agent.

        Returns:
            float: The modifier for theta.
        """
        mod = 1.0
        mod *= self.theta_modifiers['age'].get(agent.age_group, 1.0)
        mod *= self.theta_modifiers['sex'].get(agent.sex_group, 1.0)
        mod *= self.theta_modifiers['education'].get(agent.education_group, 1.0)
        return mod

    def step(self):
        """
        Executes one simulation step.
        Activates all agents in a random order.
        """
        random.shuffle(self.agents)
        for agent in self.agents:
            agent.step()
