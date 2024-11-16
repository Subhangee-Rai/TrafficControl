import random
import numpy as np

class TrafficSignalEnv:
    def __init__(self, num_lanes=4):
        self.num_lanes = num_lanes  # 4 directions: N, S, E, W
        self.state = [0] * num_lanes  # Traffic state for each lane (vehicles)
        self.time_step = 0

    def reset(self):
        self.state = [0] * self.num_lanes
        self.time_step = 0
        return self.state

    def step(self, action):
        reward = 0
        self.time_step += 1

        for i in range(self.num_lanes):
            # Simulate vehicle movement based on the signal light status (action)
            if i == action:
                self.state[i] = max(0, self.state[i] - 1)  # Vehicles move when light is green
            else:
                self.state[i] += random.randint(0, 5)  # Random number of vehicles coming in

        reward = -sum(self.state)  # More congestion, negative reward
        return self.state, reward

    def render(self):
        print(f"Time Step: {self.time_step} | State: {self.state}")


class QLearningAgent:
    def __init__(self, num_actions):
        self.q_table = np.zeros((5, num_actions))  # 5 states (simplified for demonstration)
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 1.0
        self.exploration_decay = 0.995
        self.min_exploration_rate = 0.1

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, 3)  # Random action (exploration)
        else:
            return np.argmax(self.q_table[state])  # Best action based on Q-values (exploitation)

    def learn(self, state, action, reward, next_state):
        max_next_q = np.max(self.q_table[next_state])
        self.q_table[state, action] += self.learning_rate * (reward + self.discount_factor * max_next_q - self.q_table[state, action])

        if self.exploration_rate > self.min_exploration_rate:
            self.exploration_rate *= self.exploration_decay


# Initialize environment and agent
env = TrafficSignalEnv()
agent = QLearningAgent(num_actions=4)

# Training loop
for episode in range(1000):
    state = env.reset()
    total_reward = 0

    for step in range(100):
        action = agent.choose_action(state)
        next_state, reward = env.step(action)
        agent.learn(state, action, reward, next_state)
        total_reward += reward
        state = next_state

    if episode % 100 == 0:
        print(f"Episode {episode}: Total Reward = {total_reward}")
