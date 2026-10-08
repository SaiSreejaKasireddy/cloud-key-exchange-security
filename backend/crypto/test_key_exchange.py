from key_exchange import generate_key_pair, derive_shared_key


# Generate Client key pair
client_private, client_public = generate_key_pair()

# Generate Cloud Server key pair
server_private, server_public = generate_key_pair()


# Client derives shared key using Server's public key
client_shared_key = derive_shared_key(
    client_private,
    server_public
)

# Server derives shared key using Client's public key
server_shared_key = derive_shared_key(
    server_private,
    client_public
)


print("Client shared key :", client_shared_key.hex())
print("Server shared key :", server_shared_key.hex())

print("\nKeys match:", client_shared_key == server_shared_key)