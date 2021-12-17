# Derived in part from a Microsoft Corporation file licensed under the MIT License.

import math as m
import random as r
from pytest import approx
from numpy import isclose

tests = {}

# Exercise decorator, specifying that this function needs to be tested
def exercise(fun):
    tests[fun.__name__](fun)
    return fun

# Test decorator, specifying that this is a test for an exercise
def test(fun):
    tests[fun.__name__[5:]] = fun
    return fun

################################################################################

# Generates a random complex number in Cartesian form
def prep_random_cartesian():
    real = (r.random() - 0.5) * r.randint(0, 100)
    imag = (r.random() - 0.5) * r.randint(0, 100)
    return (round(real,2), round(imag,2))

# Asserts that the result is a tuple of length 2
def assert_tuple(result):
    if result == None: return "Your function must return a value!"
    if not type(result) is tuple: return "Your function must return a tuple, returned " + type(result).__name__ + "."
    if result[0] == ... or result[1] == ...: return "You should not return an ellipsis (...) as part of your answer."
    if len(result) != 2:
        return "Your function must return a tuple of length 2, but returned tuple is of length " + str(len(result))

# # Asserts the output is a valid complex tuple, and checks that it matches expected output
# def assert_cartesian(expected, actual, message):
#     if actual != approx(expected): return message

# Asserts the output is a valid complex tuple, and checks that it matches expected output
def assert_cartesian(expected, actual, message):
    if not isclose(actual, expected).all(): return message

################################################################################

def ref_pow_imag(n):
    if (n%4)==0: return (1,0)
    if (n%4)==1: return (0,1)
    if (n%4)==2: return (-1,0)
    if (n%4)==3: return (0,-1)

@test
def test_pow_imag(fun):
    for i in range(-25, 25):
        n = 2 * i
        expected = ref_pow_imag(n)
        actual = fun(n)
        if actual == None:
            print("Your function must return a value!")
            return
        if expected != actual:
            message = "Result of exponentiation doesn't seem to match expected value: expected i**({0}) = {1}, got {2}"
            print(message.format(n, expected, actual))
            return
    print("Success!")

################################################################################

def ref_addc(x,y):
    return (x[0] + y[0], x[1] + y[1])

@test
def test_addc(fun):
    for i in range(25):
        x = prep_random_cartesian()
        y = prep_random_cartesian()
        expected = ref_addc(x, y)
        actual = fun(x, y)
        msg = assert_tuple(actual)
        if msg != None:
            print(msg)
            return
        msg = assert_cartesian(expected, actual,
                               f"Sum doesn't seem to match expected value: expected ({x},{y}) = {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")

################################################################################

def ref_mulc(x,y):
    return (x[0] * y[0] - x[1] * y[1], x[1] * y[0] + x[0] * y[1])

@test
def test_mulc(fun):
    for i in range(25):
        x = prep_random_cartesian()
        y = prep_random_cartesian()
        expected = ref_mulc(x, y)
        actual = fun(x, y)
        msg = assert_tuple(actual)
        if msg != None:
            print(msg)
            return
        msg = assert_cartesian(expected, actual,
                               f"Sum doesn't seem to match expected value: expected ({x},{y}) = {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")

################################################################################

def ref_conj(x):
    return (x[0], -x[1])

@test
def test_conj(fun):
    for i in range(25):
        x = prep_random_cartesian()
        expected = ref_conj(x)
        actual = fun(x)
        msg = assert_tuple(actual)
        if msg != None:
            print(msg)
            return
        msg = assert_cartesian(expected, actual,
                               f"Sum doesn't seem to match expected value: expected conj {x} = {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")


################################################################################

def ref_divc(x, y):
    ybar = ref_conj(y)
    numer = ref_mulc(x, ybar)
    denom = ref_mulc(y, ybar)[0]
    return ref_mulc(numer, (1 / denom, 0))

@test
def test_divc(fun):
    for i in range(25):
        x = prep_random_cartesian()
        y = (0, 0)
        while y == (0, 0):
            y = prep_random_cartesian()
        expected = ref_divc(x, y)
        actual = fun(x, y)
        msg = assert_tuple(actual)
        if msg != None:
            print(msg)
            return
        msg = assert_cartesian(expected, actual,
                               f"Sum doesn't seem to match expected value: expected ({x},{y}) = {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")

################################################################################

def ref_mod(x):
    return m.sqrt(ref_mulc(x, ref_conj(x))[0])

@test
def test_mod(fun):
    for i in range(25):
        x = prep_random_cartesian()
        expected = ref_mod(x)
        actual = fun(x)
        if actual == None:
            print("Your function must return a value!")
            return
        if not (type(actual) is float or type(actual) is int):
            print("Your function must return a number, returned " + type(actual).__name__ + ".")
            return
        msg = assert_cartesian(expected, actual,
                               f"Sum doesn't seem to match expected value: expected {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")

################################################################################

def ref_expc(x):
    realpow = m.e ** x[0]
    return (realpow * m.cos(x[1]), realpow * m.sin(x[1]))

@test
def test_expc(fun):
    for i in range(25):
        x = prep_random_cartesian()
        expected = ref_expc(x)
        actual = fun(x)
        msg = assert_tuple(actual)
        if msg != None:
            print(msg)
            return
        msg = assert_cartesian(expected, actual,
                               f"Sum doesn't seem to match expected value: expected e^{x} = {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")

