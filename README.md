## Imp_Seal
This is a cli tool to make password protected and encrypted files.

This program uses hashes to authenticate passwords, and password derived keys to allow for encryption.

First you have to create a user, when created you can then authenticate and log in. As well as creating a password and a username, the program will also create your salt in this step. When you log in, the program will then use the clear text version of your password, along with the previously generated salt to create a key. This key is generated everytime you log in. prior to loging in you should move some files into the "encrypt_me" or the "decrypt_me" directories, and all of those files will be encrypted or decrypted.

uses: sha256, and utf-8 hashing and encoding respectively aswell as a Password Derived Key to encrypt and decrypt files.
python libraries: os, hashlib, pickle, cryptography, secrets, base64, getpass, binascii
