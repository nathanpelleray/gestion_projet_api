list = []

list.append(("test1", 1))
list.append(("test2", 2))
list.append(("test3", 3))

for i in range(len(list)):
    if list[i][1] == 2:
        print(list[i][0])