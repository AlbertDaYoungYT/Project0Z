import base64
import requests, json
from uuid import UUID
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import Certificate, CertificateBuilder, NameOID
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_public_key
from datetime import datetime, timedelta
import os, pathlib

from pprint import pprint

def InitialHelloToServer(client_version):
    return requests.post(server_url + "/auth/hello", data=json.dumps({
        "client_version": client_version
    })).json()

def InitialHelloAckResponse(client_id, client_public_key: rsa.RSAPublicKey):
    return requests.post(server_url + "/auth/ack", data=json.dumps({
        "id": client_id,
        "client_public_key": "BASE64::CLIENT_PUBLIC_KEY::"+base64.b64encode(
        client_public_key.public_bytes(
            Encoding.PEM,
            PublicFormat.SubjectPublicKeyInfo
        )
    ).decode()
    })).json()

def RequestSigningChallenge(client_id):
    return requests.post(server_url + "/auth/challenge/req", data=json.dumps({
        "id": client_id
    })).json()

def SubmitSigningChallenge(client_id, challenge_submission):
    return requests.post(server_url + "/auth/challenge/res", data=json.dumps({
        "id": client_id,
        "challenge_submission": "BASE64::CHALLENGE::"+base64.b64encode(
            challenge_submission
        ).decode()
    })).json()

server_url = "http://127.0.0.1:24899"

# STEP 1 - InitHello
hello_response = InitialHelloToServer([0, 0, 2])
pprint(hello_response)

# STEP 2 - InitAck
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()
key_response = InitialHelloAckResponse(
    hello_response["id"],
    public_key
)
pprint(key_response)
server_public_key = base64.b64decode(key_response["server_public_key"][len("BASE64::SERVER_PUBLIC_KEY::"):].encode())
server_public_key: rsa.RSAPublicKey = load_pem_public_key(
    server_public_key
)

# STEP 3 - SigningChallengeRequest
challenge_response = RequestSigningChallenge(
    key_response["id"]
)
pprint(challenge_response)
decrypted_challenge = private_key.decrypt(
    base64.b64decode(challenge_response["encrypted_challenge"][len("BASE64::CHALLENGE::"):].encode()),
    padding=padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
pprint(decrypted_challenge)
signed_challenge = private_key.sign(
    decrypted_challenge,
    padding=padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    algorithm=hashes.SHA256()
)
pprint(signed_challenge)

# STEP 4 - SigningChallengeSubmit
challenge_submission = SubmitSigningChallenge(
    challenge_response["id"],
    signed_challenge
)
pprint(challenge_submission)