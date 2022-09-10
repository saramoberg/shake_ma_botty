TEAM_NAME = 'Shake Dat Botty'

import networkx
import pelita.utils
from pelita.utils import walls_to_graph

#from demo05_basic_defender import move as move_defender
#from demo04_basic_attacker import move as move_attacker

from defender_02 import move as move_defender
from attacker import move as move_attacker, border

def say_message(bot, state):
    def_messages = ['give me a hug!', 'come on', 'im nice', 'dont run away','im hugry']
    att_messages = ['be faster', 'hurry up', 'tired?','im hugry']
    first_message_len = 35
    change_chance = 0.1

    if bot.round < first_message_len:
        if bot.position not in bot.homezone:
            msg = 'catch me'
        else:
            msg = 'hola!'
    else:
        # with 5% chance set msg back to None
        if bot.random.randint(0, 100) / 100 < change_chance:
            state[bot.turn]['msg'] = None
        msg_list = def_messages if bot.position in bot.homezone else att_messages
        if state[bot.turn]['msg'] is None:
            msg = bot.random.choice(msg_list)
            state[bot.turn]['msg'] = msg
        else:
                msg = state[bot.turn]['msg']

    bot.say(msg)


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
        'msg':None,

        #"path": [],
        #"border": [],
        #"graph": [],

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
        pass
        #print(bot.round, food_diff, bot.enemy[0].position, bot.enemy[0].is_noisy, bot.enemy[1].position, bot.enemy[1].is_noisy )

def move(bot, state):
    # initiate the state dictionary
    turn = bot.turn


    if state == {}:
        # here each bot has its own state dictionary (0 and 1) and they share
        # the same game state information in the "graph"
        state['graph'] = walls_to_graph(bot.walls)
        state['prev_foodmap'] = bot.food # initial state
        state['eaten_food'] = []
        our_border = border(bot)
        state['border'] = our_border
        #### UPDATE ACCORDING TO STRATEGY #####
        state["global_strategy"] = "game_start" ## not used right now, keep for later?

        state["lastFoodFlag"] = True
        #state["enteredLastFood"] = True

        state[0] = init_state("attacker")
        state[1] = init_state("attacker")

        state[0]["defend_food_path"] = []
        state[0]["defend_food_target"] = []

        state[1]["defend_food_path"] = []
        state[1]["defend_food_target"] = []



# if conditions for each global_strategy
    if bot.round == 16: ## TODO: find better condition for switiching out of initial strategy
        state["global_strategy"] = "individual" # each bot's personality is updated individually

    if len(bot.food) == 6 and state["lastFoodFlag"]:
        #print("Food length", len(bot.food))
        state["global_strategy"] = "defend_last_food"
        #enteredLastFood = True
         # we want to enter this if only once

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

        if state["lastFoodFlag"]:
            state["lastFoodFlag"] = False
            possible_paths_turn = {}
            possible_paths_other = {}

            for target_option in target_options:
                possible_paths_turn[target_option] = len(networkx.shortest_path(state['graph'], bot.position, target_option)[1:])
                possible_paths_other[target_option] = len(networkx.shortest_path(state['graph'], bot.other.position, target_option)[1:])

            closest_food_turn = sorted(possible_paths_turn.items(), key=lambda x: x[1])
            closest_food_other = sorted(possible_paths_other.items(), key=lambda x: x[1])

            if closest_food_turn[0][0] > closest_food_other[0][0]:
                moving_bot = 1-turn
                closest_food = closest_food_other
            else:
                moving_bot = turn
                closest_food = closest_food_turn

            state[moving_bot]["defend_food_target"] = closest_food[0][0]
            state[moving_bot]["defend_food_path"] = networkx.shortest_path(state['graph'], bot.position, closest_food[0][0])[1:]
            state[moving_bot]["personality"] = "last_defender"
            # change other bots personality if they are not already an attacker
            other_bot = 1 - moving_bot
            if state[other_bot]["personality"] == "defender":
                state[other_bot]["personality"] = "attacker"

        # get a list of safe positions
        safe_positions = []
        for pos in bot.legal_positions:
            if pos not in (bot.enemy[0].position, bot.enemy[1].position):
                safe_positions.append(pos)

    #### keep track of food changes for distant enemy positions
#    track_foodchange(bot, state)
    # update previous food map

    # Only the attacker can go into the enemy zone and be killed. Therefore
    # we only need to switch roles from the perspective of the defender.

#    if bot.other.was_killed:
#        state[bot.turn]["personality"] = "attacker"
#        state[bot.other.turn]["personality"] = "defender"

    if state[bot.turn]["personality"] == "attacker":
        next_pos = move_attacker(bot, state)
        bot.say('attacker')
    elif state[bot.turn]["personality"] == "defender":
        next_pos = move_defender(bot, state)
        bot.say('defender')
    elif state[bot.turn]["personality"] == "last_defender":
        ### assing only to appropriate bot via bot.char or bot.other.char
        path = state[bot.turn]["defend_food_path"]
        #print("is full: ", path)
        #print("Bot position:", bot.position)
        # get the next position along the shortest path to reach our target
        if path == []:
            next_pos = bot.position

        else:
            next_pos = path.pop(0)

        #state[bot.turn]["personality"] = "last_defender"
        bot.say('last')
        #print('bot position: ', bot.position, 'food position:', state[bot.turn]["defend_food_target"])

    else:
        assert False, state
        # raise ValueError("Should never be here but here we are")

    if next_pos not in bot.legal_positions:
        next_pos = bot.random.choice(bot.legal_positions)

    say_message(bot, state)

    return next_pos
