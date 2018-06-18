def tree_ref(tree, index):
    if len(index) == 1:
        return tree[index[0]]

    newindex = index[1:]

    return tree_ref(tree[index[0]], newindex)


tree = (((1, 2), 3), (4, (5, 6)), 7, (8, 9, 10))
z = tree_ref(tree, (0,))
print(z)
