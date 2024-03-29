Slow KDF
========

Slow KDF for serious key stretching based on Scrypt.

 :point_right: This is my new key stretching script: [Doubleslow Keystretcher](https://github.com/vstoykovbg/doubleslow)

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

I recommend using the `Version 2 digest in base64 format`. `Version 1+2 digest in base64 format` is too long for some applications like some versions of GnuPG (with some settings).

Also I recommend my new key stretching script [Doubleslow Keystretcher](https://github.com/vstoykovbg/doubleslow) instead of SlowKDF.

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

And it also do not work as documented!
=====

There is a huge bug in GnuPG - <a href="https://www.reddit.com/r/crypto/comments/6y0eug/dsa_keys_may_be_between_1024_and_3072_bits_long/dmkeke8/">your private keys are not protected by the desired key stretching</a>:

<blockquote>
<p>I know I replied to you above about this, but this really needs to be super clear for everyone to see. <a href="https://dev.gnupg.org/T1800">Due to a bug</a>, <b>GPG completely ignored your S2K settings and isn't giving you the protection you asked for</b>. You can see this for yourself:

```
$ gpg2 --export-secret-key | gpg2 --list-packets > packets
```

<p>Running your exact command and then inspecting the packets gives me this:

```
# off=0 ctb=95 tag=5 hlen=3 plen=966
:secret key packet:
        version 4, algo 1, created 1504562320, expires 0
        pkey[0]: [2048 bits]
        pkey[1]: [17 bits]
        iter+salt S2K, algo: 7, SHA1 protection, hash: 2, salt: 8792DC994E02F5DB
        protect count: 16252928 (223)
        protect IV:  ff 9d 2c 80 7c e4 1d 0c 6a 41 17 7f 41 1e 03 51
        skey[2]: [v4 protected]
        keyid: F021CA39AB2D856D
```

<p>Notice it's using AES-128 (<a href="https://tools.ietf.org/html/rfc4880#section-9">algo 7</a>), SHA-1 (hash 2), and 16 million iterations instead of 65 million. That's why it's able to process your passphrase so quickly rather than taking a few seconds like it should.

<p>This security bug is about 3 years old now.

<p><cite><a href="https://www.reddit.com/r/crypto/comments/6y0eug/dsa_keys_may_be_between_1024_and_3072_bits_long/dmkeke8/">/u/skeeto</a></cite>
</blockquote>

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

GnuPG 2.1.11 does not accept long passwords (UPDATE: GnuPG 2.2.4 on Ubuntu accept long passwords)
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

**UPDATE: GnuPG 2.2.4 on Ubuntu accept long passwords**

Tested it with software versions:

    gpg (GnuPG) 2.2.4
    libgcrypt 1.8.1
    pinentry-gnome3 (pinentry) 1.1.0
    Ubuntu 18.04.3 LTS
And it works with an ASCII password with 495 charsacters. If I enter more characters there is an error message:

    gpg: problem with the agent: Too much data for IPC layer
    gpg: error creating passphrase: Operation cancelled

The documentation says:

    There is no limit on the length of a passphrase, and it should be carefully chosen.

This is not the case on my system.

When I use gpg (GnuPG 2.2.4) with the option `--pinentry-mode loopback` it asks for the password in the console (without popping up a dialog box) and the limit is still 255 ASCII characters. When I tried to replace 4 characters with Unicode the limit became 251 characters. This means that **the limit is in bytes (255 bytes), not in characters.**

When using options `--passphrase-file passphrase.txt --pinentry-mode loopback` it allowed **larger than 255 bytes** passwords (for example, 27665 bytes). When tried with 30185 bytes password I got error message `gpg: Warning: using insecure memory!` but it worked. When tried with 34728 bytes password I got error message `gpg: Fatal: out of core in secure memory while allocating 32800 bytes` and the program refused to continue.

Writing the password in a file is not very secure, especially when the filesystem is not `tmpfs` and full disk encryption is not used.

Update: it stopped to accept long passwords, but after I killed the pinentry process it works again. It's better to not supply to GnuPG long passwords, instead hash your long passwords and supply the output of the hash function (do not forget that the console history is saved in typical systems in more than one place, not only `~/.bash_history`, also Konsole and Gnome Terminal save your secrets that you type or see on the console. Morever, clipboard managers can save your secrets you copy/paste.

Workaround of the password length problem
========

You can use some hash function like sha256:

    echo -n "my loooooooong password" | sha256sum

Don't forget the `-n` part, because it gives different result:

    valentin@computer:~$ echo -n "my loooooooong password" | sha256sum 
    8416b2bc52278595f1283bcf524b79753f146d18989fc4d7bc11edc56a753808  -
    valentin@computer:~$ echo    "my loooooooong password" | sha256sum 
    ea492b596aa905a96f236311fade318de7c3117a0a6d22008e1cfa29498abef8  -
    valentin@computer:~$ 

Or you can use sha512sum and use only the first 127 characters (sha512sum produces 128 characters when the output is in hex format). You can use also `mnemonic-sha512.py` ([from here](https://github.com/vstoykovbg/mnemonic-hashes)) to produce a base64, base62 or Base58Check version of the hash (the longest is only 93 characters):

    valentin@computer:~$ echo -n "my loooooooong password" > tmpfs/long.txt
    valentin@computer:~$ mnemonic-sha512.py tmpfs/long.txt 

    === SHA-512 hash: ===

    Hex: f3a56f8ec032ea6d27f4ceff68e36ce9d25fc7042c737f2e4785f47d8267b5f3836987a0714921a8cc3f61dc1861523e92425ecdb90b522a81e0c82f4c5a224b
    Base64: 86VvjsAy6m0n9M7/aONs6dJfxwQsc38uR4X0fYJntfODaYegcUkhqMw/YdwYYVI+kkJezbkLUiqB4MgvTFoiSw==
    Base62: uZJwVX3oRpZtZWrvrNFHm8JLFzmhmvEMLwOBiVv4FMUyBLcdMcVpnrhijplAuMVVDARwfPvz9SteW7SQQYD8LT
    Base58Check: YsoQeY8Gep6UP5a7upPAQcPCnPjjn7ezVTU7yNpXrGLJydg4WApwSk1izGhTzNnvzTgurT5xwZHCTmPLRP1VbYPN56ukS
    BIP39 mnemonic (1): victory clock together lesson concert custom panther oil youth either swamp squirrel chalk toe awful mobile left impulse thumb trophy subway critic style hen
    BIP39 mnemonic (2): lock equip trend tip must stamp couch umbrella swing seek fee large category control dad cannon fall favorite join motion visit code matrix horror
     * This digest is 512 bits long, so it's split in two parts
       and this way two BIP39 mnemonic codes are produced.
    RFC1751 mnemonic: VEAL NEE STAY FIND OFF REB MEG KICK MUCH ROOF RAY DOES ROSA WOVE MUTT BLAT RIO HESS ABEL OR JAM AWK ELSE WELT FOAL AMID TEAL SORE HAAG RUNT RAKE WHET DRUB OW FUN JAB HACK FAR LOWE DEFY LYNN FUN FLAM BAY COT HIRE JOCK LOS
    valentin@computer:~$ 

Alternatively:

    $ sha512sum tmpfs/long.txt | cut -f1 -d\  | xxd -r -p | base64 -w 0 ; echo
    86VvjsAy6m0n9M7/aONs6dJfxwQsc38uR4X0fYJntfODaYegcUkhqMw/YdwYYVI+kkJezbkLUiqB4MgvTFoiSw==

One round of sha-512 can not be considered a key stretching, it's just a workaround to fit a long password/passphrase into a legacy system. A script from [Mnemonic Hashes](https://github.com/vstoykovbg/mnemonic-hashes) can be used to make a web password. For example, you can get the first 4 words of the BIP39 output or the Base62 version of the Blake2b-64 or Blake2b-128 hash.

⚠️ WARNING: Typically the commands are saved in a "hitory files" somewhere on the hard drive and if you type your passphrase like in the above example it may be saved. Gnome Terminal and Konsole are saving history (or not - if you disable this feature), also Bash typically is saving the history of the typed commands in the file `~/.bash_history`. If you use a Live distribution without a feature to save a session and without swap it's relatively safe to type your passphrase. But what you see on the monitor can be recorder with security or other cameras. Also the clipboard manager may keep logs on the hard drive. In the above example I am writing the password on a tmpfs, which is relatively safe (more safe than on the hard drive where the passphrase when it may persist afeter the deletion of the file). I am not using swap or use encrypted swap (with a key that is forgotten when the power of the RAM memory is turned off).

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

The length of the digest v2 is ok for the latest GnuPG version (with the password length limitation). The v1 base64 digest also should work fine. But the 'tinfoil hat edition' (version 1+2) works only with GnuPG 1 (tested it with `gpg (GnuPG) 1.4.20`). (Update: on GnuPG 2.2.4 the limit is lifted to 495 characters, however it is still 255 bytes if option `--pinentry-mode loopback` is used; the limit is bigger with `--passphrase-file passphrase.txt --pinentry-mode loopback`.)

Limiting the CPU load to prevent overheating
====

On some old computers too much CPU load may lead to overheating and automatic shutdown of the computer.

The script `cpulimit.bash` is searching for a python script with `slowkdf` in the name. There is a limitation - it slows down only the first script with such a name.

I found a bug - it says "Stopped" but it continue to run and return the data to `stdout`: https://www.youtube.com/watch?v=LN_DjgREXjU

Testing scrypt modules for speed
====

```
$ ./scrypt_test.py 
**** Testing with Scrypt from scrypt...
File of locally installed scrypt: /home/valentin/.local/lib/python3.6/site-packages/scrypt/__init__.py
Iteration 1 from 1...
*** Time:  4.310204744338989 **********************************************
Digest in base64 format: R/5/ga5KTwm8WIs9FquqJxxoIACiN8PGSTv9GvDrJO9OOhjEcf95kLJgucAXSWK2cGq+kAW3JqENKybD8tw3WOFnvPVAMOo/Zku/8kizjmYGEuhd/tOKg2hKgnnbUrsQTAZ9JYxWhR7flK7ygSmaNjZOXNObDNwAN0oXqFpbQ4k=




**** Testing with Scrypt from scrypt (old version)...
File of scrypt: /usr/lib/python3/dist-packages/scrypt.py
Iteration 1 from 1...
*** Time:  4.284672498703003 **********************************************
Digest in base64 format: R/5/ga5KTwm8WIs9FquqJxxoIACiN8PGSTv9GvDrJO9OOhjEcf95kLJgucAXSWK2cGq+kAW3JqENKybD8tw3WOFnvPVAMOo/Zku/8kizjmYGEuhd/tOKg2hKgnnbUrsQTAZ9JYxWhR7flK7ygSmaNjZOXNObDNwAN0oXqFpbQ4k=




**** Testing with Scrypt from Cryptodome...
Iteration 1 from 1...
*** Time:  5.6815948486328125 **********************************************
Digest in base64 format: R/5/ga5KTwm8WIs9FquqJxxoIACiN8PGSTv9GvDrJO9OOhjEcf95kLJgucAXSWK2cGq+kAW3JqENKybD8tw3WOFnvPVAMOo/Zku/8kizjmYGEuhd/tOKg2hKgnnbUrsQTAZ9JYxWhR7flK7ygSmaNjZOXNObDNwAN0oXqFpbQ4k=




**** Testing with Scrypt from hashlib...
Iteration 1 from 1...
*** Time:  4.702378988265991 **********************************************
Digest in base64 format: R/5/ga5KTwm8WIs9FquqJxxoIACiN8PGSTv9GvDrJO9OOhjEcf95kLJgucAXSWK2cGq+kAW3JqENKybD8tw3WOFnvPVAMOo/Zku/8kizjmYGEuhd/tOKg2hKgnnbUrsQTAZ9JYxWhR7flK7ygSmaNjZOXNObDNwAN0oXqFpbQ4k=




**** Testing with Scrypt from hazmat...
Iteration 1 from 1...
*** Time:  4.770408630371094 **********************************************
Digest in base64 format: R/5/ga5KTwm8WIs9FquqJxxoIACiN8PGSTv9GvDrJO9OOhjEcf95kLJgucAXSWK2cGq+kAW3JqENKybD8tw3WOFnvPVAMOo/Zku/8kizjmYGEuhd/tOKg2hKgnnbUrsQTAZ9JYxWhR7flK7ygSmaNjZOXNObDNwAN0oXqFpbQ4k=

```

Looks like the scrypt module from Ubuntu and the module installed with `pip3 install scrypt` are the best. My CPU is `Intel(R) Core(TM) i3-2100 CPU @ 3.10GHz`.

Collisions
====

These two passwords produce the same scrypt digiest (I learned it from [here](https://mathiasbynens.be/notes/pbkdf2-hmac#comment-3)):

```PBKDF2-HMAC-SHA256-fail-affects-scrypt-no-security-issue-bGoDFpr8```

```;`B3nR6wQ2-_LSg"mH #yszm`[#z8B&L```

The scrypt digest is (in hex format):

`2bbb625cbb0201756397c93fdee9d902fe92c176c77e50ab5016b9db85dacfd7c5478820a2b8148f8f3790a7a12e63469eeda87459d68ea505826d0bd94c245570e39da1784327b2eed33b81f2da8ca850c2707139df81d52bc6610c07f663bec69d2009e416985def67f73e8a15dbce832bbd0d53dececa1f83a04c94927cce`

This is true for any salt, N, r, p.

However, versions 2 and 1+2 of the output from the `SlowKDF` script are different.
