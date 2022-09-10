# This bot selects a food pellet at random, then goes and tries to get it by
# following the shortest path to it.
# It tries on the way to avoid being killed by the enemy: if the next move
# to get to the food would put it on a ghost, then it chooses a random safe
# position
TEAM_NAME = 'ATTACKER'


import networkx
from pelita.utils import walls_to_graph

def get_shortest_path(graph, source, target):
    """If not path, returns None"""
    try:
        return networkx.shortest_path(graph, source, target)
    except (networkx.exception.NetworkXNoPath, networkx.exception.NodeNotFound):
        return None

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
        print(f"Bot {bot.turn} command {bot.is_blue} is in homezome")
        # compute distance to all border cells
        # select the shortest path to the border
        min_path_length = float('inf')
        best_path = None
        for cell in our_border:
            path = get_shortest_path(state['graph'],
                                          bot.position, cell)
            if path is None:
                best_path = None
            else:
                if len(path) < min_path_length:
                    best_path = path[1:]
                    min_path_length = len(path)

        # remember the path
        state[bot.turn]['path'] = best_path[1:]

    else:
        print(f"Bot {bot.turn} command {bot.is_blue} is in attack mode")
        # get_greedy_path takes care of knowing 
        # where the enemies are
        for cell in bot.legal_positions:
            enemy_food = bot.enemy[0].food
            if cell in enemy_food:
                best_path = [cell] # FIXME: random of all foods
            else:
                updated_walls = (
                    bot.walls
                    .union(
                        {enemy.position
                         for enemy in bot.enemy
                         if not enemy.is_noisy}
                    )
                    .union(
                        {position
                         for enemy in bot.enemy
                         for position in enemy.legal_positions
                         if not enemy.is_noisy
                         and position != bot.position}
                    )
                )
                updated_graph = walls_to_graph(updated_walls)
                # for food in enemy_food:
                #     assert food not in updated_graph
                assert bot.position not in updated_walls
                paths = [get_shortest_path(updated_graph, bot.position, food)
                         for food in enemy_food
                         if food in updated_graph]
                # filter out None's 
                paths = [p for p in paths if p is not None]

                # if there are not paths
                if not paths:
                    best_path = None
                else:
                    best_path = min(paths, key = len)[1:]

    if best_path is not None:
        next_move = best_path.pop(0)
    else:
        good_positions = {
            pos for pos in bot.legal_positions
            if pos not in bot.enemy[0].legal_positions
            and pos not in bot.enemy[1].legal_positions
        }
        if not good_positions:
            next_move = bot.position
        else:
            next_move = bot.random.choice(list(good_positions))

    return next_move
