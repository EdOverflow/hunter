import time
import string


characters = string.ascii_lowercase
test_string = 'digest_'
for c in characters:
    if test_string != "digest_xyz":
        print(time.time())
        test_string += c
