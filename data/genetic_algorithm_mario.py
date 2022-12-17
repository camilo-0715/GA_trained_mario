import pygame as pg
import pygad
from . import setup,tools
from . states import main_menu,load_screen,level1
from . import constants as c
from pynput.keyboard import Key, Controller
import time
import numpy as np

run_it = tools.Control(setup.ORIGINAL_CAPTION)


def fitness_func(solution, solution_idx):

    #solution deberia ser una lista de movimientos  
    global run_it

    points = 0
    
    keyboard = Controller()

    min_jump_prob = 1.7
    max_jump_prob = 2.0

    moves = []
    for i in solution:
        if i >= 0.0 and  i < 1.7:
            moves.append(Key.right)
        
        elif i >= min_jump_prob and i <= max_jump_prob:
            moves.append('a')           

    counter = 0
    while True:

        if counter < len(moves):        
            keyboard.press(moves[counter])

        run_it.main()

        if counter < len(moves):        
            keyboard.release(moves[counter])
        
        if (run_it.state.game_info[c.MARIO_DEAD]):
            points = points - 100
            break
        
        #añadir este if para que siga entrenando cuando termine el mundo
        if run_it.state.mario.rect.x > 8700:
            while not run_it.state.done:
                run_it.main()

            points = points + 1000
            break

        counter = counter + 1


    #este if previene overflows del counter cuando lllega a la meta
    if counter > 2499:
        counter = 2499
        
    for i in range(counter):
        if solution[i] >= 0.0 and  solution[i] < 1.7:
            points = points + 2           
        
        elif solution[i] >= min_jump_prob and solution[i] <= max_jump_prob:
            points = points + 1

    #programacion champagne
    run_it.main()

    print("individual points: ", points )
    return points



def callback_generation(ga_instance):
        
    print("Generation  = {generation}".format(generation=ga_instance.generations_completed))


def main():
    try:
        """Add states to control here."""

        state_dict = {c.MAIN_MENU: main_menu.Menu(),
                    c.LEVEL1: level1.Level1(),
                    c.GAME_OVER: load_screen.GameOver()}

        run_it.setup_states(state_dict, c.MAIN_MENU)



        ga_instance = pygad.GA(num_generations=1000,
                                num_parents_mating=2,
                                mutation_probability=0.1,
                                fitness_func=fitness_func,
                                sol_per_pop=5, 
                                num_genes=2500,
                                init_range_low=0.0,
                                init_range_high=2.0,
                                random_mutation_min_val=0.0,
                                random_mutation_max_val=2.0,
                                    mutation_type='random', 
                                mutation_by_replacement=True,
                                callback_generation=callback_generation)

        ga_instance.run()

        ga_instance.plot_fitness()
    except KeyboardInterrupt:
        ga_instance.plot_fitness()
