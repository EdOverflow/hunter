import bcrypt
from passlib.hash import scrypt, pbkdf2_sha256


def bcrypt_password():
    password = b"hunter2"
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if bcrypt.checkpw(password, hashed):
        print("It Matches!")
    else:
        print("It Does not Match :(")

def scrypt_password():
    password = b"hunter2"
    hashed = scrypt.hash(password)
    if scrypt.verify(password, hashed):
        print("It matches! :)")
    else:
        print("It does not match :(")

def pbkdf2_sha256_password():
    password = b"hunter2"
    hashed = pbkdf2_sha256.using(rounds=10000, salt_size=32).hash(password)
    if pbkdf2_sha256.verify(password, hashed):
        print("It matches! :)")
    else:
        print("It does not match :(")
