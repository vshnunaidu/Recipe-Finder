import numpy as np
import random
import matplotlib.pyplot as plt

# Define the payoff matrix for the Prisoner's Dilemma
# Payoff matrix structure: [R, S, T, P]
# R: Reward for mutual cooperation
# S: Sucker's payoff (cooperate, defect)
# T: Temptation to defect (defect, cooperate)
# P: Punishment for mutual defection
payoff_matrix = {
    ('C', 'C'): (3, 3),
    ('C', 'D'): (0, 5),
    ('D', 'C'): (5, 0),
    ('D', 'D'): (1, 1)
}
#---------------------------------------------------------------------------------
# Define strategies
def always_cooperate(history, opponent_history):
    return 'C'

def always_defect(history, opponent_history):
    return 'D'

def tit_for_tat(history, opponent_history):
    if len(opponent_history) == 0:
        return 'C'
    return opponent_history[-1]

def average_strat(history, opponent_history):
    if len(opponent_history) == 0:
        return 'C'
    ccount = 0
    dcount = 0
    for res in history: 
        if res == 'C':
            ccount+=1
        if res == 'D':
            dcount+=1
    if ccount >= dcount:
        return 'C'
    if ccount < dcount:
        return 'D'
#---------------------------------------------------------------------------
# Define a function to simulate a single round of the game
def play_round(strategy1, strategy2, history1, history2):
    action1 = strategy1(history1, history2)
    action2 = strategy2(history2, history1)
    payoff1, payoff2 = payoff_matrix[(action1, action2)]
    return action1, action2, payoff1, payoff2

# Define the simulation
def simulate_game(strategy1, strategy2, rounds=100):
    history1, history2 = [], []
    total_payoff1, total_payoff2 = 0, 0
    
    for _ in range(rounds):
        action1, action2, payoff1, payoff2 = play_round(strategy1, strategy2, history1, history2)
        history1.append(action1)
        history2.append(action2)
        total_payoff1 += payoff1
        total_payoff2 += payoff2
    
    return total_payoff1, total_payoff2, history1, history2

# Run the simulation
rounds = 100
strategies = [always_cooperate, always_defect, tit_for_tat, average_strat]
results = {}

for strat1 in strategies:
    for strat2 in strategies:
        payoff1, payoff2, history1, history2 = simulate_game(strat1, strat2, rounds)
        results[(strat1.__name__, strat2.__name__)] = (payoff1, payoff2)

# Display the results
for key, value in results.items():
    print(f"Strategy {key[0]} vs {key[1]}: Payoff {value[0]} vs {value[1]}")

# Plot the results for one pair of strategies
strategy1 = tit_for_tat
strategy2 = average_strat
_, _, history1, history2 = simulate_game(strategy1, strategy2, rounds)

plt.plot(range(rounds), history1, label='Player 1 (Tit-for-Tat)')
plt.plot(range(rounds), history2, label='Player 2 (Always Defect)')
plt.xlabel('Round')
plt.ylabel('Action')
plt.title('Actions Over Time')
plt.legend()
plt.show()
