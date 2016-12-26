from hashlib import md5, sha256


def bad_password_hashing_md5():
	password = b"hunter2"
	hashed = md5(password).hexdigest()
	return hashed

def bad_password_hashing_sha256():
	password = b"hunter2"
	hashed = md5(password).hexdigest()
	return hashed
