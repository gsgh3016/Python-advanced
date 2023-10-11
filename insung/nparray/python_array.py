py_list1= ["abc", "def", "ghi"]
py_list2 = [1,2,3] # already constructed
for factor in py_list1:
    print("string: ", factor, end=" ")
    print("address: ", hex(id(factor)))

for factor in py_list2:
    print("string: ", factor, end=" ")
    print("address: ", hex(id(factor)))  