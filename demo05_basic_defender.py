# This bot tries to catch an enemy bot. It will stop at the border of its
# homezone if the enemy still did not cross the border.
# As long as the enemies are far away (their position is noisy), the bot
# tries to get near to the bot in the enemy team which has the same turn.
# As soon as an enemy bot is not noisy anymore, i.e. it has come near, the
# bot goes after it and leaves the other enemy alone

TEAM_NAME = 'Basic Defender Bots'


import networkx

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
        target = bot.enemy[turn].position
        #state[bot.turn]['defend_ID'] = bot.enemy[turn]
    elif not bot.enemy[0].is_noisy and not bot.enemy[1].is_noisy:
        # if none are noisy, aim for the closest one
        if bot.enemy[turn].position in bot.homezone:
            dist_turn = len(networkx.shortest_path(state['graph'], bot.position, bot.enemy[turn].position))
            dist_not_turn = len(networkx.shortest_path(state['graph'], bot.position, bot.enemy[1-turn].position))
            if dist_turn < dist_not_turn:
                target = bot.enemy[turn].position
            else:
                target = bot.enemy[1-turn].position

        #target = change_target(bot,networkx,turn,state)
    elif not bot.enemy[turn].is_noisy:
        # if our turn companion is not noisy, go for it
        target = bot.enemy[turn].position
        #state[bot.turn]['defend_ID'] = bot.enemy[turn]
    elif not bot.enemy[1-turn].is_noisy:
        # if the other enemy is not noisy, go for it
        target = bot.enemy[1-turn].position
        #state[bot.turn]['defend_ID'] = bot.enemy[1-turn]
    else:
        raise Exception('We should never be here!')

    # get the next position along the shortest path to our target enemy bot
    next_pos = networkx.shortest_path(state['graph'], bot.position, target)[1]
    # we save the current target in our state dictionary
    state[bot.turn]["defend_target"] = target

    # let's check that we don't go into the enemy homezone, i.e. stop at the
    # border
    if next_pos in bot.enemy[turn].homezone:
        next_pos = bot.position

    return next_pos


def change_target(bot,networkx,turn,state):
    if bot.enemy[turn].position in bot.homezone:
        bot.enemy[turn].dist = len(networkx.shortest_path(state['graph'], bot.position, bot.enemy[turn].position))
        bot.enemy[1-turn].dist = len(networkx.shortest_path(state['graph'], bot.position, bot.enemy[1-turn].position))
        if bot.enemy[turn].dist < bot.enemy[1-turn].dist:
            target = bot.enemy[turn].position
        else:
            target = bot.enemy[1-turn].position
    else:
        bot.enemy[turn].dist = len(networkx.shortest_path(state['graph'], bot.position, bot.enemy[turn].position))
        bot.enemy[1-turn].dist = len(networkx.shortest_path(state['graph'], bot.position, bot.enemy[1-turn].position))
        if bot.enemy[turn].dist < bot.enemy[1-turn].dist:
            target = bot.enemy[turn].position
        else:
            target = bot.enemy[1-turn].position




#if both not noisy
 #   clostest target = 
#
 #   if both in hz
 #   - go for closest one
#
  #  if one in homezone
   # - go for it 
        



