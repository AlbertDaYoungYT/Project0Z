# Project Z0 Server Security Architecture

# Overview
This project implements a secure client-server authentication protocol, ensuring trust even over untrusted networks.  
The system is based on a combination of **public key cryptography**, **certificate signing**, **challenge-response authentication**, and **XOR-based encryption**.

Project Z0's security architecture is designed for reliable communication where official and unofficial servers must be distinguishable by clients, must be sent over the HTTP/HTTPS protocol using the Authentication System. Any publicly hosted server found to be breaching Project Z0 TOS will be investigated for misuse and could potentially be permanently banned from client discovery.

## Server Authentication Flow
1. **Server Boot**:
    - If no server root key exists, it generates a new ed25519 keypair.
    - The Root Key is a default key used to issue new certificates, and is stored in the <ins>**server/certificates/trusted/**</ins> directory.

2. **Client Greeting**:
    - Client connects to the server at the HTTP/HTTPS endpoint <ins>**/auth/hello**</ins>.
    - Client provides its own version, along with various system identifiers (Not implemented yet because of testing).
    - Server Responds with either an Error or an Acknowledgement.
        - Error Response: Codes.CLIENT_VERSION_TOO_LOW
        - Acknowledgement Response:
        ```json
        {
            "id": str,                        // New Client ID
            "version": list[int*3],           // Server Version
            "min_client_version": list[int*3],// Minimum Client Version
            "region": str,                    // Servers region/location
            "uptime": str                     // Servers uptime (format: 00h 00m 00s)
        }
        ```

3. **Client Acknowledgement**:
    - Client receives the ID from the previous request and passes it onto this request.
    - Client also sends its Root Public Key encoded in Base64.
    - Server then checks to see if the ID is valid before sending its Root Public Key and a new Client ID.

4. **Challenge-Request**:
    - Client uses its new ID to request a Signing Challenge from the Server.
    - Server generates a SHA256 hash and encrypts it with the Clients Public Key.
    - Server sends the encrypted hash and a new ID to the Client.
    - Client decrypts and signs the hash.

5. **Challenge-Response**:
    - Client sends the signed hash along side the new ID.
    - Server verifies the submitted challenge, which results in either an Error or Success.
        - Error Success: Codes.CLIENT_CHALLENGE_VERIFICATION_FAILED
        - Success Response:
        ```json
        {
            "id": str,                  // Client ID (from before)
            "auth_id": str,             // Auth Token/ID (Hashed Client ID)
            "session_certificate": str  // Base64 String for the generated Session Public Key
        }
        ```

6. **XOR Encrypted Communication (Optional)**:
    - After successful authentication, the client and server obfuscate traffic using a symmetric XOR encryption key.
    - XOR key is used as another layer of security, clients can opt out of XOR communication or exclusively use it instead of RSA Key encryption.
    - Clients can Request or Provide a new XOR Key using UDP Packet Opcode (98 or 99)
        - 98 = XOR Request.
        - 99 = XOR Submit.

## Tests

### **Test System**:

Utilization is measured from the Windows Task Manager. The client and server both run on the test machine in this instance.

| Component | Model | Speed |
|----------|:-------------:|------:|
| CPU | AMD R9 3950X | ~4.2Ghz (10-15% Util) |
| RAM | 2x 16GB Corsair w. DOCP | 3200 MT/s (~40% Util) |
| SSD | Samsung 990 Pro | PCIe Gen4.0 x4 (~1% Util) |

### **Test Results**:

1. **Client** Took 937.2778 milliseconds to execute the auth_test.py script using this command ```Measure-Command { & python .\auth_test.py }```
2. **Server** Processed and finished the Authentication Process in ~103 milliseconds, this is measured using the logging to stdout starting at the first Request.
```
[REDACTED] 12:52:29.050 | DEBUG    | server.http.routes.auth.InitHello:initial_greeting_handler - Greeting Request from 127.0.0.1
[REDACTED] 12:52:29.078 | DEBUG    | server.http.routes.auth.InitAck:initial_ack_handler - Initial ACK Response from 127.0.0.1
[REDACTED] 12:52:29.083 | DEBUG    | server.http.routes.auth.SigningChallengeRequest:signing_challenge_handler - Signing Challenge Request from 127.0.0.1
[REDACTED] 12:52:29.088 | DEBUG    | server.http.routes.auth.SigningChallengeSubmit:challenge_submission_handler - Signing Challenge Submission from 127.0.0.1
[REDACTED] 12:52:29.153 | DEBUG    | database.DatabaseManager:save_document - Document saved to '[REDACTED]' with ID: 70f722e7f35f2b65888ad461f4008284, Revision: 1-66bdc0fe5e1d290471bcc166767a5e66
```

