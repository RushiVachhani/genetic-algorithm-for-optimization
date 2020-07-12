# -*- coding: utf-8 -*-


import numpy
import matplotlib.pyplot as plt

"""# **Functions for Genetic Algorithm**

1) Constraint Check
"""

def check_constaints(x, constraint_matrix, condition):
  constraint = numpy.transpose(constraint_matrix)
  if( all((numpy.matmul(x,constraint)) <= condition) ):
    if( all(i >= 0 for i in x) ):
      #print(True)
      return True
  else:
    #print(False)
    return False

"""2) Fitness Calculation"""

def calculate_fitness(equation_inputs, pop):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function caulcuates the sum of products between each input and its corresponding weight.
    
    #fitness = numpy.sum(pop*equation_inputs, axis=1)
    #print(fitness.shape)
    
    fitness = numpy.zeros( pop.shape[0] )
    for k in range(fitness.shape[0]):
      sum = 0
      for i in range(len(equation_inputs)):
        for j in range(len(equation_inputs[0])):
          sum = sum + ( equation_inputs[i][j] * (pop[k,i]**(j+1)) )
      fitness[k] = sum

    return fitness

"""3) Selecting Mating Pool"""

def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return parents

"""4) Cross - Over"""

def crossover(parents, offspring_size, constraint_matrix, condition, min_value, max_value):
  offspring = numpy.empty(offspring_size)
  for k in range(offspring_size[0]):
    parent1_index = k%parents.shape[0]
    parent2_index = (k+1)%parents.shape[0]
    flag = False
    for i in range(3,offspring_size[1]):
      crossover_point = (numpy.random.randint(1, offspring_size[1]-2, size=1))
      offspring[k, 0:crossover_point[0]] = parents[parent1_index, 0:crossover_point[0]]
      offspring[k, crossover_point[0]:] = parents[parent2_index, crossover_point[0]:]
      if( check_constaints(offspring[k,:], constraint_matrix, condition) == True ):
        #print("cross: ",offspring[k,:], "sum: ", offspring[k,:].sum())
        flag = True
        break
    if( flag == False ):
       random_flag = False
       while( random_flag == False ):
         x = (numpy.random.uniform(low=min_value, high=max_value, size=offspring_size[1]))
         #print("random x: ",x, "sum: ", x.sum())
         if( check_constaints(x, constraint_matrix, condition) == True ):
           offspring[k,:] = x
           #print("random: ",offspring[k,:], "sum: ", offspring[k,:].sum())
           random_flag = True
  
  return offspring

"""5) Mutation"""

def mutation(offspring_crossover, constraint_matrix, condition, max_value):
  for i in range(offspring_crossover.shape[0]):
    constraint_flag = False
    mutation_index1 = numpy.uint8((numpy.random.randint(0, offspring_crossover.shape[1]-1, size=1)))
    mutation_index2 = numpy.uint8((numpy.random.randint(0, offspring_crossover.shape[1]-1, size=1)))
    if( mutation_index1 == mutation_index2 ):
      mutation_index2 = ( (mutation_index2 + 1) % offspring_crossover.shape[1]-1 )
    random_value1 = ( numpy.random.uniform(0, max_value , 1) )
    random_value2 = ( numpy.random.uniform(-max_value, 0 , 1) )
    while(constraint_flag == False): 
      offspring_crossover[i, mutation_index1] = ( (offspring_crossover[i, mutation_index1] + random_value1) % max_value )
      offspring_crossover[i, mutation_index2] = ( (offspring_crossover[i, mutation_index2] + random_value2) % max_value )
      if( check_constaints(offspring_crossover[i], constraint_matrix, condition) == True ):
        constraint_flag = True
      random_value1 = random_value1 - 1
      random_value2 = random_value2 + 1
  
  return offspring_crossover