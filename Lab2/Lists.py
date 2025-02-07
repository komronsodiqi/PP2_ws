#General
thislist = ["apple", "banana", "cherry"]
print(thislist)

thislist = ["apple", "banana", "cherry"]
print(len(thislist))

list1 = ["apple", "banana", "cherry"]
list2 = [1, 5, 7, 9, 3]
list3 = [True, False, False]

list1 = ["abc", 34, True, 40, "male"]

mylist = ["apple", "banana", "cherry"]
print(type(mylist))

thislist = list(("apple", "banana", "cherry")) # note the double round-brackets
print(thislist)

#Output

thislist = ["apple", "banana", "cherry"]
print(thislist[-1]) #the last element 

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:5]) #Return the third, fourth, and fifth item

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[:4]) #This example returns the items from the beginning to, but NOT including, "kiwi"

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:]) #This example returns the items from "cherry" to the end

#Change

thislist = ["apple", "banana", "cherry"]
thislist[1] = "blackcurrant"
print(thislist) #Change the second item

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist) #Change the values "banana" and "cherry" with the values "blackcurrant" and "watermelon"

thislist = ["apple", "banana", "cherry"]
thislist[1:2] = ["blackcurrant", "watermelon"]
print(thislist) #Change the second value by replacing it with two new values

thislist = ["apple", "banana", "cherry"]
thislist[1:3] = ["watermelon"]
print(thislist) #Change the second and third value by replacing it with one value

#Adding

thislist = ["apple", "banana", "cherry"]
thislist.append("orange")
print(thislist)

thislist = ["apple", "banana", "cherry"]
thislist.insert(1, "orange")
print(thislist)

#Removing

thislist = ["apple", "banana", "cherry"]
thislist.remove("banana")
print(thislist)

thislist = ["apple", "banana", "cherry"]
thislist.pop(1)
print(thislist) #Remove the second item

thislist = ["apple", "banana", "cherry"]
thislist.pop()
print(thislist) #Remove the last item

thislist = ["apple", "banana", "cherry"]
del thislist[0]
print(thislist) #Remove the first item

thislist = ["apple", "banana", "cherry"]
del thislist #Delete the entire list

thislist = ["apple", "banana", "cherry"]
thislist.clear()
print(thislist) #Clear the list content

#Looping Lists

thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x) #Print all items in the list, one by one

thislist = ["apple", "banana", "cherry"]
for i in range(len(thislist)):
  print(thislist[i]) #Print all items by referring to their index number

#Comperhension

fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = []

for x in fruits:
  if "a" in x:
    newlist.append(x)

print(newlist)

#Sort

thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort()
print(thislist) #alphabet sorting

thislist = [100, 50, 65, 82, 23]
thislist.sort()
print(thislist) #nurmerical

thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort(reverse = True)
print(thislist) # descending alphebically 

thislist = [100, 50, 65, 82, 23]
thislist.sort(reverse = True)
print(thislist) # descending numerically

#Copy

thislist = ["apple", "banana", "cherry"]
mylist = thislist.copy()
print(mylist)

thislist = ["apple", "banana", "cherry"]
mylist = list(thislist)
print(mylist)

thislist = ["apple", "banana", "cherry"]
mylist = thislist[:]
print(mylist)

#Join

list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

list3 = list1 + list2
print(list3)

list1 = ["a", "b" , "c"]
list2 = [1, 2, 3]

for x in list2:
  list1.append(x)

print(list1) #Append list2 into list1

list1 = ["a", "b" , "c"]
list2 = [1, 2, 3]

list1.extend(list2)
print(list1) #the extend() method to add list2 at the end of list1
