import time
from hashlib import md5


def generate_unique_id() -> str:
    return md5(str(time.time()).encode()).hexdigest()
