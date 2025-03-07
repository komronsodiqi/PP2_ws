import arithmetics
arr1 = [1,23,3,40,5]
arr2 = [10,11,12,5,18]
mul2nums = []
for num1, num2 in zip(arr1, arr2):
    mul2nums.append(arithmetics.multiply(num1,num2))
print(mul2nums)
