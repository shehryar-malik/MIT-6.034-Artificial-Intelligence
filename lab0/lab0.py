# This is the file you'll use to submit most of Lab 0.

# Certain problems may ask you to modify other files to accomplish a certain
# task. There are also various other files that make the problem set work, and
# generally you will _not_ be expected to modify or even understand this code.
# Don't get bogged down with unnecessary work.


# Section 1: Problem set logistics ___________________________________________

# This is a multiple choice question. You answer by replacing
# the symbol 'fill-me-in' with a number, corresponding to your answer.

# You get to check multiple choice answers using the tester before you
# submit them! So there's no reason to worry about getting them wrong.
# Often, multiple-choice questions will be intended to make sure you have the
# right ideas going into the problem set. Run the tester right after you
# answer them, so that you can make sure you have the right answers.

# What version of Python do we *recommend* (not "require") for this course?
#   1. Python v2.3
#   2. Python v2.5 or Python v2.6
#   3. Python v3.0
# Fill in your answer in the next line of code ("1", "2", or "3"):

ANSWER_1 = '2'


# Section 2: Programming warmup _____________________________________________

# Problem 2.1: Warm-Up Stretch

def cube(x):
    return x*x*x

def factorial(x):
    if x == 0:
        return 1
    if x > 0:
        return x*factorial(x-1)
    if x < 0:
        raise Exception

def count_pattern(pattern, lst):
    y = 0
    for count1 in range(0, len(lst)):
        if len(lst) - count1  >= len(pattern):
            if lst[count1] == pattern[0]:
                x = 1
                for count2 in range(1, len(pattern)):
                    if pattern[count2] == lst[count2 + count1]:
                        x += 1
                    else:
                        break
                if x == len(pattern):
                    y += 1
        else:
            break
    return y

# Problem 2.2: Expression depth

def depth(expr):

    if not isinstance(expr, (list, tuple)):
        return 0

    leftH = depth(expr[1])
    rightH = depth(expr[2])

    return max(leftH, rightH) + 1


# Problem 2.3: Tree indexing

def tree_ref(tree, index):

    if len(index) == 1:
        return tree[index[0]]

    newindex = index[1:]

    return tree_ref(tree[index[0]], newindex)

# Section 3: Symbolic algebra

# Your solution to this problem doesn't go in this file.
# Instead, you need to modify 'algebra.py' to complete the distributer.

from algebra import Sum, Product, simplify_if_possible
from algebra_utils import distribution, encode_sumprod, decode_sumprod

# Section 4: Survey _________________________________________________________

# Please answer these questions inside the double quotes.

# When did you take 6.01?
WHEN_DID_YOU_TAKE_601 = "Never"

# How many hours did you spend per 6.01 lab?
HOURS_PER_601_LAB = "0"

# How well did you learn 6.01?
HOW_WELL_I_LEARNED_601 = "Nothing"

# How many hours did this lab take?
HOURS = ""
