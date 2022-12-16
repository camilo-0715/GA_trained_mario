import pygame as pg
import pygad
from . import setup,tools
from . states import main_menu,load_screen,level1
from . import constants as c


run_it = tools.Control(setup.ORIGINAL_CAPTION)


def fitness_function(solution, solution_idx):

    #solution deberia ser una lista de movimientos  

    return run_it.state.mario.rect.x / 8751

def callback_generation(ga_instance):
    global last_fitness
    
    best_sol_fitness = ga_instance.best_solution()[1]
    fitness_change = best_sol_fitness - last_fitness

    last_fitness = best_sol_fitness

    print(run_it.state.mario.rect.x)

    if run_it.done:
        # After either the level is completed or the character is killed, then stop the GA by returning the string "stop".
        return "stop"

    elif fitness_change != 0:
        best_sol = ga_instance.best_solution()[0]
        run_it.main()


#    print("Generation  = {generation}".format(generation=ga_instance.generations_completed))
#    print("Fitness     = {fitness}".format(fitness=ga_instance.best_solution()[1]))
#    print("Change     = {change}".format(change=fitness_change))


def fitness_func():
    pass


def main():
    """Add states to control here."""
    state_dict = {c.MAIN_MENU: main_menu.Menu(),
                  c.LEVEL1: level1.Level1(),
                  c.GAME_OVER: load_screen.GameOver()}

    run_it.setup_states(state_dict, c.MAIN_MENU)

    ga_instance = pygad.GA(num_generations=9999,
                            num_parents_mating=300, 
                            fitness_func=fitness_func,
                            sol_per_pop=1000, 
                            num_genes=2,
                            init_range_low=0.0,
                            init_range_high=1.0,
                            random_mutation_min_val=0.0,
                            random_mutation_max_val=1.0,
                            mutation_by_replacement=True,
                            callback_generation=callback_generation,
                            delay_after_gen=1)

    ga_instance.run()