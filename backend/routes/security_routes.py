from flask import Blueprint, jsonify ,request
from crypto.key_exchange import generate_key_pair, derive_shared_key
from crypto.encryption import encrypt_data, decrypt_data
from storage.database import store_encrypted_data, get_encrypted_data

security_bp = Blueprint("security", __name__)

# Temporary in-memory storage for this stage
client_private_key = None
client_public_key = None
server_private_key = None
server_public_key = None
shared_key = None


@security_bp.route("/api/key-exchange", methods=["POST"])
def key_exchange():
    global client_private_key
    global client_public_key
    global server_private_key
    global server_public_key
    global shared_key

    # Generate client key pair
    client_private_key, client_public_key = generate_key_pair()

    # Generate cloud/server key pair
    server_private_key, server_public_key = generate_key_pair()

    # Derive shared secret
    client_shared_key = derive_shared_key(
        client_private_key,
        server_public_key
    )

    server_shared_key = derive_shared_key(
        server_private_key,
        client_public_key
    )

    # Verify both sides generated the same key
    if client_shared_key != server_shared_key:
        return jsonify({
            "status": "error",
            "message": "Key exchange failed"
        }), 500

    shared_key = client_shared_key

    return jsonify({
        "status": "success",
        "message": "Secure key exchange completed",
        "algorithm": "ECDH",
        "curve": "SECP256R1",
        "key_status": "Shared secret successfully established"
    })

@security_bp.route("/api/encrypt", methods=["POST"])
def encrypt_message():
    global shared_key

    if shared_key is None:
        return jsonify({
            "status": "error",
            "message": "Secure key exchange has not been completed"
        }), 400

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({
            "status": "error",
            "message": "Message is required"
        }), 400

    message = data["message"]

    # Encrypt the message
    nonce, ciphertext = encrypt_data(
        shared_key,
        message
    )

    # Convert binary data to hexadecimal
    encrypted_hex = ciphertext.hex()
    nonce_hex = nonce.hex()

    # Store encrypted data in database
    record_id = store_encrypted_data(
        encrypted_hex,
        nonce_hex
    )

    return jsonify({
        "status": "success",
        "algorithm": "AES-256-GCM",
        "storage_id": record_id,
        "encrypted_data": encrypted_hex,
        "nonce": nonce_hex,
        "message": "Data encrypted and securely stored"
    })


@security_bp.route("/api/decrypt", methods=["POST"])
def decrypt_message():
    global shared_key

    if shared_key is None:
        return jsonify({
            "status": "error",
            "message": "Secure key exchange has not been completed"
        }), 400

    data = request.get_json()

    if not data or "storage_id" not in data:
        return jsonify({
            "status": "error",
            "message": "Storage ID is required"
        }), 400

    try:
        storage_id = int(data["storage_id"])

        # Retrieve encrypted data from cloud storage
        record = get_encrypted_data(storage_id)

        if record is None:
            return jsonify({
                "status": "error",
                "message": "Encrypted data not found"
            }), 404

        encrypted_hex = record["encrypted_data"]
        nonce_hex = record["nonce"]

        # Convert hexadecimal data back to bytes
        ciphertext = bytes.fromhex(encrypted_hex)
        nonce = bytes.fromhex(nonce_hex)

        # Decrypt the stored data
        plaintext = decrypt_data(
            shared_key,
            nonce,
            ciphertext
        )

        return jsonify({
            "status": "success",
            "algorithm": "AES-256-GCM",
            "storage_id": storage_id,
            "decrypted_data": plaintext,
            "message": "Data retrieved and decrypted successfully"
        })

    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Invalid storage ID"
        }), 400

    except Exception as e:
        print("DECRYPTION ERROR:", type(e).__name__, str(e))

        return jsonify({
            "status": "error",
            "message": "Decryption failed or data was modified"
        }), 400
@security_bp.route("/api/tamper-test", methods=["POST"])
def tamper_test():

    global shared_key

    if shared_key is None:
        return jsonify({
            "status": "error",
            "message": "Secure key exchange has not been completed"
        }), 400

    data = request.get_json()

    if not data or "storage_id" not in data:
        return jsonify({
            "status": "error",
            "message": "Storage ID is required"
        }), 400

    try:
        storage_id = int(data["storage_id"])

        record = get_encrypted_data(storage_id)

        if record is None:
            return jsonify({
                "status": "error",
                "message": "Encrypted data not found"
            }), 404

        # Deliberately modify one character of the ciphertext
        encrypted_hex = record["encrypted_data"]

        tampered_hex = (
            encrypted_hex[:-1] +
            ("0" if encrypted_hex[-1] != "0" else "1")
        )

        ciphertext = bytes.fromhex(tampered_hex)
        nonce = bytes.fromhex(record["nonce"])

        # Try decrypting the modified ciphertext
        plaintext = decrypt_data(
            shared_key,
            nonce,
            ciphertext
        )

        return jsonify({
            "status": "warning",
            "message": "Tampered data was decrypted unexpectedly",
            "decrypted_data": plaintext
        })

    except Exception as e:

        print(
            "TAMPERING DETECTED:",
            type(e).__name__,
            str(e)
        )

        return jsonify({
            "status": "protected",
            "message": "Tampering detected. Modified encrypted data was rejected.",
            "security": "AES-256-GCM integrity protection"
        }), 400