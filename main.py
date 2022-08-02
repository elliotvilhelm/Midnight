import random
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

N_FACES = 6

def game(use_strategy = False):
    one = False
    four = False
    count = 0
    dice = 6

    while dice > 0:
        taken = False
        rolls = [random.randint(1, N_FACES) for _ in range(dice)]

        if not one and 1 in rolls:
            # cache the first one we find
            one = True
            dice -= 1
            rolls.remove(1)
            taken = True
        if not four and 4 in rolls:
            # cache the first four we find
            four = True
            dice -= 1
            rolls.remove(4)
            taken = True
        
        if dice == 0:
            break

        if use_strategy:
            if not taken and 6 not in rolls:
                # Take max available
                max_roll = max(rolls)
                count += max_roll
                dice -= 1
                rolls.remove(max_roll)
            elif 6 in rolls:
                if not one or not four:
                    count += 6
                    dice -= 1
                    rolls.remove(6)
                else:
                    # take all the sixes available
                    while 6 in rolls:
                        count += 6
                        dice -= 1
                        rolls.remove(6)

        else:
            if not taken:
                random_dice = rolls[random.randint(0, len(rolls)-1)]
                count += random_dice
                dice -= 1
                rolls.remove(random_dice)
    
    if one and four:
        return count
    return 0


if __name__ == "__main__":
    results = [game() for _ in range(1000000)]

    results_ctr = Counter(results)
    for k, v in results_ctr.items():
        results_ctr[k] = (v / len(results)) * 100

    results_df = pd.DataFrame(results)

    print(results_df.describe())
    print(results_ctr)

    plt.bar(results_ctr.keys(), results_ctr.values())
    plt.grid(True)
    plt.ylabel('Probability Percentage')
    plt.xlabel('Points')
    plt.show()