import arithmetics
arr1 = [1,23,3,40,5]
arr2 = [10,11,12,5,18]
sum2nums = []
for num1, num2 in zip(arr1, arr2):
    sum2nums.append(arithmetics.add(num1,num2))
print(sum2nums)