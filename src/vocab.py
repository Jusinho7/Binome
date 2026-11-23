"""Vocabulary loading with byte-level BPE decoding."""
import json
from typing import Optional
import sys

try:
    from pydantic import BaseModel
except ImportError:
    print(
        "Pydantic is not installed. "
        "Please install it using 'pip install pydantic'."
    )
    sys.exit(1)

def bytes_to_unicode() -> dict[int, str]:
    """Return the GPT-2 byte -> printable unicode character mapping.

    Byte-level BPE tokenizers store each byte as a printable character
    (e.g. the space byte 0x20 is stored as 'Ġ').

    Returns:
        Mapping from byte value (0-255) to its unicode character.
    """
    printable = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    chars = printable[:]
    extra = 0
    for byte in range(256):
        if byte not in printable:
            printable.append(byte)
            chars.append(256 + extra)
            extra += 1
    return {b: chr(c) for b, c in zip(printable, chars)}


class Vocabulary(BaseModel):
    """Maps token ids to the real text each token represents.

    Attributes:
        texts: texts[i] is the decoded text of token i, or None when the
            token is not valid UTF-8 on its own (partial multi-byte char)
            or has no entry in the vocabulary file.
    """

    texts: list[Optional[str]]
    index: dict[str, list[int]] = {}

    @classmethod
    def load(cls, vocab_path: str) -> "Vocabulary":
        """Load a vocab.json file and decode every token.

        Args:
            vocab_path: path to the vocab.json file.

        Returns:
            A Vocabulary instance.

        Raises:
            ValueError: if the file is missing or is not a valid vocab.
        """
        try:
            with open(vocab_path, "r", encoding="utf-8") as file:
                raw: dict[str, int] = json.load(file)
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(
                f"Cannot read vocab {vocab_path}: {error}"
            ) from error

        char_to_byte = {c: b for b, c in bytes_to_unicode().items()}
        texts: list[Optional[str]] = [None] * (max(raw.values()) + 1)

        for token, token_id in raw.items():
            try:
                data = bytes(char_to_byte[c] for c in token)
                texts[token_id] = data.decode("utf-8")
            except (KeyError, UnicodeDecodeError):
                texts[token_id] = None

        index: dict[str, list[int]] = {}
        for token_id, text in enumerate(texts):
            if text is not None:
                index.setdefault(text, []).append(token_id)
        return cls(texts=texts, index=index)

    def allowed_prefixes(
        self, generated: str, targets: list[str]
    ) -> list[int]:
        """Return ids of tokens that keep `generated` on track to a target.

        A token is allowed when its text is a non-empty prefix of what
        remains of at least one target string.

        Args:
            generated: text produced so far.
            targets: complete strings the output must end up equal to.

        Returns:
            List of allowed token ids.
        """
        allowed: set[int] = set()
        for target in targets:
            if not target.startswith(generated):
                continue
            remaining = target[len(generated):]
            for size in range(1, len(remaining) + 1):
                allowed.update(self.index.get(remaining[:size], []))
        return sorted(allowed)
