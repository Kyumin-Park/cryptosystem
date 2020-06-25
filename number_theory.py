def is_relatively_prime(a, b):
    if a < b:
        a, b = b, a
    while True:
        r = a % b
        if r == 0:
            break
        a, b = b, r
    return b == 1


def extended_euclid(number, divisor):
    x1, x2, x3 = 1, 0, divisor
    y1, y2, y3 = 0, 1, number

    while True:
        if y3 == 0:
            return x3, None
        if y3 == 1:
            return y3, y2 % divisor

        q = x3 // y3

        t1, t2, t3 = x1 - q * y1, x2 - q * y2, x3 - q * y3
        x1, x2, x3 = y1, y2, y3
        y1, y2, y3 = t1, t2, t3


def modulo_power(basis, exponent, divisor):
    c = 1
    while exponent > 0:
        exponent, r = divmod(exponent, 2)
        if r == 1:
            c = (c * basis) % divisor
        basis = (basis * basis) % divisor
    return c


if __name__ == '__main__':
    print(is_relatively_prime(4, 9))
    print(extended_euclid(246, 426))
    print(modulo_power(23, 3, 9))
