thisset = {"apple", "banana", "cherry", "apple"}

print(thisset)


thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x)


thisset = {"apple", "banana", "cherry"}

thisset.add("orange")

print(thisset)


thisset = {"apple", "banana", "cherry"}
mylist = ["kiwi", "orange"]

thisset.update(mylist)

print(thisset)


thisset = {"apple", "banana", "cherry"}

thisset.remove("banana")

print(thisset)


thisset = {"apple", "banana", "cherry"}

x = thisset.pop()

print(x)

print(thisset)


thisset = {"apple", "banana", "cherry"}

del thisset

print(thisset)



thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x)



set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1.union(set2)
print(set3)

