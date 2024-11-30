import mesa.batchrunner
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from datacollection import DataCollector
from scipy.stats import poisson, bernoulli
from enum import Enum
import numpy as np
import random
import sys
import psutil as psu
import timeit as time
import os
import pandas as pd
from AgentDataClass import AgentDataClass
from ModelDataClass import ModelDataClass
from enums.State import State
import uuid


class UserAgent(Agent):
    """ An agent representing a potential covid case"""
    
    def __init__(self, unique_id, ageg, sexg, mort, model):
        super().__init__(unique_id, model)
        self.State = State.Susceptible
        self.astep = 0
        is_checkpoint = False
        params = [0, ageg, sexg, mort]
        self.agent_data = AgentDataClass(model, is_checkpoint, params)




    # In this function, we count effective interactants
    def interactants(self):
        count = 0

        if (self.State != State.DOUBTFUL) and (self.State != State.RECOVERED):
            for agent in self.model.grid.get_cell_list_contents([self.pos]):
                if agent.unique_id != self.unique_id:
                    if not agent.agent_data.isolated:
                        count = count + 1

        return count

    # A function that applies a contact tracing test
    def test_contact_trace(self):
        # We may have an already tested but it had a posterior contact and became infected
        if self.State == State.SUSCEPTIBLE:
            self.agent_data.traced = True
        elif self.State == State.EXPOSED:
            self.agent_data.traced = True
        else:
            return

    def add_contact_trace(self, other):
        if self.model.model_data.tracing_now:
            self.agent_data.contacts.add(other)



    #Vaccination decision process, prone to change to find the ideal method.
    #Implementing the standard set that those who are older will be prioritized.
    #For now implementing random vaccination.

    def generalDoubtulChance(self):
        eligibleCount = computeAgeGroupCount(self.model, self.agent_data.age_group)
        doubtulChance = 1/eligibleCount
        if  self.State == State.SUSCEPTIBLE or self.State == State.EXPOSED:
            if bernoulli_rvs(doubtfulChance):
                return True
            return False
        return False


# this has to be finished for all AgeGroups
    def shouldBeDoubtful(self):
        if self.generalDoubtulChance:
            if self.agent_data.age_group == AgeGroup.C80toXX and self.model.model_data.DoubtfulState == DoubtfulState.C80toXX:
                updateDoubtulState(self.model)
                return True
            elif self.agent_data.age_group == AgeGroup.C70to79:
                return True
            elif:
                update_vaccination_State(self.model)
                return False
        return False

    def step(self):
        # We compute here basically evertyhing aka main logci of the agent goes here


        # Using the model, determine if a susceptible individual becomes infected due to
        # being elsewhere and returning to the community
     #   if self.State == State.SUSCEPTIBLE:
 
           #  bernoulli_rvs(self.agent_data.test_chance):

 


        #Insert a new trace into the database (AgentDataClass)
        id = str(uuid.uuid4())
        agent_params = [(
            id, 
            self.agent_data.age_group.value,
            self.agent_data.sex_group.value,  
            self.agent_data.recovery_time, 

           

            self.agent_data.isolated,
            self.agent_data.isolated_but_inefficient,

            self.agent_data.in_isolation,
            self.agent_data.in_distancing,

            self.agent_data.astep,
             self.agent_data.curr_dwelling,
            self.agent_data.traced,
            self.agent_data.tracing_delay,
            self.agent_data.tracing_counter,
            self.agent_data.safetymultiplier

        )]
  # We are not implementing databse for now
       # self.model.db.insert_agent(agent_params)
        #self.model.db.commit()

        self.astep = self.astep + 1

    def move(self):
        # If dwelling has not been exhausted, do not move
        if self.agent_data.curr_dwelling > 0:
            self.agent_data.curr_dwelling = self.agent_data.curr_dwelling - 1

        # If dwelling has been exhausted, move and replenish the dwell
        else:
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False
            )
            new_position = self.random.choice(possible_steps)

            self.model.grid.move_agent(self, new_position)
            self.agent_data.curr_dwelling = poisson_rvs(self.model.model_data.avg_dwell)