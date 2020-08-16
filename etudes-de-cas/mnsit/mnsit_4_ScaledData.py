import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime
import scipy.ndimage as sc

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import MinMaxScaler

pd.options.display.max_columns = None

print ("Start ...")
TRAIN = pd.read_csv("../datasources/mnsit/train.csv", delimiter=',') #, skiprows=1)
TRAINEXT = pd.read_csv("../datasources/mnsit/trainextended.csv", delimiter=',') #, skiprows=1)
X_TRAIN = TRAINEXT.copy()
y = TRAINEXT.label
del X_TRAIN["label"]

TEST = pd.read_csv("../datasources/mnsit/test.csv", delimiter=',') #, skiprows=1)
X_TEST = TEST.copy()

print ("Scale ...")
scale = MinMaxScaler()
X_TRAIN = scale.fit_transform(X_TRAIN)

print ("Fit ...")
rf = RandomForestClassifier(n_estimators=800, random_state=3, max_features=0.5)
rf.fit(X_TRAIN, y)
print ("Score Train -->", round(rf.score(X_TRAIN, y) *100,2), " %")

print ("Predict ...")
X_TEST = scale.fit_transform(X_TEST)
p_test = rf.predict(X_TEST)
result = pd.DataFrame(p_test, columns=['label'])
result.insert(0, 'ImageId', result.index+ 1)
fichier = "./data/result_" + str(datetime.datetime.now()).replace(":", "-").replace(" ", "_")
print ("Export to -->" + fichier)
result.to_csv(fichier, columns=["ImageId", "label"], index=False)

