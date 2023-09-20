import functools
import random
import re
from pathlib import Path

from signwriting import join_signs

fingerspelling_dir = Path(__file__).parent.parent.parent.joinpath('data/fingerspelling')


@functools.lru_cache(maxsize=None)
def get_chars(language: str):
    with open(fingerspelling_dir.joinpath(f"{language}.txt"), "r", encoding="utf-8") as f:
        content = re.sub(r'#.*$', '', f.read())  # Remove comments
        lines = [line.strip().split(",") for line in content.splitlines() if len(line.strip()) > 0]
    return {first.lower(): others for [first, *others] in lines}


def spell(word: str, language='en-us-ase-asl'):
    chars = get_chars(language)

    sl = []
    caret = 0
    while caret < len(word):
        found = False
        for c, options in chars.items():
            if word[caret:caret + len(c)].lower() == c:
                sl.append(random.choice(options))
                caret += len(c)
                found = True
                break
        if not found:
            return None

    return join_signs(*sl, spacing=10)


if __name__ == "__main__":
    for word in ["12345", "hello", "Amit"]:
        print(word, spell(word))