################################################################################

def ref_powc_real(r, x):
    if r == 0: return (0, 0)
    lnr = m.log(r)
    return ref_expc(ref_mulc((lnr, 0), x))

@test
def test_powc_real(fun):
    for i in range(25):
        base = r.random() * r.randint(1, 100)
        if i == 0:
            base = 0
        x = prep_random_cartesian()
        expected = ref_powc_real(base, x)
        actual = fun(base, x)
        msg = assert_tuple(actual)
        if msg != None:
            print(msg)
            return
        msg = assert_cartesian(expected, actual,
                               f"Sum doesn't seem to match expected value: expected {base}^{x} = {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")

################################################################################

# Generates a random complex number in Cartesian form
def prep_random():
    real = (r.random() - 0.5) * r.randint(0, 100)
    while m.isclose(real,0.0):
        real = (r.random() - 0.5) * r.randint(0, 100)
    return (round(real,2))

################################################################################

def ref_iadd(x,y):
  return (x[0]+y[0],x[1]+y[1])

@test
def test_iadd(fun):
    for i in range(25):
        x = sorted((prep_random(),prep_random()))
        y = sorted((prep_random(),prep_random()))
        expected = ref_iadd(x, y)
        actual = fun(x, y)
        msg = assert_tuple(actual)
        if msg != None:
            print(msg)
            return
        msg = assert_cartesian(expected, actual,
                               f"Sum doesn't seem to match expected value: expected ({x},{y}) = {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")

################################################################################

def ref_imul(x,y):
  lb = min(x[0]*y[0], x[0]*y[1], x[1]*y[0], x[1]*y[1])
  rb = max(x[0]*y[0], x[0]*y[1], x[1]*y[0], x[1]*y[1])
  return (lb,rb)

@test
def test_imul(fun):
    for i in range(25):
        x = sorted((prep_random(),prep_random()))
        y = sorted((prep_random(),prep_random()))
        expected = ref_imul(x, y)
        actual = fun(x, y)
        msg = assert_tuple(actual)
        if msg != None:
            print(msg)
            return
        msg = assert_cartesian(expected, actual,
                               f"Sum doesn't seem to match expected value: expected ({x},{y}) = {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")

################################################################################

def ref_idiv(x,y):
  if not (y[0] <= 0 and y[1] >= 0):
    return ref_imul(x,(1/y[1],1/y[0]))
  else:
    lt = ref_imul(x,(-float('Inf'),1/y[0]))
    rt = ref_imul(x,(1/y[1],float('Inf')))
    return (lt,rt)

@test
def test_idiv(fun):
    for i in range(25):
        x = sorted((prep_random(),prep_random()))
        y = sorted((prep_random(),prep_random()))
        expected = ref_idiv(x, y)
        actual = fun(x, y)
        if type(expected[0]) is tuple:
            for i in range(2):
                msg = assert_tuple(actual[i])
            if msg != None:
                print(msg)
                continue
            msg = assert_cartesian(expected[i], actual[i],
                                   f"Sum doesn't seem to match expected value: expected ({x},{y}) = {expected}, got {actual}.")
        else:
            msg = assert_tuple(actual)
            if msg != None:
                print(msg)
                return
            msg = assert_cartesian(expected, actual,
                                   f"Sum doesn't seem to match expected value: expected ({x},{y}) = {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")

################################################################################

def ref_iexp(a):
    from math import exp
    return (min(exp(a[0]),exp(a[1])),max(exp(a[0]),exp(a[1])))

@test
def test_iexp(fun):
    for i in range(25):
        x = sorted((prep_random(),prep_random()))
        expected = ref_iexp(x)
        actual = fun(x)
        msg = assert_tuple(actual)
        if msg != None:
            print(msg)
            return
        msg = assert_cartesian(expected, actual,
                               f"Sum doesn't seem to match expected value: expected e^{x} = {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")

################################################################################

def ref_ilog(a):
    from math import log
    return (min(log(a[0]),log(a[1])),max(log(a[0]),log(a[1])))

@test
def test_ilog(fun):
    for i in range(25):
        x = sorted((abs(prep_random()),abs(prep_random())))
        expected = ref_ilog(x)
        actual = fun(x)
        msg = assert_tuple(actual)
        if msg != None:
            print(msg)
            return
        msg = assert_cartesian(expected, actual,
                               f"Sum doesn't seem to match expected value: expected log {x} = {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")

################################################################################

def ref_ipow(a,b):
    from math import log
    if b % 2 != 1:  return
    return (a[0]**b,a[1]**b)

@test
def test_ipow(fun):
    for i in range(1,27,2):
        x = sorted((prep_random(),prep_random()))
        expected = ref_ipow(x,i)
        actual = fun(x,i)
        msg = assert_tuple(actual)
        if msg != None:
            print(msg)
            return
        msg = assert_cartesian(expected, actual,
                               f"Sum doesn't seem to match expected value: expected {x}^{i} = {expected}, got {actual}.")
        if msg != None:
            print(msg)
            return
    print("Success!")

################################################################################

print("Successfully loaded module.")

