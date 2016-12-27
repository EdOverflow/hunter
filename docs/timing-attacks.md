# Timing Attacks

Timing attacks are a type of side channel attack where one can discover valuable information by recording the time it takes for a cryptographic algorithm to execute.

### 👎 Don't use this:

~~~
return "digest_abc" == "digest_xyz"
~~~

The `==` and `!=` operations do a byte-by-byte comparison of two values and as soon as the two differentiate they terminate. In the example above the operation returns when it detects `a` and `x` are the not the same. 

This means the longer it takes until the operation returns, the more correct characters the attacker has guessed.

### 👍 Use this instead:

~~~
hmac.compare_digest(a, b)
~~~

The `compare_digest()` function does not terminate as soon as two bytes are not the same.

Many of the recommended password hashing modules listed in the "Password Storage" document come with a ready made time independent comparison function. The bcrypt package uses the `checkpw()` function.

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

## Example bad implementation

The canton of Geneva open sourced their electronic voting system (CHVote) on [GitHub](https://github.com/republique-et-canton-de-geneve/chvote-1-0) requesting developers and security researchers to inspect the code. I reported a timing attack vulnerability to them responsibly via email. A day later, [@kAworu](https://github.com/kAworu) kindly submitted a [pull request](https://github.com/republique-et-canton-de-geneve/chvote-1-0/pull/10) to solve this issue.

The code is Java, but the same rules apply. CHVote was using a byte-by-byte comparison function for the MAC values.

~~~
return Arrays.equals(knownMac, calculatedMac);
~~~

As noted in the response from the CHVote security team there were several other layers of defense in place which would have prevented this type of attack from being carried out.

Link to source code: https://github.com/republique-et-canton-de-geneve/chvote-1-0/blob/master/commons-base/commons-crypto/src/main/java/ch/ge/ve/commons/crypto/SensitiveDataCryptoUtils.java#L203