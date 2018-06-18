from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    # Add your forward checking logic here.
    Xinstance = state.get_current_variable()
    if Xinstance is not None:
        Xvar = Xinstance.get_name()
        xval = Xinstance.get_assigned_value()

        all_binary_constraints = state.get_constraints_by_name(Xvar)
        for binary_constraint in all_binary_constraints:
            Yvar = binary_constraint.get_variable_j_name()
            Yinstance = state.get_variable_by_name(Yvar)
            for yval in Yinstance.get_domain():
                if not binary_constraint.check(state, value_i=xval, value_j=yval):
                    Yinstance.reduce_domain(yval)
                if Yinstance.domain_size() == 0:
                    return False

    return True

# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def is_in_list(x,lst):
    for i in lst:
        if x == i:
            return True
    return False

def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    # Add your propagate singleton logic here.
    singeltons = []
    visited_singeltons = []

    for variable in state.get_all_variables():
        if variable.domain_size() == 1:
            singeltons += [variable]

    while len(singeltons) is not 0:
        X = singeltons[0]
        visited_singeltons += [X]
        for i in range(1, len(singeltons)):
            singeltons[i - 1] = singeltons[i]
        del singeltons[len(singeltons)-1]

        Xname = X.get_name()
        all_binary_constraints = state.get_constraints_by_name(Xname)
        for binary_constraint in all_binary_constraints:
            Yname = binary_constraint.get_variable_j_name()
            Y = state.get_variable_by_name(Yname)
            for yval in Y.get_domain():
                if not binary_constraint.check(state, value_i=X.get_domain()[0], value_j=yval):
                    Y.reduce_domain(yval)
                if Y.domain_size() == 0:
                    return False
            if Y.domain_size() == 1 and not is_in_list(Y,singeltons) and not is_in_list(Y,visited_singeltons):
                new_singeltons = [Y]
                for i in range(0, len(singeltons)):
                    new_singeltons += [singeltons[i]]
                del singeltons
                singeltons = new_singeltons

    return True

## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')

### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    assert isinstance(list1, list)
    assert isinstance(list2, list)

    dist = 0

    for item1, item2 in zip(list1, list2):
        dist += math.pow(item1-item2, 2)
    dist = math.sqrt(dist)
    return dist

#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2, verbose=1)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance, 5)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    yes_disorder = information_disorder_branch_value(yes)
    no_disorder  = information_disorder_branch_value(no)
    yes_size = len(yes)
    no_size  = len(no)
    total_size = float(yes_size + no_size)

    average_disorder = (yes_size / total_size) * yes_disorder + (no_size / total_size) * no_disorder

    return average_disorder

def information_disorder_branch_value(lst):
    class_names = []
    class_sample_size = []

    class_names += [lst[0]]
    class_sample_size += [1]
    for x in lst[1:]:
        count = 0
        for y in class_names:
            found = False
            if x == y:
                found = True
                break
            count += 1
        if found:
            class_sample_size[count] += 1
        else:
            class_names += [x]
            class_sample_size += [1]

    disorder = 0
    for item in class_sample_size:
        ratio = item/float(len(lst))
        disorder -= (ratio)*math.log(ratio,2)

    return disorder

#print CongressIDTree(senate_people, senate_votes, information_disorder)
#evaluate(idtree_maker(senate_votes, information_disorder), senate_group1, senate_group2, verbose=1)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 44
rep_classified = limited_house_classifier(house_people, house_votes, N_1, verbose=False)
#print rep_classified

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 67
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)
#print senator_classified

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)
#print old_senator_classified

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "0"
WHAT_I_FOUND_INTERESTING = "Nothing"
WHAT_I_FOUND_BORING = "Nothing"


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn
