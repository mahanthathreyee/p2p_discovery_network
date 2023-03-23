import hashlib

def generate_hash(o: str) -> str:
    return hashlib.sha256(o.encode('utf-8')).hexdigest()