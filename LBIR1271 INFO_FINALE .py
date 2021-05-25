# Projet partie informatique 

# 1. Chargement des packages 
import matplotlib.rcsetup as rc
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import pandas as pd 
import seaborn as sns   # Seaborn est une libraire de Data Visualisation basé sur matplotlib

#%% 

# 2. Chargement des données 

debit_ex = pd.read_excel('/Users/quoilinguillaume/Downloads/bafonbe_fev21.xlsx', sheet_name='Débits Exutoire',usecols=(0, 1))
debit_ex = debit_ex.rename(columns= {'REFERENCES TEMPORELLES':'Date_stamp', 'Débits à L2-BV (m3/s)':'debit'})

print(debit_ex)

#%%

limn = pd.read_excel('/Users/quoilinguillaume/Downloads/bafonbe_fev21.xlsx', sheet_name='Limnimétrie',
                     usecols=(0, 1, 2))
limn = limn.rename(columns= {'REFERENCES TEMPORELLES':'Date_stamp', 'Hauteur eau L1-BV (cm)':'L1', 'Hauteur eau L2- BV(Exutoire)' : 'L2'})
print(limn)

#%%

piez = pd.read_excel('/Users/quoilinguillaume/Downloads/bafonbe_fev21.xlsx',
                     sheet_name='Piézométrie', usecols=(0, 2, 3, 4, 5, 6, 7))
piez = piez.rename(columns={'REFERENCES TEMPORELLES':'Date_stamp', 'Hauteur eau P1-BF (cm)':'p1_bf','Hauteur eau P2-BF (cm)':'p2_bf', 'Hauteur eau P3-BF (cm)':'p3_bf',
                            'Hauteur eau P1-BV (cm)':'p1_bv','Hauteur eau P2-BV (cm)':'p2_bv','Hauteur eau P3-BV (cm)':'p3_bv'})
print(piez)

#%%

pluv_15 = pd.read_excel('/Users/quoilinguillaume/Downloads/bafonbe_fev21.xlsx', sheet_name='Pluviométrie-Site 15 Minutes', usecols=(0, 1), skiprows=[0])  
# Le skiprows permet de ne pas prendre en compte la première ligne 
pluv_15 = pluv_15.rename(columns= {'Date - Heure':'Date_stamp', 'Hauteurs pluviométriques (mm)':'pluv'})
print(pluv_15)

#%%

# 3. Définir un index

debit_ex['Date_stamp'] = pd.to_datetime(debit_ex['Date_stamp']) 
debit_ex = debit_ex.set_index('Date_stamp') # Définissions de la colone Date_stamp comme index


#%%

limn['Date_stamp'] = pd.to_datetime(limn['Date_stamp'])
limn = limn.set_index('Date_stamp')

#%% 

piez['Date_stamp'] = pd.to_datetime(piez['Date_stamp'])
piez = piez.set_index('Date_stamp')

#%%

pluv_15['Date_stamp'] = pd.to_datetime(pluv_15['Date_stamp'])
pluv_15 = pluv_15.set_index('Date_stamp')

# 4. Agrégation et sélection des données

#%% 

debit_ex_h = debit_ex.resample('1H').mean()
debit_ex_h = debit_ex_h['2020-06-19': '2020-09-15 00:00:00 ']

limn_h = limn.resample('1H').mean()
limn_h = limn_h['2020-06-19': '2020-09-15 00:00:00 ']

piez_h = piez.resample('1H').mean()
piez_h = piez_h['2020-06-19': '2020-09-15 00:00:00 ']

pluv_15_h = pluv_15.resample('1H').sum()
pluv_15_h = pluv_15_h['2020-06-19': '2020-09-15 00:00:00 ']

# Test pour voir s'il réalise bien la somme des précipitations d'une heure 
print(pluv_15_h.loc['2020-06-25 06:00:00'])

# Suppresion des DataFrames

del(debit_ex, limn, piez, pluv_15)


#%%

# 5. Fusionner les données 

datafull = pd.concat([debit_ex_h, limn_h, piez_h, pluv_15_h]).groupby(level=0).first()
datafull.columns = ["debit_h", "L1_h", "L2_h", "p1_bf_h", "p2_bf_h", "p3_bf_h", "p1_bv_h",
                    "p2_bv_h", "p3_bv_h", "pluv_h" ]
print(datafull.describe())  # affichage d'un résumé statistique du dataframe

datafull.to_csv("bafonde_data.csv")  # sauvegarde du nouveau DataFrame datafull sous le format .csv

#%% 

# 6. Figures 

plt.plot(debit_ex_h)

plt.xlabel("Dates")
plt.ylabel("Débit ($m^3$/s)")   # Les $ permettent de mettre le 3 en exposant
plt.title("Evolution du débit en fonction du temps ")
plt.xticks(fontsize=8.5)    # permet de réduire la taille 
plt.savefig("débit.png")  # Sauvegarde des figures en format .png

plt.show()


plt.plot(pluv_15_h)

plt.xlabel("Dates")
plt.ylabel("Hauteur pluviométrique en mm")
plt.title("Evolution de la hauteur pluviométrique en fonction du temps")
plt.xticks(fontsize=8)
plt.savefig("pluviométrie.png")

plt.show()


#%%
limn_h.plot(subplots=True) # Utilisation du subplot qui sert à mettre les données 
                           #  sur plusieurs sous-graphiques au lieu d'un. 
plt.xlabel("Dates")
plt.ylabel("Hauteur d'eau (cm)")
plt.suptitle("Hauteur d'eau en fonction du temps")
plt.savefig("limnimétrie.png")


#%%

piez_h.plot(subplots=True)
plt.xlabel("Dates")
plt.ylabel("Hauteur d'eau (cm)")
plt.suptitle("Hauteur d'eau en fonction du temps")

plt.savefig("piézométrie.png")

#%%

#Création d'un 'pairplot'

sns.pairplot(datafull)
plt.savefig("pairplot.png")
            