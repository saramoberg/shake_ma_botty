import numpy as np
from attacker import move
from pelita.utils import setup_test_game

def test_eat_food():
    # do we eat food when it's available?
    layout="""
    ########
    #    a.#
    #.b yx #
    ########
    """
    bot = setup_test_game(layout=layout, is_blue=True)
    next_move = move(bot, {})
    assert next_move == (6, 1)

def test_no_kamikaze():
    # do we avoid enemies when they can kill us?
    layout="""
    ########
    #    x.#
    #.b  ay#
    ########
    """
    bot = setup_test_game(layout=layout, is_blue=True)
    next_move = move(bot, {})
    assert next_move == (4, 2) or next_move == (5, 2)

def test_do_not_step_on_enemy():
    # check that we don't step back on an enemy when we are fleeing
    layout="""
    ########
    #    x.#
    #.b #ay#
    ########
    """
    bot = setup_test_game(layout=layout, is_blue=True)
    next_move = move(bot, {})
    assert next_move == (5, 2)

def test_escape_mode_given_enemy_steps():
    layout="""
    ########
    #    x.#
    #.b a y#
    ########
    """
    bot = setup_test_game(layout=layout, is_blue=True)
    next_move = move(bot, {})
    assert next_move == (3, 2) or next_move == (4, 2)