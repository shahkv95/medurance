# -*- coding: utf-8 -*-

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

"""The insurance.csv dataset contains 1300+ observations (rows) and 7 features (columns). The dataset contains 4 numerical features (age, bmi, number_of_children, expenses) and 3 nominal features (gender/sex, is_a_smoker_or_not and region) that were converted into factors with numerical value desginated for each level.

The purposes of this project to look into different features to observe their relationship, and plot a multiple linear regression based on several features of individual such as age, physical/family condition and location against their existing medical expense to be used for predicting future medical expenses of individuals that help health insurers to make decision on charging the premium.
"""

filename = 'https://raw.githubusercontent.com/shahkv95/Datasets/master/insurance.csv'

df = pd.read_csv(filename)
df.head()

df.rename(columns = {'expenses':'charges'}, inplace = True)

df.head()

df.shape

# Checking the data type of each feature
df.info()

# Generate descriptive statistics that summarize the central tendency, dispersion and shape of a dataset’s distribution, excluding NaN values.
df.describe()

# Compute pairwise correlation of columns, excluding NA/null values.
corr = df.corr()
corr

# Calculating total number of null values, if exists, for each feature
df.isnull().sum()

# Visualizing the correlation of numerical features with each other 
# From the below heatmap, we can observe that age is highly correlated with charges compared to the other features
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot = True)

# The below piechart depicts that the data of the people is uniformly distributed over all the four regions. So the region feature can be dropped. 
df.region.value_counts().plot(kind="pie")

# The below piechart depicts that almost 75% of the people are non-smoker compared to the remaining one-forth of the people
df.smoker.value_counts().plot(kind="pie")

# The tabular data shows the mean and median of the charges that the people are paying as premium group by category of smokers
df.groupby("smoker").charges.agg(["mean","median","count"])

# The tabular data shows the mean and median of the charges that the people are paying as premium group by category of gender
df.groupby("sex").charges.agg(["mean","median","count"])

""" 
Scatter plots allow you to map various data attributes to graphical properties of the plot.
The dots in a scatter plot not only report the values of individual data points, but also patterns when the data are taken as a whole.
"""
def scatterplot_with_common_y_axis_feature(x1 = 'age', x2 = 'children', x3 = 'bmi', y_common = 'charges'):
  fig, axes = plt.subplots(ncols = 3, figsize = (15,6), squeeze=True)
  plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.4, hspace=None)
  df.plot(kind='scatter', x=x1, y=y_common, ax=axes[0], color = "orange")
  df.plot(kind='scatter', x=x2, y=y_common, ax=axes[1], color = "green")
  df.plot(kind='scatter', x=x3, y=y_common, ax=axes[2], color = "blue")
scatterplot_with_common_y_axis_feature('age', 'children', 'bmi', 'charges')

"""
Draw one histogram of the DataFrame’s columns.

A histogram is a representation of the distribution of data. This function groups the values of all given Series in the DataFrame into bins and draws all bins in one 
matplotlib.axes.Axes. This is useful when the DataFrame’s Series are in a similar scale.
"""

def histogram_with_feature_and_frequency():

  fig, axes = plt.subplots(nrows = 2, ncols = 2, figsize = (15,10))
  df.plot(kind='hist', y='age', ax=axes[0][0], color = 'blue', bins = 10)
  df.plot(kind='hist', y='bmi', ax=axes[0][1], color = 'orange', bins = 54)
  df.plot(kind='hist', y='children', ax=axes[1][0], color = 'red', bins = 5)
  df.plot(kind='hist', y='charges', ax=axes[1][1], color = 'green', bins = 80)

histogram_with_feature_and_frequency()

""" 
Scatter plots allow you to map various data attributes to graphical properties of the plot.
The dots in a scatter plot not only report the values of individual data points, but also patterns when the data are taken as a whole.
"""
def scatterplot_with_three_dimensions(x = 'bmi', y = 'charges', z1 = 'sex', z2 = 'smoker', z3 = 'region'):
  palette=['#EB5050','#3EA2FF']
  fig, axes = plt.subplots(ncols = 3, figsize = (24,6), squeeze=True)
  sns.scatterplot(x=x, y=y, ax=axes[0], data=df,hue=z1, palette=palette)
  sns.scatterplot(x=x, y=y, ax=axes[1], data=df,hue=z2, palette=palette)
  sns.scatterplot(x=x, y=y, ax=axes[2], data=df,hue=z3)
scatterplot_with_three_dimensions(x = 'bmi', y = 'charges', z1 = 'sex', z2 = 'smoker', z3 = 'region')

"""
Show point estimates and confidence intervals as rectangular bars.

A bar plot represents an estimate of central tendency for a numeric variable with the height of each rectangle and provides some indication of the uncertainty around that estimate 
using error bars. Bar plots include 0 in the quantitative axis range, and they are a good choice when 0 is a meaningful value for the quantitative variable, and you want to make 
comparisons against it.
"""
def barplot_with_feature_counts(x1 = 'sex', x2 = 'region', x3 = 'smoker'):

  fig, axes = plt.subplots(ncols=3, figsize = (15,6))
  df[x1].value_counts().plot(kind='bar', color = 'orange', ax=axes[0],title=str(x1), legend = x1) 
  df[x2].value_counts().plot(kind='bar', color = 'green', ax=axes[1],title=str(x2), legend = x2)
  df[x3].value_counts().plot(kind='bar', color = 'blue', ax=axes[2],title=str(x3), legend = x3)
  
