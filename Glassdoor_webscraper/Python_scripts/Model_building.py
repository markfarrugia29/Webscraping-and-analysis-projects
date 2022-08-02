# Credit to Ken Jee for the follow along: https://youtu.be/7O4dpR9QMIM
# Generated 6/22/22 by Mark A. Farrugia

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pip
from sklearn.model_selection import train_test_split

pd.set_option('display.max_rows', 1000)

path = r"C:\Users\Tineash\Projects\Glassdoor_webscraper\Data\DA_data_cleaned_2.csv"
df = pd.read_csv(path)

df.columns

df_model = df[['Rating', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue', 'Salary Average', 'City', 'State', 'Company Age (years)']]

#set up dummy columns (drastically increases col #)
df_dummy = pd.get_dummies(df_model)
df_dummy['Salary Average']
#split data into test and train data
#define indep and dep variables

X = df_dummy.drop('Salary Average', axis=1) # get rid of the variable we wish to predict where axis=1 is column to search
y = df_dummy["Salary Average"] # values produces an array, not a series


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42,stratify=y)

#multiple linear regression
import statsmodels.api as sm

X_sm = X = sm.add_constant(X) # this puts in a constant column to act as a y-intercept
X_train.head()
model= sm.OLS(y,X_sm) # https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html
OLS_model = model.fit().summary()
OLS_model

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score as cv #sample model and compare to test set to see if it generalizes fine


sk_lr = LinearRegression().fit(X_train, y_train)
np.mean(cv(sk_lr,X_train,y_train, scoring='neg_mean_absolute_error',cv=5)) #https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html

#lasso regression - apply an alpha smoother to the LR
sk_lr_l = Lasso(alpha=0.78)
sk_lr_l.fit(X_train,y_train)
np.mean(cv(sk_lr_l,X_train,y_train, scoring='neg_mean_absolute_error',cv=5)) #https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html

alpha = []
error = []

for i in range(1,100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cv(lml,X_train,y_train,scoring='neg_mean_absolute_error',cv=5)))

plt.plot(alpha, error)
plt.show()

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err,columns = ['alpha','error'])
df_err[df_err.error == max(df_err.error)] # find value where alpha is at max error
# random forest - tree based decision process (multicolinearity nulled)
from sklearn.ensemble import RandomForestRegressor as RFR

rf = RFR()

np.mean(cv(rf,X_train,y_train,scoring='neg_mean_absolute_error',cv=5))


# tune models using GridSearchCV
#GridSearchCV runs all the models and spits out the most accurate one
from sklearn.model_selection import GridSearchCV

parameters = {'n_estimators':(range(10,300,10)),'criterion':('squared_error','absolute_error'), 'max_features':(1.0,'sqrt','log2')} #n_estimators is number of decision trees in the model 

gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=5)
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_

#test models on the test data
tpred_lm=sk_lr.predict(X_test)
tpred_lml=sk_lr_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error as mae
mae(y_test,tpred_lm)
mae(y_test,tpred_lml)
mae(y_test,tpred_rf)

#could explore combining models and applying weights to them to see how they affect things