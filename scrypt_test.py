#!/usr/bin/python3


import binascii
import getpass
import time

# pip3 install scrypt
import scrypt as scrypt_locally_installed 

from hashlib import scrypt as scrypt_from_hashlib

#from Crypto.Protocol.KDF import scrypt as scrypt_from_Crypto

from Cryptodome.Protocol.KDF import scrypt as scrypt_from_pyCryptodome

from cryptography.hazmat.primitives.kdf import scrypt as scrypt_from_hazmat
from cryptography.hazmat.backends import default_backend

import importlib.util
spec = importlib.util.spec_from_file_location("scrypt", "/usr/lib/python3/dist-packages/scrypt.py")
scrypt_old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scrypt_old)

mypass = "password"

mysalt = "salt"
iterations = 1
memory = 1048576
#memory = 64*1024

mypass = mypass.encode()
mysalt = mysalt.encode()

#print ("Version of scrypt:", scrypt.__version__)

# ******************************************************************************************
digest=mypass

print ("**** Testing with Scrypt from scrypt...")
print ("File of locally installed scrypt:", scrypt_locally_installed.__file__)

# ******** Time **********
start = time.time()

for counter in range(iterations):
    print ("Iteration %s from %s..." % (counter+1, iterations) )
    digest = scrypt_locally_installed.hash(digest, mysalt, N = memory, r = 8, p = 1, buflen = 128)

# ******** Time **********
end = time.time()
print ("*** Time: ", end - start, "**********************************************")
print ("Digest in base64 format:", binascii.b2a_base64(digest).decode("utf-8"))

print ("\n\n")
# ******************************************************************************************
digest=mypass

print ("**** Testing with Scrypt from scrypt (old version)...")
print ("File of scrypt:", scrypt_old.__file__)

# ******** Time **********
start = time.time()

for counter in range(iterations):
    print ("Iteration %s from %s..." % (counter+1, iterations) )
    digest = scrypt_old.hash(digest, mysalt, N = memory, r = 8, p = 1, buflen = 128)

# ******** Time **********
end = time.time()
print ("*** Time: ", end - start, "**********************************************")
print ("Digest in base64 format:", binascii.b2a_base64(digest).decode("utf-8"))

print ("\n\n")
# ******************************************************************************************
digest=mypass

print ("**** Testing with Scrypt from Cryptodome...")
# ******** Time **********
start = time.time()

for counter in range(iterations):
    print ("Iteration %s from %s..." % (counter+1, iterations) )
    digest = scrypt_from_pyCryptodome(digest, mysalt, key_len=128, N=memory, r=8, p=1)

# ******** Time **********
end = time.time()
print ("*** Time: ", end - start, "**********************************************")
print ("Digest in base64 format:", binascii.b2a_base64(digest).decode("utf-8"))

print ("\n\n")
# ******************************************************************************************


# ******************************************************************************************
digest=mypass

print ("**** Testing with Scrypt from hashlib...")
# ******** Time **********
start = time.time()

for counter in range(iterations):
    print ("Iteration %s from %s..." % (counter+1, iterations) )
    digest = scrypt_from_hashlib(password=digest, salt=mysalt, n=memory, r=8, p=1, maxmem=2147483646, dklen=128)

#ValueError: maxmem must be positive and smaller than 2147483647

# ******** Time **********
end = time.time()
print ("*** Time: ", end - start, "**********************************************")
print ("Digest in base64 format:", binascii.b2a_base64(digest).decode("utf-8"))

print ("\n\n")
# ******************************************************************************************




# ******************************************************************************************
digest=mypass

print ("**** Testing with Scrypt from hazmat...")
# ******** Time **********
start = time.time()

for counter in range(iterations):
    print ("Iteration %s from %s..." % (counter+1, iterations) )
#   digest = scrypt_from_hashlib(password=digest, salt=mysalt, n=memory, r=8, p=1, maxmem=2147483646, dklen=128)
    backend = default_backend()
    kdf = scrypt_from_hazmat.Scrypt(salt=mysalt, length=128, n=memory, r=8, p=1, backend=backend)
    digest = kdf.derive(digest)


# ******** Time **********
end = time.time()
print ("*** Time: ", end - start, "**********************************************")
print ("Digest in base64 format:", binascii.b2a_base64(digest).decode("utf-8"))

print ("\n\n")
# ******************************************************************************************
