# region DEPENDENCIES
import config_store
from utils import file_handler
from utils import logger_handler

from constants import cryptography_constants as constants

import pickle
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
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


def get_public_key():
    key = PUBLIC_KEY.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return base64.b64encode(key).decode('utf-8')