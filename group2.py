TEAM_NAME = 'NonViolentPelitas'

import networkx
import pelita.utils
from pelita.utils import walls_to_graph

from demo05_basic_defender import move as move_defender
from demo04_basic_attacker import move as move_attacker

#from defender_02 import move as move_defender
#from attacker_02 import move as move_attacker

#import utils

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
        state["global_strategy"] = "game_start" ## not used right now, keep for later?

        state[0] = init_state("attacker")
        state[1] = init_state("attacker")

## if conditions for each global_strategy
    if bot.round == 16: ## TODO: find better condition for switiching out of initial strategy
        state["global_strategy"] = "individual" # each bot's personality is updated individually
    elif len(bot.food) <= 4:
        state["global_strategy"] = "defend_last_food"
### define what to do based on global_strategy
# game start --> move to midline
# individual --> for now one attacker one defender
# defend_all --> both bots to defense
# attack_all --> both bots to attack

    if state["global_strategy"] == "game_start":
        pass ## TODO: move to optimal midline position while enemy is_noisy

    elif state["global_strategy"] == "individual":
        # TODO: assign attacker/defender based on some smart idea (e.g. is food closer or enemy?)
        state[0]["personality"] = "attacker"
        state[1]["personality"] = "defender"

    elif state["global_strategy"] == "defend_last_food":
        target_options = bot.food
        # figure out how far each food is
        # for loop over target_options -- distance/shortest attack_path
        # pick shortest path target
        possible_paths = {}
        for target_option in target_options:
            possible_paths[target_option] = len(networkx.shortest_path(state['graph'], bot.position, target)[1:])

        closest_food = sorted(possible_paths.items(), key=lambda x: x[1], reverse=True)
        state[bot.turn]["defend_path"] = closest_food[0]

        # choose a target food pellet if we still don't have one or
        ## if the old target has been already eaten

    #if (target is None) or (target not in enemy[0].food):
        # position of the target food pellet
        #target = bot.random.choice(bot.food)
        # use networkx to get the shortest path from here to the target
        # we do not use the first position, which is always equal to bot_position
        #path = networkx.shortest_path(state['graph'], bot.position, target)[1:]
        state[bot.turn]["defend_path"] = path
        state[bot.turn]["defend_target"] = target

        # get the next position along the shortest path to reach our target
        next_pos = path.pop(0)
        # if we are not in our homezone we should check if it is safe to proceed
        if next_pos in bot.homezone:
            # get a list of safe positions
            safe_positions = []
            for pos in bot.legal_positions:
                if pos not in (enemy[0].position, enemy[1].position):
                    safe_positions.append(pos)




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
