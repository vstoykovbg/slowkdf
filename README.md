Slow KDF
========

Slow KDF for serious key stretching based on Scrypt.

You need to install `scrypt` before to use this program:
```
$ pip install --user scrypt
```

If you prefer the version written in Python 3:

```
$ sudo apt-get install python3-pip
```

```
$ pip3 install --user scrypt
```
Warning: your computer may freeze if you run this program (if you have too little available RAM). It requires about 1GB of free RAM.

<a href="http://en.wikipedia.org/wiki/Magic_SysRq_key" target="_blank">See here</a> how to take control of your Linux if X freezes.

<img src="http://i.imgur.com/qdpSWw4.png" alt="" />

Updated version
====

The difference between v1 and v2 digest is that v2 is protected against hypothetical loss of entropy (due to repeated hashing with scrypt) with additional `sha512(key+salt+digest_v1)`.

I recommend using the `Version 2 digest in base64 format` or `Version 1+2 digest in base64 format` (if your application allow such long passwords - GnuPG 2 does not allow, you may use GnuPG 1!).

Why?
====

The problem is: popular cryptographic tools have laughable key stretching functionality.

How many seconds after you enter wrong passwords you get response "bad password", while using LUKS, TrueCrypt, GnuPG? Less than a second? Two seconds? Do you think that this is enogh?

WTF? There is a huge bug in GnuPG - your private keys are not protected by the desired key stretching: <a href="https://www.reddit.com/r/crypto/comments/6y0eug/dsa_keys_may_be_between_1024_and_3072_bits_long/dmkeke8/">I know this really needs to be super clear for everyone to see. Due to a bug, GPG completely ignored your S2K settings and isn't giving you the protection you asked for.</a>

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
=====

To see your `s2k-count`, type this command:

```
$ gpg --list-packets ~/.gnupg/secring.gpg | grep count
        protect count: 65536 (96)
        protect count: 65536 (96)
        protect count: 65536 (96)
        protect count: 65536 (96)
```

In this example the `s2k-count` is 65536 (default).


<blockquote>
<p>The reason you can't make an S2K count over 65,011,712 is because values higher than that cannot be encoded into a single byte which is what RFC 4880 requires.

<p>https://tools.ietf.org/html/rfc4880#section-3.7.1.3

<p>Your problem is not with GnuPG, but with OpenPGP.

<p>You could propose or implement a new S2K specifier type however: https://tools.ietf.org/html/rfc4880#section-10.1

<p><cite><a href="http://www.reddit.com/r/crypto/comments/2m86df/gnupgs_key_stretching_is_laughable/cm2b9ep">/u/mitchellrj</a></cite>
</blockquote>

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

Changes to the key with GnuPG 1 are invisible to GnuPG 2!
========

I tested it. First, I changed the password of my key with gpg (GnuPG 1) and then tried to use gpg2. I confirmed that the two programs now require different passwords for the same key.

Then, I also changed the password with gpg2. These changes are seen only by gpg2.

Discussion on Reddit: https://www.reddit.com/r/sysadmin/comments/6rzrut/changes_to_the_key_with_gnupg_1_are_invisible_to/

Please make sure that you are not keeping or exporting (backing up) the other version of your key with a weaker password!

GnuPG 2.1.11 does not accept long passwords
========

In my version of GnuPG it does not accept passwords longer than 255 characters (ASCII). Just tested it again. It says:

    Passphrase too long

My software versions:

    gpg (GnuPG) 2.1.11
    libgcrypt 1.6.5
    pinentry-gnome3 (pinentry) 0.9.7
    Ubuntu 16.04.3 LTS

The old version of GnuPG (`gpg (GnuPG) 1.4.20`) works fine.

Conspirologists would say that this is part of the conspiracy to undermine the security of the popular open source security-related applications.

Read more about the conspiracy-relate stuff on Google: https://www.google.com/search?q=NSA%27s%20Decade-Long%20Plan%20to%20Undermine%20Encryption

Workaround of the password length problem
========

You can use some hash function like sha512:

    echo -n "my loooooooong password" | sha512sum

