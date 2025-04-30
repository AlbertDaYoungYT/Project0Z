

def xor(data, key) -> str: 
  
    # calculate length of data string 
    length = len(data)
  
    # perform XOR operation of key 
    # with every character in string 
    for i in range(length):
        data = (data[:i] + 
             chr(ord(data[i]) ^ ord(key)) +
                     data[i + 1:])
      
    return data


from uuid import UUID
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509 import Certificate, CertificateBuilder, NameOID
from cryptography import x509
from datetime import datetime, timedelta
import os, pathlib

import loguru

from utils.Errors import Codes

class CertificateAuthority:
    def __init__(self, 
                 root_key_path="certificates/trusted/official_key.pem", 
                 root_cert_path="certificates/trusted/official_cert.pem"):
        self.root_key_path = root_key_path
        self.root_cert_path = root_cert_path
        self.root_private_key = None
        self.root_certificate = None
        self._load_or_generate_root()

    def _load_or_generate_root(self):
        if os.path.exists(self.root_key_path):
            with open(self.root_key_path, "rb") as key_file:
                self.root_private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None
                )
        else:
            self.root_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            with open(self.root_key_path, "wb") as f:
                f.write(self.root_private_key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.TraditionalOpenSSL,
                    serialization.NoEncryption()
                ))

        if os.path.exists(self.root_cert_path):
            with open(self.root_cert_path, "rb") as cert_file:
                self.root_certificate = x509.load_pem_x509_certificate(cert_file.read())
        else:
            self.root_certificate = self._generate_root_certificate()
            with open(self.root_cert_path, "wb") as f:
                f.write(self.root_certificate.public_bytes(serialization.Encoding.PEM))

    def _generate_root_certificate(self):
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u"Project Z0 Root CA"),
        ])
        cert = CertificateBuilder().subject_name(subject).issuer_name(issuer)\
            .public_key(self.root_private_key.public_key())\
            .serial_number(x509.random_serial_number())\
            .not_valid_before(datetime.utcnow())\
            .not_valid_after(datetime.utcnow() + timedelta(days=3650))\
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)\
            .sign(self.root_private_key, hashes.SHA256())
        return cert

    def issue_certificate(self, public_key, common_name="Server Session", invalid_days=7):
        subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])
        cert = CertificateBuilder()\
            .subject_name(subject)\
            .issuer_name(self.root_certificate.subject)\
            .public_key(public_key)\
            .serial_number(x509.random_serial_number())\
            .not_valid_before(datetime.utcnow())\
            .not_valid_after(datetime.utcnow() + timedelta(days=invalid_days))\
            .sign(self.root_private_key, hashes.SHA256())
        return cert


#class OfficialCA:
#
#    def __init__(self, 
#                 root_key_path="../certificates/trusted/official_key.pem", 
#                 root_cert_path="../certificates/trusted/official_cert.pem"):
#        self.root_key_path = root_key_path
#        self.root_cert_path = root_cert_path
#        self.root_private_key = None
#        self.root_certificate = None
#        self._load()
#    
#    def _load(self):
#        if os.path.exists(self.root_key_path):
#            with open(self.root_key_path, "rb") as key_file:
#                self.root_private_key = serialization.load_pem_private_key(
#                    key_file.read(),
#                    password=os.getenv("CERTIFICATE_PASSWORD", None)
#                )
#        else:
#            loguru.logger.error(Codes.FAILED_LOADING_OFFICIAL_CERTIFICATES.value.to_logger())
#
#        if os.path.exists(self.root_cert_path):
#            with open(self.root_cert_path, "rb") as cert_file:
#                self.root_certificate = x509.load_pem_x509_certificate(cert_file.read())
#        else:
#            loguru.logger.error(Codes.FAILED_LOADING_OFFICIAL_CERTIFICATES.value.to_logger())


class SessionKeyManager:
    def __init__(self, ca: CertificateAuthority):
        self.ca = ca
        self.signed_certs: dict[UUID, list[rsa.RSAPrivateKey, Certificate]] = {}

    def generate_session_cert(self, id: UUID):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cert = self.ca.issue_certificate(private_key.public_key(), "Session Key")

        self.signed_certs[id] = [private_key, cert]
        return cert
