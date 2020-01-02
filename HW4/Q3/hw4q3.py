## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to detect eye state

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA

######################################### Reading and Splitting the Data ###############################################
# XXX
# TODO: Read in all the data. Replace the 'xxx' with the path to the data set.
# XXX
data = pd.read_csv('eeg_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the parameter 'shuffle' set to true and the 'random_state' set to 100.
# XXX
x_train, x_test, y_train, y_test = train_test_split(
        x_data, y_data, test_size=0.3, random_state=100)

# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
# XXX
LR_classifier = LinearRegression().fit(x_train, y_train)

# XXX
# TODO: Test its accuracy (on the training set) using the accuracy_score method.
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Round the output values greater than or equal to 0.5 to 1 and those less than 0.5 to 0. You can use y_predict.round() or any other method.
# XXX
y_train_pre = LR_classifier.predict(x_train).round()
y_test_pre = LR_classifier.predict(x_test).round()
train_accuracy = accuracy_score(y_train, y_train_pre)
test_accuracy = accuracy_score(y_test, y_test_pre)
print("LR train: ", round(train_accuracy,2))
print("LR test: ", round(test_accuracy,2))

# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
# XXX
RF_classifier = RandomForestClassifier().fit(x_train,y_train)

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
y_train_pre = RF_classifier.predict(x_train).round()
y_test_pre = RF_classifier.predict(x_test).round()
train_accuracy = accuracy_score(y_train, y_train_pre)
test_accuracy = accuracy_score(y_test, y_test_pre)
print("RF train: ", round(train_accuracy,2))
print("RF test: ", round(test_accuracy,2))

# XXX
# TODO: Determine the feature importance as evaluated by the Random Forest Classifier.
#       Sort them in the descending order and print the feature numbers. The report the most important and the least important feature.
#       Mention the features with the exact names, e.g. X11, X1, etc.
#       Hint: There is a direct function available in sklearn to achieve this. Also checkout argsort() function in Python.
# XXX
features = RF_classifier.feature_importances_
#print(features)
columns_sorted = np.argsort(features)
columns_sorted = np.flip(columns_sorted)
for i in columns_sorted:
    print('X'+str(i+1))

# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
parameters = {'n_estimators':list(range(15,19)), 'max_depth':list(range(25,29))}
RF_tuning = GridSearchCV(RandomForestClassifier(), parameters, cv=10)
RF_tuning.fit(x_train,y_train)
mean_test_score = RF_tuning.cv_results_['mean_test_score']
mean_fit_time = RF_tuning.cv_results_['mean_fit_time']
used_params = RF_tuning.cv_results_['params']
for score, time,  param in zip(mean_test_score, mean_fit_time, used_params):
    print("score: %0.2f,time: %0.2f for %r " %(score, time, param))

y_tuning = RF_tuning.predict(x_test).round()
test_accuracy = accuracy_score(y_test, y_tuning)
print("RF tuning test: ", round(test_accuracy,2))

# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Pre-process the data to standardize or normalize it, otherwise the grid search will take much longer
# TODO: Create a SVC classifier and train it.
# XXX
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
SVC_classifier = SVC().fit(x_train_scaled,y_train)

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
y_train_pre = SVC_classifier.predict(x_train).round()
y_test_pre = SVC_classifier.predict(x_test).round()
train_accuracy = accuracy_score(y_train, y_train_pre)
test_accuracy = accuracy_score(y_test, y_test_pre)
print("SVC train: ", train_accuracy.round(2))
print("SVC test: ", test_accuracy.round(2))

# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
parameters = {'kernel':['rbf','linear'], 'C':[0.001*(10**i)  for i in range(1,4)] }
SVC_tuning = GridSearchCV(SVC(), parameters, cv=10)
SVC_tuning.fit(x_train_scaled,y_train)
mean_test_score = SVC_tuning.cv_results_['mean_test_score']
mean_train_score = SVC_tuning.cv_results_['mean_train_score']
mean_fit_time = SVC_tuning.cv_results_['mean_fit_time']
used_params = SVC_tuning.cv_results_['params']
for testscore, trainscore, time,  param in zip(mean_test_score, mean_train_score, mean_fit_time, used_params):
    print("test score: %0.2f,train score: %0.2f, time: %0.2f for %r " %(testscore, trainscore, time, param))

y_tuning = SVC_tuning.predict(x_test).round()
test_accuracy = accuracy_score(y_test, y_tuning)
print("SCV tuning test: ", round(test_accuracy,2))

# ######################################### Principal Component Analysis #################################################
# XXX
# TODO: Perform dimensionality reduction of the data using PCA.
#       Set parameters n_component to 10 and svd_solver to 'full'. Keep other parameters at their default value.
#       Print the following arrays:
#       - Percentage of variance explained by each of the selected components
#       - The singular values corresponding to each of the selected components.
# XXX
pca = PCA(n_components=10,svd_solver='full')
pca.fit_transform(x_data)
variance = pca.explained_variance_ratio_
print("percentage of varianace explained ")
print(variance)
print("singular values")
print(pca.singular_values_)