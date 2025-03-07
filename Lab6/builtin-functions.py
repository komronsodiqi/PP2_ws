import math
import time
import functools
import operator

# 1. Multiply all numbers in a list
def multiply_list(lst):
    return functools.reduce(operator.mul, lst, 1)

print(multiply_list([1, 2, 3, 4]))  # Output: 24

# 2. Count uppercase and lowercase letters in a string
def count_case(s):
    upper = sum(1 for c in s if c.isupper())
    lower = sum(1 for c in s if c.islower())
    return {"Uppercase": upper, "Lowercase": lower}

print(count_case("Hello World!"))  # Output: {'Uppercase': 2, 'Lowercase': 8}

# 3. Check if a string is a palindrome
def is_palindrome(s):
    s = s.lower().replace(" ", "")  # Normalize string
    return s == s[::-1]

print(is_palindrome("madam"))  # True
print(is_palindrome("hello"))  # False

# 4. Invoke square root function after specific milliseconds
def delayed_sqrt(number, delay_ms):
    time.sleep(delay_ms / 1000)  # Convert milliseconds to seconds
    return math.sqrt(number)

num = 25100
delay = 2123
print(f"Square root of {num} after {delay} milliseconds is {delayed_sqrt(num, delay)}")

# 5. Check if all elements of a tuple are true
def all_true(tpl):
    return all(tpl)

print(all_true((True, True, True)))  # True
print(all_true((True, False, True)))  # False
