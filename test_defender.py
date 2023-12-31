from defender_02 import move
from pelita.utils import setup_test_game

def test_kill_enemy():
    # do we kill enemies when possible?
    layout="""
    ########
    #    b.#
    #.ax  y#
    ########
    """
    bot = setup_test_game(layout=layout, is_blue=True)
    next_pos = move(bot, {})
    assert next_pos == (3, 2)

def test_stop_at_the_border():
    # do we stop at the border when we reach it?
    layout="""
    ########
    #    b.#
    #. ax y#
    ########"""
    bot = setup_test_game(layout=layout, is_blue=True)
    next_pos = move(bot, {})
    assert next_pos == bot.position

def test_face_the_enemy():
    # do we move along the border to face the enemy when it's still in its own
    # homezone?
    layout="""
    ########
    #  a b.#
    #.  x y#
    ########"""
    bot = setup_test_game(layout=layout, is_blue=True)
    next_pos = move(bot, {})
    assert next_pos == (3, 2)
