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

pd.options.display.max_columns = None

TRAIN = pd.read_csv("../datasources/mnsit/train.csv", delimiter=',') #, skiprows=1)
TEST = pd.read_csv("../datasources/mnsit/test.csv", delimiter=',') #, skiprows=1)
X_TRAIN = TRAIN.copy()
X_TEST = TEST.copy()
y = TRAIN.label
del X_TRAIN["label"]

# Fonction d'export pour kaggle ()
def exportKaggle(algo):
    p_test = algo.predict(X_TEST)
    result = pd.DataFrame(X_TEST.index + 1, columns=['ImageId'])
    pred = pd.DataFrame(p_test, columns=['Label'])
    result = result.join(pred)
    fichier = "./data/result_" + str(datetime.datetime.now()).replace(":", "-").replace(" ", "_")
    print (str(datetime.datetime.now()) + " > Export to file " + fichier)
    result.to_csv(fichier, columns=["ImageId", "Label"], index=False)
    
# returns the image in digit (28x28)
# fromIndex = 0 if no labels 1 else
def getImageMatriceDigit(dataset, rowIndex, fromIndex):
    return dataset.iloc[rowIndex, fromIndex:].values.reshape(28,28)

# returns the image matrix in one row
# fromIndex = 0 if no labels 1 else
def getImageLineDigit(dataset, rowIndex, fromIndex):
    return dataset.iloc[rowIndex, fromIndex:]

# display an image defined in the data given (train/test)
def displayImageFromData(data, row, fromIndex):
    imgDigitMatrice = getImageMatriceDigit(data, row, fromIndex)
    displayImage(imgDigitMatrice)

# display an image from the Matrix 28:28
def displayImage(image):
    plt.imshow(image, cmap=matplotlib.cm.binary, interpolation="nearest")
    plt.axis("off")
    plt.show()

# shift the image
def shiftImage(imageMatrix, shiftConfig):
    return sc.shift(imageMatrix, shiftConfig, cval=0)

# convert an image 28:28 in one matrix row
def convertImageInRow(img):
    return pd.DataFrame(img.reshape(1,784), 
                        columns=["pixel" + str(x) for x in range(784)])

# returns 4 images shifted from the original one
def shift4LineImages(_imageMatrix, label):
    shft = 1
    row1 = convertImageInRow(shiftImage(_imageMatrix, [0, shft]))
    row2 = convertImageInRow(shiftImage(_imageMatrix, [shft, 0]))
    row3 = convertImageInRow(shiftImage(_imageMatrix, [shft * -1, 0]))
    row4 = convertImageInRow(shiftImage(_imageMatrix, [0, shft * -1]))
    row1.insert(0, 'label', label)
    row2.insert(0, 'label', label)
    row3.insert(0, 'label', label)
    row4.insert(0, 'label', label)
    #row1['label'] = row2['label'] =row3['label'] =row4['label'] = label
    return pd.concat([row1, row2, row3, row4], ignore_index=True)

# # Extension du jeu de donnees d'entrainement
# Ajout de 4 images par image originale / via decalage de pixel

datebefore = dateinit = datetime.datetime.now()
print (str(dateinit) + "Begin new train data generation ...")
X_NEWTRAIN = pd.DataFrame()
Rangeloop = range(X_TRAIN.shape[0])

for rowIdx in Rangeloop:
    if (rowIdx % 100 == 0):
        elapsed = datetime.datetime.now() - datebefore
        print ("Elapsed: " + str(elapsed.total_seconds()) + " sec. | Index: " + str(rowIdx) + " | Shape: " + str(X_NEWTRAIN.shape))
        datebefore = datetime.datetime.now()
    X_NEWTRAIN = pd.concat([X_NEWTRAIN, shift4LineImages(getImageMatriceDigit(TRAIN, rowIdx, 1), y[rowIdx])], ignore_index=True)
X_NEWTRAIN = pd.concat([X_NEWTRAIN, TRAIN], ignore_index=True)

elapsedTotal = datetime.datetime.now() - dateinit
print ("Total Elapsed: " + str(elapsedTotal.total_seconds()) + " sec. | Global Shape: " + str(X_NEWTRAIN.shape))

print (str(datetime.datetime.now()) + "Export data to file.")
X_NEWTRAIN.to_csv("./data/trainextended.csv", index=False)

print (str(datetime.datetime.now()) + "New train data generated.")