### **Conclusion**:
The testing system consists of an AMD R9 3950X CPU, 2x16GB Corsair RAM, and a Samsung 990 Pro SSD. The client and server both ran their respective scripts on this test machine. Results showed that the client script completed in about 937 milliseconds which could be caused by the Client having to load libraries before attempting to connect, while the server finished the authentication process in approximately 103 milliseconds as it already had the libraries loaded and only needed to listen for Client Requests.

Overall, Project Z0's Authentication System demonstrates impressive performance and robust security features such as public key cryptography, challenge-response authentication, and XOR encryption for optional client-server obfuscation.

---

## Security Layers

The following security layers have been successfully integrated into Project Z0's Authentication System:

1. **Public Key Cryptography**: Utilizes ed25519 key generation, signing, and encryption for secure communication between client and server; certificates are issued to clients after successful authentication.
2. **Certificate Signing**: The root authority (server) signs the intermediate and leaf certificates of clients using a private key after verifying their authenticity during the challenge-response phase.
3. **Challenge-Response Authentication**: An XOR-based hash challenge is initiated by the client, and the server generates a SHA256 hash of the provided challenge. Both parties confirm each other's acknowledgement before proceeding.
4. **Optional XOR Encryption (Symmetric Key)**: Allows clients to communicate with servers securely using an XOR cipher for confidentiality purposes during data transmission. The shared secret key is derived from a combination of timestamps and the authentication ID obtained during challenge-response authentication.
5. **Server Authentication**: Ensures that only authorized and up-to-date client instances can communicate with official servers by checking client versions and minimum requirements.
6. **Access Control and Authorization**: Controls access to sensitive resources by verifying user credentials through the presented identity (certificates).
7. Session Timeout and Revocation: Invalidates unused or compromised sessions after a certain period, improving overall system security.
8. **Data Integrity Protection**: Uses HMAC-256 during key exchange and communication phases to securely transmit sensitive data while ensuring its authenticity and integrity.

## Threat Model
Project Z0's Authentication System effectively counters the following threat models:

1. **Man-in-the-Middle (MITM) Attacks**: Implementing public key cryptography, certificate signing, and HMAC ensures data integrity throughout the communication process.
2. **Brute Force and Denial of Service Attacks**: Implementing rate-limiting, challenge-response authentication, and access controls deters such attacks by limiting the number of attempted connections by non-authenticated clients or bots.
3. **Eavesdropping and Information Disclosure**: Utilizing encrypted communication, data hashes, and XOR-based encryption protects sensitive information from unauthorized viewing during transmission.
4. **Session Hijacking**: Expiring sessions and implementing proper authentication measures ensure continuous protection against session hijacking attempts.
5. **Unauthorized Access or Use of Resources**: Strict access controls on resources ensure unauthorized users can't perform harmful actions within the system.
6. **Compromised Client Devices/Identity Theft**: By requiring clients to present their root public key during authentication, an authentic client device can be identified, reducing the risk of identity theft and compromised devices posing as genuine instances.


## Future Improvements
- [ ]: Implement systems to ensure data security while gathering system information.
- [ ]: Implement session-specific XOR keys for enhanced secrecy.
- [ ]: Add timestamps or nonces to certificates to reduce misuse risk.
- [ ]: Add timestamps to every HTTP or UDP packet/message sent over the network.
- [x]: Create new client IDs for every step in Authentication Process.
- [ ]: Implement UDP Authentication System.
- [ ]: Rewrite the ServerSigning.md Documentation and remake the UML Diagram.
- [ ]: Rewrite the auth_test.py file to be easier to read.
- [ ]: Implement flexibility in terms of Key Hashes or Padding types.