#%% Importation des packages 

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.integrate import odeint


#%% Tâche 1

bafond = pd.read_csv("/Users/quoilinguillaume/Downloads/bafonde_data.csv")

bafond["Date_stamp"] = pd.to_datetime(bafond["Date_stamp"])
bafond = bafond.set_index("Date_stamp") #Colonne des dates transformée en un index
bafond = bafond.loc["2020/06/27":"2020/07/13"] #sélection de la période du 27 juin 2020 au 13 juillet 2020

#%% Tâche 2 

bafond["temps"] = np.arange(0, len(bafond),1) # Ajout de la variable 'temps' dans le DataFrame bafonbe
                                              # Allant de l'heure 0 à l'heure longueur du DataFrame par incrément de 1 heure
#%% Tâche 3 

tm = 3 
sigma = 1
tau = bafond["temps"]

htau = (1/(np.sqrt(2*np.pi*sigma)))*np.exp((-(tau-tm)**2)/(2*sigma)) # Calcul fonction impulsionnelle

convolve_produit = np.convolve(bafond["pluv_h"], htau, mode = "full")  # Calcul produit de convolution de la fonction impulsionnelle et de pluv_h 
                                                                       # Produit de convolution multiplié par un facteur de correction donnera peff=flux d'entrée
bafond["peff"] = convolve_produit[0:len(bafond)] 

#%% Tâche 4 

def bilanhydrique_odeint (S, t): 
    Cr1 = 3     # facteur de correction
    Dmax = 50   # unités : mmm/h
    Smin = 70   #  unités : mm
    Smax = 150  # unités : mm
    lam = 2     #lamda
    pluie = np.interp(t, bafond["temps"], bafond["peff"]) # Interpolation des points des données discrètes de la pluie effective entre les heures
    dSdt = Cr1*pluie-Dmax*((S-Smin)/(Smax-Smin))**(lam) # Bilan hydrique = flux d'entrée (pluie) - flux de sortie (drainage)
    return dSdt  # Bilan hydrique dS/dt = Jint - Jout

#%% Tâche 5 

Cr1 = 3 # Facteur de correction
Dmax = 50 # Unités : mmm/h
Smin = 70 # Unités : mm
Smax = 150 # Unités : mm
lam = 2 

S0 = 75 # Stock initiale à t=0

bafond["stock"] = odeint(bilanhydrique_odeint, S0 , bafond["temps"])

date_form=mdates.DateFormatter("%d-%b")
fig, ax=plt.subplots()

plt.plot(bafond["stock"]) # Graphique évolution du stock

plt.title("Evolution du stock d'eau du bas-fond en fonction du temps")
ax.xaxis.set_major_formatter(date_form)
ax.set(ylabel="Stock d'eau [mm]")
plt.savefig("Evolution du stock d'eau du bas-fond en fonction du temps.png")
plt.show()

#%% Tâche 6 

Cr2 = 1 # Facteur de correction fixé à 1
bafond["L1"] = Cr2*(Dmax*((bafond["stock"]-Smin)/(Smax-Smin))**(lam))
# L1 (hauteurs d'eau simulées au capteur L1) = Cr2 (facteur de correction) x D(t) (intensité de drainage)
# L1_h = hauteurs d'eau observées au capteur L1

date_form=mdates.DateFormatter("%d-%b")
fig, ax=plt.subplots()
plt.plot(bafond.index, bafond["L1"], bafond["L1_h"])  
plt.title("Comparaison des hauteurs d'eau observées et simulées")
ax.xaxis.set_major_formatter(date_form)
ax.set(ylabel="Hauteur d'eau [cm]")
blue_line = plt.Line2D([],[], color = 'steelblue' , label = "Simulées (Cr = 1)")
orange_line = plt.Line2D([],[], color='orange' , label = "Observées")
plt.legend(handles= [blue_line, orange_line])
plt.savefig("Comparaison des hauteurs d'eau observées et simulées.png")
plt.show()



#%% Tâche 7

# On va faire varier le facteur de correction (3,9, 12 et 25) de façon arbitraire.
# On trouvera ainsi la valeur optimale pour modéliser le niveau d'eau en aval du bas-fond au niveau de L1.

bafond["L1(Cr=3)"] = 3*(Dmax*((bafond["stock"]-Smin)/(Smax-Smin))**(lam))   #Cr=3
bafond["L1(Cr=9)"] = 9*(Dmax*((bafond["stock"]-Smin)/(Smax-Smin))**(lam))   #Cr=9
bafond["L1(Cr=12)"] = 12*(Dmax*((bafond["stock"]-Smin)/(Smax-Smin))**(lam)) #Cr=12
bafond["L1(Cr=25)"] = 25*(Dmax*((bafond["stock"]-Smin)/(Smax-Smin))**(lam)) #Cr=25

date_form=mdates.DateFormatter("%d-%b")
fig, ax=plt.subplots()

plt.plot(bafond.index, bafond["L1_h"], label = 'Observées')   # Mesures observées
plt.plot(bafond.index, bafond["L1(Cr=3)"], label= 'Cr=3')     # Mesures simulées  
plt.plot(bafond.index, bafond["L1(Cr=9)"], label = 'Cr=9')    # Mesures simulées
plt.plot(bafond.index, bafond["L1(Cr=12)"], label = 'Cr=12')  # Mesures simulées
plt.plot(bafond.index, bafond["L1(Cr=25)"], label = 'Cr=25')  # Mesures simulées

plt.title("Comparaison des hauteurs d'eau observées et simulées")
ax.xaxis.set_major_formatter(date_form)
ax.set(ylabel="Hauteur d'eau [cm]")
plt.legend()
plt.savefig("Comparaison des hauteurs d'eau observées et simulées.png")
plt.show() #Graphique de ces 5 mesures afin de visualiser afin de visualiser le facteur Cr qui modélise le mieux L1.



                    