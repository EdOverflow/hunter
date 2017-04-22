# Hunter

By @EdOverflow

# Table of Contents

1) Authentication
2) Cross-Site Request Forgery (CSRF)
	2.1) Generating CSRF tokens
3) Cross-Site Scripting (XSS)
	3.1) Reflected XSS
	3.2) Stored XSS
	3.3) Self-XSS
	3.4) DOM based XSS
4) Cryptography
	4.1) HTTPS
	4.2) Randomness
	4.3) Password Storage
	4.4) Timing Attacks
5) Denial of Service
6) Information Disclosure
7) SQL Injection
8) Unvalidated / Open Redirects
9) Best Practices

# 1) Authentication

# 2) Cross-Site Request Forgery (CSRF)

## 2.1) Generating CSRF tokens

# 3) Cross-Site Scripting (XSS)

Cross-site scripting (XSS) is a form of client-side code injection wherein one can execute malicious scripts into a page. XSS exists whenever input can be interpreted as code. In order to prevent XSS all input should be escaped server-side.

Cross-site scripting can be divided into 4 main categories:

* Reflected XSS
* Stored XSS
* Self-XSS
* DOM based XSS

## 3.1) Reflected XSS

Reflected XSS is non-persistent and executes in form of a request.

For example, you may see the following:

~~~
https://example.com/page?url=value
~~~

This vulnerable website does not escape nor validate the input and it is simply placed inside a link:

~~~html
<a href={{ url }}>Link</a>
~~~

Now if one submits the following we are prompted with an alert box display the value `1`:

~~~html
onload=alert(1)
~~~

## 3.2) Stored XSS

