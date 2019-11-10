from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import math
import numpy.random as npr

data = pd.read_csv('tunedit_genres.csv')
percentage = sum(data.iloc[:, -1]) / len(data)
print(percentage)

X = data.iloc[:, :-1]
X = (X - X.mean()) / X.std()
Y = data.iloc[:, -1]

c = np.random.RandomState(123).permutation(len(X))
X = X.iloc[c]
X = X.reset_index(drop=True)
Y = Y.iloc[c]
Y = Y.reset_index(drop=True)
num_train = math.ceil(len(X) * 0.75)
X_train = X[:num_train]
X_test = X[num_train:]
Y_train = Y[:num_train]
Y_test = Y[num_train:]


percentage_train = sum(Y_train) / len(Y_train)
percentage_test = sum(Y_test) / len(Y_test)
print('percentage_train=', percentage_train)
print('percentage_test=', percentage_test)
