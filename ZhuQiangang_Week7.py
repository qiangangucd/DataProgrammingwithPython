# Assessed exercises 7
# Look at cuts and creating ROC curves

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy.random as npr

# This week we will use the ebola_test dataset to test the code. It contains the
# results for a new medical test for detecting Ebola that is much faster, though
# less accurate, than that currently available. The new test has been applied to 
# a number of patients who are known (from the old test) to have the disease or 
# not. The first column of the data set (called 'prob') is the probability under 
# the new test that the patient has Ebola. The second column ('ebola') is the 
# result from the older test which definitively says whether the patient has ebola 
# (ebola = 1) or not (ebola=0). Download the dataset, load it in and have a look
# at the first few entries to see what it looks like.
eb = pd.read_csv('ebola_test.csv')


# Q1 Write a function that returns a dict with some information about the
# DataFrame df. The keys of the dict should be 'Percentage' and 'Quartiles'. The 
# value for 'Percentage' should be a single number (not a list with a number in
# it), specifying the percentage of entries with positive results for the given
# criteria, i.e. indicator variable is 1. This value should be rounded to 1
# decimal place. The value for 'Quartiles' should be a list (not a Series or 
# array) with the number of observations in the 1st quartile (0-25%), 2nd 
# quartile (25-50%), 3rd quartile (50-75%) and 4th quartile (75-100%) for a
# specified observation column. 
# The name of the indicator and observation variable should be given to the 
# function as strings.
# Be sure that your keys are exactly as specified above and that the values have
# # the data type specified above.
def exercise1(df, ind_col, obs_col):
    index_ind_col = df.columns.get_loc(ind_col)
    index_obs_col = df.columns.get_loc(obs_col)
    Percentage = round((sum(df.iloc[:, index_ind_col]) / len(df)) * 100, 1)
    Quartiles = [sum(1 for i in range(len(df)) if
                     np.quantile(df.iloc[:, index_obs_col], 0) <= df.iloc[i, index_obs_col] <= np.quantile(
                         df.iloc[:, index_obs_col], 0.25))]
    Quartiles.append(sum(1 for i in range(len(df)) if
                         np.quantile(df.iloc[:, index_obs_col], 0.25) < df.iloc[i, index_obs_col] <= np.quantile(
                             df.iloc[:, index_obs_col], 0.5)))
    Quartiles.append(sum(1 for i in range(len(df)) if
                         np.quantile(df.iloc[:, index_obs_col], 0.5) < df.iloc[i, index_obs_col] <= np.quantile(
                             df.iloc[:, index_obs_col], 0.75)))
    Quartiles.append(sum(1 for i in range(len(df)) if
                         np.quantile(df.iloc[:, index_obs_col], 0.75) < df.iloc[i, index_obs_col] <= np.quantile(
                             df.iloc[:, index_obs_col], 1)))
    return {'Percentage': Percentage, 'Quartiles': Quartiles}


# Suggested test
exercise1(eb, 'ebola', 'prob')


# This should return
# {'Percentage': 10.4, 'Quartiles': [128, 125, 125, 121]}
# in this exact form. If it does not your function is not correct.


# In classification problems one must define a cutoff, a value for which
# observations above that value are classified as positive results (and assigned
# the value 1), and those less than or equal to the value are classified as 
# negative results (and assigned the value 0). If we had a perfect classifier,
# the predicted values (0s or 1s) would match the indicator variable. A false 
# positive is defined as the classifier predicting a positive result (1), when
# the actual result was negative (0). A false negative is the opposite, the 
# classifier predicts a negative result (0), when the true result was positive (1).

# Q2 Write a function that takes a DataFrame, two strings specifying the names of 
# indicator column and the observation column, and a cutoff value, and
# returns the rate of false positive and rate of the false negative as a dict.
# The keys of the dict should be 'False Pos' and 'False Neg' and the values 
# must be rounded to 3 decimal places. 
def exercise2(df, ind_col, obs_col, cutoff):
    index_ind_col = df.columns.get_loc(ind_col)
    index_obs_col = df.columns.get_loc(obs_col)
    df['prediction'] = (df.iloc[:, index_obs_col] > cutoff).astype(int)
    false_pos = 0
    false_neg = 0
    for i in range(len(df)):
        if df.loc[i, 'prediction'] == 1 and df.iloc[i, index_ind_col] == 0:
            false_pos += 1
        if df.loc[i, 'prediction'] == 0 and df.iloc[i, index_ind_col] == 1:
            false_neg += 1
    return {'False Pos': round(false_pos / len(df), 3), 'False Neg': round(false_neg / len(df), 3)}


# Suggested test
exercise2(eb, 'ebola', 'prob', 0.15)


# This should return
# {'False Pos': 0.126, 'False Neg': 0.07}
# in this exact form. If it does not your function is not correct.    

# We do not know a priori what the best cutoff value is, as such, we should 
# loop over a range of cutoffs to decide on the best one. 