barplot_with_feature_counts('sex', 'region', 'smoker')

"""
Figure-level interface for drawing categorical plots onto a FacetGrid.

This function provides access to several axes-level functions that show the relationship between a numerical and one or more categorical variables using one of several visual 
representations.
"""
palette=['orange','green'] 
sns.catplot(x='sex', y='charges', kind='violin', palette=palette, data=df)

"""
catplot interpretation - analogous to box plot 
median (a white dot on the violin plot)
interquartile range (the black bar in the center of violin)
the lower/upper adjacent values (the black lines stretched from the bar) — defined as first quartile — 1.5 IQR and third quartile + 1.5 IQR respectively. 
These values can be used in a simple outlier detection technique (Tukey’s fences) — observations lying outside of these “fences” can be considered outliers.
"""
sns.catplot(x='sex', y='charges', kind='violin', hue='smoker', palette=palette, data=df)

"""
A distplot plots a univariate distribution of observations. The distplot() function combines the matplotlib hist function with the seaborn kdeplot() and rugplot() functions.
"""
def distplot_for_features(x = 'charges'):
  from scipy import stats
  from scipy.stats import norm
  fig =plt.figure(figsize=(18,6))
  plt.subplot(1,2,1)
  sns.distplot(df[x], fit=norm, color="green")
  (mu,sigma)= norm.fit(df[x])
  plt.legend(['For Normal dist. mean: {:.2f} | std: {:.2f}'.format(mu,sigma)])
  plt.ylabel('Frequency')
  plt.title('Distribution of Charges')
distplot_for_features('charges')

"""
Plot pairwise relationships in a dataset.

By default, this function will create a grid of Axes such that each numeric variable in data will by shared across the y-axes across a single row and the x-axes across a 
single column. The diagonal plots are treated differently: a univariate distribution plot is drawn to show the marginal distribution of the data in each column.
"""
def pairplot():
  palette=['#EB5050','#2DFFAB'] 
  sns.set(style="ticks")
  sns.pairplot(data=df, hue='smoker', palette=palette)
pairplot()

df.head()

df.drop(["region"], axis=1, inplace=True) 
df.head()

# Changing binary categories to 1s and 0s
df['sex'] = df['sex'].map(lambda s :1  if s == 'female' else 0)
df['smoker'] = df['smoker'].map(lambda s :1  if s == 'yes' else 0)

df.head()

X = df.drop(['charges'], axis = 1)
y = df.charges
print('Shape of X: ', X.shape)
print('Shape of y: ', y.shape)

"""
Ordinary least squares Linear Regression

Fits a linear model with coefficients w = (w1, …, wp) to minimize the residual sum of squares between the observed targets in the dataset, 
and the targets predicted by the linear approximation.

predict(X) used for predicting the output using the linear model.

score(X) 
Return the coefficient of determination of the prediction.

The coefficient of determination R^2 is defined as (1 - (u/v)), 
where u is the residual sum of squares ((y_true - y_pred)** 2).sum() 
and v is the total sum of squares ((y_true - y_true.mean()) ** 2).sum(). 
The best possible score is 1.0 and it can be negative (because the model can be arbitrarily worse).
"""
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)
lr = LinearRegression().fit(X_train, y_train)

y_train_pred = lr.predict(X_train)
y_test_pred = lr.predict(X_test)

print(lr.score(X_test, y_test))

results = pd.DataFrame({'Actual': y_test, 'Predicted': y_test_pred})
results

"""
Standardize features by removing the mean and scaling to unit variance.

The standard score of a sample x is calculated as: 
z = (x - u) / s
where u is the mean of the training samples or zero if with_mean=False, and s is the standard deviation of the training samples or one if with_std=False.

fit(X[, y, sample_weight]) - Compute the mean and std to be used for later scaling.
fit_transform(X[, y]) - Fit to data, then transform it.

"""
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

pd.DataFrame(X_train).head()

pd.DataFrame(y_train).head()

from math import sqrt 
from sklearn.model_selection import cross_val_predict  
from sklearn.metrics import r2_score, mean_squared_error

def model_summary(model, model_name, cvn=20): # Default value for cvn = 20
    print(model_name)
    y_pred_model_train = model.predict(X_train)
    y_pred_model_test = model.predict(X_test)
    accuracy_model_train = r2_score(y_train, y_pred_model_train)
    print("Training Accuracy: ", accuracy_model_train)
    accuracy_model_test = r2_score(y_test, y_pred_model_test)
    print("Testing Accuracy: ", accuracy_model_test)
    RMSE_model_train = sqrt(mean_squared_error(y_train, y_pred_model_train))
    print("RMSE for Training Data: ", RMSE_model_train)
    RMSE_model_test = sqrt(mean_squared_error(y_test, y_pred_model_test))
    print("RMSE for Testing Data: ", RMSE_model_test)
