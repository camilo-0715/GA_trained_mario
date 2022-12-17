__author__ = 'juan camilo carmona sanchez'

from . import setup,tools
from .states import main_menu,load_screen,level1
from . import constants as c
from pynput.keyboard import Key, Controller
import time

def main():
    """Add states to control here."""
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {c.MAIN_MENU: main_menu.Menu(),
                  c.LEVEL1: level1.Level1()}

    run_it.setup_states(state_dict, c.MAIN_MENU)
    #keyboard = Controller()
    #moves = [Key.right,Key.right,Key.right,Key.right,Key.right,Key.right, 'a',Key.right,'a']
    counter = 0

    while not run_it.state.game_info[c.MARIO_DEAD]:
        #if counter < len(moves):        
        #    keyboard.press(moves[counter])

        run_it.main()

        #if counter < len(moves):        
        #    keyboard.release(moves[counter])

        counter = counter + 1
        print(run_it.state.mario.rect.x)




