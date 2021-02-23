import random
from number_theory import *


def shor(N):
    while True:
        a = random.randint(1, N)
        print('a:', a)
        gcd, inv = extended_euclid(a, N)
        print('gcd:', gcd)
        if gcd != 1:
            return

        x = 1
        f = modulo_power(a, x, N)
        print('f:', f)
        r = 1
        while True:
            fr = modulo_power(a, x + r, N)
            print('fr:', fr, 'r:', r)
            if fr == f:
                break
            r += 1

        if r % 2 == 1:
            continue

        ar = modulo_power(a, r // 2, N)
        print('ar:', ar)
        if ar == N - 1:
            continue

        arp = a ** (r // 2) + 1
        arm = a ** (r // 2) - 1
        print(arp, arm)
        print(extended_euclid(arp, N))
        print(extended_euclid(arm, N))
        return

shor(77)