from models.DisinformationModel import DisinformationModel
from enums.State import State


def run_model():
    N = 1000  # Number of agents
    alpha = 0.05  # Infection rate
    beta = 0.1  # Probability of believing in disinformation
    gamma = 0.05  # Skepticism rate
    delta = 0.02  # Probability of recovering immunity
    theta = 0.01  # Probability of re-exposure

    model = DisinformationModel(N, alpha, beta, gamma, delta, theta)

    num_steps = 100
    for step in range(num_steps):
        model.step()
        counts = model.get_state_counts()
        print(f"Step {step + 1}:")
        for state in State:
            print(f"  {state.name}: {counts.get(state, 0)}")
        print("-" * 30)

        if counts.get(State.RECOVERED, 0) == model.num_agents:
            print("All agents have recovered. Ending simulation.")
            break


if __name__ == "__main__":
    run_model()
