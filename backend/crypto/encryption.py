import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_data(key, plaintext):
    """
    Encrypt plaintext using AES-256-GCM.
    """

    aes = AESGCM(key)

    # A fresh random nonce must be used for every encryption.
    nonce = os.urandom(12)

    ciphertext = aes.encrypt(
        nonce,
        plaintext.encode("utf-8"),
        None
    )

    return nonce, ciphertext


def decrypt_data(key, nonce, ciphertext):
    """
    Decrypt AES-256-GCM encrypted data.
    """

    aes = AESGCM(key)

    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode("utf-8")