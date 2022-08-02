import random
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


def game():
    obj = {
        "one": False,
        "four": False,
        "count": 0,
        "dice": 5
    }

    while obj["dice"] > 0:
        taken = False
        rolls = [random.randint(1, 6) for _ in range(obj["dice"])]

        if (not obj["one"]) and (1 in rolls):
            # cache the first one we find
            obj["one"] = True
            obj["dice"] -= 1
            rolls.remove(1)
            taken = True
        if (not obj["four"]) and (4 in rolls):
            # cache the first four we find
            obj["four"] = True
            obj["dice"] -= 1
            rolls.remove(4)
            taken = True
        
        if obj["dice"] == 0:
            break

        if (not taken) and (6 not in rolls):
            # just take max available
            max_roll = max(rolls)
            obj["count"] += max_roll
            obj["dice"] -= 1
            rolls.remove(max_roll)
        elif (6 in rolls):
            if (not obj["one"]) or (not obj["four"]):
                obj["count"] += 6
                obj["dice"] -= 1
                rolls.remove(6)
            else:
                # take a random number of 6s
                # c = Counter(rolls)
                # for _ in range(random.randint(1, c[6])):
                #     obj["count"] += 6
                #     obj["dice"] -= 1
                #     rolls.remove(6)

                # take all the sixes available
                while 6 in rolls:
                    obj["count"] += 6
                    obj["dice"] -= 1
                    rolls.remove(6)
    
    if (obj["one"] and obj["four"]):
        return obj["count"]
    return 0


if __name__ == "__main__":
    results = [game() for _ in range(1000000)]

    results_ctr = Counter(results)
    for k, v in results_ctr.items():
        results_ctr[k] = (v / len(results)) * 100

    itz_df = pd.DataFrame(results)

    print(itz_df.describe())
    print(results_ctr)

    plt.bar(results_ctr.keys(), results_ctr.values())
    plt.ylabel('percent odds')
    plt.xlabel('points')
    plt.show()