# Q3 Write a function that takes the same inputs as Q2, but cutoff will now be
# replaced with cutoff_list (an array of different cutoff values to test). The 
# function should run the classification for each value in cutoff_list and 
# determine which is the best cutoff value. We will define the best classifier 
# as having the lowest false results (false positives plus false negatives). The 
# function should return a dict with the keys 'Cutoff value', 'False Pos' and 
# 'False Neg', and the values of the false positive rate and false negative rate 
# should be rounded to 3 decimal places
def exercise3(df, ind_col, obs_col, cutoff_list):
    index_ind_col = df.columns.get_loc(ind_col)
    index_obs_col = df.columns.get_loc(obs_col)
    smallest = len(df)
    best_cutoff = min(cutoff_list)
    for cutoff in cutoff_list:
        df['prediction'] = (df.iloc[:, index_obs_col] > cutoff).astype(int)
        df['diff'] = np.abs(df['prediction'] - df[ind_col])
        if sum(df['diff']) < smallest:
            smallest = sum(df['diff'])
            best_cutoff = cutoff
    df['prediction'] = (df.iloc[:, index_obs_col] > best_cutoff).astype(int)
    false_pos = 0
    false_neg = 0
    for i in range(len(df)):
        if df.loc[i, 'prediction'] == 1 and df.iloc[i, index_ind_col] == 0:
            false_pos += 1
        if df.loc[i, 'prediction'] == 0 and df.iloc[i, index_ind_col] == 1:
            false_neg += 1
    return {'Cutoff value': best_cutoff, 'False Pos': round(false_pos / len(df), 3),
            'False Neg': round(false_neg / len(df), 3)}


# Suggested test
exercise3(eb, 'ebola', 'prob', np.arange(0, 1, 0.01))


# This should return
# {'Cutoff value': 0.21, 'False Pos': 0.0, 'False Neg': 0.102}
# in this exact form. If it does not your function is not correct.

# A related concept to the choice of cut-offs is the Receiver Operator Characteristic
# (ROC) curve. The ROC curve aims to quantify how well a classifier beats a random
# classifier for any level of probability cut-off. An introduction can be found here:
# http://en.wikipedia.org/wiki/Receiver_operating_characteristic
# The idea is to plot the false positive rate against the true positive rate for
# every possible cut-off

# Q4 Write a function which calculates the ROC curve. The function should have
# three arguments, the DataFrame df, the name of the indicator variable ind_col
# and the name of the observation variable obs_col
# Your ROC curve function should perform the following steps
# 1) Find the unique values in the observation column
# 2) Use each of these unique values as a cutoff value and
# a) Classify all the obs as either positive or negative based on the current cutoff value
# b) Calculate the number of true positives (tp), true negatives (tn), false positives (fp) and false negatives (fn)
# Note 1: a tp is when the classification value and actual value are both 1, a tn is when they're both 0
# Note 2: tp, fn, etc must all be vectors/Series of the same length as the vector/Series of cutoff values
# Note 4: be careful when you're at the maximum cutoff value that you can still calculate these values correctly
# 3) Create the true positive rate (tpr) as tp/(tp+fn)
# 4) Create the false positive rate (fpr) as fp/(fp+tn)
# 5) Create a DataFrame, indexed by the cutoff values (unique values of
# observation column), with columns 'True_Pos' and 'False_Pos', containing tpr
# and fpr, respectively.
# 6) Return the DataFrame sorted by index (lowest to highest)

def exercise4(df, ind_col, obs_col):
    uni_obs = np.unique(df[obs_col])
    d = {}
    index = []
    tpr = []
    fpr = []
    for cutoff in uni_obs:
        df['prediction'] = (df.loc[:, obs_col] > cutoff).astype(int)
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        d[cutoff] = {}
        for i in range(len(df)):
            if df.loc[i, 'prediction'] == 1 and df.loc[i, ind_col] == 0:
                fp += 1
            if df.loc[i, 'prediction'] == 0 and df.loc[i, ind_col] == 1:
                fn += 1
            if df.loc[i, 'prediction'] == 0 and df.loc[i, ind_col] == 0:
                tn += 1
            if df.loc[i, 'prediction'] == 1 and df.loc[i, ind_col] == 1:
                tp += 1
        tpr_ = tp / (tp + fn)
        fpr_ = fp / (fp + tn)
        index.append(cutoff)
        tpr.append(tpr_)
        fpr.append(fpr_)
    df_roc = pd.DataFrame({'True_Pos': tpr, 'False_Pos': fpr}, index=index).sort_index(axis=0)
    return df_roc


# Suggested test
Q4_ans = exercise4(eb, 'ebola', 'prob')
Q4_ans.plot(x='False_Pos', y='True_Pos')
plt.show()
# This should create a plot of the false positive rate vs true positive rate.
# When the false positive rate is ~0.5, the true positive rate is ~0.85
