#!/usr/bin/python3

import scrypt
import binascii
import getpass
from hashlib import sha512

def SlowKDF(password, salt, i):
    digest = password
    for counter in range(i):
        print ("Iteration %s from %s..." % (counter+1, i) )
        digest = scrypt.hash(digest, salt, N = 1048576, r = 8, p = 1, buflen = 128)
    return digest

mypass = getpass.getpass("Passphrase: ")

if mypass != getpass.getpass("Repeat passphrase: "):
    print ("ERROR: Passwords do not match.")
    quit()

if mypass != getpass.getpass("Repeat passphrase (again): "):
    print ("ERROR: Passphrases do not match.")
    quit()

mysalt = input("Salt: ")
mynumber = int(input("Number of iterations: "))

mypass = mypass.encode()
mysalt = mysalt.encode()

mydigest = SlowKDF(mypass, mysalt, mynumber)

print ("\n == Version 1 ==")

print ("\n\nDigest in hex format:", binascii.b2a_hex(mydigest).decode("utf-8"))

print ("\n\nDigest in base64 format:", binascii.b2a_base64(mydigest).decode("utf-8"))

print ("\n == Version 2 ==")

mydigest_v2 = sha512(mypass+mysalt+mydigest).digest()

print ("\n\nVersion 2 digest in hex format:", binascii.b2a_hex(mydigest_v2).decode("utf-8"))

print ("\n\nVersion 2 digest in base64 format:", binascii.b2a_base64(mydigest_v2).decode("utf-8"))

print ("\n == Version 1+2 ==")

mydigest_v1plus2=mydigest+mydigest_v2

print ("\n\nVersion 1+2 digest in hex format:", binascii.b2a_hex(mydigest_v1plus2).decode("utf-8"))

print ("\n\nVersion 1+2 digest in base64 format:", binascii.b2a_base64(mydigest_v1plus2).decode("utf-8"))
