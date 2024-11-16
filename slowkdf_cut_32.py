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

mydigest_v2 = sha512(mypass+mysalt+mydigest).digest()

base64_v2 = binascii.b2a_base64(mydigest_v2).decode("utf-8")
base64_v2_cut_32 = base64_v2[:32]

print ("\n\nVersion 2 digest in base64 format, first 32 characters:", base64_v2_cut_32)


