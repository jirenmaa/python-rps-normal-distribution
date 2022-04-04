# github : https://github.com/jirenmaa

import math
import os
import random as rand

import numpy as np

initial = {"r": [], "p": [], "s": []}
p1_samples = {**initial}  # player sample
p2_samples = {**initial}  # computer sample

results = {
    "computer": [0, 0, 0],  # win, lose, draw
    "player": [0, 0, 0],    # win, lose, draw
}

playing = True
number_of_game = 1
os.system("clear")


def compare_choices(player_choice: int, comp_choice: int) -> str:
    winner = None
    # both player and computer choose the same choice
    if player_choice == comp_choice:
        results["computer"][2] += 1
        results["player"][2] += 1
        winner = "draw"
    # player choose `rock` and computer choose `paper`
    elif player_choice == 0 and comp_choice == 1:
        results["computer"][0] += 1
        results["player"][1] += 1
        winner = "computer"
    # player choose `rock` and computer choose `scissors`
    elif player_choice == 0 and comp_choice == 2:
        results["computer"][1] += 1
        results["player"][0] += 1
        winner = "player"
    # player choose `paper` and computer choose `rock`
    elif player_choice == 1 and comp_choice == 0:
        results["computer"][1] += 1
        results["player"][0] += 1
        winner = "player"
    # player choose `paper` and computer choose `scissors`
    elif player_choice == 1 and comp_choice == 2:
        results["computer"][0] += 1
        results["player"][1] += 1
        winner = "computer"
    # player choose `scissors` and computer choose `rock`
    elif player_choice == 2 and comp_choice == 0:
        results["computer"][0] += 1
        results["player"][1] += 1
        winner = "computer"
    # player choose `scissors` and computer choose `paper`
    elif player_choice == 2 and comp_choice == 1:
        results["computer"][1] += 1
        results["player"][0] += 1
        winner = "player"

    return winner


# player choice `rock, paper, scissors` based on the probability of the samples
def n_probability(player_samples: dict, counter: int, choices: str) -> float:
    variant = np.var(player_samples[choices], ddof=1)
    n_means = np.mean(player_samples[choices])

    # print("choices : ", choices)
    # print("variant : ", variant)
    # print("n_means : ", n_means)
    # print("===================")

    # calculate the probability of the player choice, by the formula of the normal distribution
    # https://en.wikipedia.org/wiki/Normal_distribution
    probability = abs(
        (1 / math.sqrt(2 * math.pi * variant))
        * math.exp(-pow((counter - n_means), 2) / abs((2 * variant)))
    )

    return probability


while playing:
    input("press enter to continue ...")
    os.system("clear")
    p1_wins, p2_wins = str(results["player"][0]), str(results["computer"][0])

    print("game rounds :", number_of_game)
    print(f"Player : {p1_wins:10s} Computer: {p2_wins}\n")
    p1_choice = int(input("[1] rock\n[2] paper\n[3] scissors\n[4] exit\n>>> "))
    p2_choice = 0

    # exit the game
    if p1_choice == 4:
        break

    # update the player samples for learning
    p1_samples[["r", "p", "s"][p1_choice - 1]].append(number_of_game)

    # use random for computer choice, if the game is less than 10 because it doesn't have enough samples
    # to make the decision
    if p1_choice in [1, 2, 3] and number_of_game < 10:
        p2_choice = rand.randint(1, 3)

    # use the probability to make the computer choice after the samples are enough
    if number_of_game >= 10:
        # print("player_samples : ", p1_samples)
        # probability of the player choose rock
        prob_r = n_probability(p1_samples, number_of_game, "r")
        # probability of the player choose paper
        prob_p = n_probability(p1_samples, number_of_game, "p")
        # probability of the player choose scissors
        prob_s = n_probability(p1_samples, number_of_game, "s")

        print("=========================")
        print("probability of rock     : ", prob_r)
        print("probability of paper    : ", prob_p)
        print("probability of scissors : ", prob_s)
        print("=========================")

        # update the samples for learning and set the computer choice
        if prob_r > prob_p and prob_r > prob_s:
            if prob_p > prob_s:
                p2_samples["p"].append(number_of_game)
                p2_choice = 2
            if prob_p < prob_s:
                p2_samples["r"].append(number_of_game)
                p2_choice = 1
        if prob_p > prob_r and prob_p > prob_s:
            if prob_s > prob_r:
                p2_samples["s"].append(number_of_game)
                p2_choice = 3
            if prob_s < prob_r:
                p2_samples["p"].append(number_of_game)
                p2_choice = 2
        if prob_s > prob_p and prob_s > prob_r:
            if prob_r > prob_p:
                p2_samples["r"].append(number_of_game)
                p2_choice = 1
            if prob_r < prob_p:
                p2_samples["s"].append(number_of_game)
                p2_choice = 3

    print("player choice   :", ["r", "p", "s"][p1_choice - 1])
    print("computer choice :", ["r", "p", "s"][p2_choice - 1])
    print("=================")
    print("winner          :", compare_choices(p1_choice - 1, p2_choice - 1))
    number_of_game += 1
    print("\n==============================================================")

os.system("clear")
p1_wins, p2_wins = str(results["player"][0]), str(results["computer"][0])

print("===========================================================")
print("game played :", number_of_game)
print(f"Player: {p1_wins:10s} Computer: {p2_wins}")
