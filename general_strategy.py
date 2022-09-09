TEAM_NAME = 'NonViolentPelitas'

import pelita.utils
from pelita.utils import walls_to_graph

from demo05_basic_defender import move as move_defender
from demo04_basic_attacker import move as move_attacker

#from defender_02 import move as move_defender
#from attacker_02 import move as move_attacker
import utils


# our own food: bot.food

## initiate the state dictionary
def init_state(personality):
    return {
        # specifies which personality we are: "attacker" or "defender"
        "personality": personality,

        # entries prefixed with "attack_" are used by the move_attacker function
        "attack_target": None,
        "attack_path": None,

        # entries prefixed with "defend_" are used by the move_defender function
        "defend_target": None,
        "defend_path": None,

        # # entries about previous food postions
        # "prev_foodmap": [],
        # "eaten_food": [],
    }


def track_foodchange(bot, state):
    # turn food lists into sets for set comparison
    food_diff = set(state['prev_foodmap']) - set(bot.food)
    state['eaten_food'].append(food_diff)
    # update state for prev foodmap
    state['prev_foodmap'] = bot.food
    if food_diff:
        print(bot.round, food_diff, bot.enemy[0].position, bot.enemy[0].is_noisy, bot.enemy[1].position, bot.enemy[1].is_noisy )

def move(bot, state):
    # initiate the state dictionary
    if state == {}:
        # here each bot has its own state dictionary (0 and 1) and they share
        # the same game state information in the "graph"
        state['graph'] = walls_to_graph(bot.walls)
        state['prev_foodmap'] = bot.food # initial state
        state['eaten_food'] = []
        #### UPDATE ACCORDING TO STRATEGY #####
        state[0] = init_state("attacker")
        state[1] = init_state("defender")


    # keep track of food changes for distant enemy positions
    track_foodchange(bot, state)
    # update previous food map

    # Only the attacker can go into the enemy zone and be killed. Therefore
    # we only need to switch roles from the perspective of the defender.
    if bot.other.was_killed:
        state[bot.turn]["personality"] = "attacker"
        state[bot.other.turn]["personality"] = "defender"

    if state[bot.turn]["personality"] == "attacker":
        next_pos = move_attacker(bot, state)
        bot.say('attacker')
    else:
        next_pos = move_defender(bot, state)
        bot.say('defender')



    return next_pos
