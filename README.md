# arbitrary-precision-integer-calculator

This project implements a custom BigInt class in Python, designed to handle arbitrary-precision integers—numbers that exceed the limits of native integer types (such as Python's int). The class supports basic arithmetic operations like addition, subtraction, multiplication, division, and modulus, as well as comparison and string representation.

## Introduction
This implementation focuses on providing an efficient and extensible way to handle arbitrarily large integers, which Python’s native int type can support, but this project focuses on manually handling the digits, as would be necessary in low-level programming. The BigInt class includes features like handling negative numbers, performing long arithmetic operations, and supporting basic operations commonly used in large number calculations.
## Features
Arbitrary Precision: Can handle integers of arbitrary size limited only by memory.

Basic Arithmetic: Supports addition, subtraction, multiplication, division, and modulus operations.

Negative Numbers: Handles negative integers and operations involving negative numbers correctly.

Comparison: Supports comparing the magnitude of two BigInt objects.

String Representation: Converts a BigInt object to a string for easy display.

### Class Design
Constructor
def __init__(self, value):

Purpose: The constructor initializes a BigInt object from a string or numeric value.

How it works:
The input value is first converted to a string and any extra spaces are removed using strip().
If the first character of the value is a minus sign (-), it marks the number as negative.
The digits of the number are then extracted and stored as a list of integers (e.g., ['1', '2', '3'] for the number 123).

### String Representation

def __str__(self):

Purpose: Converts the BigInt object into a human-readable string.
How it works:
If the number is negative, the method prepends a minus sign (-).
The digits are joined together into a single string and returned.

### Arithmetic Operations
#### Addition
def __add__(self, other):

Purpose: Adds two BigInt objects.
How it works:
If both numbers have the same sign, the BigInt._add_positive() method is used to add their absolute values.
If the signs differ, the method compares their magnitudes and subtracts the smaller number from the larger one, preserving the sign of the larger number.
#### Subtraction

def __sub__(self, other):

Purpose: Subtracts one BigInt from another.
How it works:
The sign of the second operand is negated (i.e., the subtraction becomes addition), and the __add__ method is used to perform the subtraction.
The sign of the second operand is then restored.
#### Multiplication

def __mul__(self, other):

Purpose: Multiplies two BigInt objects.
How it works:
A result list is initialized to hold the product of the multiplication.
The algorithm uses long multiplication (multiplying each digit of one number by each digit of the other).
The carry is handled appropriately during the multiplication, ensuring the result is stored in reverse order to facilitate easier addition later.
The result is then converted back to a string representation, and the sign is determined by the multiplication rules (positive if both numbers have the same sign, negative otherwise).
#### Division

def __floordiv__(self, other):

Purpose: Performs floor division (integer division) between two BigInt objects.
How it works:
The method uses the helper function _divmod() to obtain both the quotient and the remainder, returning only the quotient.
#### Modulus

def __mod__(self, other):

Purpose: Returns the remainder when one BigInt is divided by another.
How it works:
The method uses _divmod() to calculate the quotient and remainder, returning the remainder.
#### Helper Methods
##### _add_positive

@staticmethod
def _add_positive(a, b):

Purpose: Adds two positive BigInt numbers.
How it works:
Both numbers are reversed to facilitate addition starting from the least significant digit.
Each digit is added together with the carry, and the result is stored in a list.
If there is any leftover carry after the addition, it is appended to the result.
##### _subtract_positive

@staticmethod
def _subtract_positive(a, b):

Purpose: Subtracts one positive BigInt from another.
How it works:
Similar to addition, both numbers are reversed. The algorithm subtracts each digit, borrowing when necessary.
The final result is reversed again and returned.
##### _compare_magnitude

@staticmethod
def _compare_magnitude(a, b):

Purpose: Compares the magnitude (absolute value) of two BigInt objects.
How it works:
First, the lengths of the numbers are compared. A longer number is greater.
If the numbers are of equal length, the digits are compared one by one to determine which is larger.
## Testing
Test Suite
The BigInt class is thoroughly tested using Python's built-in unittest framework. The test cases include:
Arithmetic Tests: Tests for addition, subtraction, multiplication, division, and modulus operations.
Zero Operations: Tests involving zero, including division and modulus by zero.
Large Number Operations: Tests for operations on arbitrarily large integers.
To run the tests:
Clone the repository.
Run the following command in the terminal:
bash

python -m unittest discover


Test Cases
Test cases cover scenarios like:
Simple operations: Adding and subtracting small numbers.
Negative numbers: Ensuring proper handling of sign and magnitude.
Division and modulus: Handling of edge cases like division by zero.
Large numbers: Testing with numbers that go beyond typical integer ranges.
Usage
Example Usage

### Create BigInt objects
num1 = BigInt('123456789123456789')
num2 = BigInt('987654321987654321')

#### Perform arithmetic operations
sum_result = num1 + num2
print(sum_result)  # Output: 1111111111111111110

difference_result = num1 - num2
print(difference_result)  # Output: -864197532864197532

product_result = num1 * num2
print(product_result)  # Output: 121932631137021795804246029035453312

quotient_result = num1 // num2
print(quotient_result)  # Output: 0

modulus_result = num1 % num2
print(modulus_result)  # Output: 123456789123456789

### Challenges and Design Decisions

Handling Large Numbers: The main challenge in implementing this class was managing large integers manually, without relying on built-in libraries like int. The solution was to store the digits as a list and perform arithmetic step-by-step, using techniques such as long multiplication and manual carry/borrow handling.

Negative Numbers: A key design decision was handling negative numbers in a way that didn’t complicate the operations. The class simplifies this by keeping a boolean flag is_negative to track the sign and using standard methods for handling negative results in arithmetic.

Efficiency Considerations: The performance of operations like addition and multiplication is optimized by reversing the numbers for easier digit manipulation. However, for extremely large numbers, some of the algorithms (like multiplication) could still be improved further with more efficient methods like Karatsuba or Fast Fourier Transform (FFT).
