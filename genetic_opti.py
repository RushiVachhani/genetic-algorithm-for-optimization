# -*- coding: utf-8 -*-

import numpy
import matplotlib.pyplot as plt
import ga_algo_functions
import read_input

"""# **Driver Code**"""


equation_inputs = read_input.get_equation_inputs()
constraint = read_input.get_constraint_inputs()
condition = read_input.get_condition_inputs()
min_value_variable, max_value_variable, min_sol_per_pop, max_sol_per_pop, pop_increase, num_generations = read_input.get_variable_values()

# Number of the weights we are looking to optimize.
num_weights = len(equation_inputs)

if(min_sol_per_pop == max_sol_per_pop):
  verbose = 1
else:
  verbose = 0

if(verbose ==1):
  file = open("output_pop_constant.txt","w")
else:
  file = open("output_pop_increasing.txt","w")

if(min_sol_per_pop != max_sol_per_pop):
  final_best_fit = numpy.zeros( numpy.uint8((max_sol_per_pop - min_sol_per_pop)/pop_increase) + 1 )
  num_pop_size = numpy.arange(min_sol_per_pop, max_sol_per_pop+1, pop_increase)
else:
  pop_increase = 1

for solution_number in range(min_sol_per_pop, max_sol_per_pop+1, pop_increase):
  # Defining the population size.
  sol_per_pop = solution_number
  # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
  pop_size = (sol_per_pop,num_weights)

  #Creating the initial population.
  if(verbose==1):
    print("Creating initial population")
  new_population=numpy.empty((sol_per_pop, num_weights))
  succsess=0
  failure=0
  while succsess <= sol_per_pop-1:
    x = (numpy.random.uniform(low=min_value_variable, high=2, size=num_weights))
    if( ga_algo_functions.check_constaints(x, constraint, condition) == True ):
      new_population[succsess,:] = x
      succsess = succsess + 1
      if( verbose==1 ):
        if( (succsess % 1) == 0 ):
          print(succsess)
    #if( verbose == 1 ):
     # failure = failure + 1
     # if( (failure % 100) == 0):
      #  print(failure)
  if(verbose==1):
    print("Created initial population")
    #print(new_population)
    file.write("initial population generated\n")
    file.write(str(new_population))

  
  num_parents_mating = int(sol_per_pop/2.5)

  if( min_sol_per_pop == max_sol_per_pop ):
    best_fit_arr = numpy.zeros(num_generations)
    fitness_change_arr = numpy.zeros(num_generations)

  for generation in range(num_generations):

      # Measuring the fitness of each chromosome in the population.
      fitness = ga_algo_functions.calculate_fitness(equation_inputs, new_population)
      #print(fitness)

      # Selecting the best parents in the population for mating.
      #print("Select Mating Pool")   
      parents = ga_algo_functions.select_mating_pool(new_population, fitness, num_parents_mating)
 
      # Generating next generation using crossover.
      offspring_size=(pop_size[0]-parents.shape[0], num_weights)
      #print("Crossing over")
      offspring_crossover = ga_algo_functions.crossover(parents, offspring_size, constraint, condition, min_value_variable, max_value_variable)

      # Adding some variations to the offsrping using mutation.
      # Creating the new population based on the parents and offspring.
      #print("Mutating")
      offspring_mutation = ga_algo_functions.mutation(offspring_crossover, constraint, condition, max_value_variable)
    
      new_population[0:parents.shape[0], :] = parents
      new_population[parents.shape[0]:, :] = offspring_mutation
    
      if( min_sol_per_pop == max_sol_per_pop ):
        best_fit_arr[generation] = numpy.max(ga_algo_functions.calculate_fitness(equation_inputs, new_population))
        if(generation == 0):
          fitness_change_arr[generation] = 0
        else:
          fitness_change_arr[generation] = (best_fit_arr[generation] - best_fit_arr[generation-1])
        print( "Generation: ", generation+1, " Best result: ", best_fit_arr[generation], " Fitness change: ", fitness_change_arr[generation] )

  # Getting the best solution after iterating finishing all generations.
  #At first, the fitness is calculated for each solution in the final generation.
  fitness = ga_algo_functions.calculate_fitness(equation_inputs, new_population)

  # Then return the index of that solution corresponding to the best fitness.
  best_match_idx = numpy.where(fitness == numpy.max(fitness))

  if( verbose == 1 ):
    print("Best solution : ", new_population[best_match_idx, :])
    file.write("\n\n")
    file.write("Final best solution\n")
    file.write(str(new_population[best_match_idx, :]))
    file.close()

  if( min_sol_per_pop != max_sol_per_pop ):
    final_best_fit[ int( ((solution_number/pop_increase) - 1) ) ] = fitness[best_match_idx]
    print("Population Size:", new_population.shape[0], " Parents mating:", num_parents_mating, " Best solution fitness : ", fitness[best_match_idx])
  if( verbose == 0 ):
    file.write("Population Size:"+str(new_population.shape[0])+" Parents mating:"+str(num_parents_mating)+" Best solution fitness :"+str(fitness[best_match_idx])+"\n")

if( verbose==1 ):
  plt.plot(best_fit_arr, label = "Fit value")
  plt.xlabel("Generation Index")
  plt.ylabel("Best fit value")
  plt.legend()
  plt.grid(True)
  plt.grid(True, which = 'minor')
  plt.minorticks_on()
  plt.savefig('gen vs best fit.png')
  plt.show()

  plt.plot(fitness_change_arr, label = "Fitness change")
  plt.xlabel("Generation Index")
  plt.ylabel("Fitness change value")
  plt.legend()
  plt.grid(True)
  plt.grid(True, which = 'minor')
  plt.minorticks_on()
  plt.savefig('gen vs fitness change.png')
  plt.show()

    

if( verbose==0 ):
  plt.plot(num_pop_size, final_best_fit, label = "Fit value")
  plt.xlabel("Population Size")
  plt.ylabel("Best fit value")
  plt.legend()
  plt.grid(True)
  plt.grid(True, which = 'minor')
  plt.minorticks_on()
  plt.savefig('Pop_size vs best fit.png')
  plt.show()

file.close()

input()