matrix = r.read('LatinSquares.txt')
fail = 0
order = 1
for i in matrix:
    print('Example order:', order)
    size = i[0]
    matrix = i[1:]
    b = p.Problem(matrix,size)
    a = b.initial_state()
    c = Search(b)
    c = Search.DepthFirstSearch(c,a)
    print(c.__str__())
    order += 1
    if c.success == False:
        fail +=1
print('Fail number:', fail)



matrix = r.read('LatinSquares.txt')
fail = 0
order = 1
for i in matrix:
    print('Example order:', order)
    size = i[0]
    matrix = i[1:]
    b = pp.Problem(matrix,size)
    a = b.initial_state()
    c = Search(b)
    c = Search.DepthFirstSearch(c,a)
    print(c.__str__())
    order += 1
    if c.success == False:
        fail +=1
print('Fail number:', fail)


def result(self, a_state: State, action):
    r = action[0]
    c = action[1]
    num = action[2]
    new_state = State(a_state.size)
    for row in range(0, self.size):
        for col in range(0, self.size):
            new_state.collection['(' + str(row) + ', ' + str(col) + ')'].val = a_state.collection[
                '(' + str(row) + ', ' + str(col) + ')'].val
    a_state.blank_location.discard((r, c))
    new_state.blank_location = set()
    for i in a_state.blank_location:
        new_state.blank_location.add(i)
    new_state.collection['(' + str(r) + ', ' + str(c) + ')'].val = num
    for i in new_state.blank_location:
        new_state.collection[str(i)].domain.discard(num)
    return new_state