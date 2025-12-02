import math
import random
import matplotlib.pyplot as plt
from fontTools.misc.bezierTools import epsilon


#creating the path in the plot
def drawing_path(path,Cities,x_coords,y_coords,color,title):
    plt.figure()
    plt.title(title,fontsize=15,family="Arial",color="black")
    plt.scatter(x_coords, y_coords, color="red")
    for i in range(len(path)-1):
        plt.plot([x_coords[path[i]], x_coords[path[i + 1]]],
                 [y_coords[path[i]], y_coords[path[i + 1]]],
                 color=color)
    # Close the loop: draw line from last city back to first
    plt.plot([x_coords[path[-1]], x_coords[path[0]]],
             [y_coords[path[-1]], y_coords[path[0]]],
             color=color)
    for j, city in enumerate(Cities):
         plt.text(x_coords[j] + 0.15, y_coords[j] + 0.15, city, fontsize=8)
    plt.xlabel("X Coordonnées",fontsize=10,family="Arial")
    plt.ylabel("Y Cordonnées",fontsize=10,family="Arial")
    plt.grid(True)
    plt.show()

def Calculate_distance_path(path,Distance_matrix):
    distance_path=0
    for i in range(len(path)-1):
        distance_path += Distance_matrix[path[i],path[i+1]]
    distance_path += Distance_matrix[path[-1], path[0]] #Return to alger
    return distance_path

#----- Random Search -----
def Genereate_random_path(Distance_Matrix,nbr_villes,algiers_Index):
    other_cities=[i for i in range(nbr_villes) if i != algiers_Index] #Generating a path without algiers
    random.shuffle(other_cities)
    path=[algiers_Index]+other_cities #Adding algiers as the beginning
    distance_path=Calculate_distance_path(path,Distance_Matrix)
    return path,distance_path

def Random_Search(Distance_Matrix,nbr_villes, algiers_Index,num_iterations):
    #Generate the first random path
    best_path,best_distance=Genereate_random_path(Distance_Matrix,nbr_villes,algiers_Index)
    while num_iterations>0:
        random_path,random_distance=Genereate_random_path(Distance_Matrix,nbr_villes,algiers_Index)
        if random_distance<best_distance:
            best_path=random_path
            best_distance = random_distance

        num_iterations=num_iterations-1
    return best_path,best_distance

#------- Local Search -------
def swap_cities(path):
    new_path=path.copy()
    a,b= random.sample(range(1,len(path)),2) #we're not gonna touch the first index
    new_path[a], new_path[b] = new_path[b], new_path[a]
    return new_path
def Local_Search(Distance_Matrix,nbr_villes,algiers_Index,num_iterations):
    #Premier trajet initial aléatoire:
    first_path,first_distance=Genereate_random_path(Distance_Matrix, nbr_villes, algiers_Index)
    while num_iterations>0: #On faire des p'tites modifications sur le path
        path= swap_cities(first_path)
        distance=Calculate_distance_path(path,Distance_Matrix)
        if distance<first_distance:
            first_path=path
            first_distance=distance
        num_iterations=num_iterations-1
    return first_path,first_distance


#------- Multi_Start Local Search -------
def Multi_Start_Local_Search(Distance_Matrix, nbr_villes, algiers_Index, num_starts=10, local_iterations=500):

    solutions = []  # List to store solutions of the local searches
    for i in range(num_starts):

        # Applying Local Search multiple times:
        local_path, local_distance = Local_Search(Distance_Matrix, nbr_villes, algiers_Index, local_iterations)
        # Step 3: Store result
        solutions.append((local_path, local_distance))
        print(f"Local search {i+1}: Distance = {round(local_distance, 2)}")
    # Finding  the best among all stored solutions
    best_solution = min(solutions, key=lambda s: s[1])
    best_path, best_distance = best_solution

    return best_path, best_distance

#------- Hill Climbing -------
"""
this method doesn't guarantee the global maximum, just the local maximum
which means it doesn't work everytime
"""
def Hill_Climbing(Distance_Matrix, nbr_villes, algiers_Index, nbr_itérations):
    #First random solution
    ran_path,ran_distance= Genereate_random_path(Distance_Matrix, nbr_villes, algiers_Index)
    i=0
    while i < nbr_itérations:
     #Generating a new solution close to the old solution using swap
     Hill_path =swap_cities(ran_path)
     Hill_distance = Calculate_distance_path(Hill_path,Distance_Matrix)
     if(Hill_distance<ran_distance):
        ran_path = Hill_path
        ran_distance = Hill_distance
     i+=1
    return ran_path, ran_distance

#------- Recuit Simulé -------
def Diminuer_T(T0):
    alpha=0.9995
    T=alpha*T0
    return T

def Recuit_Simulé(Distance_Matrix, nbr_villes, algiers_Index,nbr_itération):
    #Solution de base
    base_path,base_distance=Genereate_random_path(Distance_Matrix,nbr_villes, algiers_Index)
    T = 1000  # Température initiale
    epsiloon = 1e-6 #Tmin
    while nbr_itération>0 and T>epsiloon:
        RS_path=swap_cities(base_path)
        RS_distance = Calculate_distance_path(RS_path,Distance_Matrix)
        DELTA= RS_distance-base_distance
        if DELTA<0:
            base_path=RS_path
            base_distance=RS_distance
        else:
            #Accept avec proba P= exp(-delta/T), the proba chooses if we take the worst value or not
            P=math.exp(-DELTA/T)
            if random.random()<P:
                base_path=RS_path
                base_distance=RS_distance
        # refroidissement
        T=Diminuer_T(T)
        nbr_itération-=1
    return base_path, base_distance