#     if model == polynomial_reg:
#         polynomial_features = PolynomialFeatures(degree=3)
#         y_pred_cv_PR = cross_val_predict(model, polynomial_features.fit_transform(X), y, cv=20)
#     else:
    y_pred_cv_model = cross_val_predict(model, X, y, cv=cvn)
    accuracy_cv_model = r2_score(y, y_pred_cv_model)
    print("Accuracy for", cvn,"- Fold Cross Predicted: ", accuracy_cv_model)

from sklearn.linear_model import LinearRegression  

multiple_linear_reg = LinearRegression(fit_intercept=False)  
multiple_linear_reg.fit(X_train, y_train)  
model_summary(multiple_linear_reg, "Multiple_linear_Regression")

"""
Epsilon-Support Vector Regression.

The free parameters in the model are C and epsilon.
The implementation is based on libsvm. 
The fit time complexity is more than quadratic with the number of samples which makes it hard to scale to datasets with more than a couple of 10000 samples.
"""
from sklearn.svm import SVR  

support_vector_reg = SVR(gamma="auto", kernel="linear", C=1000)  
support_vector_reg.fit(X_train, y_train)  
model_summary(support_vector_reg, "Support_Vector_Regressor")

"""
Generate polynomial and interaction features.

Generate a new feature matrix consisting of all polynomial combinations of the features with degree less than or equal to the specified degree. 
"""

from sklearn.preprocessing import PolynomialFeatures

polynomial_features = PolynomialFeatures(degree=3)  
x_train_poly = polynomial_features.fit_transform(X_train)  
x_test_poly = polynomial_features.fit_transform(X_test) 

polynomial_reg = LinearRegression(fit_intercept=False)  
polynomial_reg.fit(x_train_poly, y_train)  
print("PolynomialFeatures")
y_pred_PR_train = polynomial_reg.predict(x_train_poly)
y_pred_PR_test = polynomial_reg.predict(x_test_poly)
accuracy_PR_train = r2_score(y_train, y_pred_PR_train)
print("Training Accuracy: ", accuracy_PR_train)
accuracy_PR_test = r2_score(y_test, y_pred_PR_test)
print("Testing Accuracy: ", accuracy_PR_test)
RMSE_PR_train = sqrt(mean_squared_error(y_train, y_pred_PR_train))
print("RMSE for Training Data: ", RMSE_PR_train)
RMSE_PR_test = sqrt(mean_squared_error(y_test, y_pred_PR_test))
print("RMSE for Testing Data: ", RMSE_PR_test)
y_pred_cv_PR = cross_val_predict(polynomial_reg, polynomial_features.fit_transform(X), y, cv=20)
accuracy_cv_PR = r2_score(y, y_pred_cv_PR)
print("Accuracy for 20-Fold Cross Predicted: ", accuracy_cv_PR)

"""
Decision tree regression observes features of an object and trains a model in the structure of a tree to predict data in the future to produce meaningful continuous output. 
Continuous output means that the output/result is not discrete, i.e., it is not represented just by a discrete, known set of numbers or values.
"""

from sklearn.tree import DecisionTreeRegressor

decision_tree_reg = DecisionTreeRegressor(max_depth=5, random_state=13)  
decision_tree_reg.fit(X_train, y_train) 
model_summary(decision_tree_reg, "Decision_Tree_Regression")

"""
Plot a decision tree.

The sample counts that are shown are weighted with any sample_weights that might be present.
The visualization is fit automatically to the size of the axis. Use the figsize or dpi arguments of plt.figure to control the size of the rendering.
"""
import sklearn
from sklearn import tree
fig, ax = plt.subplots(figsize=(10, 10))
sklearn.tree.plot_tree(decision_tree_reg)

"""
Random forest regressor

A random forest is a meta estimator that fits a number of classifying decision trees on various sub-samples of the dataset and uses averaging to improve the predictive accuracy 
and control over-fitting. The sub-sample size is controlled with the max_samples parameter if bootstrap=True (default), otherwise the whole dataset is used to build each tree.
"""

from sklearn.ensemble import RandomForestRegressor  

random_forest_reg = RandomForestRegressor(n_estimators=400, max_depth=5, random_state=13)  
random_forest_reg.fit(X_train, y_train) 
model_summary(random_forest_reg, "Random_Forest_Regression")

"""**The model with the highest accuracy is Random Forest compared to other models.**"""

# input_data = {'age': [35],
#               'sex': ['male'],
#               'bmi': [26],
#               'children': [0],
#               'smoker': ['no'],
#               'region': ['southeast']}

# input_data = pd.DataFrame(input_data)
# input_data

# # Scale our input data  
# input_data = sc.transform(input_data)
# input_data

# # Reshape our input data in the format required by sklearn models
# input_data = input_data.reshape(1, -1)
# print(input_data.shape)
# input_data

# # Get our predicted insurance rate for our new customer
# model_rfr.predict(input_data)

# # Note Standard Scaler remembers your inputs so you can use it still here
# print(sc.mean_)
# print(sc.scale_)
