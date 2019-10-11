# Assessed exercises 3 
# Notice that there is not an 'Ans:' line in this week's template file.
# Instead, each question has an associated function, with input arguements 
# matching those sqecified in the question. Your functions will be test for a 
# range of different input values, against a model solution, to see if they 
# produce the same answers.
import math
import numpy as np


# Q1 Write a function that takes n, a and b as inputs. The function should
# create a 1D array containing the numbers 0,1,...,n-1 (n elements), multiple 
# every element by a, add b to the 1st element and return the result
def exercise1(n, a, b):
    array = np.arange(n)
    product = array * a
    return np.insert(product, 0, b)


# Q2 Write a function that takes n, m, a, b and val as inputs. The function
# should create a n x m matrix (2D array) of zeros, set the entry [a,b] equal
# to val and return this matrix as its output
def exercise2(n, m, a, b, val):
    matrix = np.zeros((n, m))
    matrix[a][b] = val
    return matrix


# Q3 Write a function that takes an array X, and the numbers a and b as inputs, 
# and returns all of the values in X that at greater than a and less than b.
def exercise3(X, a, b):
    return X[X > a][X[X > a] < b]


# Q4 Write a function that takes x as an input, converts x from degrees to 
# radians and calculates sin of the x in radians
def exercise4(x):
    x_radians = math.radians(x)
    return math.sin(x_radians)


if __name__ == '__main__':
    print(exercise1(10, 2, 7))
    print(exercise2(8, 9, 2, 4, 99))
    a = np.array(([9, 3, 2, 5, 7, 9, 3, 6, 9], [5, 7, 9, 4, 6, 8, 3, 1, 0]))
    print(exercise3(a, 3, 6))
    print(exercise4(30))
