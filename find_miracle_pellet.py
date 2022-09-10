import networkx

def find_best_path(updated_graph, legal_positions, enemy_food):
    for next_legal_position in legal_positions:
        for pellet in enemy_food:
            paths = networkx.shortest_path(updated_graph, next_legal_position, pellet)
return next_legal_position, path_length, paths


def find_closest_x_food(current_position, x):
    path_lengths = []
    for en, pellet in enumerate(bot.enemy.food):
        path_lengths.append(len(networkx.shortest_path(graph, current_position, pellet)))

    closest_pellets = np.argsort(path_lengths)[:x]

    closest_food_loc = bot.enemy.food[closest_pellets]
    closest_food_dist = path_length[closest_pellets]

    return closest_food_loc, closest_food_dist

def search_several_steps_ahead(bot, state)

    # Locations for closest food
    closest_food_loc, closest_food_dist = find_closest_x_food(bot.turn.position, 3)
    
    total_lengths = []

    # Loop through x closest pellets
    for en, pellet in enumerate(closest_food_loc):

        pellet_current_loc = pellet
        
        path_length = closest_food_dist[en]
        # Look at shortest path lengths to x closest pellets
        for next_pellet in range(5):
            next_pellet_loc, next_pellet_dist = find_closest_x_food(pellet_location,1)
            path_length += next_pellet_dist

            pellet_current_loc = next_pellet_loc

        total_lengths.append(path_length)

    shortest_total_length_idx = np.argmin(total_lengths)
    miracle_pellet = closest_food_loc[shortest_total_length_idx]

    return miracle_pellet


    





        












        
