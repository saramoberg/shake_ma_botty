# This bot selects a food pellet at random, then goes and tries to get it by
# following the shortest path to it.
# It tries on the way to avoid being killed by the enemy: if the next move
# to get to the food would put it on a ghost, then it chooses a random safe
# position
TEAM_NAME = 'ATTACKER'

import networkx
from pelita.utils import walls_to_graph
import numpy as np


def find_closest_x_food(bot, state, position, x, visited_pellets=[]):
    """Find the closest x food locations and distances to them."""
    path_lengths = []

    all_food = bot.enemy[0].food
    not_visited_food = [food for food in all_food if food not in visited_pellets]

    # Looks at shortest path to all pellet location
    for en, pellet in enumerate(not_visited_food):
        path = get_shortest_path(state['updated_graph'], position, pellet)

        if not path:
            path_lengths.append(50)
        else:
            path_lengths.append(len(path))

    # Pick the closest x pellets
    closest_pellets = np.argsort(path_lengths)[:x]

    # Return the location and distance of the selected pellets
    closest_food_loc = [not_visited_food[i] for i in closest_pellets]
    closest_food_dist = [path_lengths[i] for i in closest_pellets]

    return closest_food_loc, closest_food_dist

def find_path_to_best_pellet(bot, state):
    """Find path to best yummiest pellet"""
    # Current bot location
    current_bot_location = bot.position

    # Locations for closest food
    closest_food_loc, closest_food_dist = find_closest_x_food(bot, state, current_bot_location, 5)

    total_lengths = []
    # Loop through x closest pellets
    for en, pellet in enumerate(closest_food_loc):

        # Current pellet to consider as starting point
        pellet_current_loc = pellet

        # Distance to first pellet
        path_length = closest_food_dist[en]
        visited_pellet_loc = []

        # Look at shortest path length from first pellet to 5 others
        for next_pellet in range(5):
            next_pellet_loc, next_pellet_dist = find_closest_x_food(bot, state, pellet_current_loc,1, visited_pellet_loc)

            # Add pathlength
            path_length += next_pellet_dist[0]

            # Switch to next pellet
            pellet_current_loc = next_pellet_loc
            visited_pellet_loc.append(pellet_current_loc)

        # Total length for given starting pellet
        total_lengths.append(path_length)

    # Select starting pellet optimal path length as target
    shortest_total_length_idx = np.argmin(total_lengths)
    miracle_pellet_location = closest_food_loc[shortest_total_length_idx]

    path_to_miracle_pellet = get_shortest_path(state['updated_graph'], bot.position, miracle_pellet_location)

    return path_to_miracle_pellet


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

def update_graph_for_enemies(bot, state):
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
    return updated_graph, updated_walls

def move(bot, state):
    graph = state['graph']
    our_border = state['border']
    state['updated_graph'], state['updated_walls'] = update_graph_for_enemies(bot, state)

    # else:
    best_path = find_path_to_best_pellet(bot,state)
    if best_path == None:
        pass
    else:
        best_path = find_path_to_best_pellet(bot,state)[1:]

    print(f"Bot {bot.turn} command {bot.is_blue} is in attack mode")
    print(best_path)

    if best_path is not None:
        next_move = best_path[0]
    else:
        good_positions = {
            pos for pos in bot.legal_positions
            if pos not in bot.enemy[0].legal_positions
            and pos not in bot.enemy[1].legal_positions
        }
        if not good_positions:
            next_move = bot.position
            reasoning = {next_move, 'staying in place since there are no good positions'}
        else:
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            next_move = bot.random.choice(list(good_positions))
            reasoning = {next_move, 'moving randomly from the enemy'}

    # print(reasoning)
    return next_move
