import pygame as pg
import pygad
from . import setup,tools
from . states import main_menu,load_screen,level1
from . import constants as c
from pynput.keyboard import Key, Controller
import time
import numpy as np

run_it = tools.Control(setup.ORIGINAL_CAPTION)


def mario_fitness(solution, solution_idx):

    #solution deberia ser una lista de movimientos  
    global run_it
    points = 0
    
    keyboard = Controller()
    moves = []

    min_jump_prob = 1.8
    max_jump_prob = 2.0

    for i in solution:
        if i >= 0.0 and  i < min_jump_prob:
            moves.append(Key.right)
           
        elif i >= min_jump_prob and i <= max_jump_prob:
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
            points = points - 100
            break


    points = run_it.state.mario.rect.x + run_it.state.game_info[c.SCORE]
    
    run_it.state.game_info[c.SCORE] = 0
    if run_it.state.mario.rect.x >= 8749:
        points = points + 100000

    run_it.main()
    print("individual points: ", points )
    return points

def callback_generation(ga_instance):
    
    #best_sol_fitness = ga_instance.best_solution()[1]
    
    print("Generation  = {generation}".format(generation=ga_instance.generations_completed))


#    print("Generation  = {generation}".format(generation=ga_instance.generations_completed))
#    print("Fitness     = {fitness}".format(fitness=ga_instance.best_solution()[1]))
#    print("Change     = {change}".format(change=fitness_change))


def main():
    """Add states to control here."""

    state_dict = {c.MAIN_MENU: main_menu.Menu(),
                  c.LEVEL1: level1.Level1(),
                  c.GAME_OVER: load_screen.GameOver()}

    run_it.setup_states(state_dict, c.MAIN_MENU)



    ga_instance = pygad.GA(num_generations=100,
                               num_parents_mating=1,
                               mutation_type='scramble', 
                               mutation_probability=0.25,
                               fitness_func=mario_fitness,
                               sol_per_pop=3, 
                               num_genes=10000,
                               init_range_low=0.0,
                               init_range_high=2.0,
                               random_mutation_min_val=0.0,
                               random_mutation_max_val=3.0,
                               mutation_by_replacement=False,
                               callback_generation=callback_generation)

    ga_instance.run()
