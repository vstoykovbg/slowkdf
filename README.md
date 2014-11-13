Slow KDF
========

Slow KDF for serious key stretching based on Scrypt.

You need to install `scrypt` before to use this program:
```
$ pip install --user scrypt
```
Warning: your computer may freeze if you run this program (if you have too little available RAM). It requires about 1GB of free RAM.

<a href="http://en.wikipedia.org/wiki/Magic_SysRq_key" target="_blank">See here</a> how to take control of your Linux if X freezes.

<img src="http://i.imgur.com/qdpSWw4.png" alt="" />

Why?
====

The problem is: popular cryptographic tools have laughable key stretching functionality.

How many seconds after you enter wrong passwords you get response "bad password", while using LUKS, TrueCrypt, GnuPG? Less than a second? Two seconds? Do you think that this is enogh?

See this example:

```$ gpg -vv -c --force-mdc --s2k-mode 3 --s2k-count 65011712 --s2k-digest-algo SHA512 --cipher-algo TWOFISH MyFile.txt```

* hashes the password using SHA512
* key-stretches the hash 65 million times
* and encrypts the file data using the Twofish cipher with a 256-bit key

```
$ time gpg --output clear.txt  -vv -d MyFile.txt.gpg
:symkey enc packet: version 4, cipher 10, s2k 3, hash 10
        salt ef1ae7a1f536715c, count 65011712 (255)
gpg: TWOFISH encrypted data
:encrypted data packet:
        length: unknown
        mdc_method: 2
gpg: encrypted with 1 passphrase
:compressed packet: algo=1
:literal data packet:
        mode b (62), created 1415914804, name="MyFile.txt",
        raw data: 7780 bytes
gpg: original file name='MyFile.txt'
gpg: decryption okay

real    0m2.684s
user    0m1.105s
sys     0m0.004s
```

It takes about 1 second to decrypt the file after I wrote correct password!

With wrong password it takes about 1 second:

```
:symkey enc packet: version 4, cipher 10, s2k 3, hash 10
        salt ef1ae7a1f536715c, count 65011712 (255)
gpg: TWOFISH encrypted data
:encrypted data packet:
        length: unknown
        mdc_method: 2
gpg: encrypted with 1 passphrase
gpg: decryption failed: bad key

real    0m2.769s
user    0m1.144s
sys     0m0.004s
```

From the `man gpg`:

``
 -s2k-count n
    Specify how many times the passphrase mangling is repeated.  This value may range between 1024 and
    65011712  inclusive.   The  default  is  inquired from gpg-agent.  Note that not all values in the
    1024-65011712 range are legal and if an illegal value is selected, GnuPG  will  round  up  to  the
    nearest legal value.  This option is only meaningful if --s2k-mode is 3.
``

So, you can't enter number greater than 65011712 <b>without modifying the source code</b>.

The same weak key stretching is used for protecting your GnuPG/PGP private keys!

To see your `s2k-count`, type this command:

```
$ gpg --list-packets ~/.gnupg/secring.gpg | grep count
        protect count: 65536 (96)
        protect count: 65536 (96)
        protect count: 65536 (96)
        protect count: 65536 (96)
```

In this example the `s2k-count` is 65536 (default).

<img src="http://i.imgur.com/K6dAvXn.jpg" alt="It's a conspiracy!" />

<blockquote>
<p>PBKDF2, just like TrueCrypt?  I hope you decide to have better password 
security than those guys.  The PBKDF2 key stretching in TrueCrypt is a 
joke.  You have to find an obscure option to even enable the 2000-round 
SHA256 key stretching, which provides close to no security at all.  The 
kinds of passwords your users on Facebook will actually use have very 
few bits of entropy, and can be guessed by hardware based brute force 
attacks very quickly.</p>
(...)
<p>Now for my tin hat conspiracy theories: Why is Microsoft so stupid about 
where to perform key stretching?  Why wont the TrueCrypt team adopt 
decent password security?  Why does PGP have 0 key stretching by 
default, and why is my SSH private key encrypted with no key stretching 
and no option to use it?  You want to encrypt Facebook traffic with real 
security?  I just have to wonder if some tall suits with dark sunglasses 
are going to convince you to do otherwise.  My other theory is people 
are really that stupid, whether they write SSH encryption code, PGP, or 
TrueCrypt.</p><cite><a target="_blank" href="http://www.metzdowd.com/pipermail/cryptography/2013-December/019048.html">Bill Cox</a></cite></blockquote>


