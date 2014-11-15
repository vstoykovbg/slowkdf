#!/usr/bin/python2

import scrypt
import binascii
import getpass

def SlowKDF(password, salt, max_counter):
    counter = 0
    digest = password
    while counter < max_counter:
      counter += 1
      print "Iteration %s from %s..." % (counter, max_counter)
      digest = scrypt.hash(digest, salt, N = 1048576, r = 8, p = 1, buflen = 128)
    return digest

mypass = getpass.getpass()

if mypass != getpass.getpass("Password (again): "):
  print "Wrong password."
  quit()

if mypass != getpass.getpass("Password (and again): "):
  print "Wrong password."
  quit()

mysalt = raw_input("Salt: ")
mynumber = int(input("Number of iterations: "))

mydigest = SlowKDF(mypass, mysalt, mynumber)

print "\n\nDigest in hex format:", binascii.b2a_hex(mydigest)

print "\n\nDigest in base64 format:", binascii.b2a_base64(mydigest)
