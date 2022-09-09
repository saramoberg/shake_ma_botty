# This bot selects a food pellet at random, then goes and tries to get it by
# following the shortest path to it.
# It tries on the way to avoid being killed by the enemy: if the next move
# to get to the food would put it on a ghost, then it chooses a random safe
# position
TEAM_NAME = 'ATTACKER'


import networkx
from pelita.utils import walls_to_graph

def border(bot):
    real_walls = bot.walls
    our_last_pos = 15 if bot.is_blue else 16
    potential_walls = [(our_last_pos, v) for v in range(15)]
    border = [cell
              for cell in potential_walls
              if cell not in real_walls]
    return border


def init_attack_state():
    return {
            "attack_target": None,
            "attack_path": None,
        }

def move(bot, state):
    if state == {}:
        state[0] = init_attack_state()
        state[1] = init_attack_state()
        state['graph'] = walls_to_graph(bot.walls)
        our_border = border(bot)
        state['border'] = our_border
    else:
        graph = state['graph']
        our_border = state['border']

    if bot.position in bot.homezone and bot.position not in our_border:
        # compute distance to all border cells
        # select the shortest path to the border
        min_path_length = float('inf')
        best_path = None
        for cell in our_border:
            path = networkx.shortest_path(state['graph'],
                                          bot.position, cell)
            if len(path) < min_path_length:
                best_path = path[1:]
                min_path_length = len(path)

        # remember the path
        state[bot.turn]['path'] = best_path[1:]

    else:
        best_path = [bot.position]

    # do safety shit FIXME
    next_move = best_path.pop(0)

    return next_move
