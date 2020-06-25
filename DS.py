import random
import hashlib

from number_theory import *


class DS:
    def __init__(self, **kwargs):
        self.public_key, self.private_key = None, None
        self.keygen(**kwargs)

    def keygen(self, **kwargs):
        pass

    def signature(self, *args, **kwargs):
        pass

    def verify(self, *args, **kwargs):
        pass


class RSA(DS):
    def __init__(self, **kwargs):
        super(RSA, self).__init__(**kwargs)

    def keygen(self, **kwargs):
        """
                RSA keygen function
                set public key and private key from two input prime numbers
                """
        try:
            p, q = kwargs['p'], kwargs['q']
        except KeyError:
            return
        n = p * q
        phi_n = (p - 1) * (q - 1)
        # Select random e s.t. phi(n) and e are relatively prime
        while True:
            e = random.randint(2, 2 * phi_n)
            if is_relatively_prime(phi_n, e):
                break

        # Get multiplicative inverse of e mod phi(n)
        d = extended_euclid(e, phi_n)[1]

        self.public_key, self.private_key = (n, e), d

    def signature(self, m, hash_func=None):
        (n, _), d = self.public_key, self.private_key
        return modulo_power(m, d, n) if hash_func is None else modulo_power(hash_func(m), d, n)

    def verify(self, s, m, hash_func=None):
        n, e = self.public_key
        m_ = modulo_power(s, e, n)
        if hash_func is None:
            return m == m_
        else:
            return m_ == hash_func(m)


class ElGamal(DS):
    def __init__(self, **kwargs):
        super(ElGamal, self).__init__(**kwargs)

    def keygen(self, **kwargs):
        try:
            p, g = kwargs['p'], kwargs['g']
        except KeyError:
            return
        try:
            x = kwargs['x']
        except KeyError:
            x = random.randint(1, p - 1)
        y = modulo_power(g, x, p)
        self.public_key, self.private_key = (p, g, y), x

    def signature(self, m, k=None):
        (p, g, _), x = self.public_key, self.private_key
        if k is None:
            k = random.randint(1, p - 1)

        r = modulo_power(g, k, p)
        ks = (m - ((x * r) % (p - 1))) % (p - 1)
        _, k_inv = extended_euclid(k, p - 1)
        s = (ks * k_inv) % (p - 1)
        return r, s

    def verify(self, r, s, m):
        p, g, y = self.public_key
        left = (modulo_power(y, r, p) * modulo_power(r, s, p)) % p
        right = modulo_power(g, m, p)
        return left == right


if __name__ == '__main__':
    # DS: RSA
    ds_rsa = RSA(p=3, q=11)
    s = ds_rsa.signature(10)
    print(ds_rsa.verify(s, 10))

    # DS: ElGamal
    eg = ElGamal(p=23, g=7, x=9)
    r, s = eg.signature(20, 3)
    print(eg.verify(r, s, 20))
