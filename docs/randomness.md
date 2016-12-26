# Randomness

A PRNG is an algorithm used to produce random-looking numbers with certain desirable statistical properties. In order for a PRNG to be cryptographically secure it must be resistant to prediction.

## The random module

In order to produce cryptograpically secure strings you must ensure that you are using `random.SystemRandom` and not `random.choice`.

### 👎 Don't use this:

~~~
''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
~~~

This uses the [Mersenne Twister](https://en.wikipedia.org/wiki/Mersenne_Twister), which is designed for simulation (Monte-Carlo simulation) and modeling, and is therefore not suitable for cryptographic purposes.

### 👍 Use this instead:

~~~
''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
~~~

`random.SystemRandom` runs `os.urandom()` (as seen in the code snippet below), which uses the operating system's PRNG. On *nix machines that's `/dev/urandom` and `CryptGenRandom()` on Windows machines.

~~~
def random(self):
        """Get the next random number in the range [0.0, 1.0)."""
        return (long(_hexlify(_urandom(7)), 16) >> 3) * RECIP_BPF

def getrandbits(self, k):
    """getrandbits(k) -> x.  Generates a long int with k random bits."""
    if k <= 0:
        raise ValueError('number of bits must be greater than zero')
    if k != int(k):
        raise TypeError('number of bits should be an integer')
    bytes = (k + 7) // 8
    x = long(_hexlify(_urandom(bytes)), 16)
    return x >> (bytes * 8 - k)  
~~~

Link to docs: https://docs.python.org/2/library/random.html
Link to source code: https://hg.python.org/cpython/file/2.7/Lib/random.py#l805

## The secrets module

If you are running Python 3.6 and want to ensure you are using a CPRNG, please opt for the secrets module. `secrets.SystemRandom` is just an alias for `random.SystemRandom`. The reason behind creating this module was the fact that some developers were using `random.choice` and therefore by creating a module that only uses cryptographically secure functions there would be no way of making the same mistake. On top of that, for a very long time when looking for a random string generator in Python, the number one result was the following insecure method: http://stackoverflow.com/a/2257449.

In the secrets module's source code you can see that the SystemRandom class from the random module is imported as follows:

~~~
from random import SystemRandom

_sysrand = SystemRandom()
~~~

Link to docs: https://docs.python.org/dev/library/secrets.html
Link to source code: https://hg.python.org/cpython/file/3.6/Lib/secrets.py