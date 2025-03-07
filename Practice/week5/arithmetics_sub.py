import arithmetics
arr1 = [1,23,3,40,5]
arr2 = [10,11,12,5,18]
dif2nums = []
for num1, num2 in zip(arr1, arr2):
    dif2nums.append(arithmetics.subtract(num1,num2))
print(dif2nums)
