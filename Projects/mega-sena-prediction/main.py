import random as rd  #importing random module
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression as lr
from sklearn.ensemble import RandomForestRegressor as rf
from sklearn import metrics

#read data from mega_sena.csv
df = pd.read_csv('mega_sena.csv')

#split each sequence into 6 integers rows
df['winning_numbers_1'] = df['winning_numbers'].str.split(' ').str[0].apply(pd.to_numeric)
df['winning_numbers_2'] = df['winning_numbers'].str.split(' ').str[1].apply(pd.to_numeric)
df['winning_numbers_3'] = df['winning_numbers'].str.split(' ').str[2].apply(pd.to_numeric)
df['winning_numbers_4'] = df['winning_numbers'].str.split(' ').str[3].apply(pd.to_numeric)
df['winning_numbers_5'] = df['winning_numbers'].str.split(' ').str[4].apply(pd.to_numeric)
df['winning_numbers_6'] = df['winning_numbers'].str.split(' ').str[5].apply(pd.to_numeric)

#drop the original winning_numbers column
df.drop(['winning_numbers'], axis=1, inplace=True)
# print(df.info())

sns.heatmap(df.corr(), annot=True, cmap='RdYlGn')
#plt.show()

#function to generate a random number between 1 and 1000
def random_number():
    return rd.randint(1,1000)

#function to generate a random number between 1 and 6
def random_number_6():
    return rd.randint(1,6)

win_num = f'winning_numbers_{random_number_6()}'

X = df.drop([win_num], axis=1)  
y = df[win_num]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=random_number())

#train the AI model
# regressor = lr()
# regressor.fit(X_train, y_train)
forest_regressor = rf()
forest_regressor.fit(X_train, y_train)

#test the AI models
# test_regressor_results = regressor.predict(X_test)
test_forest_results = forest_regressor.predict(X_test)

#test the regression model
# r2_lin = metrics.r2_score(y_test, test_regressor_results)
# rmse_lin = np.sqrt(metrics.mean_squared_error(y_test, test_regressor_results))
# print('R2 Score: ', r2_lin)
# print('RMSE: ', rmse_lin)

#test the forest model
# r2_fr = metrics.r2_score(y_test, test_forest_results)
# rmse_fr = np.sqrt(metrics.mean_squared_error(y_test, test_forest_results))
# print('R2 Score: ', r2_fr)
# print('RMSE: ', rmse_fr)

#configure graph
df_result = pd.DataFrame()
df_result[win_num] = y_test
# df_result['regressor_prediction'] = test_regressor_results
df_result['forest_prediction'] = test_forest_results
df_result = df_result.reset_index(drop=True)

#show graph
fig = plt.figure(figsize=(12,8))
sns.lineplot(data=df_result)
#plt.show()
# print(df_result)

def lottery_draw():
    # Generate 6 unique numbers between 1 and 60
    numbers = rd.sample(range(1, 61), 6)
    return sorted(numbers)

#print regular random 6 numbers
print("Random 6 numbers: ")
random_numbers = lottery_draw()
print(random_numbers)
#print the next 6 winning numbers from prediction)
print('Next 6 winning numbers: ')
six_num = sorted(df_result.tail(6)[win_num])
print(six_num)
# print(df_result.tail(6)['regressor_prediction'])
print('Forest prediction: ')
forest_num = sorted(df_result.tail(6)['forest_prediction'])
print(forest_num)
