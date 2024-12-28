import random

from enums.groups.SexGroup import SexGroup
from enums.State import State
from enums.SocialPlatform import SocialPlatform


class UserAgent:
    def __init__(self, unique_id, model, age_group, sex_group, education_group, social_platform):
        """
        Initializes a user agent.

        Args:
            unique_id (int): Unique identifier for the agent.
            model (DisinformationModel): Reference to the model.
            age_group (AgeGroup): Age group of the agent.
            sex_group (SexGroup): Sex of the agent.
            education_group (EducationGroup): Education level of the agent.
            social_platform (SocialPlatform): Social media platform of the agent.
        """
        self.unique_id = unique_id
        self.model = model
        self.age_group = age_group
        self.sex_group = sex_group
        self.education_group = education_group
        self.social_platform = social_platform
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
        Transition from S (Susceptible) to E (Exposed) with probability alpha adjusted by attributes.
        """
        base_alpha = self.model.alpha
        alpha_modifier = self.model.get_alpha_modifier(self)
        effective_alpha = base_alpha * alpha_modifier

        if random.random() < effective_alpha:
            self.state = State.EXPOSED

    def _exposed_transition(self):
        """
        Transition from E (Exposed) to I (Infected) with probability beta adjusted by attributes
        or to D (Doubtful) with probability gamma adjusted by attributes.
        """
        base_beta = self.model.beta
        base_gamma = self.model.gamma
        beta_modifier = self.model.get_beta_modifier(self)
        gamma_modifier = self.model.get_gamma_modifier(self)

        effective_beta = base_beta * beta_modifier
        effective_gamma = base_gamma * gamma_modifier

        rand = random.random()
        if rand < effective_beta:
            self.state = State.INFECTED
        elif rand < effective_gamma:
            self.state = State.DOUBTFUL

    def _infected_to_recovered(self):
        """
        Transition from I (Infected) to R (Recovered) with probability delta adjusted by attributes.
        """
        base_delta = self.model.delta
        delta_modifier = self.model.get_delta_modifier(self)
        effective_delta = base_delta * delta_modifier

        if random.random() < effective_delta:
            self.state = State.RECOVERED

    def _doubtful_to_exposed(self):
        """
        Transition from D (Doubtful) to E (Exposed) with probability theta adjusted by attributes.
        """
        base_theta = self.model.theta
        theta_modifier = self.model.get_theta_modifier(self)
        effective_theta = base_theta * theta_modifier

        if random.random() < effective_theta:
            self.state = State.EXPOSED

    def __repr__(self):
        return (f"UserAgent(id={self.unique_id}, age_group={self.age_group.name}, "
                f"sex_group={self.sex_group.name}, education_group={self.education_group.name}, "
                f"social_platform={self.social_platform.name}, state={self.state.name})")

    def to_dict(self):
        """
        Returns a dictionary representation of the UserAgent.
        """
        return {
            "ID": self.unique_id,
            "Age Group": self.age_group.name,
            "Sex Group": self.sex_group.name,
            "Education Group": self.education_group.name,
            "Social Platform": self.social_platform.name,
            "State": self.state.name
        }

    def to_string(self):
        """
        Returns a detailed string representation of the UserAgent.
        """
        return (f"UserAgent [ID: {self.unique_id}, Age Group: {self.age_group.name}, "
                f"Sex Group: {self.sex_group.name}, Education Group: {self.education_group.name}, "
                f"Social Platform: {self.social_platform.name}, State: {self.state.name}]")
