# -*- coding: utf-8 -*-
# Week 1 - Assessed exercises
import math
# Q1 Write a for loop to compute the sum of x^2 for x from 0 to 8. What is the
# value of this sum?
sum = 0
for i in range(0, 9):
    sum += i
print('sum=', sum)


# Ans:36

# Q2 Define a function (addition) that returns the sum of two numbers x and y.
# Use the function to calculate 2.09 + 8.73


def addition(x, y):
    return x + y


print('2.09+8.73=', addition(2.09, 8.73))

# Ans: 10.82

# Q3 Find the 3 errors in the code below. The function sin_estimate should
# calculate an estimate of the sine function at the value 'x', with an error
# tolerance of 'tol'. After finding the 3 errors and fixing the code, the
# variable y should equal 0.09983341666666667

def sin_estimate(x, tol=10 ** -10):
    sin_est = 0
    i = 0
    error = abs(sin_est - math.sin(x))
    while error > tol and i < 50:
        sin_est += ((-1) ** i) * (x ** (2 * i + 1)) / math.factorial(2 * i + 1)
        error = abs(sin_est - math.sin(x))
        i += 1
    return sin_est


y = sin_estimate(0.1)
print(y)


# Ans: Error 1 = One colon is missing, Error 2 = 'i+=3' should be fixed with 'i+=1", Error 3 = No return value

# Q4 A bakery sells cupcakes, cookies and pastries. A cupcake costs €1.50, a
# cookie costs €1.00 and a pastry costs €0.80. However, the bakery offers
# discounts if you buy multiple items. If you buy 4-8 cupcakes they cost €1.20
# each, and if you buy more then 8 they are €1.00 each. If you buy 5 or more
# cookies they are €0.80. If you buy more than 3 pastries they are reduced to
# €0.65 each, and reduced further to €0.50 if you buy 10 or more.
# Create a set of nested if/elif/else statements to determine the price of each
# item based on the amount the customer requests and then computes the total
# cost of the order.
# Pay attention to the phrasing "more than n", "n or more" one includes the
# value 'n' and the other does not.
# Use your code to determine the total cost of 8 cupcakes, 4 cookies and 12
# pastries.
def total_cost(num_cupcakes, num_cookies, num_pastries):
    cost = 0
    if 4 <= num_cupcakes <= 8:
        cost += 1.2 * num_cupcakes
    elif num_cupcakes > 8:
        cost += num_cupcakes
    else:
        cost += 1.5 * num_cupcakes
    if num_cookies >= 5:
        cost += num_cookies * 0.8
    else:
        cost += num_cookies
    if 3 < num_pastries < 10:
        cost += num_pastries * 0.65
    elif num_pastries >= 10:
        cost += num_pastries * 0.5
    else:
        cost += 0.8 * num_pastries
    return cost


cost = total_cost(8, 4, 12)
print(cost)
# Ans:19.6
