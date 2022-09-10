# This bot tries to catch an enemy bot. It will stop at the border of its
# homezone if the enemy still did not cross the border.
# As long as the enemies are far away (their position is noisy), the bot
# tries to get near to the bot in the enemy team which has the same turn.
# As soon as an enemy bot is not noisy anymore, i.e. it has come near, the
# bot goes after it and leaves the other enemy alone

# TODO
# Back and forth wiggling
# More reliable tracking of a transiently noisy enemy

TEAM_NAME = 'Basic Defender Bots'

import networkx
import numpy as np
from pelita.utils import walls_to_graph
def init_defend_state():
    return {
            "defend_target": None,
            "defend_path": None,
        }

def move(bot, state):
    if state == {}:
        # store the graph representation of the maze in the state object
        state['graph'] = walls_to_graph(bot.walls)
        state[0] = init_defend_state()
        state[1] = init_defend_state()

    turn = bot.turn
    if bot.enemy[0].is_noisy and bot.enemy[1].is_noisy:
        # if both enemies are noisy, just aim for our turn companion
        if bot.enemy[turn].position not in bot.homezone and bot.enemy[1-turn].position in bot.homezone:
            target = bot.enemy[1-turn].position
        else:
            target = bot.enemy[turn].position
    elif not bot.enemy[0].is_noisy and not bot.enemy[1].is_noisy:
        # if none are noisy, aim for the closest one
        if bot.enemy[turn].position in bot.homezone:
            dist_turn = len(networkx.shortest_path(state['graph'], bot.position, bot.enemy[turn].position))
            dist_not_turn = len(networkx.shortest_path(state['graph'], bot.position, bot.enemy[1-turn].position))
            if dist_turn < dist_not_turn:
                target = bot.enemy[turn].position
            else:
                target = bot.enemy[1-turn].position
        elif bot.enemy[1-turn].position in bot.homezone:
            dist_turn = len(networkx.shortest_path(state['graph'], bot.position, bot.enemy[turn].position))
            dist_not_turn = len(networkx.shortest_path(state['graph'], bot.position, bot.enemy[1-turn].position))
            if dist_turn < dist_not_turn:
                target = bot.enemy[turn].position
            else:
                target = bot.enemy[1-turn].position
        else:
            dist_turn = len(networkx.shortest_path(state['graph'], bot.position, bot.enemy[turn].position))
            dist_not_turn = len(networkx.shortest_path(state['graph'], bot.position, bot.enemy[1-turn].position))
            if dist_turn < dist_not_turn:
                target = bot.enemy[turn].position
            else:
                target = bot.enemy[1-turn].position
    elif not bot.enemy[turn].is_noisy:
        # if our turn companion is not noisy, go for it
        if bot.enemy[turn].position not in bot.homezone and bot.enemy[1-turn].position in bot.homezone:
            target = bot.enemy[1-turn].position
        else:
            target = bot.enemy[turn].position

        #state[bot.turn]['defend_ID'] = bot.enemy[turn]
    elif not bot.enemy[1-turn].is_noisy:
        # if the other enemy is not noisy, go for it
        if bot.enemy[1-turn].position not in bot.homezone and bot.enemy[turn].position in bot.homezone:
            target = bot.enemy[turn].position
        else:
            target = bot.enemy[1-turn].position
    else:
        raise Exception('We should never be here!')

    # get the next position along the shortest path to our target enemy bot
    next_pos = networkx.shortest_path(state['graph'], bot.position, target)[1]
    if next_pos == bot.enemy[0].enemy[1-bot.turn].position:
        next_pos = bot.position
    #if bot.position == state[bot.turn]["position"][-5] and target == next_pos:
        #find_former_position = 
        #find_former_position = diff(state[bot.turn])


    # we save the current target in our state dictionary
    state[bot.turn]["defend_target"] = target
    #state[bot.turn]["position"] = bot.position
    # let's check that we don't go into the enemy homezone, i.e. stop at the
    # border
    if next_pos in bot.enemy[turn].homezone:
        next_pos = bot.position

    

    return next_pos



        



