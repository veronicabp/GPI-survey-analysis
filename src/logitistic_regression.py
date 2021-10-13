from respondents_treatments import respondents, results, treatment_description, convert_number_to_response
import pandas as pd
import numpy as np 
from sklearn.preprocessing import OneHotEncoder
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression

####################################################
# Logistic Regression 
###################################################

# Currently running one question at a time, ideal to do all at once 
independent_vars = ['age', 'income', 'education', 'ethnicity', 'party', 'political_involvement']
dependent_var = 'Q1'
x_data = []
y_data = []
for respondent in respondents:
    x = []
    for x_var in independent_vars:
        x.append(getattr(respondent,x_var))
    x_data.append(x)
    y_data.append(convert_number_to_response(respondent.responses[dependent_var]))

#Requires a variable encoder for categorical independent variables 
df = pd.DataFrame(x_data, columns = independent_vars)
def categorical_variable_splitter(df, var):
    onehotencoder = OneHotEncoder()
    X = onehotencoder.fit_transform(df[var].values.reshape(-1,1)).toarray()
    dfOneHot = pd.DataFrame(X, columns = [var + "_" + str(int(i)) for i in range(len(df[var].unique()))])
    df = pd.concat([df, dfOneHot], axis=1)
    df = df.drop([var], axis=1)
    return df

for var in independent_vars:
    df = categorical_variable_splitter(df, var)
   
log_reg = LogisticRegression(solver='lbfgs', multi_class = 'multinomial')
log_reg.fit(df, y_data)
coef_dict = {}
for coef, feat in zip(log_reg.coef_[0,:], independent_vars):
    coef_dict[feat] = coef

data = sm.add_constant(df, prepend = False)
mnLogit_mod = sm.MNLogit(y_data, data.astype(float))
mnlogit_fit = mnLogit_mod.fit()

print(coef_dict)
print(mnlogit_fit.summary())