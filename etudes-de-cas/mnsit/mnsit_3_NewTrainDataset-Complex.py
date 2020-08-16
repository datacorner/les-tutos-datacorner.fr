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

# Fonction d'export pour kaggle
def exportKaggle(algo):
    p_test = algo.predict(X_TEST)
    result = pd.DataFrame(X_TEST.index + 1, columns=['ImageId'])
    pred = pd.DataFrame(p_test, columns=['Label'])
    result = result.join(pred)
    fichier = "./data/result_" + str(datetime.datetime.now()).replace(":", "-").replace(" ", "_")
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
def convertImageInRow(_img):
    return pd.DataFrame(_img.reshape(1,784), 
                        columns=["pixel" + str(x) for x in range(784)])

# dark or white / wash the pixel
def addNoise(val, thresoldMin, thresoldMax):
    if (val < thresoldMin):
        return 0
    elif val > thresoldMax:
        return val - 40
    else:
        return val
    
# Clean a global dataset 
def noiseImage(dataset, thresoldMin, thresoldMax):
    for i in range(dataset.shape[1]):
        dataset['pixel' + str(i)] = [addNoise(x, thresoldMin, thresoldMax) for x in dataset['pixel' + str(i)]]

# returns 4 images shifted from the original one
# _imageMatrix : image in a (1, 784) array
# _label : original image label
def shift4LineImages(_imageMatrix, _label):
    img = _imageMatrix.reshape(28,28)
    # Image shifting in 4 axes
    row1 = convertImageInRow(shiftImage(img, [0, 1]))
    row2 = convertImageInRow(shiftImage(img, [2, 0]))
    row3 = convertImageInRow(shiftImage(img, [-3, 0]))
    row4 = convertImageInRow(shiftImage(img, [0, -2]))
    # Noise images
    noiseImage(row1, 100, 200)
    noiseImage(row2, 150, 240)
    noiseImage(row3, 60, 170)
    noiseImage(row4, 90, 180)
    # Add image Label
    row1.insert(0, 'label', _label)
    row2.insert(0, 'label', _label)
    row3.insert(0, 'label', _label)
    row4.insert(0, 'label', _label)
    # returns the 4 new images
    return pd.concat([row1, row2, row3, row4], ignore_index=True)

print ("Copy originals: " + str(datetime.datetime.now()))
TRAIN.to_csv("./data/trainextendedcomplex.csv", index=False, mode='w', header=True)

datebefore = dateinit = datetime.datetime.now()
print ("Start: " + str(datebefore))
Rangeloop = range(X_TRAIN.shape[0])
for rowIdx in Rangeloop:
    if (rowIdx % 50 == 0):
        elapsed = datetime.datetime.now() - datebefore
        print ("Elapsed: " + str(elapsed.total_seconds()) + " sec. | Index: " + str(rowIdx))
    newImages = shift4LineImages(getImageMatriceDigit(TRAIN, rowIdx, 1), y[rowIdx])
    head = True
    newImages.to_csv("./data/trainextendedcomplex.csv", index=False, mode='a', header=False)
    
elapsedTotal = datetime.datetime.now() - dateinit
print ("Total Elapsed: " + str(elapsedTotal.total_seconds()))