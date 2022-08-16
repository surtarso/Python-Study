#this is an artificial intelligence program that will generate 6 random numbers from 1 to 60 based on trained data
#train data is a list of the past 6 winning numbers, contained in the file mega_sena_sorteio.xlsx as rows
#it will train the model to predict the next 6 winning numbers
#in the end, it will print the 6 numbers predicted

import pandas as pd  #import pandas library
import numpy as np  # for mathematical operations
import random as rd  #importing random module
import math as m  #import math module for math functions
import matplotlib.pyplot as plt #for plotting
import seaborn as sns #for plotting
from sklearn.model_selection import train_test_split #split the data into train and test sets
from sklearn.linear_model import LinearRegression as lr  #import linear regression model
from sklearn.metrics import mean_squared_error as mse  #import mean squared error
from sklearn.metrics import r2_score as r2  #import r2 score
from sklearn.metrics import mean_absolute_error as mae   #import mean absolute error
from sklearn.metrics import median_absolute_error as medae  #import median absolute error
from sklearn.metrics import explained_variance_score as evs  #import explained variance score
from sklearn.metrics import mean_squared_log_error as msle  #import mean squared log error


#importing the data from the file
data = pd.read_excel('mega_sena_sorteio.xlsx')

#splitting the data into train and test sets
X = data.iloc[:,0:6].values
y = data.iloc[0:2509].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=0)

#fitting the model to the training set
regressor = lr()
regressor.fit(X_train, y_train)

#predicting the test set results
y_pred = regressor.predict(X_test)

#printing the results
print('Mean Squared Error: ', mse(y_test, y_pred))
print('R2 Score: ', r2(y_test, y_pred))
print('Mean Absolute Error: ', mae(y_test, y_pred))
print('Median Absolute Error: ', medae(y_test, y_pred))
print('Explained Variance Score: ', evs(y_test, y_pred))
print('Mean Squared Log Error: ', msle(y_test, y_pred))

#plotting the results
plt.scatter(y_test, y_pred)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.show()





#generating the next 6 winning numbers
next_numbers = []
for i in range(0,6):
    next_numbers.append(rd.randint(1,60))
print('Next winning numbers: ', next_numbers)


#generating the next 6 winning numbers based on predictions
next_numbers = []
for i in range(0,6):
    next_numbers.append(rd.randint(1,60))
    while next_numbers[i] in next_numbers[:i]:
        next_numbers[i] = rd.randint(1,60)
print('Next winning numbers: ', next_numbers)