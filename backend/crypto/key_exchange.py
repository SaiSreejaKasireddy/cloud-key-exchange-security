from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


def generate_key_pair():
    """
    Generate an ECDH private key and its corresponding public key.
    """
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    return private_key, public_key


def derive_shared_key(private_key, peer_public_key):
    """
    Generate a shared secret using ECDH and derive
    a secure 256-bit encryption key using HKDF.
    """

    shared_secret = private_key.exchange(
        ec.ECDH(),
        peer_public_key
    )

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"cloud-key-exchange"
    ).derive(shared_secret)

    return derived_key