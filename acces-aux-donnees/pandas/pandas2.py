# Common imports
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

#housing = load_housing_data()
housing = pd.read_csv("datasets/housing/housing.csv")

print("## First lines")
print(housing.head())

print("\n## Metadata")
housing.info()

print("\n## Freq. Distrib for ocean_proximity")
print(housing["ocean_proximity"].value_counts())

print("\n## Stats")
print(housing.describe())

housing.hist(bins=50, figsize=(20,15))
plt.show()