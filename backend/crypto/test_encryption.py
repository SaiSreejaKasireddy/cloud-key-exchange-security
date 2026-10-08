from key_exchange import generate_key_pair, derive_shared_key
from encryption import encrypt_data, decrypt_data


# Generate Client keys
client_private, client_public = generate_key_pair()

# Generate Cloud Server keys
server_private, server_public = generate_key_pair()


# Establish shared key
client_shared_key = derive_shared_key(
    client_private,
    server_public
)

server_shared_key = derive_shared_key(
    server_private,
    client_public
)


# Message from client
message = "Confidential Cloud Computing Data"


# Client encrypts the message
nonce, ciphertext = encrypt_data(
    client_shared_key,
    message
)

print("Original message:")
print(message)

print("\nEncrypted data:")
print(ciphertext.hex())


# Cloud server decrypts the message
decrypted_message = decrypt_data(
    server_shared_key,
    nonce,
    ciphertext
)

print("\nDecrypted message:")
print(decrypted_message)

print("\nEncryption successful:",
      message == decrypted_message)