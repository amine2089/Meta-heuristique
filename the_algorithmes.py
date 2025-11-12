import random
import matplotlib.pyplot as plt



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
    other_cities=[i for i in range(nbr_villes) if i != algiers_Index]
    random.shuffle(other_cities)
    path=[algiers_Index]+other_cities
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


#------- Hill Climbing -------
def Hill_Climbing(Distance_Matrix, nbr_villes, algiers_Index, max_iterations):
    #Premier trajet initial aléatoire:
    current_path, current_distance = Genereate_random_path(Distance_Matrix, nbr_villes, algiers_Index)
    iterations = 0
    
    while iterations < max_iterations:
        best_neighbor = None
        best_neighbor_distance = current_distance
        improved = False
        
        # Explorer tous les voisins possibles (tous les swaps possibles)
        # On ne touche pas à l'index 0 (Algiers)
        for i in range(1, len(current_path)):
            for j in range(i + 1, len(current_path)):
                # Créer un voisin en échangeant les villes aux indices i et j
                neighbor_path = current_path.copy()
                neighbor_path[i], neighbor_path[j] = neighbor_path[j], neighbor_path[i]
                neighbor_distance = Calculate_distance_path(neighbor_path, Distance_Matrix)
                
                # Si ce voisin est meilleur, le garder en mémoire
                if neighbor_distance < best_neighbor_distance:
                    best_neighbor = neighbor_path
                    best_neighbor_distance = neighbor_distance
                    improved = True
        
        # Si on a trouvé un meilleur voisin, on l'accepte
        if improved:
            current_path = best_neighbor
            current_distance = best_neighbor_distance
            iterations += 1
        else:
            # Pas d'amélioration trouvée, on s'arrête (on a atteint un optimum local)
            break
    
    return current_path, current_distance