As the name already suggests, stored XSS means that the payload is stored in the page, for example, in form of a comment. This [self-retweeting tweet](https://twitter.com/dergeruhn/status/476764918763749376) used a stored XSS vulnerability to force people loading the page to retweet the tweet. 

The payload looked as follows:

~~~html
<script class="xss">
	$('.xss').parents().eq(1).find('a').eq(1).click();
	$('[data-action=retweet]').click();
	alert('XSS in Tweetdeck')
</script>♥
~~~

If you would like to find out how this payload works, please refer to the fantastic video by Tom Scott.

[![self-retweeting tweet](https://i.ytimg.com/vi/zv0kZKC6GAM/maxresdefault.jpg)](https://www.youtube.com/watch?v=zv0kZKC6GAM)

The [Samy worm](https://samy.pl/popular/tech.html) was also a form of stored XSS in MySpace.

## 3.3) Self-XSS

Self-XSS requires an attacker to convince (social engineer) the victim into executing the XSS. This form of XSS can neither be sent in form of a URL nor stored in a page.

## 3.4) DOM based XSS

**TODO:** Write about DOM based XSS.

## XSS mitigations

Django escapes certain characters by default, but there are exceptions which you should read up on here: https://docs.djangoproject.com/en/1.10/topics/security/#cross-site-scripting-xss-protection

In the case of Flask, they have implemented [Jinja2](http://jinja.pocoo.org/docs/dev/templates/#html-escaping) to escape input: http://flask.pocoo.org/docs/0.12/security/#cross-site-scripting-xss

In both frameworks it is very important to note that the mitigations put in place will not protect against attribute injection. Therefore, be sure to always quote your attributes with either double or single quotes.

**👎 Don't do this:**

`<a href={{ url }}>Link</a>`

**👍 Use this instead:**

`<a href="{{ url }}">Link</a>`

In particular, the Django docs demonstrate that it is possible to inject `'classname onmouseover=javascript:alert(1)'` into unquoted class attributes.

~~~
<style class={{ var }}>...</style>
~~~

If you would rather directly implement Jinja2, you can manually escape HTML by passing a value through `|e`.

~~~
{{ url|e }}
~~~ 

Another method is to escape with the `escape()` function.

~~~python
>>> from jinja2 import utils
>>> str(utils.escape("<h1>XSS</h1>"))
'&lt;h1&gt;XSS&lt;/h1&gt;'
~~~

# 4) Cryptography

## 4.1) HTTPS

## 4.2) Randomness

A PRNG is an algorithm used to produce random-looking numbers with certain desirable statistical properties. In order for a PRNG to be cryptographically secure it must be resistant to prediction.

### The random module

In order to produce cryptograpically secure strings you must ensure that you are using `random.SystemRandom` and not `random.choice`.

**👎 Don't use this:**

~~~python
''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
~~~

This uses the [Mersenne Twister](https://en.wikipedia.org/wiki/Mersenne_Twister), which is designed for simulation (Monte-Carlo simulation) and modeling, and is therefore not suitable for cryptographic purposes.

**👍 Use this instead:**

~~~python
''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
~~~

`random.SystemRandom` runs `os.urandom()` (as seen in the code snippet below), which uses the operating system's PRNG. On *nix machines that's `/dev/urandom` and `CryptGenRandom()` on Windows machines.

~~~python
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

### The secrets module

If you are running Python 3.6 and want to ensure you are using a CPRNG, please opt for the secrets module. `secrets.SystemRandom` is just an alias for `random.SystemRandom`. The reason behind creating this module was the fact that some developers were using `random.choice` and therefore by creating a module that only uses cryptographically secure functions there would be no way of making the same mistake. On top of that, for a very long time when looking for a random string generator in Python, the number one result was the following insecure method: http://stackoverflow.com/a/2257449.

In the secrets module's source code you can see that the SystemRandom class from the random module is imported as follows:

~~~python
from random import SystemRandom

_sysrand = SystemRandom()
~~~

Link to docs: https://docs.python.org/dev/library/secrets.html

Link to source code: https://hg.python.org/cpython/file/3.6/Lib/secrets.py

## 4.3) Password Storage

A hash function takes input of a variable length and outputs a fixed length sequence. Contrary to encryption, hashing is a one way function. This means you cannot "decrypt" the output of a hash function. In order to figure out whether the password is correct, one must first hash it and then compare it to the stored hash. The output of a hash function is often referred to as a "message digest".

When hashing passwords you want to use a **slow** hash function. That way the cost of brute forcing (i.e, trying all combinations) becomes too expensive to compute. You **should not** use MD5, because it is a fast hashing function. I recommend either using the bcrypt, scrypt or PBKDF2 [key derivation algorithms](https://github.com/crypto101/book/blob/master/Crypto101.org#key-derivation-functionskey-derivation-function). 

Another benefit of using the key derivation functions I mentioned above is that they have a built in salt. The salt is randomly generated for each password and then included in the hashing process. For example, in bcrypt you can see the salt in the digest:

~~~
$2a$10$I/NxkD0Qk1ElSoVzgWl/degIq0.AQ/KptUQAe9VKlzyZ2HnYsUjnW
~~~

The salt is: `I/NxkD0Qk1ElSoVzgWl/de`

**👎 Don't do this:**

Do **not** use the MD5 hash function for password hashing:

~~~python
from hashlib import md5


def bad_password_hashing():
	password = b"hunter2"
	hashed = md5(password).hexdigest()
	return hashed
~~~

Do **not** use any functions from the SHA family to hash passwords:

~~~python
from hashlib import sha256


def bad_password_hashing():
	password = b"hunter2"
	hashed = sha256(password).hexdigest()
	return hashed
~~~

**👍 Use this instead:**

Use the [bcrypt module](https://pypi.python.org/pypi/bcrypt/3.1.0):

~~~python
import bcrypt


def bcrypt_password():
    password = b"hunter2"
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if bcrypt.checkpw(password, hashed):
        print("It matches! :)")
    else:
        print("It does not match :(")
~~~

Use [scrypt](https://passlib.readthedocs.io/en/stable/index.html):

~~~python
from passlib.hash import scrypt


def scrypt_password():
    password = b"hunter2"
    hashed = scrypt.hash(password)
    if scrypt.verify(password, hashed):
        print("It matches! :)")
    else:
        print("It does not match :(")
~~~

Use [PBKDF2 with SHA-256](https://pythonhosted.org/passlib/lib/passlib.hash.pbkdf2_digest.html):

~~~python
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

## 4.4) Timing Attacks

Timing attacks are a type of side channel attack where one can discover valuable information by recording the time it takes for a cryptographic algorithm to execute.

**👎 Don't use this:**

~~~python
return "digest_abc" == "digest_xyz"
~~~

The `==` and `!=` operations do a byte-by-byte comparison of two values and as soon as the two differentiate they terminate. In the example above the operation returns when it detects `a` and `x` are the not the same. 

This means the longer it takes until the operation returns, the more correct characters the attacker has guessed.

In the `demo` folder you will find code that demonstrates a theoretical timing attack. When running the different operations we can clearly see we are getting hotter, since each iteration takes longer.

~~~
1482777135.5899296
1482777135.6195188
1482777135.6365209
~~~

**👍 Use this instead:**

~~~python
hmac.compare_digest(a, b)
~~~

The `compare_digest()` function does not terminate as soon as two bytes are not the same.

Many of the recommended password hashing modules listed in the "Password Storage" document come with a ready made time independent comparison function. The bcrypt package uses the `checkpw()` function.

~~~python
import bcrypt


def bcrypt_password():
    password = b"hunter2"
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if bcrypt.checkpw(password, hashed):
        print("It matches! :)")
    else:
        print("It does not match :(")
~~~

### Example bad implementation

The canton of Geneva open sourced their electronic voting system (CHVote) on [GitHub](https://github.com/republique-et-canton-de-geneve/chvote-1-0) requesting developers and security researchers to inspect the code. I reported a timing attack vulnerability to them responsibly via email. A day later, [@kAworu](https://github.com/kAworu) kindly submitted a [pull request](https://github.com/republique-et-canton-de-geneve/chvote-1-0/pull/10) to solve this issue.

The code is Java, but the same rules apply. CHVote was using a byte-by-byte comparison function for the MAC values.

~~~java
return Arrays.equals(knownMac, calculatedMac);
~~~

As noted in the response from the CHVote security team there were several other layers of defense in place which would have prevented this type of attack from being carried out.

Link to source code: https://github.com/republique-et-canton-de-geneve/chvote-1-0/blob/master/commons-base/commons-crypto/src/main/java/ch/ge/ve/commons/crypto/SensitiveDataCryptoUtils.java#L203

# 5) Denial of Service

# 6) Information Disclosure

# 7) SQL Injection

# 8) Unvalidated / Open Redirects

## 8.1) Reverse Tabnabbing

The following `<a href="https://example.com/" target="_blank">link</a>` is vulnerable to reverse tabnabbing, because it uses `target="_blank"`:

~~~html
<a href="https://example.com/" target="_blank">link</a>
~~~

This means the page that opens in a new tab can access the initial tab and change its location using the `window.opener` property.

In order to mitigate this issue, developers are encouraged to use `rel="nofollow noopener noreferrer"` as follows:

~~~html
<a href="https://example.com/" target="_blank" rel="nofollow noopener noreferrer">link</a>
~~~

Now when you click on this `<a href="https://example.com/" target="_blank" rel="nofollow noopener noreferrer">link</a>`, the attacker cannot access the initial tab.

For more on reverse tabnabbing, please refer to the following page: https://www.jitbit.com/alexblog/256-targetblank---the-most-underestimated-vulnerability-ever/

# 9) Best Practices