# region DEPENDENCIES
import config_store
from utils import file_handler
from utils import logger_handler
from file_discovery import node_file_handler

from constants import cryptography_constants as constants

import pickle
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
#endregion

#region UTILITIES
def __load_constants():
    global SECRETS_CONFIG
    SECRETS_CONFIG = config_store.APP_CONFIG['secrets']
    
    global SECRET_DIRECTORY
    SECRET_DIRECTORY = file_handler.get_absolute_file_location(SECRETS_CONFIG['secrets_directory'])
    
    global PRIVATE_KEY_FILE
    PRIVATE_KEY_FILE = SECRET_DIRECTORY / SECRETS_CONFIG['private_key_file']

def __generate_asym_key() -> RSAPrivateKey:
    return rsa.generate_private_key(
        public_exponent=constants.PUBLIC_EXPONENT, 
        key_size=constants.KEY_SIZE
    )

def __store_key(private_key: RSAPrivateKey):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(PRIVATE_KEY_FILE, 'wb') as pem_file:
        pem_file.write(pem)
    

def __load_key() -> RSAPrivateKey:
    with open(PRIVATE_KEY_FILE, 'rb') as pem_file:
        pem_content = pem_file.read()

    return serialization.load_pem_private_key(pem_content, None)
#endregion

def load_or_create_new_key():
    __load_constants()
    
    if not SECRET_DIRECTORY.exists():
        SECRET_DIRECTORY.mkdir()
        private_key = __generate_asym_key()
        __store_key(private_key)
        logger_handler.get_logger().info("Created new key")

    global PRIVATE_KEY
    PRIVATE_KEY =  __load_key()

    global PUBLIC_KEY
    PUBLIC_KEY = PRIVATE_KEY.public_key()

def encrypt_data(raw_content):
    cipher_text = PUBLIC_KEY.encrypt(
        pickle.dumps(raw_content),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return cipher_text

def encrypt_data_with_key(raw_content, key):
    public_key = serialization.load_der_public_key(base64.b64decode(key))
    
    cipher_text = public_key.encrypt(
        pickle.dumps(raw_content),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return cipher_text

def decrypt_data(cipher_text: str):
    raw_content = PRIVATE_KEY.decrypt(
        cipher_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return pickle.loads(raw_content)

def encrypt_file(file_name: str, key: str):
    file: Path = node_file_handler.get_file(file_name)
    if not file or not file.exists:
        return None

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=base64.b64decode('QhiLlZpIguCoNOPm2BiaKw=='),
        iterations=480000
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(key, 'utf-8')))
    fernet = Fernet(key)

    with open(file, 'rb') as f:
        content = f.read()

    return fernet.encrypt(content)

def decrypt_file(content, key: str):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=base64.b64decode('QhiLlZpIguCoNOPm2BiaKw=='),
        iterations=480000
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(key, 'utf-8')))
    fernet = Fernet(key)

    return fernet.decrypt(content)

def get_public_key():
    key = PUBLIC_KEY.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return base64.b64encode(key).decode('utf-8')