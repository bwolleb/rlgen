def numberToBase(n, b):
	if n == 0:
		return [0]
	digits = []
	while n:
		digits.append(int(n % b))
		n //= b
	return digits[::-1]

def numberToCol(n, b):
	digits = []
	n -= 1
	while n >= 0:
		digits.insert(0, n % b)
		n = int(n / b)
		n -= 1
	return digits

def arab(n): return n

def ALPHA(n):
	digits = numberToCol(n, 26)
	chars = [chr(ord("A") + x) for x in digits]
	return str.join("", chars)

def alpha(n):
	return ALPHA(n).lower()

def Alpha(n):
	return alpha(n).capitalize()

# From O'Reilly python-cookbook
# Module: Roman Numerals
# Credit: Paul M. Winkler
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s24.html
# Modified to make it shorter, should be ok to use, reimplement otherwise
def ROMAN(n):
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = []
    for i in range(len(ints)):
        count = int(n / ints[i])
        result.append(nums[i] * count)
        n -= ints[i] * count
    return str.join("", result)

def roman(n):
	return ROMAN(n).lower()

def Roman(n):
	return roman(n).capitalize()

Formatters = {}
Formatters["1"] = arab
Formatters["A"] = ALPHA
Formatters["a"] = alpha
Formatters["Aa"] = Alpha
Formatters["I"] = ROMAN
Formatters["i"] = roman
Formatters["Ii"] = Roman
