
import random
import pandas as pd
import matplotlib.pyplot as plt



#creating the path in the plot
def drawing_path(path,Cities,x_coords,y_coords,color,title):
    plt.figure()
    plt.title(title,fontsize=20,family="Arial",color="black")
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
    plt.xlabel("X Coordonnées",fontsize=15,family="Arial")
    plt.ylabel("Y Cordonnées",fontsize=15,family="Arial")
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
