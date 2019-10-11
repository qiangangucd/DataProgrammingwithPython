# Week 1 - Assessed Exercises
# Fill in the following Python script and submit it on Brightspace.
# An empty line between the question and 'Ans:' implies that you will need to 
# write a piece of code to get the answer.
import pandas as pd

# Import Heart Disease UCI data set and call is heart
heart = pd.read_csv('heart.csv')

# Q1 (a) How many rows and columns there are in the Heart Disease UCI data set?
num_rows = heart.shape[0]
num_columns = heart.shape[1]
print('num_rows={}, num_columns={}'.format(num_rows, num_columns))
# Ans: This data set has _303_ rows and _14_ columns

# Q1 (b) What sex is the 3rd person in the data set, i.e. on the third row?
sex_third = heart.sex[2]
if sex_third == 0:
    print('sex_third:', 'female')
else:
    print('sex_third:', 'male')
# Ans: female

# Compute the table of different chest pain types. 

# Q2 How many people have type 3 chest pain?
num_cp = heart.cp.value_counts()
print(num_cp)
# Ans: 23

# Q3 (a) What age is the youngest person in this dataset? 
mix_age = heart.age.min()
print('mix_age:', mix_age)
# Ans:29

# Q3 (b) What age is the oldest person in this dataset? 
max_age = heart.age.max()
print('max_age:', max_age)
# Ans:77

# Look up what the cut function (pd.cut) does and use it to create a new 
# variable which is age grouped into 20-30, 30-40, 40-50, 50-60, 60-70, 70-80. 
# heart['age_groups'] =

# Q4 How many people are in the group (50,60)? 
heart['age_groups'] = pd.cut(heart['age'], [20, 30, 40, 50, 60, 70, 80])
num_group = heart['age_groups'].value_counts()
print(num_group)
# Ans:129