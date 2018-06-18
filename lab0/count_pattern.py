def count_pattern(pattern, list):
    y = 0
    for count1 in range(0, len(list)):
        if len(list) - count1  >= len(pattern):
            if list[count1] == pattern[0]:
                x = 1
                for count2 in range(1, len(pattern)):
                    if pattern[count2] == list[count2 + count1]:
                        x += 1
                    else:
                        break
                if x == len(pattern):
                    y += 1
        else:
            break
    return y

z = count_pattern(['a','b','a'],['g','a','b','a','b','a','b','a'])
print(z)