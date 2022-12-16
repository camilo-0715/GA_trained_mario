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

    
    keyboard = Controller()
    moves = []

    #print(solution)
    for i in solution:
        if i >= 0.0 and  i < 1.0:
            moves.append(Key.right)           
           
        elif i >= 1.0 and i <= 2.0:
            moves.append('a')           

    counter = 0
    while not run_it.done:

        if counter < len(moves):        
            keyboard.press(moves[counter])

        run_it.main()

        if counter < len(moves):        
            keyboard.release(moves[counter])
        
        counter = counter + 1

        if (run_it.state.game_info[c.MARIO_DEAD]):
            break


    return run_it.state.mario.rect.x / 8751

def callback_generation(ga_instance):
    global last_fitness
    
    best_sol_fitness = ga_instance.best_solution()[1]
    fitness_change = best_sol_fitness - last_fitness

    last_fitness = best_sol_fitness


    print("Generation  = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness     = {fitness}".format(fitness=ga_instance.best_solution()[1]))
    print("Change     = {change}".format(change=fitness_change))


#    print("Generation  = {generation}".format(generation=ga_instance.generations_completed))
#    print("Fitness     = {fitness}".format(fitness=ga_instance.best_solution()[1]))
#    print("Change     = {change}".format(change=fitness_change))


def main():
    """Add states to control here."""

    state_dict = {c.MAIN_MENU: main_menu.Menu(),
                  c.LEVEL1: level1.Level1(),
                  c.GAME_OVER: load_screen.GameOver()}

    run_it.setup_states(state_dict, c.MAIN_MENU)


    ga_instance = pygad.GA(num_generations=10,
                            num_parents_mating=1, 
                            fitness_func=fitness_func,
                            sol_per_pop=100, 
                            num_genes=10000,
                            init_range_low=0.0,
                            init_range_high=3.0,
                            random_mutation_min_val=0.0,
                            random_mutation_max_val=2.0,
                            callback_generation=callback_generation,
                            mutation_by_replacement=True,
                            delay_after_gen=1)

    ga_instance.run()
