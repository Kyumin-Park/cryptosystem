import random

from number_theory import *


class PKC:
    def __init__(self, **kwargs):
        self.public_key, self.private_key = None, None
        self.keygen(**kwargs)

    def keygen(self, **kwargs):
        pass

    def encrypt(self, *args, **kwargs):
        pass

    def decrypt(self, *args, **kwargs):
        pass


class RSA(PKC):
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

    def encrypt(self, M):
        """
        Encrypt Message with generated key
        :param M: Message
        :return: Encrypted message
        """
        n, e = self.public_key
        return modulo_power(M, e, n)

    def decrypt(self, C):
        """
        Decrypt encrypted message with generated key
        :param C: Encrypted message
        :return: Decrypted message
        """
        d, (n, _) = self.private_key, self.public_key
        return modulo_power(C, d, n)


class ElGamal(PKC):
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

    def encrypt(self, m, k=None):
        p, g, y = self.public_key
        if k is None:
            k = random.randint(1, p - 1)
        C1 = modulo_power(g, k, p)
        C2 = (m * modulo_power(y, k, p)) % p
        return C1, C2

    def decrypt(self, C1, C2):
        (p, _, _), x = self.public_key, self.private_key
        _, C1_inv = extended_euclid(C1, p)
        C1_inx_x = modulo_power(C1_inv, x, p)
        m = (C2 * C1_inx_x) % p
        return m


if __name__ == '__main__':
    # RSA
    rsa = RSA(p=3, q=11)
    C = rsa.encrypt(M=5)
    M = rsa.decrypt(C=C)
    print(M, C)

    # Elgamal
    eg = ElGamal(p=23, g=7, x=9)
    c1, c2 = eg.encrypt(20, 3)
    m = eg.decrypt(c1, c2)
    print(eg.private_key, eg.public_key)
    print(c1, c2, m)
