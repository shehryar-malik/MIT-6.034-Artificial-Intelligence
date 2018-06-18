def maximum(x,y):
    if x>y:
        return x
    return y

def depth(expr):
    if not isinstance(expr,(list,tuple)):
        return 0

    leftH  = depth(expr[1])
    rightH = depth(expr[2])

    return max(leftH,rightH)+1

#z = depth(('+', 5, 2))
#print(z)
expr1 = ['a','b']
expr2 = ['c','d']
answer = []
x = []
for val1 in range(0, len(expr1)):
    x = expr1[val1]
    for val2 in range(0, len(expr2)):
        answer += [[x, expr2[val2]]]

print(answer)
