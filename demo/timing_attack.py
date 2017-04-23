import time, hmac


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap

@timing
def timing_attack_diff_tokens():
    token_1 = "100000000000000000000000000000000"
    token_2 = "000000000000000000000000000000001"
    for i in range(200):
        if not token_1 == token_2:
            print i

@timing
def timing_attack_same_tokens():
    token_1 = "100000000000000000000000000000000"
    token_2 = "100000000000000000000000000000000"
    for i in range(200):
        if token_1 == token_2:
            print i

@timing
def constant_time_diff_tokens():
    token_1 = b"100000000000000000000000000000000"
    token_2 = b"000000000000000010000000000000000"
    for i in range(200):
        if not hmac.compare_digest(token_1, token_2):
            print i
        
@timing
def constant_time_same_tokens():
    token_1 = b"100000000000000000000000000000000"
    token_2 = b"100000000000000000000000000000000"
    for i in range(200):
        if hmac.compare_digest(token_1, token_2):
            print i

timing_attack_diff_tokens()
timing_attack_same_tokens()
constant_time_diff_tokens()
constant_time_same_tokens()