import re
from typing import List


class Syllablizer:
    def __call__(self, word: str) -> List[str]:
        pattern = r'[^aeiouyąęó]*[aeiouyąęó]+(?:[^aeiouyąęó]*(?=[^aeiouyąęó]|$))?'
        syllables = re.findall(pattern, word, re.IGNORECASE)
        return syllables
