# Password Storage

A hash function takes input of a variable length and outputs a fixed length sequence. Contrary to encryption, hashing is a one way function. This means you cannot "decrypt" the output of a hash function. In order to figure out whether the password is correct, one must first hash it and then compare it to the stored hash. The output of a hash function is often referred to as a "message digest".

When hashing passwords you want to use a **slow** hash function. That way the cost of brute forcing (i.e, trying all combinations) becomes too expensive to compute. You **should not** use MD5, because it is a fast hashing function. I recommend either using the bcrypt, scrypt or PBKDF2 [key derivation algorithms](https://github.com/crypto101/book/blob/master/Crypto101.org#key-derivation-functionskey-derivation-function). 

Another benefit of using the key derivation functions I mentioned above is that they have a built in salt. The salt is randomly generated for each password and then included in the hashing process. For example, in bcrypt you can see the salt in the digest:

~~~
$2a$10$I/NxkD0Qk1ElSoVzgWl/degIq0.AQ/KptUQAe9VKlzyZ2HnYsUjnW
~~~

The salt is: `I/NxkD0Qk1ElSoVzgWl/de`

### 👎 Don't do this

Do **not** use the MD5 hash function for password hashing:

~~~
from hashlib import md5


def bad_password_hashing():
	password = b"hunter2"
	hashed = md5(password).hexdigest()
	return hashed
~~~

Do **not** use any functions from the SHA family to hash passwords:

~~~
from hashlib import sha256


def bad_password_hashing():
	password = b"hunter2"
	hashed = sha256(password).hexdigest()
	return hashed
~~~

### 👍 Use this instead

**Use the [bcrypt module](https://pypi.python.org/pypi/bcrypt/3.1.0):**

~~~
import bcrypt


def bcrypt_password():
    password = b"hunter2"
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if bcrypt.checkpw(password, hashed):
        print("It matches! :)")
    else:
        print("It does not match :(")
~~~

**Use [scrypt](https://passlib.readthedocs.io/en/stable/index.html):**

~~~
from passlib.hash import scrypt


def scrypt_password():
    password = b"hunter2"
    hashed = scrypt.hash(password)
    if scrypt.verify(password, hashed):
        print("It matches! :)")
    else:
        print("It does not match :(")
~~~

**Use [PBKDF2 with SHA-256](https://pythonhosted.org/passlib/lib/passlib.hash.pbkdf2_digest.html):**

~~~
from passlib.hash import pbkdf2_sha256


def pbkdf2_sha256_password():
    password = b"hunter2"
    hashed = pbkdf2_sha256.using(rounds=10000, salt_size=32).hash(password)
    if pbkdf2_sha256.verify(password, hashed):
        print("It matches! :)")
    else:
        print("It does not match :(")
~~~

Since we are using SHA-256 for PBKDF2 we must ensure that the salt is the same length as the output size of SHA-256 (i.e., 32 bytes) and that we are using the recommended 10'000 rounds.