#------- Tabu Search -------
def Tabu_Search(Distance_Matrix, nbr_villes, algiers_Index,nbr_iterations):
    #Solution initiale
    initial_path,initial_distance=Genereate_random_path(Distance_Matrix, nbr_villes, algiers_Index)
    best_path,best_distance=initial_path,initial_distance
    #Initialisation de Tabu list
    Tabu_list=[]
    Tabu_len=10
    num_neighbors=10
    while nbr_iterations>0:
        neighbors=[]
        for i in range(num_neighbors):
            neighbor=swap_cities(initial_path)
            neighbor_distance=Calculate_distance_path(neighbor,Distance_Matrix)
            neighbors.append((neighbor,neighbor_distance))
        #select best neighbor
        best_neighbor = None
        best_neighbor_distance = float("inf")
        for path,dist in neighbors:
                #allow tabu move if it beats global best
                if path in Tabu_list and dist>=best_neighbor_distance:
                    continue
                if dist<best_neighbor_distance:
                    best_neighbor=path
                    best_neighbor_distance=dist
        # Move to best admissible neighbor (even if worse)
        initial_path = best_neighbor
        initial_distance = best_neighbor_distance
        if initial_distance<best_distance:
            best_path=initial_path
            best_distance=initial_distance
        Tabu_list.append(initial_path)
        if len(Tabu_list)>Tabu_len:
            Tabu_list.remove(Tabu_list[0])
        
        nbr_iterations -= 1

    return best_path, best_distance


#------- Genetic Algorithm -------

def Crossover(parent1, parent2, algiers_Index):
    size=len(parent1)
    #Choosing two random point to cut
    a= random.randint(1,size-2)
    b=random.randint(a+1,size-1)

    #Initialize child with None values
    child=[None]*size
    child[0]=algiers_Index
    child[a:b]=parent1[a:b]
    #Filling the remaining places
    remaining=[]
    for gene in parent2:
        if gene not in child:
            remaining.append(gene)
    # Fill the None positions with remaining genes from parent2
    position=1
    for gene in remaining:
        while position<size and child[position] is not None:
            position+=1
        if position<size:
            child[position]=gene
            position+=1
    return child

def Mutate(path, mutation_rate, algiers_Index):
    mutated=path.copy()
    for i in range(1, len(mutated)):
        if random.random()<mutation_rate:
            j=random.randint(1, len(mutated)-1)
            mutated[i], mutated[j]=mutated[j], mutated[i]
    return mutated
def Genetic_Algorithm(Distance_Matrix, nbr_villes, algiers_Index,mutation_rate, population_size=40, generations=200):
    #population size represents the number of chromosomes generated
    # ---- Create initial population ----
    population=[]
    for _ in range(population_size):
        individual=Genereate_random_path(Distance_Matrix, nbr_villes, algiers_Index)[0]
        distance_individual=Calculate_distance_path(individual,Distance_Matrix)
        population.append((individual,distance_individual))
    
    #Track best solution across all generations
    best_path=None
    best_distance=float("inf")
    
    #Evolution loop
    for generation in range(generations):
        #Calculating the fitness
        Fitness_list=[]
        total_fit=0
        for individual,distance in population:
            Fitness=1/distance
            Fitness_list.append(Fitness)
            total_fit+=Fitness
        #Selection Probability
        Selection_proba=[]
        for fit in Fitness_list:
            proba=fit/total_fit #the probability to choose a chromosome to be the father
            Selection_proba.append(proba)
        
        #Create new generation
        new_population=[]
        
        #Keep best individual (elitism)
        best_individual=min(population, key=lambda x: x[1])
        new_population.append(best_individual)
        if best_individual[1]<best_distance:
            best_path=best_individual[0]
            best_distance=best_individual[1]
        
        #Generate rest of population through crossover and mutation
        while len(new_population)<population_size:
            #Selecting two parents using roulette wheel selection (inline)
            #Select parent1
            r1=random.random()
            cumulative_prob1=0
            parent1=None
            for i, prob in enumerate(Selection_proba):
                cumulative_prob1+=prob
                if r1<=cumulative_prob1:
                    parent1=population[i][0]
                    break
            if parent1 is None:
                parent1=population[-1][0]  #Fallback
            
            #Select parent2 (ensure different from parent1)
            parent2=None
            while parent2 is None or parent2==parent1:
                r2=random.random()
                cumulative_prob2=0
                for i, prob in enumerate(Selection_proba):
                    cumulative_prob2+=prob
                    if r2<=cumulative_prob2:
                        parent2=population[i][0]
                        break
                if parent2 is None:
                    parent2=population[-1][0]  #Fallback
            
            #Crossover to create child
            child=Crossover(parent1, parent2, algiers_Index)
            
            #Mutate child
            child=Mutate(child, mutation_rate, algiers_Index)
            
            #Calculate child's distance
            child_distance=Calculate_distance_path(child, Distance_Matrix)
            new_population.append((child, child_distance))
        
        #Replace old population with new population
        population=new_population
        
        #Optional: print progress every 50 generations
        if (generation+1)%50==0:
            print(f"Generation {generation+1}: Best distance = {round(best_distance, 2)} km")
    
    return best_path, best_distance



