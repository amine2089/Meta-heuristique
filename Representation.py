import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from the_algorithmes import *

"""
The first row is special: city,lat,lon,x_km,y_km
These are column headers.
Pandas uses this row to name the columns in the DataFrame.
The following rows are data rows, with values corresponding to each column.

Reads the file line by line.
Splits each line by commas (, is the default separator for CSV).
First line → column names (city, lat, lon, x_km, y_km).
Remaining lines → data rows. Each value goes under its respective column.
"""

#--------- Extraction de données ---------
file=pd.read_csv(r"C:\Users\lenovo\Downloads\algeria_20_cities_xy.csv")

    #Reading data:
    #Creating the lists
Cities= file['city'].values
latitudes = file['lat'].values
x_coords = file['x_km'].values
y_coords = file['y_km'].values

nbr_villes=len(Cities)

  #Putting the data in the plot

plt.figure()

plt.scatter(x_coords, y_coords, color="red") #putting each city in its place

for i in range(nbr_villes):
    plt.text(x_coords[i]+1, y_coords[i]+1, Cities[i],fontsize=7) #adding the name of each city
plt.title("Les Coordonnées des wilayas d'algérie",fontsize=15, family="Arial",color="black")
plt.xlabel("X Coordonnées",fontsize=10,family="Arial")
plt.ylabel("Y Cordonnées",fontsize=10,family="Arial")
plt.grid(True)
plt.show()

#La création de la table de distance:
Distance_Matrix = np.zeros((nbr_villes, nbr_villes))

for i in range(nbr_villes):
    for j in range(i+1,nbr_villes): #Filling only one side
        dx=x_coords[j]-x_coords[i]
        dy=y_coords[j]-y_coords[i]
        distance= np.sqrt(dx**2 + dy**2) # La distance euclidienne
        Distance_Matrix[i][j] = distance
        Distance_Matrix[j][i] = distance

print(Distance_Matrix)

#------- Using Random Search -------
algiers_Index=list(Cities).index("Algiers")
path_Random,distance_Random=Random_Search(Distance_Matrix,nbr_villes,algiers_Index,10000)
drawing_path(path_Random,Cities,x_coords,y_coords,"blue","random Search Visualization")
city_path=[]
for i in range(nbr_villes):
    city_path.append(Cities[path_Random[i]])
the_distance=Calculate_distance_path(path_Random,Distance_Matrix)
print("\nBest random path found:")
print(city_path)
print(str(the_distance)+" km")

#------- Using Local Search -------
path_Local,distance_Local= Local_Search(Distance_Matrix,nbr_villes,algiers_Index,800)
drawing_path(path_Local,Cities,x_coords,y_coords,"green","Local Search Visualization")
city_path2=[]
for i in range(nbr_villes):
    city_path2.append(Cities[path_Local[i]])
the_distance2=Calculate_distance_path(path_Local,Distance_Matrix)
print("\nBest Local path found:")
print(city_path2)
print(str(the_distance2)+" km")

#------- Using Multi Start Local Seach -------
path_MT,distance_MT= Multi_Start_Local_Search(Distance_Matrix, nbr_villes, algiers_Index, 1000)
drawing_path(path_MT,Cities,x_coords,y_coords,"purple","Multi start local search Visualization")
city_path3=[]
for i in range(nbr_villes):
    city_path3.append(Cities[path_MT[i]])
the_distance3=Calculate_distance_path(path_MT,Distance_Matrix)
print("\nBest Multi start local search found:")
print(city_path3)
print(str(the_distance3)+" km")

#------- Using Hill Climbing -------
path_hill,distance_hill= Hill_Climbing(Distance_Matrix, nbr_villes, algiers_Index, 800)
drawing_path(path_hill,Cities,x_coords,y_coords,"pink","Hill Climbing Visualization")
city_path4=[]
for i in range(nbr_villes):
    city_path4.append(Cities[path_hill[i]])

print(f"\nThe Hill Climbing path is {city_path4}")
print("\nBest Hill Climbing search found:")
print(str(distance_hill)+" km")
##------- Using Simulated Annealing -------

SA_path,SA_distance=Recuit_Simulé(Distance_Matrix, nbr_villes,algiers_Index,5000)
drawing_path(SA_path,Cities,x_coords,y_coords,"silver","Simulated Annealing Visualization")
city_path5=[]
for i in range(nbr_villes):
    city_path5.append(Cities[SA_path[i]])
print(f"\nThe Simulated Annealing path is {city_path5}")
print("\nBest Simulated Annealing search found:")
print(str(SA_distance)+" km")