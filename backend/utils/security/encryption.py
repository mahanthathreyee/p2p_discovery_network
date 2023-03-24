# import os
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# key = os.urandom(32)
# iv = os.urandom(16)
#
# cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
# encryptor = cipher.encryptor()
# buf = bytearray(31)
# len_encrypted = encryptor.update_into(b"a secret message",buf)
#
# ct = bytes(buf[:len_encrypted])+encryptor.finalize()
#
# decryptor = cipher.decryptor()
# len_decrypted = decryptor.update_into(ct,buf)
# s = bytes(buf[:len_decrypted]+decryptor.finalize())
# print(s)

import os

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

def read_file(file_path):
    file = open(file_path,"r")
    s = file.read()
    if s != "":
        print("String is not empty, here's what it said: " + s)
    file.close()
    return s

def write_file(s,file_path):
    file = open(file_path,"w")
    file.write(s)
    file.close()


def encrypt(key, plaintext, associated_data):
    # Generate a random 96-bit IV.
    iv = os.urandom(12)

    # Construct an AES-GCM Cipher object with the given key and a
    # randomly generated IV.
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
    ).encryptor()

    # associated_data will be authenticated but not encrypted,
    # it must also be passed in on decryption.
    encryptor.authenticate_additional_data(associated_data)

    # Encrypt the plaintext and get the associated ciphertext.
    # GCM does not require padding.
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return (iv, ciphertext, encryptor.tag)

def decrypt(key, associated_data, iv, ciphertext, tag):
    # Construct a Cipher object, with the key, iv, and additionally the
    # GCM tag used for authenticating the message.
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
    ).decryptor()

    # We put associated_data back in or the tag will fail to verify
    # when we finalize the decryptor.
    decryptor.authenticate_additional_data(associated_data)

    # Decryption gets us the authenticated plaintext.
    # If the tag does not match an InvalidTag exception will be raised.
    return decryptor.update(ciphertext) + decryptor.finalize()
key = os.urandom(32)
print("key :", key)

contents = read_file("in.txt")
b = bytes(contents,'utf-8')

iv, ciphertext, tag = encrypt(
    key,
    b,
    # b"a secret message!",
    b"authenticated but not encrypted payload"
)
s = str(decrypt(
    key,
    b"authenticated but not encrypted payload",
    iv,
    ciphertext,
    tag
))
print(s)
write_file(s,"out.txt")