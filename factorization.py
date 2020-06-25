import math


def factor_base(B):
    """
    Find prime numbers less than bound B
    Used Eratosthenes' sieve
    :return: list of prime number less than B
    """
    prime_list = list(range(2, B))
    idx = 0
    while idx < len(prime_list):
        prime = prime_list[idx]
        prime_list = prime_list[:idx + 1] + [n for n in prime_list[idx + 1:] if n % prime != 0]
        idx += 1
    return prime_list


def factorize(primes, n):
    """
    Factorize n as a compound of prime numbers in PRIMES list
    :param primes: list of prime numbers
    :param n: integer to be factorized
    :return: list of factorized primes [(prime, coordinate), ...]
    """
    factor = []
    for prime in primes:
        ex = 0
        while n % prime == 0:
            ex += 1
            n = n // prime
        if ex != 0:
            factor.append((prime, ex))

    return factor if n == 1 else None


def quadratic_sieve(n, B):
    m = math.floor(math.sqrt(n))
    primes = factor_base(B)

    def Q(x):
        return (m + x) ** 2 - n

    cnt = 0
    x = 0
    while True:
        q = Q(x)
        x += 1
        if q < 0:
            factors = factorize(primes, -q)
            result = [(-1, 1)]
        else:
            factors = factorize(primes, q)
            result = []
        if factors is not None:
            print(f'Q(x): {q}, factors: {result + factors}')
            cnt += 1

        if cnt == len(primes):
            break


if __name__ == '__main__':
    # Naive factorization
    prime = factor_base(10)
    print(factorize(prime, 500))

    # Quadratic Sieve
    quadratic_sieve(493, 20)
