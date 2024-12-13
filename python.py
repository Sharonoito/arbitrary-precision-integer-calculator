class BigInt:
    def __init__(self, value):
        value = str(value).strip()
        self.is_negative = value[0] == '-'
        self.value = [int(d) for d in value.lstrip('-')]

    def __str__(self):
        return ('-' if self.is_negative else '') + ''.join(map(str, self.value))

    def __add__(self, other):
        if self.is_negative == other.is_negative:
            result = BigInt._add_positive(self, other)
            result.is_negative = self.is_negative
            return result
        else:
            if BigInt._compare_magnitude(self, other) >= 0:
                result = BigInt._subtract_positive(self, other)
                result.is_negative = self.is_negative
                return result
            else:
                result = BigInt._subtract_positive(other, self)
                result.is_negative = other.is_negative
                return result

    def __sub__(self, other):
        other.is_negative = not other.is_negative
        result = self + other
        other.is_negative = not other.is_negative
        return result

    def __mul__(self, other):
        result = [0] * (len(self.value) + len(other.value))
        for i in range(len(self.value) - 1, -1, -1):
            carry = 0
            for j in range(len(other.value) - 1, -1, -1):
                temp = result[i + j + 1] + self.value[i] * other.value[j] + carry
                result[i + j + 1] = temp % 10
                carry = temp // 10
            result[i] += carry
        result_value = ''.join(map(str, result)).lstrip('0') or '0'
        is_negative = self.is_negative != other.is_negative
        return BigInt('-' + result_value if is_negative else result_value)

    def __floordiv__(self, other):
        quotient, _ = self._divmod(other)
        return quotient

    def __mod__(self, other):
        _, remainder = self._divmod(other)
        return remainder

    def _divmod(self, other):
        if other == BigInt('0'):
            raise ZeroDivisionError("division by zero")
        dividend = BigInt('0')
        quotient = []
        for digit in self.value:
            dividend = BigInt(str(dividend) + str(digit))
            count = 0
            while BigInt._compare_magnitude(dividend, other) >= 0:
                dividend -= other
                count += 1
            quotient.append(str(count))
        return BigInt(('' if not self.is_negative == other.is_negative else '-') + ''.join(quotient).lstrip('0') or '0'), dividend

    @staticmethod
    def _add_positive(a, b):
        result = []
        carry = 0
        a.value, b.value = a.value[::-1], b.value[::-1]
        for i in range(max(len(a.value), len(b.value))):
            digit_a = a.value[i] if i < len(a.value) else 0
            digit_b = b.value[i] if i < len(b.value) else 0
            total = digit_a + digit_b + carry
            result.append(total % 10)
            carry = total // 10
        if carry:
            result.append(carry)
        return BigInt(''.join(map(str, result[::-1])))

    @staticmethod
    def _subtract_positive(a, b):
        result = []
        borrow = 0
        a.value, b.value = a.value[::-1], b.value[::-1]
        for i in range(len(a.value)):
            digit_a = a.value[i]
            digit_b = b.value[i] if i < len(b.value) else 0
            total = digit_a - digit_b - borrow
            if total < 0:
                total += 10
                borrow = 1
            else:
                borrow = 0
            result.append(total)
        return BigInt(''.join(map(str, result[::-1])).lstrip('0') or '0')

    @staticmethod
    def _compare_magnitude(a, b):
        if len(a.value) != len(b.value):
            return len(a.value) - len(b.value)
        for x, y in zip(a.value, b.value):
            if x != y:
                return x - y
        return 0

class Calculator:
    def start(self):
        print("Welcome to the arbitrary-precision calculator. Type 'exit' to quit.")
        while True:
            try:
                user_input = input("calc> ").strip()
                if user_input.lower() == 'exit':
                    break
                print(self.evaluate(user_input))
            except Exception as e:
                print(f"Error: {e}")

    def evaluate(self, expression):
        tokens = expression.split()
        if len(tokens) != 3:
            raise ValueError("Expected format: <num1> <operator> <num2>")

        num1, operator, num2 = tokens
        num1, num2 = BigInt(num1), BigInt(num2)

        if operator == '+':
            return num1 + num2
        elif operator == '-':
            return num1 - num2
        elif operator == '*':
            return num1 * num2
        elif operator == '/':
            return num1 // num2
        elif operator == '%':
            return num1 % num2
        else:
            raise ValueError(f"Unknown operator: {operator}")

if __name__ == "__main__":
    calc = Calculator()
    calc.start()

# Unit Testing
import unittest

class TestBigInt(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(str(BigInt('123') + BigInt('456')), '579')
        self.assertEqual(str(BigInt('-123') + BigInt('-456')), '-579')
        self.assertEqual(str(BigInt('-123') + BigInt('456')), '333')
        self.assertEqual(str(BigInt('123') + BigInt('-456')), '-333')

    def test_subtraction(self):
        self.assertEqual(str(BigInt('456') - BigInt('123')), '333')
        self.assertEqual(str(BigInt('-456') - BigInt('-123')), '-333')
        self.assertEqual(str(BigInt('-456') - BigInt('123')), '-579')
        self.assertEqual(str(BigInt('456') - BigInt('-123')), '579')

    def test_multiplication(self):
        self.assertEqual(str(BigInt('123') * BigInt('456')), '56088')
        self.assertEqual(str(BigInt('-123') * BigInt('-456')), '56088')
        self.assertEqual(str(BigInt('-123') * BigInt('456')), '-56088')
        self.assertEqual(str(BigInt('123') * BigInt('-456')), '-56088')

    def test_division(self):
        self.assertEqual(str(BigInt('56088') // BigInt('456')), '123')
        self.assertEqual(str(BigInt('-56088') // BigInt('-456')), '123')
        self.assertEqual(str(BigInt('-56088') // BigInt('456')), '-123')
        self.assertEqual(str(BigInt('56088') // BigInt('-456')), '-123')

    def test_modulus(self):
        self.assertEqual(str(BigInt('56088') % BigInt('456')), '0')
        self.assertEqual(str(BigInt('123') % BigInt('10')), '3')
        self.assertEqual(str(BigInt('-123') % BigInt('10')), '7')  # Python-like behavior

    def test_zero_operations(self):
        self.assertEqual(str(BigInt('0') + BigInt('0')), '0')
        self.assertEqual(str(BigInt('0') - BigInt('0')), '0')
        self.assertEqual(str(BigInt('0') * BigInt('456')), '0')
        with self.assertRaises(ZeroDivisionError):
            _ = BigInt('456') // BigInt('0')
        with self.assertRaises(ZeroDivisionError):
            _ = BigInt('456') % BigInt('0')

    def test_large_numbers(self):
        large_num1 = BigInt('9' * 100)
        large_num2 = BigInt('1' + '0' * 99)
        self.assertEqual(str(large_num1 + BigInt('1')), '1' + '0' * 100)
        self.assertEqual(str(large_num1 * BigInt('2')), '1' + '8' + '0' * 99)
        self.assertEqual(str(large_num1 - large_num2), '9' * 99)

if __name__ == "__main__":
    unittest.main()
