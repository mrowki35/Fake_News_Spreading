import numpy as np

def compute_state(model,state):
    return count_type(model,state)

def count_type(model, stage):
    count = 0
    for agent in model.schedule.agents:
        if agent.stage == stage:
            count = count + 1

    return count

def compute_isolated(model):
    count = 0
    for agent in model.schedule.agents:
        if agent.agent_data.isolated:
            count = count + 1
    return count


def compute_contacts(model):
    count = 0
    for agent in model.schedule.agents:
        count = count + agent.interactants()
    return count

def compute_stepno(model):
    return model.stepno

def compute_cumul_private_value(model):
    value = 0
    for agent in model.schedule.agents:
        value = value + agent.agent_data.cumul_private_value
    return np.sign(value)*np.power(np.abs(value), model.model_data.alpha_private)/model.num_agents

def compute_cumul_public_value(model):
    value = 0

    for agent in model.schedule.agents:
        value = value + agent.agent_data.cumul_public_value

    return np.sign(value)*np.power(np.abs(value), model.model_data.alpha_public)/model.num_agents


def compute_willing_agents(model):
    count = 0
    for agent in model.schedule.agents:
        if agent.agent_data.willingness:
            count = count + 1
    return count



def compute_age_group_count(model,agegroup):
    count = 0
    for agent in model.schedule.agents:
        if agent.agent_data.age_group == agegroup:
            count = count + 1
    return count


def compute_traced(model):
    tested = 0

    for agent in model.schedule.agents:
        if agent.agent_data.traced:
            tested = tested + 1

    return tested

def compute_num_agents(model):
    return model.num_agents


def compute_datacollection_time(model):
    return model.datacollection_time

def compute_step_time(model):
    return model.step_time

def compute_generally_infected(model):
    return model.model_data.generally_infected
