#!/usr/bin/env python3

def sum_numbers(a, b):
    """Add two numbers and return the result."""
    return a + b

def multiply_numbers(a, b):
    """Multiply two numbers and return the result."""
    return a * b

def divide_numbers(a, b):
    """Divide two numbers and return the result."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Example usage
if __name__ == "__main__":
    # Test sum function
    num1 = 2
    num2 = 2
    sum_result = sum_numbers(num1, num2)
    print(f"{num1} + {num2} = {sum_result}")

    # Test multiply function
    multiply_result = multiply_numbers(num1, num2)
    print(f"{num1} × {num2} = {multiply_result}")

    # Test divide function
    divide_result = divide_numbers(num1, num2)
    print(f"{num1} ÷ {num2} = {divide_result}")

