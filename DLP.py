import math
import random

from number_theory import *
from factorization import *


def baby_giant(p, a, b):
    """
    Implementation of Baby step Giant step algorithm
    followed p27-28 instructions
    :param p: modulo divisor
    :param a: exponential base
    :param b: modulus calculation equivalent value
    :return: x = log_a (b) mod p (a.k.a. a^x = b mod p)
    """
    # Build L1, L2 list
    m = math.ceil(math.sqrt(p - 1))
    print('1. a = {}, b = {}, m = ceil(sqrt({})) = {}\n'.format(a, b, p - 1, m),
          '2. a^{} mod {} = {}'.format(m, p, modulo_power(a, m, p)))

    L1 = [(j, modulo_power(a, m * j, p)) for j in range(m)]
    L2 = [(i, (b * extended_euclid(modulo_power(a, i, p), p)[1]) % p) for i in range(m)]
    # print('3. ordered pairs L1\n',
    #       '\t{}\n'.format(L1),
    #       '4. ordered pairs L2\n',
    #       '\t{}\n'.format(L2))

    # Sort L1, L2 in ascending order of second coordinate
    L1.sort(key=lambda x: x[1])
    L2.sort(key=lambda x: x[1])

    # Finding pair function
    # Increase index of smaller-valued list
    def find_pair():
        idx1, idx2 = 0, 0
        while idx1 < len(L1) and idx2 < len(L2):
            y1, y2 = L1[idx1][1], L2[idx2][1]
            if y1 == y2:
                print('5. find match {} in L1 and {} in L2\n'.format(L1[idx1], L2[idx2]))
                return L1[idx1][0], L2[idx2][0]
            elif y1 < y2:
                idx1 += 1
            else:
                idx2 += 1
        return None, None

    # Find matching pair
    j, i = find_pair()
    if (i, j) is (None, None):
        return None

    # Calculate x value
    x = (m * j + i) % (p - 1)
    print('6. log_{}({}) = {} x {} + {} = {}\n'.format(a, b, m, j, i, x),
          '7. (Confirmation) {} ^ {} = {} mod {}\n'.format(a, x, modulo_power(a, x, p), p))
    return x


def solve_linear(linear_relations, p, prime_list, g):
    """
    Solve linear problem by filling solution one-by-one
    get solution first from problem with single variable, then extend to multi-variable problem
    ex) 1. solve ax = b mod p
        2. solve cx + dy = e mod p
        ...
    :param linear_relations: Linear relations to be solved
    :param p: modulo divisor
    :param prime_list: list of prime numbers to be solved as variable
                       ex) [2, 3] -> solve for [log_g(2), log_g(3)]
    :param g: exponent basis
    :return: dictionary of solution
             ex) { 2: 1, 3: 72 } -> log_g(2) = 1 mod p, log_g(3) = 72 log p
    """
    # Declare solution dictionary
    solution = {prime: None for prime in prime_list}
    for relation, k in linear_relations:
        # If all solution computed: finish to solve
        if all([v is not None for v in solution.values()]):
            break

        unsolved = relation.copy()
        # Substitute variables that solved by prior relations
        for prime, val in solution.items():
            if val is None:
                continue

            for log, a in relation:
                if prime == log:
                    k -= a * val
                    while k < 0:
                        k += p
                    unsolved.remove((log, a))

        # Solve relation for single-variable relation
        if len(unsolved) == 1:
            prime, a = unsolved[0]
            tmp = k if prime == g else k + p
            while tmp % a != 0:
                tmp += p
            solution[prime] = (tmp // a) % p

    return solution


def index_calculus(p, g, y, B):
    """
    Index Calculus implementation, following slide p29-30
    :param p: modulo divisor
    :param g: exponent basis
    :param y: exponent result
    :param B: prime number boundary
    :return: x = log_g(y) mod p, s.t. y = g^x mod p
    """
    # Get list of prime numbers
    prime_list = factor_base(B)
    linear_relations = []
    print('Index Calculus Algorithm\n',
          '1. Factor base S = {} when B = {}\n'.format(prime_list, B))

    # Collect sufficient linear relations
    for k in range(1, y + 1):
        g_k = modulo_power(g, k, p)
        cnt = 0
        # Try modulo factorization, until g_k + 10 * p
        while factorize(prime_list, g_k) is None or cnt == 10:
            g_k += p
            cnt += 1
        factor = factorize(prime_list, g_k)
        if factor is not None:
            linear_relations.append((factor, k))

    print('2. Collect Linear relations')
    for i, (factor, k) in enumerate(linear_relations):
        output_str = ' * '.join(['{}^{}'.format(pr, ai) for pr, ai in factor])
        print('\t{}^{} = {} mod {}'.format(g, k, output_str, p))

    # Sort linear relations by number of variables included, then solve linear equations
    linear_relations.sort(key=lambda x: len(x[0]))
    log_prime = solve_linear(linear_relations, p - 1, prime_list, g)
    print('3. Find logarithms of elements in S solving the linear relations\n')
    for pr, l in log_prime.items():
        print('\tlog_{}({}) = {}\n'.format(g, pr, l))

    # Get random number until factorization succeed
    while True:
        r = random.randint(2, p)

        ygr = (y * modulo_power(g, r, p)) % p
        factor_ygr = factorize(prime_list, ygr)
        if factor_ygr:
            break

    # Compute x by summing factorized prime numbers
    x = sum([log_prime[pr] * a for pr, a in factor_ygr]) - r
    while x < 0:
        x += (p - 1)
    x %= p - 1

    x_factor_str = ' * '.join(['{}^{}'.format(pr, ex) for pr, ex in factor_ygr])
    x_log_str = ' + '.join(['{}*log_{}({})'.format(ex, g, pr) for pr, ex in factor_ygr])
    print('4. Find x\n',
          '\t{} * {}^{} = {} mod {}\n'.format(y, g, r, x_factor_str, p),
          '\tlog_{}({}) = -{} + {} mod {} = {}\n'.format(g, y, r, x_log_str, p, x),
          'Solution (Confirmation): {}^{} mod {} = {}\n'.format(g, x, p, y))
    return x


if __name__ == '__main__':
    # Baby step-Giant step
    # baby_giant(p=809, a=3, b=500)

    # Index Calculus
    index_calculus(p=101, g=2, y=17, B=10)