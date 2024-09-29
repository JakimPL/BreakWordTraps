import hashlib
import json
import os
from typing import Any, Dict


def compute_sha256(file_path: os.PathLike) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def save_dict_to_json_file(data: Dict[str, Any], filename: os.PathLike) -> None:
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
