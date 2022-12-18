from shutil import move
import pygame as pg
import pygad
from . import setup,tools
from . states import main_menu,load_screen,level1
from . import constants as c
from pynput.keyboard import Key, Controller
import time
import numpy as np
import csv
import os
import sys

run_it = tools.Control(setup.ORIGINAL_CAPTION)

f = open('winning_solutions.txt', 'a')
writer = csv.writer(f)
gen_ctr = 0
    
min_jump_prob = 1.8
max_jump_prob = 1.9
stop_prob = 2.0

def mario_fitness(solution, solution_idx):

    global run_it
    points = 0
    
    keyboard = Controller()
    moves = []

    for i in solution:
        if i >= 0.0 and  i < min_jump_prob:
            moves.append(Key.right)
           
        elif i >= min_jump_prob and i <= max_jump_prob:
            moves.append('a')      
        elif i >= max_jump_prob and i <= stop_prob:
            moves.append(" ")          

    counter = 0

    while True:
        
        if counter < len(moves):        
            keyboard.press(moves[counter])
        
        run_it.main()
    
        if counter < len(moves):                
            keyboard.release(moves[counter])
        
        if (run_it.state.game_info[c.MARIO_DEAD]):
            points = points - 500
            break
 
        if run_it.state.mario.rect.x > 8700:    
            writer.writerow(solution[:counter])
            while not run_it.state.done:
                run_it.main()
                
            break

        counter = counter + 1
        
    points = points + run_it.state.mario.rect.x + run_it.state.game_info[c.SCORE] - run_it.state.overhead_info_display.time
    run_it.state.game_info[c.SCORE] = 0

    run_it.main()
    print("individual points: ", points )
   
    return points

def callback_generation(ga_instance):
    
    #best_sol_fitness = ga_instance.best_solution()[1]
    print("Generation  = {generation}".format(generation=ga_instance.generations_completed))

#    print("Generation  = {generation}".format(generation=ga_instance.generations_completed))
#    print("Fitness     = {fitness}".format(fitness=ga_instance.best_solution()[1]))
#    print("Change     = {change}".format(change=fitness_change))


def execute_generated_win(win_moves):
    solution = win_moves.split(",")
    solution[-1] = solution[-1].strip()
    
    keyboard = Controller()
    counter = 0
    moves = []
    
    for i in solution:
        i = float(i)
        if i >= 0.0 and  i < min_jump_prob:
            moves.append(Key.right)
           
        elif i >= min_jump_prob and i <= max_jump_prob:
            moves.append('a')      
        elif i >= max_jump_prob and i <= stop_prob:
            moves.append(" ")  
    
    while True:
        if counter < len(moves):        
            keyboard.press(moves[counter])
        
        run_it.main()
    
        if counter < len(moves):                
            keyboard.release(moves[counter])
 
        if run_it.state.mario.rect.x > 8700:    
            while not run_it.state.done:
                run_it.main()
            break
        counter = counter + 1
        
def main(arg_list):

    """Add states to control here."""

    winning_file = ""
    load_model_flag = False

    for arg in arg_list:
        if (arg == "winning_solution.txt"):
            winning_file = arg
        elif (arg == "--load-model"):
            load_model_flag = True

    if winning_file != "":
        state_dict = {c.MAIN_MENU: main_menu.Menu(),
                        c.LEVEL1: level1.Level1(),
                        c.GAME_OVER: load_screen.GameOver()}

        run_it.setup_states(state_dict, c.MAIN_MENU)
            
        with open(winning_file) as f:
            last_line = f.readlines()[-1]
            
            execute_generated_win(last_line)
        
    else:
        try: 
            state_dict = {c.MAIN_MENU: main_menu.Menu(),
                        c.LEVEL1: level1.Level1(),
                        c.GAME_OVER: load_screen.GameOver()}

            run_it.setup_states(state_dict, c.MAIN_MENU)


            if (os.path.isfile('./mario_swap.pkl') and load_model_flag):
                ga_instance = pygad.load("mario_swap")
            
            else:
                ga_instance = pygad.GA(num_generations=2,
                                        num_parents_mating=2,
                                        mutation_type='scramble', 
                                        mutation_probability=0.35,
                                        fitness_func=mario_fitness,
                                        sol_per_pop=5, 
                                        num_genes=2500,
                                        init_range_low=0.0,
                                        init_range_high=2.0,
                                        random_mutation_min_val=0.0,
                                        random_mutation_max_val=3.0,
                                        mutation_by_replacement=False,
                                        callback_generation=callback_generation)

            ga_instance.run()

            ga_instance.plot_fitness()
            ga_instance.save("mario_model")
        except KeyboardInterrupt:
            ga_instance.plot_fitness()
            ga_instance.save("mario_model")