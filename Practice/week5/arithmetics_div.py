import arithmetics
arr1 = [1,23,3,40,5]
arr2 = [10,11,12,5,18]
div2nums = []
for num1, num2 in zip(arr1, arr2):
    if num1 < num2:
        div2nums.append(arithmetics.divide(num2,num1))
    elif num1 > num2:
         div2nums.append(arithmetics.divide(num1,num2))
print(div2nums)