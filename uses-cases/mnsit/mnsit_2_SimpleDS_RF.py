import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

pd.options.display.max_columns = None
#pd.set_printoptions(max_columns=500)

print (str(datetime.datetime.now()) + " - Import des jeux de données")
TRAIN = pd.read_csv("../datasources/mnsit/train.csv", delimiter=',') #, skiprows=1)
TEST = pd.read_csv("../datasources/mnsit/test.csv", delimiter=',') #, skiprows=1)
X_TRAIN = TRAIN.copy()
X_TEST = TEST.copy()
y = TRAIN.label
del X_TRAIN["label"]

print (str(datetime.datetime.now()) + " - Données importées")
print (str(datetime.datetime.now()) + " - Grid Search sur Random Forest en cours ...")
# Fonction d'export pour kaggle
def ExportKaggle(algo):
    p_test = algo.predict(X_TEST)
    result = pd.DataFrame(X_TEST.index + 1, columns=['ImageId'])
    pred = pd.DataFrame(p_test, columns=['Label'])
    result = result.join(pred)
    fichier = "./data/result_" + str(datetime.datetime.now()).replace(":", "-").replace(" ", "_")
    result.to_csv(fichier, columns=["ImageId", "Label"], index=False)

param_grid_rf = { 'n_estimators' : [800, 1000], 
               'max_features' : [1, 0.5, 0.2],
               'random_state' : [3, 4]}
grid_search_rf = GridSearchCV(RandomForestClassifier(), param_grid_rf, cv=5)
grid_search_rf.fit(X_TRAIN, y)
print ("Score final : ", round(grid_search_rf.score(Xtrain, y) *100,4), " %")
print ("Meilleurs parametres: ", grid_search_rf.best_params_)
print ("Meilleure config: ", grid_search_rf.best_estimator_)

print (str(datetime.datetime.now()) + " - Parametres trouvés, export dans un fichier résultat.")
ExportKaggle(param_grid_rf)

