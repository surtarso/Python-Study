
import pandas as pd
import numpy as np


#read data from mega_sena.csv
df = pd.read_csv('mega_sena.csv')

#split each row into 6 integers
df['winning_numbers'] = df['winning_numbers'].str.split(' ').apply(pd.to_numeric)

#create a dataframe with pandas and numpy
df = pd.DataFrame(np.array(df['winning_numbers']))

#transform sequence into array elements
df = df.values.reshape(-1,1)
print(df)