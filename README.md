## Imp_Seal
Imperial Seal is a command line tool used to: encrypt/decrypt files, and check your password strength.<br>
This program uses hashes to authenticate passwords, and password derived keys to allow for authenticated encryption.

![The Imperial Seal Gif](https://media.tenor.com/QmBFjr5QR24AAAAd/seal.gif)

### File Encryption and Decryption:
Once you create a user you can then authenticate and log in. As well as creating a password and a username, the program will also create your salt in this step. When you log in, the program will then use the clear text version of your password, along with the previously generated salt to create a key. This key is generated every time you log in. Before authenticating, move files into the "encrypt_me" or "decrypt_me" directories, you can encrypt and decrypt those files through to programs options.

### New! Now includes hash breaking program!!!!
To test your password first use the main program's user creation, and write to .csv file functionality to create a record of your users. Then you can run "hash_breaker.py" and set your target information to the information in the csv file, and unload the csv target's hash and salt. Now just run the brute force attack, and wait for your password to get cracked.

#### Dependencies:
Uses sha256 hashing, utf-8 and ascii encoding, aswell as a Password Derived Key to encrypt and decrypt files.<br>
pPython Libraries: os, hashlib, pickle, cryptography, secrets, base64, getpass, binascii
