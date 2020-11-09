
import pandas as pd
import numpy as np
import datetime

from sklearn.ensemble import RandomForestClassifier

# dark or white / wash the pixel
def darkOrWhite(val):
    if (val > 150):
        return 255
    else:
        return 0

def removeNoise(val):
    if (val < 20):
        return 0
    else:
        return val
    
# Clean a global dataset 
def darkOrWhiteDataset(dataset):
    for i in range(dataset.shape[1]):
        dataset['pixel' + str(i)] = [darkOrWhite(x) for x in dataset['pixel' + str(i)]]
        
# Remove noise to the global dataset 
def removeNoiseDataset(dataset):
    for i in range(dataset.shape[1]):
        dataset['pixel' + str(i)] = [removeNoise(x) for x in dataset['pixel' + str(i)]]
        
# Fonction d'export pour kaggle
def exportKaggle(algo):
    p_test = algo.predict(X_TEST)
    result = pd.DataFrame(X_TEST.index + 1, columns=['ImageId'])
    pred = pd.DataFrame(p_test, columns=['Label'])
    result = result.join(pred)
    fichier = "./data/result_" + str(datetime.datetime.now()).replace(":", "-").replace(" ", "_")
    result.to_csv(fichier, columns=["ImageId", "Label"], index=False)

print (str(datetime.datetime.now()) + " > Read data ...")
X_NEWTRAIN = pd.read_csv("../datasources/mnsit/trainextended.csv", delimiter=',') #, skiprows=1)
TEST = pd.read_csv("../datasources/mnsit/test.csv", delimiter=',') #, skiprows=1)
X_TEST = TEST.copy()
y = X_NEWTRAIN.label
del X_NEWTRAIN["label"]

print (str(datetime.datetime.now()) + " > Remove noises ...")
removeNoiseDataset(X_NEWTRAIN)

print (str(datetime.datetime.now()) + " > Train ...")
rf = RandomForestClassifier(n_estimators=1000, random_state=3, max_features=1)
rf.fit(X_NEWTRAIN, y)
print (str(datetime.datetime.now()) +  " > Score Train : ", round(rf.score(X_NEWTRAIN, y) *100,2), " %")

print (str(datetime.datetime.now()) + " > Predict and export ...")
exportKaggle(rf)

print (str(datetime.datetime.now()) + " > Finished.")


