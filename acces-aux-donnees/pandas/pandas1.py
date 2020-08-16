import pandas as pd
pd.set_option('max_rows', 5)
df = pd.DataFrame({'Apples': [30], 'Bananas': [21]})
print(df)
df = pd.DataFrame({'Apples': [35, 41], 'Bananas': [21, 34]}, index=['2017 Sales', '2018 Sales'])
print(df)
df = pd.Series(["4 cups", "1 cup", "2 large", "1 can"], index=["Flour", "Milk", "Eggs", "Spam"], name='Dinner, dtype: object')
print(df)
