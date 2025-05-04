import hashlib

def get_hash(key: str) -> int:
    return int(hashlib.md5(key.encode()).hexdigest(), 16)