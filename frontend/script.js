const API_URL = "";


// ================================
// DOM ELEMENTS
// ================================

const keyExchangeBtn = document.getElementById("keyExchangeBtn");
const encryptBtn = document.getElementById("encryptBtn");
const decryptBtn = document.getElementById("decryptBtn");

const messageInput = document.getElementById("message");
const decryptStorageId = document.getElementById("decryptStorageId");

const connectionStatus = document.getElementById("connectionStatus");
const statusDot = document.querySelector(".status-dot");

const keyExchangeResult = document.getElementById("keyExchangeResult");
const encryptionResult = document.getElementById("encryptionResult");
const decryptionResult = document.getElementById("decryptionResult");

const storageIdDisplay = document.getElementById("storageId");
const storageStatus = document.getElementById("storageStatus");


// ================================
// KEY EXCHANGE
// ================================

keyExchangeBtn.addEventListener("click", async () => {

    keyExchangeBtn.disabled = true;
    keyExchangeBtn.textContent = "Establishing...";

    keyExchangeResult.textContent = "Generating secure key pair...";

    try {

        const response = await fetch(
            `${API_URL}/api/key-exchange`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        );

        const data = await response.json();

        if (response.ok && data.status === "success") {

            connectionStatus.textContent = "Secure Connection";

            statusDot.style.background = "#22c55e";

            keyExchangeResult.textContent =
                "✓ Secure ECDH key exchange completed successfully.";

        } else {

            keyExchangeResult.textContent =
                data.message || "Key exchange failed.";
        }

    } catch (error) {

        console.error(error);

        keyExchangeResult.textContent =
            "Unable to connect to the security server.";

    } finally {

        keyExchangeBtn.disabled = false;
        keyExchangeBtn.textContent = "Establish Secure Connection";
    }
});


// ================================
// ENCRYPT AND STORE
// ================================

encryptBtn.addEventListener("click", async () => {

    const message = messageInput.value.trim();

    if (!message) {

        encryptionResult.textContent =
            "Please enter some confidential data.";

        return;
    }

    encryptBtn.disabled = true;
    encryptBtn.textContent = "Encrypting...";

    encryptionResult.textContent =
        "Encrypting data and storing securely...";

    try {

        const response = await fetch(
            `${API_URL}/api/encrypt`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: message
                })
            }
        );

        const data = await response.json();

        if (response.ok && data.status === "success") {

            storageIdDisplay.textContent = data.storage_id;

            storageStatus.textContent = "Encrypted & Stored";

            decryptStorageId.value = data.storage_id;

            encryptionResult.textContent =
                "✓ Data encrypted using AES-256-GCM and securely stored.";

        } else {

            encryptionResult.textContent =
                data.message || "Encryption failed.";
        }

    } catch (error) {

        console.error(error);

        encryptionResult.textContent =
            "Unable to connect to the security server.";

    } finally {

        encryptBtn.disabled = false;
        encryptBtn.textContent = "Encrypt & Store";
    }
});


// ================================
// RETRIEVE AND DECRYPT
// ================================

decryptBtn.addEventListener("click", async () => {

    const storageId = decryptStorageId.value.trim();

    if (!storageId) {

        decryptionResult.textContent =
            "Please enter a storage ID.";

        return;
    }

    decryptBtn.disabled = true;
    decryptBtn.textContent = "Decrypting...";

    decryptionResult.textContent =
        "Retrieving encrypted data...";

    try {

        const response = await fetch(
            `${API_URL}/api/decrypt`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    storage_id: Number(storageId)
                })
            }
        );

        const data = await response.json();

        if (response.ok && data.status === "success") {

            decryptionResult.textContent =
                `✓ Decrypted Data: ${data.decrypted_data}`;

        } else {

            decryptionResult.textContent =
                data.message || "Decryption failed.";
        }

    } catch (error) {

        console.error(error);

        decryptionResult.textContent =
            "Unable to connect to the security server.";

    } finally {

        decryptBtn.disabled = false;
        decryptBtn.textContent = "Retrieve & Decrypt";
    }
});