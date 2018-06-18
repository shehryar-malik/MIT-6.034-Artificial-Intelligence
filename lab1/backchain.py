from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    new_hyp_list = []
    goaltree = []

    for rule in rules:
        for word in rule.consequent():
            if match(rule.consequent()[0], hypothesis)!=None:
                new_hyp = populate(rule.antecedent(),match(rule.consequent()[0],hypothesis))
                new_hyp_list += [new_hyp]

    goaltree += [hypothesis]
    for new_hyp in new_hyp_list:
        goaltree += [new_hyp]

    goaltree = OR(goaltree)

    if len(goaltree)!=0:
        for i in range(1,len(goaltree)):
            if isinstance(goaltree[i], (list,tuple)):
                for j in range(0,len(goaltree[i])):
                    goaltree[i][j] = simplify(backchain_to_goal_tree(rules, goaltree[i][j]))
            else:
                goaltree[i] = simplify(backchain_to_goal_tree(rules, goaltree[i]))

    goaltree = simplify(goaltree)

    return goaltree

#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