Don't forget the `-n` part, because it gives different result:

    valentin@computer:~$ echo -n "my loooooooong password" | sha512sum
    f3a56f8ec032ea6d27f4ceff68e36ce9d25fc7042c737f2e4785f47d8267b5f3836987a0714921a8cc3f61dc1861523e92425ecdb90b522a81e0c82f4c5a224b  -
    valentin@computer:~$ echo "my loooooooong password" | sha512sum
    d7cbfb4629b661eef421474817587be5a6c7d96599f43638d32252ec88ba657314ba2dcb9c47bd2eeb6a24c8a9620f37ce570496eb758a6ae19ac30ef988eea4  -
    valentin@computer:~$ 

Example
========

    valentin@computer:~$ slowkdf.py 
    Passphrase: 
    Repeat passphrase: 
    Repeat passphrase (again): 
    Salt: salt
    Number of iterations: 1
    Iteration 1 from 1...

     == Version 1 ==


    Digest in hex format: ea6a7a27acbb972a6c280d12cbd63fb60b37bc666bf368ea58edaac7e08a41063fa00aac7206e183dd2fdd64db01636668182fc2f145f67f45f4588f32742bfd24cf3131462792b228a11522a0d8d65609be1d47a8a1ccc4098b6491f2be0b769eafca253812bf408f493e05210cc0e80b3de496dcc854e98976c4b7763c6551


    Digest in base64 format: 6mp6J6y7lypsKA0Sy9Y/tgs3vGZr82jqWO2qx+CKQQY/oAqscgbhg90v3WTbAWNmaBgvwvFF9n9F9FiPMnQr/STPMTFGJ5KyKKEVIqDY1lYJvh1HqKHMxAmLZJHyvgt2nq/KJTgSv0CPST4FIQzA6As95JbcyFTpiXbEt3Y8ZVE=


     == Version 2 ==


    Version 2 digest in hex format: b3d17366ac96465cbcaa843950dd9d77999055861f3550a11d61cb895cb54fc9d78c56dd6d053093fa43cfaa2eed628effa3555ee4f7a2adc4d068dc4004b5cf


    Version 2 digest in base64 format: s9FzZqyWRly8qoQ5UN2dd5mQVYYfNVChHWHLiVy1T8nXjFbdbQUwk/pDz6ou7WKO/6NVXuT3oq3E0GjcQAS1zw==


     == Version 1+2 ==


    Version 1+2 digest in hex format: ea6a7a27acbb972a6c280d12cbd63fb60b37bc666bf368ea58edaac7e08a41063fa00aac7206e183dd2fdd64db01636668182fc2f145f67f45f4588f32742bfd24cf3131462792b228a11522a0d8d65609be1d47a8a1ccc4098b6491f2be0b769eafca253812bf408f493e05210cc0e80b3de496dcc854e98976c4b7763c6551b3d17366ac96465cbcaa843950dd9d77999055861f3550a11d61cb895cb54fc9d78c56dd6d053093fa43cfaa2eed628effa3555ee4f7a2adc4d068dc4004b5cf


    Version 1+2 digest in base64 format: 6mp6J6y7lypsKA0Sy9Y/tgs3vGZr82jqWO2qx+CKQQY/oAqscgbhg90v3WTbAWNmaBgvwvFF9n9F9FiPMnQr/STPMTFGJ5KyKKEVIqDY1lYJvh1HqKHMxAmLZJHyvgt2nq/KJTgSv0CPST4FIQzA6As95JbcyFTpiXbEt3Y8ZVGz0XNmrJZGXLyqhDlQ3Z13mZBVhh81UKEdYcuJXLVPydeMVt1tBTCT+kPPqi7tYo7/o1Ve5PeircTQaNxABLXP

    valentin@computer:~$ 

The password used in this example is `my loooooooong password`.

The length of the digest v2 is ok for the latest GnuPG version (with the password length limitation). The v1 base64 digest also should work fine. But the 'tinfoil hat edition' (version 1+2) works only with GnuPG 1 (tested it with `gpg (GnuPG) 1.4.20`).
