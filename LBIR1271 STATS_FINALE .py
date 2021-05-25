#%%
# Importation des packages

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
import matplotlib.dates as mdates

#%% 1. Précipitations et hauteur d'eau mesurées aux heures 180 à 820 après le 19/06/2020 à minuit.

bafonbe = pd.read_csv('/Users/quoilinguillaume/Downloads/bafonde_data.csv', usecols = (0, 2, 10))
bafonbe['Date_stamp'] = pd.to_datetime(bafonbe['Date_stamp'])
bafonbe = bafonbe.set_index('Date_stamp')

data = bafonbe[180:821] #sélection des heures 180 à 820 (821 étant exclu)
data['pluv_h10'] = data['pluv_h']*10

print(data) #contient les 641 valeurs de hauteurs d'eau et de précipitations

#%%

plu = data[['L1_h', 'pluv_h10']]
date_form=mdates.DateFormatter("%d-%b")
fig, ax= plt.subplots()
plt.plot(plu) #graphique des hauteurs d'eau et des précipitations multipliées par 10
plt.title("""Précipitations et hauteur d’eau mesurées aux heures 180 à 820 après le 19/06/2020 à minuit.""")
ax.xaxis.set_major_formatter(date_form)
ax.set(ylabel="""Précipitation et hauteur d'eau mesurées.""", xlabel="Dates[jj-m]")
blue_line = plt.Line2D([],[], color="steelblue", label = "Hauteur d'eau L1-BV")
orange_line = plt.Line2D([],[], color="orange", label = "Précipitations (x10)")
plt.legend(handles= [orange_line,blue_line]) #ordre d'apparition des légendes

plt.savefig("Précipitations et hauteur d’eau mesurées.png")
plt.show()


#%% 2. L'hydrogramme unitaire 

tmax = 37 # à ajuster de façon à arriver au 0 sans descendre dans les valeurs négatives
          # 37h pour que TOUTE la pluie unitaire ruisselle 
h = data[['L1_h']].iloc[tmax:] 
h["L1_h"] = h["L1_h"] - 1.65 # on enlève l'écart moyen calculé à la ligne 88, et ce à toutes nos valeurs 
                             # de hauteurs d'eau de sorte que lorsqu'il ne pleut pas, notre hauteur d'eau
                             # tourne autour de 0.

n = len(h)

R = [] #Création d'une liste vide
for i in range (n):
    r = data.iloc[i:i+tmax+1][["pluv_h"]].T
    R.append(r) # Ajout de r à R
R = np.concatenate(R) # Transformation de R(=liste) en un np.array

û = np.linalg.inv(R.T @ R) @ (R.T @ h['L1_h']) # Calcul de l'estimatuer û via la méthode des moindres carrés
u = np.flip(û) # Inversion du vecteur û
h["prédit"]= R @ û # Calcul des hauteurs prédites ĥ via l'estimateur et ajout de la colonne "prédit" au DataFrame h
plt.plot(u)
plt.xlabel('Temps après une précipitation unitaire [heures]')
plt.ylabel('Hydrogramme unitaire estimé')
plt.title('Hydrogramme unitaire estimé par la méthode des moindres carrés')
plt.axhline(y=0, color='r', linestyle='dashed')

plt.savefig("Hydrogramme unitaire.png")
plt.show()


#%% 3. Prédictions hauteur d'eau

hi=h[["L1_h","prédit"]] + 1.65  # On ré-ajoute la valeur de l'écart moyen entre prédit et observé de sorte que l'on retrouve un débit cohérent avec le débit observé 
date_form=mdates.DateFormatter("%d-%b") 
fig, ax= plt.subplots()
plt.plot(hi) #Graphique des hauteurs d'eau prédites et observées
plt.title('Comparaison des hauteurs mesurées avec les hauteurs prédites par convolution des précipitations')
ax.xaxis.set_major_formatter(date_form)
ax.set(ylabel="Hauteur d'eau [cm]", xlabel="Dates[j-m]")
blue_line = plt.Line2D([],[], color = 'steelblue', label = "Observé")
orange_line = plt.Line2D([],[], color = 'orange', label = "Prédit")
plt.legend(handles= [blue_line,orange_line]) # Ordre d'apparition des légendes

plt.savefig("Comparaison des hauteurs d'eau prédites et observées.png")
plt.show()

#%% Ecart moyen entre hauteurs prédites et observées afin de corriger les calculs ensuite

hi1= hi.sort_values("prédit")  # On trie les valeurs prédites par ordre croissant
hi1= hi1[hi1["prédit"] - 1.65 ==0] # On cherche les valeurs de 1.65 - 1.65 = 0
hi1= hi1[hi1["L1_h"]<10]  # Bien que la condition = 0, nous avions 3 valeurs parasites > 10
print(hi1['L1_h'].mean()) 


          


#%%


#%%