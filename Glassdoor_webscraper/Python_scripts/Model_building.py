# Credit to Ken Jee for the follow along: https://youtu.be/7O4dpR9QMIM
# Generated 6/22/22 by Mark A. Farrugia

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pip
from sklearn.model_selection import train_test_split

path = r"C:\Users\Tineash\Projects\Glassdoor_webscraper\Data\DA_data_cleaned_2.csv"
df = pd.read_csv(path)

df.columns

df_model = df[['Rating', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue', 'Salary Average', 'City', 'State', 'Company Age (years)']]

#set up dummy columns (drastically increases col #)
df_dummy = pd.get_dummies(df_model)
df_dummy.head()
df_dummy_dropped = df_dummy.dropna()

#split data into test and train data
#define indep and dep variables
X = df_dummy.drop('Salary Average', axis=1) # get rid of the variable we wish to predict where axis=1 is column to search

X.columns
y = df_dummy["Salary Average"].values # values produces an array, not a series
y

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)

#multiple linear regression
import statsmodels.api as sm

X_sm = X = sm.add_constant(X) # this puts in a constant column to act as a y-intercept

model= sm.OLS(y_dropped,X_sm_dropped, missing='drop') # https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html
OLS_model = model.fit().summary()
OLS_model

#lasso regression
# random forest
# tune models using GridSearchCV
#test