import random as rd


def generate(size):
    matrix = []
    for i in range(size):
        temp = []
        for i in range(size):
            temp.append(rd.randint(1,30))
        temp.sort()
        matrix.append(temp)
    return matrix


def display(mx):
    for i in mx:
        print(i)

col, row = 0, 0
g = generate(4)
display(g)
print(g)